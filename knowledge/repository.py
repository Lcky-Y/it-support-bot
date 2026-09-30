"""
知识库 SQLite 仓库
把知识条目与检索切块（chunk）持久化到 SQLite，供运行时检索直接读取。
Markdown 文档仍保留，仅作为导入源（由 importer.py 写入本库）。

对外只读接口 get_all_chunks() 返回与 text_splitter.split_entries() 完全一致的
chunk 结构；fts_search() 提供基于 FTS5 的全文（BM25）检索。
"""
import os
import re
import json
import sqlite3

from config import KNOWLEDGE_DB_PATH

_SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")

# FTS5 trigram 分词无法匹配 <3 字符的词；只保留中英文数字，其余作为分隔符
_NON_WORD_RE = re.compile(r"[^\u4e00-\u9fa5A-Za-z0-9]+")
_MIN_TERM_LEN = 3


def _sanitize_fts(text: str) -> str:
    """把用户查询转成安全的 FTS5 MATCH 表达式：去除特殊字符，多词用 OR 连接。"""
    cleaned = _NON_WORD_RE.sub(" ", text or "")
    terms = [t for t in cleaned.split() if len(t) >= _MIN_TERM_LEN]
    return " OR ".join(terms)


class KnowledgeRepository:
    def __init__(self, db_path: str = KNOWLEDGE_DB_PATH):
        self.db_path = db_path

    # ------------------------------------------------------------------
    # 基础
    # ------------------------------------------------------------------
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def exists(self) -> bool:
        return os.path.isfile(self.db_path)

    def init_schema(self):
        """建库并创建表结构（幂等）。"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(_SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = f.read()
        with self._connect() as conn:
            conn.executescript(schema)

    # ------------------------------------------------------------------
    # 读取
    # ------------------------------------------------------------------
    @staticmethod
    def _row_to_chunk(r) -> dict:
        def _list(field):
            try:
                val = json.loads(r[field])
            except (ValueError, TypeError):
                val = []
            return val if isinstance(val, list) else []

        return {
            "source": r["source"],
            "category": r["category"],
            "title": r["title"],
            "subcategory": r["subcategory"] or "",
            "issue_type": r["issue_type"] or "",
            "error_type": r["error_type"] or "",
            "platform": _list("platform"),
            "technology": _list("technology"),
            "keywords": _list("keywords"),
            "aliases": _list("aliases"),
            "content": r["content"],
        }

    def get_all_chunks(self) -> list:
        """返回全部 chunk，结构与 split_entries() 输出一致；失败返回空列表。"""
        if not self.exists():
            return []
        try:
            with self._connect() as conn:
                rows = conn.execute(
                    "SELECT i.title, i.category, i.subcategory, i.issue_type, "
                    "i.error_type, i.platform, i.technology, i.keywords, i.aliases, "
                    "i.source, c.content "
                    "FROM knowledge_chunks c "
                    "JOIN knowledge_items i ON c.knowledge_id = i.id "
                    "ORDER BY i.id, c.chunk_index"
                ).fetchall()
        except Exception:
            return []
        return [self._row_to_chunk(r) for r in rows]

    def fts_search(self, query: str, limit: int = 10) -> list:
        """FTS5/BM25 全文检索，返回按相关度排序的 chunk 列表；失败/无结果返回空列表。"""
        match = _sanitize_fts(query)
        if not match or not self.exists():
            return []
        try:
            with self._connect() as conn:
                rows = conn.execute(
                    "SELECT i.title, i.category, i.subcategory, i.issue_type, "
                    "i.error_type, i.platform, i.technology, i.keywords, i.aliases, "
                    "i.source, c.content "
                    "FROM knowledge_fts "
                    "JOIN knowledge_chunks c ON c.id = knowledge_fts.chunk_id "
                    "JOIN knowledge_items i ON c.knowledge_id = i.id "
                    "WHERE knowledge_fts MATCH ? "
                    "ORDER BY bm25(knowledge_fts) LIMIT ?",
                    (match, limit),
                ).fetchall()
        except Exception:
            return []
        return [self._row_to_chunk(r) for r in rows]

    def count_items(self) -> int:
        return self._scalar("SELECT COUNT(*) FROM knowledge_items")

    def count_chunks(self) -> int:
        return self._scalar("SELECT COUNT(*) FROM knowledge_chunks")

    def get_metadata(self) -> dict:
        if not self.exists():
            return {}
        try:
            with self._connect() as conn:
                rows = conn.execute("SELECT key, value FROM metadata").fetchall()
            return {r["key"]: r["value"] for r in rows}
        except Exception:
            return {}

    def _scalar(self, sql: str) -> int:
        if not self.exists():
            return 0
        try:
            with self._connect() as conn:
                row = conn.execute(sql).fetchone()
            return int(row[0]) if row else 0
        except Exception:
            return 0
