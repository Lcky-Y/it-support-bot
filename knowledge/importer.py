"""
知识库导入脚本
把 knowledge/documents/ 下的 Markdown 文档解析、切块后写入 SQLite 知识库。
Markdown 仅作为数据源，运行时检索直接从 SQLite 读取。

用法：python knowledge/importer.py
"""
import os
import sys
import json
import sqlite3
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import KNOWLEDGE_DB_PATH, EMBEDDING_MODEL_NAME
from knowledge.document_loader import load_documents
from knowledge.text_splitter import split_entries
from knowledge.repository import KnowledgeRepository


def import_to_db(documents_dir=None, db_path=None, verbose: bool = True) -> int:
    """把 Markdown 知识导入 SQLite，返回导入的 chunk 数量。"""
    entries = load_documents(documents_dir) if documents_dir else load_documents()
    chunks = split_entries(entries)

    repo = KnowledgeRepository(db_path or KNOWLEDGE_DB_PATH)
    repo.init_schema()

    os.makedirs(os.path.dirname(repo.db_path), exist_ok=True)
    conn = sqlite3.connect(repo.db_path)
    try:
        with conn:
            conn.execute("DELETE FROM knowledge_chunks")
            conn.execute("DELETE FROM knowledge_items")

            item_ids = {}
            chunk_counts = {}
            for c in chunks:
                key = (c["source"], c["title"])
                if key not in item_ids:
                    cur = conn.execute(
                        "INSERT INTO knowledge_items(title, category, source, keywords) "
                        "VALUES (?, ?, ?, ?)",
                        (
                            c["title"],
                            c["category"],
                            c["source"],
                            json.dumps(c.get("keywords", []), ensure_ascii=False),
                        ),
                    )
                    item_ids[key] = cur.lastrowid
                    chunk_counts[key] = 0
                idx = chunk_counts[key]
                chunk_counts[key] += 1
                conn.execute(
                    "INSERT INTO knowledge_chunks(knowledge_id, chunk_index, content) "
                    "VALUES (?, ?, ?)",
                    (item_ids[key], idx, c["content"]),
                )

            meta = {
                "schema_version": "1",
                "source": "markdown",
                "entry_count": str(len(entries)),
                "chunk_count": str(len(chunks)),
                "embedding_model": EMBEDDING_MODEL_NAME,
                "last_import": datetime.now().isoformat(timespec="seconds"),
            }
            for k, v in meta.items():
                conn.execute(
                    "INSERT OR REPLACE INTO metadata(key, value) VALUES (?, ?)", (k, v)
                )
    finally:
        conn.close()

    if verbose:
        print(f"[完成] 已导入 {len(entries)} 条知识 / {len(chunks)} 个 chunk -> {repo.db_path}")
    return len(chunks)


if __name__ == "__main__":
    import_to_db()
