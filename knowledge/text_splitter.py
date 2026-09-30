"""
文档切块器
把加载器得到的知识条目切分成适合检索/嵌入的文本块（chunk）。

Stage 4 先按“一条知识 = 一个 chunk”处理，内容过长时按小节再切分，
保证每个 chunk 长度可控，便于后续 Stage 5 直接喂给向量模型。
"""
import re

# 内容里哪些小节属于“检索正文”（关键词仅用于匹配，不进入正文）
_CONTENT_SECTIONS = ["症状", "常见原因", "检查命令", "解决思路"]


def _section_block(name: str, items: list) -> str:
    if not items:
        return ""
    body = "\n".join(f"- {i}" for i in items)
    return f"【{name}】\n{body}"


def _entry_content(entry: dict) -> str:
    parts = []
    for name in _CONTENT_SECTIONS:
        block = _section_block(name, entry.get("sections", {}).get(name, []))
        if block:
            parts.append(block)
    return "\n".join(parts)


def _chunk(entry: dict, content: str, suffix: str = "") -> dict:
    return {
        "source": entry["source"],
        "category": entry["category"],
        "title": entry["title"],
        "keywords": entry.get("keywords", []),
        "aliases": entry.get("aliases", []),
        "platform": entry.get("platform", []),
        "technology": entry.get("technology", []),
        "issue_type": entry.get("issue_type", ""),
        "error_type": entry.get("error_type", ""),
        "subcategory": entry.get("subcategory", ""),
        "content": content,
    }


def split_entries(entries: list, max_chars: int = 900) -> list:
    """把条目列表切分为 chunk 列表。"""
    chunks = []
    for entry in entries:
        content = _entry_content(entry)
        if len(content) <= max_chars:
            chunks.append(_chunk(entry, content))
            continue

        # 内容过长：按小节逐块切分
        sections = entry.get("sections", {})
        parts = []
        for name in _CONTENT_SECTIONS:
            block = _section_block(name, sections.get(name, []))
            if block:
                parts.append(block)
        # 简单策略：顺序打包到 max_chars 内
        current = []
        current_len = 0
        for p in parts:
            if current and current_len + len(p) > max_chars:
                chunks.append(_chunk(entry, "\n".join(current)))
                current = []
                current_len = 0
            current.append(p)
            current_len += len(p)
        if current:
            chunks.append(_chunk(entry, "\n".join(current)))

    return chunks


def count_chars(text: str) -> int:
    return len(text)
