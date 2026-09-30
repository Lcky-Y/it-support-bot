-- 知识库 SQLite 表结构（V2）
-- 知识条目（与 Markdown 文档一一对应） + 检索切块（chunk）+ 元数据 + FTS5 全文索引。

PRAGMA foreign_keys = ON;

-- 知识条目：一条故障知识 = 一行
-- keywords / aliases / platform / technology 以 JSON 数组字符串存储
CREATE TABLE IF NOT EXISTS knowledge_items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    category    TEXT NOT NULL,
    subcategory TEXT NOT NULL DEFAULT '',
    issue_type  TEXT NOT NULL DEFAULT '',
    error_type  TEXT NOT NULL DEFAULT '',
    platform    TEXT NOT NULL DEFAULT '[]',
    technology  TEXT NOT NULL DEFAULT '[]',
    keywords    TEXT NOT NULL DEFAULT '[]',
    aliases     TEXT NOT NULL DEFAULT '[]',
    source      TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at  TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
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

-- FTS5 全文索引（trigram 分词，兼顾中英文）；chunk_id 关联 knowledge_chunks.id
CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts USING fts5(
    chunk_id UNINDEXED,
    title,
    keywords,
    aliases,
    content,
    tokenize = 'trigram'
);

CREATE INDEX IF NOT EXISTS idx_chunks_knowledge ON knowledge_chunks(knowledge_id);
CREATE INDEX IF NOT EXISTS idx_items_category ON knowledge_items(category);
