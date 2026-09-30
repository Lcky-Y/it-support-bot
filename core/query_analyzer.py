"""
Query Analyzer（V1.2）
在检索前对用户问题做轻量理解：提取技术错误 token、技术栈、平台、版本号等结构化字段，
供检索时的 Metadata Boost 与精确 token 加成使用。

纯规则 + 词表实现，无外部依赖，保证完全离线。
"""
import re

# 已知技术栈词表（用于 Metadata Boost）；ASCII 词用词边界匹配，避免误命中
TECHNOLOGIES = [
    "docker", "docker-compose", "compose", "container", "镜像", "容器", "registry",
    "python", "pip", "torch", "pytorch", "cuda", "conda", "anaconda", "miniconda",
    "git", "github", "gitlab", "npm", "node", "nodejs", "nvm", "npx", "pnpm",
    "node-gyp", "yarn", "java", "jdk", "jre", "jvm", "javac", "maven", "mvn",
    "gradle", "spring", "springboot",
    "mysql", "postgres", "postgresql", "redis", "mongodb", "nginx", "kubernetes",
    "k8s", "vue", "react", "wsl", "vscode", "jupyter", "tensorflow",
]

# 已知平台词表（用于 Metadata Boost）
PLATFORMS = [
    "windows", "win10", "win11", "linux", "ubuntu", "centos", "debian", "fedora",
    "macos", "osx", "wsl", "powershell", "cmd", "bash", "shell",
]

# 技术错误 token 提取正则
_ERROR_CLASS_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9]*(?:Error|Exception|Warning|Failure|Fault)\b")
_WINERR_RE = re.compile(r"WinError\s+\d+")
_HEXCODE_RE = re.compile(r"0x[0-9A-Fa-f]{4,}")
_HTTP_STATUS_RE = re.compile(r"\b[1-5][0-9]{2}\b")
_VERSION_RE = re.compile(r"\b\d+\.\d+(?:\.\d+)?\b")


def _match_terms(text: str, terms: list) -> list:
    """词表匹配：ASCII 词用词边界，中文词用子串，避免 'mac' 命中 'machine' 等误报。"""
    hits = []
    for t in terms:
        if t.isascii():
            if re.search(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])", text):
                hits.append(t)
        elif t in text:
            hits.append(t)
    return hits


def analyze(text: str) -> dict:
    """提取查询的结构化信号。"""
    text = text or ""
    lower = text.lower()

    technologies = _match_terms(lower, TECHNOLOGIES)
    platforms = _match_terms(lower, PLATFORMS)

    error_terms = []
    error_terms.extend(_ERROR_CLASS_RE.findall(text))
    error_terms.extend(_WINERR_RE.findall(text))
    error_terms.extend(_HEXCODE_RE.findall(text))
    error_terms.extend(_HTTP_STATUS_RE.findall(text))

    versions = _VERSION_RE.findall(text)

    return {
        "technologies": technologies,
        "platforms": platforms,
        "error_terms": error_terms,
        "versions": versions,
    }
