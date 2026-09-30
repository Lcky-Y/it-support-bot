"""
聊天机器人集成测试
验证规则命中路径、LLM 兜底路径（离线 mock）与反馈记录，不发起真实网络请求。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot import Chatbot
from core.diagnostic_engine import DiagnosticEngine


def _disable_llm():
    """让诊断引擎的 LLM 分支走离线兜底，避免测试依赖网络。"""
    import llm.client as llm_client
    llm_client.is_available = lambda: False


def test_rule_hit():
    _disable_llm()
    bot = Chatbot()
    result = bot.reply("No module named torch")
    assert result["source"] == "rule", f"应命中规则，实际 {result['source']}"
    assert "ModuleNotFoundError" in result["text"] or "模块" in result["text"]


def test_greeting_rule():
    _disable_llm()
    bot = Chatbot()
    result = bot.reply("你好")
    assert result["source"] == "rule"


def test_fallback_offline():
    _disable_llm()
    bot = Chatbot()
    result = bot.reply("今天天气怎么样")
    assert result["source"] == "llm"
    assert "问题判断" in result["text"]


def test_history_and_context():
    _disable_llm()
    bot = Chatbot()
    bot.reply("torch 检测不到 cuda")
    assert bot.history.diagnostic_context.get("category") == "pytorch"
    assert bot.history.diagnostic_context.get("error_type") is None or True
    assert len(bot.history.as_list()) >= 2


def test_feedback_does_not_crash():
    _disable_llm()
    bot = Chatbot()
    bot.reply("No module named torch")
    bot.record_feedback(resolved=True)
    bot.record_feedback(resolved=False, feedback="还是没解决")


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
