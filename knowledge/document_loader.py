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

    可选小节（V1.2 新增，用于检索增强，缺失时为空）：
    ### 别名       空格/逗号分隔的常见口语化说法
    ### 平台       windows / linux / macos（可多个）
    ### 技术栈     相关技术（docker、compose 等）
    ### 故障类型   安装失败 / 权限问题 / 网络问题 等
    ### 错误类型   标准化错误标识（如 docker_daemon_not_running）
    ### 子类       更细粒度分类

    返回的每条条目结构：
    {
        "source": "knowledge/documents/python.md",
        "category": "python",
        "title": "ModuleNotFoundError 模块缺失",
        "keywords": ["ModuleNotFoundError", "No module named", ...],
        "aliases": [...], "platform": [...], "technology": [...],
        "issue_type": "...", "error_type": "...", "subcategory": "...",
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
    "docker.md": "docker",
    "linux.md": "linux",
    "node.md": "node",
    "java.md": "java",
    "maven.md": "maven",
}

_BULLET_RE = re.compile(r"^[-*]\s+")
_NUMBER_RE = re.compile(r"^\d+[.、)]\s*")


def _clean_line(line: str) -> str:
    line = line.strip()
    line = _BULLET_RE.sub("", line)
    line = _NUMBER_RE.sub("", line)
    return line


# 列表型小节（解析成 token 列表）
_LIST_SECTIONS = {
    "关键词": "keywords",
    "别名": "aliases",
    "平台": "platform",
    "技术栈": "technology",
}
# 单值小节（取首行作为字符串）
_SINGLE_SECTIONS = {
    "故障类型": "issue_type",
    "错误类型": "error_type",
    "子类": "subcategory",
}


def _split_tokens(items: list) -> list:
    tokens = []
    for item in items:
        for part in re.split(r"[\s,，、]+", item):
            if part:
                tokens.append(part)
    return tokens


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

    entry = {
        "source": source,
        "category": category,
        "title": title,
        "keywords": [],
        "aliases": [],
        "platform": [],
        "technology": [],
        "issue_type": "",
        "error_type": "",
        "subcategory": "",
        "sections": sections,
    }
    for sec, field in _LIST_SECTIONS.items():
        entry[field] = _split_tokens(sections.get(sec, []))
    for sec, field in _SINGLE_SECTIONS.items():
        items = sections.get(sec, [])
        entry[field] = items[0].strip() if items else ""
    return entry


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
