"""
错误解析器单元测试
直接验证 error_parser 对常见报错信息的解析结果。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import error_parser


def _check(query, expected_type=None, expected_category=None, expected_module=None):
    parsed = error_parser.parse(query)
    if expected_type is None:
        assert parsed is None, f"{query!r} 应无法解析，实际得到 {parsed}"
        return
    assert parsed is not None, f"{query!r} 应能解析出错误类型"
    assert parsed["error_type"] == expected_type, \
        f"{query!r} 错误类型期望 {expected_type}，实际 {parsed['error_type']}"
    if expected_category:
        assert parsed["category"] == expected_category, \
            f"{query!r} 分类期望 {expected_category}，实际 {parsed['category']}"
    if expected_module:
        assert parsed.get("module") == expected_module, \
            f"{query!r} 模块名期望 {expected_module}，实际 {parsed.get('module')}"


def test_module_not_found():
    _check("ModuleNotFoundError: No module named 'torch'",
           "ModuleNotFoundError", "python", "torch")
    _check("No module named numpy", "ModuleNotFoundError", "python", "numpy")


def test_ssl_error():
    _check("CERTIFICATE_VERIFY_FAILED", "SSLError", "network")
    _check("SSLError: HTTPSConnectionPool", "SSLError", "network")


def test_timeout():
    _check("Connection to pypi.org timed out", "TimeoutError", "network")


def test_cuda():
    _check("CUDA out of memory", "CUDAOutOfMemory", "pytorch")
    _check("CUDA error: device-side assert triggered", "CUDAError", "pytorch")


def test_git():
    _check("fatal: not a git repository", "NotARepository", "git")
    _check("fatal: Authentication failed for 'https://github.com'",
           "AuthenticationFailed", "git")
    _check("CONFLICT (content): Merge conflict in file.txt",
           "MergeConflict", "git")
    _check(" ! [rejected] main -> main (non-fast-forward)", "PushRejected", "git")


def test_pip():
    _check("ERROR: Could not find a version that satisfies the requirement torch",
           "PackageNotFound", "pip", "torch")


def test_windows():
    _check("'python' 不是内部或外部命令", "CommandNotFound", "windows")
    _check("ImportError: DLL load failed", "DllMissing", "windows")
    _check("Access is denied.", "PermissionDenied", "windows")


def test_no_match():
    _check("今天天气不错")
    _check("你好，请问你是谁")


def main():
    import traceback
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for fn in tests:
        try:
            fn()
            print(f"✓ {fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {fn.__name__}: {e}")
        except Exception:
            print(f"✗ {fn.__name__} 异常:")
            traceback.print_exc()
    print(f"\n通过 {passed}/{len(tests)}")


if __name__ == "__main__":
    main()
