"""
错误解析器
程序报错具有非常明显的结构，本模块负责从用户输入（含粘贴的完整 traceback）中
提取标准化的错误类型、分类与关键信息，供规则引擎做“错误代码精确匹配”。

示例：
    输入 "ModuleNotFoundError: No module named 'torch'"
    输出 {"error_type": "ModuleNotFoundError", "category": "python", "module": "torch", ...}
"""
import re

# (正则, 归一化错误类型, 所属分类)
# 顺序重要：更具体的模式放在前面，避免被宽泛模式抢先匹配。
# 统一用 re.IGNORECASE 匹配，因此无需担心大小写。
_ERROR_PATTERNS = [
    # Python 异常
    (r"ModuleNotFoundError|No module named", "ModuleNotFoundError", "python"),
    (r"DLL load failed|ImportError: DLL|找不到.*\.dll|程序无法启动.*缺少", "DllMissing", "windows"),
    (r"ImportError", "ImportError", "python"),
    (r"IndentationError", "IndentationError", "python"),
    (r"SyntaxError", "SyntaxError", "python"),
    (r"FileNotFoundError", "FileNotFoundError", "python"),
    (r"PermissionError", "PermissionError", "python"),
    (r"AttributeError", "AttributeError", "python"),
    (r"TypeError", "TypeError", "python"),
    (r"ValueError", "ValueError", "python"),
    (r"KeyError", "KeyError", "python"),
    (r"IndexError", "IndexError", "python"),
    (r"NameError", "NameError", "python"),
    (r"ZeroDivisionError", "ZeroDivisionError", "python"),
    # CUDA / GPU
    (r"CUDA out of memory", "CUDAOutOfMemory", "pytorch"),
    (r"CUDA error[:\s]|CUDA (kernel|launch|runtime)", "CUDAError", "pytorch"),
    (r"out of memory", "OutOfMemory", "pytorch"),
    # 网络
    (r"CERTIFICATE_VERIFY_FAILED|SSL: CERTIFICATE|ssl\.SSLCertVerificationError", "SSLError", "network"),
    (r"SSLError|SSL_ERROR|ssl error|ssl certificate", "SSLError", "network"),
    (r"Failed to establish a new connection|Connection refused|ConnectionResetError", "ConnectionError", "network"),
    (r"ConnectionError|Connection aborted", "ConnectionError", "network"),
    (r"timed out|TimeoutError|ReadTimeout|ConnectTimeout", "TimeoutError", "network"),
    # pip
    (r"Could not find a version that satisfies|No matching distribution found", "PackageNotFound", "pip"),
    (r"ERROR: Could not install packages|ERROR: Cannot uninstall", "PipError", "pip"),
    # git
    (r"fatal: not a git repository|Not a git repository", "NotARepository", "git"),
    (r"fatal: Authentication failed|Authentication failed for|remote: Invalid username", "AuthenticationFailed", "git"),
    (r"merge conflict|CONFLICT \(content\)|Automatic merge failed", "MergeConflict", "git"),
    (r"push rejected|non-fast-forward|fetch first|failed to push", "PushRejected", "git"),
    (r"repository not found|Remote not found", "RepositoryNotFound", "git"),
    # Windows
    (r"不是内部或外部命令|不是内部命令|not recognized as an internal", "CommandNotFound", "windows"),
    (r"Access is denied|拒绝访问|Access denied", "PermissionDenied", "windows"),
]

_MODULE_RE = re.compile(r"No module named ['\"]?([A-Za-z_][\w\.]*)", re.IGNORECASE)
_QUOTED_RE = re.compile(r"[`'\"]+([A-Za-z_][\w\.-]*)[`'\"]+")


def parse(text: str):
    """
    从文本中解析错误信息，命中则返回标准化 dict，未命中返回 None。
    返回结构：
        {
            "error_type": 归一化错误类型,
            "category": 所属分类,
            "module": 涉及的模块/包名（可选）,
            "matched": 命中的原始片段,
        }
    """
    if not text:
        return None

    for pattern, error_type, category in _ERROR_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if not m:
            continue

        result = {
            "error_type": error_type,
            "category": category,
            "matched": m.group(0),
        }

        # 提取模块名：ModuleNotFoundError / ImportError 场景
        if error_type in ("ModuleNotFoundError", "ImportError"):
            mm = _MODULE_RE.search(text)
            if mm:
                result["module"] = mm.group(1)

        # 提取包名：pip 找不到包场景
        if error_type == "PackageNotFound":
            mm = re.search(r"(?:requirement|distribution|package)[\'\": ]+([\w\.\-]+)", text, re.IGNORECASE)
            if not mm:
                mm = _QUOTED_RE.search(text)
            if mm:
                result["module"] = mm.group(1)

        return result

    return None


# 归一化错误类型 -> 中文可读名称，供回复格式化使用
ERROR_TYPE_LABELS = {
    "ModuleNotFoundError": "Python 模块缺失",
    "ImportError": "Python 导入失败",
    "IndentationError": "Python 缩进错误",
    "SyntaxError": "Python 语法错误",
    "FileNotFoundError": "文件未找到",
    "PermissionError": "权限错误",
    "AttributeError": "属性错误",
    "TypeError": "类型错误",
    "ValueError": "值错误",
    "KeyError": "键错误",
    "IndexError": "索引越界",
    "NameError": "名称未定义",
    "ZeroDivisionError": "除零错误",
    "CUDAOutOfMemory": "CUDA 显存不足",
    "CUDAError": "CUDA 错误",
    "OutOfMemory": "内存不足",
    "SSLError": "SSL 证书/加密错误",
    "ConnectionError": "网络连接错误",
    "TimeoutError": "网络超时",
    "PackageNotFound": "依赖包不存在",
    "PipError": "pip 安装错误",
    "NotARepository": "不是 Git 仓库",
    "AuthenticationFailed": "Git 认证失败",
    "MergeConflict": "Git 合并冲突",
    "PushRejected": "Git 推送被拒绝",
    "RepositoryNotFound": "Git 仓库不存在",
    "DllMissing": "DLL 缺失",
    "CommandNotFound": "命令未找到",
    "PermissionDenied": "权限被拒绝",
}
