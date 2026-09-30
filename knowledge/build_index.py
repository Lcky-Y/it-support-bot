"""
向量索引构建脚本
读取知识库文档 → 切块 → embedding → 构建 FAISS 索引 → 持久化到 embeddings/。

用法：python knowledge/build_index.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from knowledge.document_loader import load_documents
from knowledge.text_splitter import split_entries
from knowledge.embedding_model import get_embedder, dependencies_available
from knowledge.vector_store import VectorStore


def build(documents_dir=None, verbose: bool = True) -> bool:
    if not dependencies_available():
        if verbose:
            print("[跳过] 未安装 sentence-transformers / faiss，无法构建向量索引。")
            print("       可运行：pip install -r requirements-rag.txt")
        return False

    embedder = get_embedder()
    if not embedder.available:
        if verbose:
            print("[失败] embedding 模型加载失败（可能离线或模型下载异常）。")
        return False

    entries = load_documents(documents_dir) if documents_dir else load_documents()
    chunks = split_entries(entries)
    if not chunks:
        if verbose:
            print("[失败] 没有可用的知识条目。")
        return False

    texts = [c["content"] for c in chunks]
    if verbose:
        print(f"正在对 {len(chunks)} 个 chunk 进行 embedding ...")
    vectors = embedder.encode(texts)

    store = VectorStore()
    store.build(vectors, chunks)
    if store.save():
        if verbose:
            print(f"[完成] 已构建并保存向量索引：{len(chunks)} 个 chunk")
        return True

    if verbose:
        print("[失败] 索引保存失败。")
    return False


if __name__ == "__main__":
    build()
