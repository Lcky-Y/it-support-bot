"""
端到端场景测试（Stage 7）
验证完整链路：规则命中、规则+LLM、Hybrid RAG、向量降级、LLM 失败、
清空上下文、CLI 命令、中英文 traceback、超长日志、非 IT 问题。
默认关闭 LLM 以避免联网，仅“LLM 失败”用例显式模拟。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import llm.client as llm_client

# 默认关闭 LLM，保证测试离线、确定性
llm_client.is_available = lambda: False

from chatbot import Chatbot


def test_rule_hit():
    bot = Chatbot()
    r = bot.reply("No module named torch")
    assert r["source"] == "rule"
    assert r["category"] == "python"
    assert "ModuleNotFoundError" in r["text"] or "模块" in r["text"]


def test_rule_llm_band():
    bot = Chatbot()
    r = bot.reply("git push 被拒绝")
    assert r["source"] == "rule+llm"


def test_hybrid_fallback_with_references():
    bot = Chatbot()
    r = bot.reply("如何撤销 git 上一次提交")
    assert r["source"] == "llm"
    assert r.get("references"), "兜底应返回参考来源"
    assert any("撤销" in t for t in r["references"])


def test_vector_degradation():
    from services.knowledge_service import KnowledgeService
    ks = KnowledgeService(use_vector=False)   # 模拟向量不可用
    top = ks.retrieve("CERTIFICATE_VERIFY_FAILED", top_k=3)
    assert top and top[0]["source"].endswith(".md")


def test_llm_failure_graceful():
    def _raise(*a, **k):
        raise RuntimeError("mock llm failure")

    llm_client.is_available = lambda: True
    llm_client.generate_with_prompt = _raise
    try:
        bot = Chatbot()
        r = bot.reply("如何撤销 git 提交")   # 走 LLM 路径但会失败
        assert r["source"] == "llm"
        assert r["text"].strip(), "LLM 失败仍应有兜底文本"
    finally:
        llm_client.is_available = lambda: False


def test_empty_input():
    bot = Chatbot()
    r = bot.reply("   ")
    assert "text" in r and r["text"].strip()


def test_clear_context():
    bot = Chatbot()
    bot.reply("No module named torch")
    assert len(bot.get_history()) == 2
    bot.clear()
    assert bot.get_history() == []
    assert bot.history.diagnostic_context == {}


def test_cli_status_command():
    import cli
    bot = Chatbot()
    out, _ = cli.handle_command(bot, "status")
    assert "Rule Engine" in out
    assert "Retrieval Mode" in out


def test_chinese_traceback():
    bot = Chatbot()
    r = bot.reply("报错说找不到模块 pandas")
    assert r["source"] == "rule"
    assert r["category"] == "python"


def test_english_traceback():
    bot = Chatbot()
    r = bot.reply("Traceback (most recent call last):\n  ...\nModuleNotFoundError: No module named 'torch'")
    assert r["source"] == "rule"
    assert r["category"] == "python"


def test_long_error_log():
    bot = Chatbot()
    long_text = 'File "C:/x/y.py", line 1, in <module>\n' * 200 + "ModuleNotFoundError: No module named 'torch'"
    r = bot.reply(long_text)
    assert r["source"] == "rule"


def test_non_it_question():
    bot = Chatbot()
    r = bot.reply("今天天气怎么样")
    assert r["source"] == "llm"
    assert "问题判断" in r["text"]


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
