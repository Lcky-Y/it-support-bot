-- 知识库 SQLite 表结构
-- 知识条目（与 Markdown 文档一一对应） + 检索切块（chunk）+ 元数据。

PRAGMA foreign_keys = ON;

-- 知识条目：一条故障知识 = 一行；keywords 以 JSON 数组字符串存储
CREATE TABLE IF NOT EXISTS knowledge_items (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT NOT NULL,
    category   TEXT NOT NULL,
    source     TEXT NOT NULL,
    keywords   TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 检索切块：一条知识可切分为多个 chunk，按 chunk_index 排序
CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    knowledge_id INTEGER NOT NULL,
    chunk_index  INTEGER NOT NULL DEFAULT 0,
    content      TEXT NOT NULL,
    FOREIGN KEY (knowledge_id) REFERENCES knowledge_items(id) ON DELETE CASCADE
);

-- 元数据：schema_version / 模型名 / 导入时间等
CREATE TABLE IF NOT EXISTS metadata (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_chunks_knowledge ON knowledge_chunks(knowledge_id);
CREATE INDEX IF NOT EXISTS idx_items_category ON knowledge_items(category);
