"""
知识库 SQLite 仓库
把知识条目与检索切块（chunk）持久化到 SQLite，供运行时检索直接读取。
Markdown 文档仍保留，仅作为导入源（由 importer.py 写入本库）。

对外只读接口 get_all_chunks() 返回与 text_splitter.split_entries() 完全一致的
chunk 结构：{source, category, title, keywords, content}。
"""
import os
import json
import sqlite3

from config import KNOWLEDGE_DB_PATH

_SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")


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
    def get_all_chunks(self) -> list:
        """返回全部 chunk，结构与 split_entries() 输出一致；失败返回空列表。"""
        if not self.exists():
            return []
        try:
            with self._connect() as conn:
                rows = conn.execute(
                    "SELECT i.title, i.category, i.source, i.keywords, c.content "
                    "FROM knowledge_chunks c "
                    "JOIN knowledge_items i ON c.knowledge_id = i.id "
                    "ORDER BY i.id, c.chunk_index"
                ).fetchall()
        except Exception:
            return []

        chunks = []
        for r in rows:
            try:
                keywords = json.loads(r["keywords"])
            except (ValueError, TypeError):
                keywords = []
            if not isinstance(keywords, list):
                keywords = []
            chunks.append({
                "source": r["source"],
                "category": r["category"],
                "title": r["title"],
                "keywords": keywords,
                "content": r["content"],
            })
        return chunks

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
