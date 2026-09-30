"""
知识库检索服务（RAG / Hybrid Retrieval）

Stage 5.1：向量检索（sentence-transformers + FAISS）+ 关键词降级。
Stage 5.2：Hybrid 融合 —— Lexical Top-N + Vector Top-N → RRF 融合
           → 技术错误精确命中加成（Exact Match Boost）→ Top-K。

对外接口不变：retrieve(query, top_k)，并可指定 mode：
    mode = "auto"   （默认）向量可用则 Hybrid，否则 Lexical
    mode = "hybrid" 显式 Hybrid（向量不可用时退化为 Lexical）
    mode = "vector" 纯向量（不可用时退化为 Lexical）
    mode = "lexical" 纯关键词 + 字符 n-gram
"""
import re

from config import (
    FUSION_TOP_N, RRF_K, EXACT_BOOST, KNOWLEDGE_DB_PATH,
)
from knowledge.document_loader import load_documents
from knowledge.text_splitter import split_entries
from knowledge.embedding_model import dependencies_available, get_embedder
from knowledge.vector_store import VectorStore
from knowledge.repository import KnowledgeRepository


def _bigrams(text: str) -> set:
    """提取字符二元组（兼容中文与英文），用于轻量相似度。"""
    cleaned = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]+", "", text)
    return {cleaned[i:i + 2] for i in range(len(cleaned) - 1)}


class KnowledgeService:
    def __init__(self, documents_dir=None, use_vector: bool = True, db_path=None):
        # 默认从 SQLite 知识库读取 chunk（由 Markdown 导入）；数据库缺失/为空时回退到
        # 直接解析 Markdown。显式传入 documents_dir 时按旧逻辑直接读取该目录（测试/离线源）。
        if documents_dir is None:
            repo = KnowledgeRepository(db_path or KNOWLEDGE_DB_PATH)
            self.chunks = repo.get_all_chunks()
            if not self.chunks:
                self.chunks = split_entries(load_documents())
        else:
            self.chunks = split_entries(load_documents(documents_dir))

        # (source, title) -> 完整 chunk（含 keywords），用于融合时补齐向量结果的字段
        self._chunk_index = {(c["source"], c["title"]): c for c in self.chunks}

        self._use_vector = use_vector
        self._vector_store = None
        self._embedder = None
        self._vector_initialized = False

    # ------------------------------------------------------------------
    # 向量后端
    # ------------------------------------------------------------------
    def _ensure_vector_backend(self):
        if not self._use_vector or self._vector_initialized:
            return
        self._vector_initialized = True
        if not dependencies_available():
            return
        store = VectorStore()
        if not store.load():
            return
        embedder = get_embedder()
        if not embedder.available:
            return
        self._vector_store = store
        self._embedder = embedder

    @property
    def using_vector(self) -> bool:
        self._ensure_vector_backend()
        return self._vector_store is not None

    def __len__(self):
        return len(self.chunks)

    # ------------------------------------------------------------------
    # 单路检索
    # ------------------------------------------------------------------
    def _keyword_hits(self, query_lower: str, chunk: dict) -> int:
        return sum(1 for kw in chunk.get("keywords", []) if kw and kw.lower() in query_lower)

    def _score_chunk(self, query_lower: str, chunk: dict) -> float:
        score = 0.0
        for kw in chunk.get("keywords", []):
            if kw and kw.lower() in query_lower:
                score += 3
        title = chunk.get("title", "").lower()
        if title and title in query_lower:
            score += 4
        score += len(_bigrams(query_lower) & _bigrams(chunk.get("content", "").lower())) * 0.1
        return score

    def _retrieve_lexical(self, query: str, top_k: int) -> list:
        query_lower = (query or "").lower()
        scored = []
        for chunk in self.chunks:
            s = self._score_chunk(query_lower, chunk)
            if s > 0:
                scored.append((s, chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:top_k]]

    def _retrieve_vector(self, query: str, top_k: int) -> list:
        vec = self._embedder.encode([query])[0]
        return self._vector_store.search(vec, top_k)

    # ------------------------------------------------------------------
    # 融合
    # ------------------------------------------------------------------
    @staticmethod
    def _key(chunk: dict):
        return (chunk.get("source"), chunk.get("title"))

    def _rrf(self, *ranked_lists, k: int = RRF_K):
        """Reciprocal Rank Fusion：合并多个排序列表，返回 [(score, full_chunk), ...]。"""
        scores = {}
        chunk_by_key = {}
        for lst in ranked_lists:
            for rank, chunk in enumerate(lst):
                key = self._key(chunk)
                chunk_by_key[key] = self._chunk_index.get(key, chunk)
                scores[key] = scores.get(key, 0.0) + 1.0 / (k + rank + 1)
        ordered = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        return [(score, chunk_by_key[key]) for key, score in ordered]

    def _apply_exact_boost(self, query: str, scored):
        """技术错误精确命中时给予额外排名加成，且与命中强度成正比：
        命中关键词越多 / 命中标题，加成越大，避免通用词（如 "git"、"pip"）把
        更具体的正确条目挤下去。"""
        query_lower = query.lower()
        out = []
        for score, chunk in scored:
            hits = self._keyword_hits(query_lower, chunk)
            title = (chunk.get("title") or "").lower()
            if title and title in query_lower:
                hits += 3   # 标题被完整命中，信号极强
            if hits >= 1:
                score += EXACT_BOOST * hits
            out.append((score, chunk))
        out.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in out]

    def _hybrid_retrieve(self, query: str, top_k: int) -> list:
        lexical = self._retrieve_lexical(query, FUSION_TOP_N)
        vector = self._retrieve_vector(query, FUSION_TOP_N)
        fused = self._rrf(lexical, vector)
        return self._apply_exact_boost(query, fused)[:top_k]

    # ------------------------------------------------------------------
    # 对外接口
    # ------------------------------------------------------------------
    def retrieve(self, query: str, top_k: int = 3, mode: str = "auto") -> list:
        """返回与 query 最相关的 top_k 个知识片段（带来源引用）。"""
        self._ensure_vector_backend()

        if mode == "lexical":
            return self._retrieve_lexical(query, top_k)

        if mode == "vector":
            if self._vector_store is None:
                return self._retrieve_lexical(query, top_k)
            return self._retrieve_vector(query, top_k)

        if mode == "hybrid":
            if self._vector_store is None:
                return self._retrieve_lexical(query, top_k)
            return self._hybrid_retrieve(query, top_k)

        # auto
        if self._vector_store is not None:
            return self._hybrid_retrieve(query, top_k)
        return self._retrieve_lexical(query, top_k)
