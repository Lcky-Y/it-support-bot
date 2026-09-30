"""
意图分类器
在规则未命中、即将转交 LLM 时，对用户问题所属技术领域做粗分类，
以便选择针对性的提示词 / 检索方向。纯关键词实现，轻量、可解释。

返回 (category, score)：category 为 7 大领域之一，score 为命中关键词比例。
"""
import re

DOMAIN_KEYWORDS = {
    "python": [
        "python", "import", "module", "syntax", "venv", "虚拟环境", "解释器",
        "traceback", "模块", "语法", "缩进", "notebook", "pycharm", "vscode",
    ],
    "pip": [
        "pip", "install", "uninstall", "requirements", "依赖", "安装包", "安装",
        "镜像", "源", "whl", "wheel",
    ],
    "conda": [
        "conda", "anaconda", "miniconda", "环境", "激活", "activate", "channel",
    ],
    "git": [
        "git", "clone", "commit", "push", "pull", "branch", "merge", "仓库",
        "提交", "分支", "合并", "github", "gitlab", "远程", "remote", "rebase",
    ],
    "windows": [
        "windows", "cmd", "powershell", "环境变量", "path", "权限", "dll",
        "注册表", "管理员", "批处理", "命令",
    ],
    "pytorch": [
        "torch", "pytorch", "cuda", "gpu", "显卡", "显存", "模型", "张量",
        "tensor", "训练", "推理",
    ],
    "network": [
        "ssl", "timeout", "connection", "proxy", "代理", "网络", "证书", "超时",
        "dns", "防火墙", "下载", "连接", "请求", "request", "vpn",
    ],
}

# 中文分词辅助：将连续中文拆成词组便于关键词匹配（简单按英文/数字边界切分）
_CN_TOKEN_RE = re.compile(r"[A-Za-z0-9_.\-]+")


def classify(text: str):
    """返回 (category, score)，未识别到任何领域时返回 ("unknown", 0.0)。"""
    if not text:
        return "unknown", 0.0

    text_lower = text.lower()
    best_cat = "unknown"
    best_ratio = 0.0

    for category, keywords in DOMAIN_KEYWORDS.items():
        hits = sum(1 for k in keywords if k in text_lower)
        ratio = hits / len(keywords)
        if ratio > best_ratio:
            best_ratio = ratio
            best_cat = category

    if best_ratio <= 0.0:
        return "unknown", 0.0
    return best_cat, best_ratio
