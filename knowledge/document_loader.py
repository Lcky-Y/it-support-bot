"""
知识库文档加载器
解析 knowledge/documents/ 下的 Markdown 文件，把每条故障知识解析为结构化条目。

约定格式（一个文件可包含多条条目）：

    ## 条目标题
    ### 关键词
    空格分隔的关键词
    ### 症状
    - ...
    ### 常见原因
    - ...
    ### 检查命令
    - ...
    ### 解决思路
    - ...

返回的每条条目结构：
    {
        "source": "knowledge/documents/python.md",
        "category": "python",
        "title": "ModuleNotFoundError 模块缺失",
        "keywords": ["ModuleNotFoundError", "No module named", ...],
        "sections": {"症状": [...], "常见原因": [...], ...},
    }
"""
import os
import re

from config import DOCUMENTS_DIR

# 文件名 -> 技术领域分类（cuda 与 pytorch 同属 GPU 开发领域）
CATEGORY_BY_FILE = {
    "python.md": "python",
    "pip.md": "pip",
    "conda.md": "conda",
    "git.md": "git",
    "windows.md": "windows",
    "pytorch.md": "pytorch",
    "cuda.md": "pytorch",
    "network.md": "network",
}

_BULLET_RE = re.compile(r"^[-*]\s+")
_NUMBER_RE = re.compile(r"^\d+[.、)]\s*")


def _clean_line(line: str) -> str:
    line = line.strip()
    line = _BULLET_RE.sub("", line)
    line = _NUMBER_RE.sub("", line)
    return line


def _parse_entry(source: str, category: str, lines: list) -> dict:
    title = lines[0][3:].strip()
    sections = {}
    current_section = None
    for raw in lines[1:]:
        line = raw.rstrip()
        if line.startswith("### "):
            current_section = line[4:].strip()
            sections.setdefault(current_section, [])
        elif line.strip() == "":
            continue
        else:
            cleaned = _clean_line(line)
            if cleaned and current_section is not None:
                sections.setdefault(current_section, []).append(cleaned)

    keywords = []
    for item in sections.get("关键词", []):
        keywords.extend(item.split())
    return {
        "source": source,
        "category": category,
        "title": title,
        "keywords": keywords,
        "sections": sections,
    }


def load_documents(documents_dir: str = DOCUMENTS_DIR) -> list:
    """加载所有知识库文档，返回结构化条目列表。"""
    entries = []
    if not os.path.isdir(documents_dir):
        return entries

    for filename in sorted(os.listdir(documents_dir)):
        if not filename.endswith(".md"):
            continue
        path = os.path.join(documents_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        category = CATEGORY_BY_FILE.get(filename, "general")
        source = os.path.relpath(path, os.path.dirname(documents_dir))

        # 按 "## " 切分成条目块
        blocks = []
        current = []
        for line in lines:
            if line.startswith("## "):
                if current:
                    blocks.append(current)
                current = [line]
            elif line.startswith("# "):
                continue  # 跳过文件级标题
            else:
                current.append(line)
        if current:
            blocks.append(current)

        for block in blocks:
            if block and block[0].startswith("## "):
                entries.append(_parse_entry(source, category, block))

    return entries
