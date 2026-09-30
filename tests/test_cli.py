"""
CLI 交互层测试
测试命令解析、命令分派与展示函数，不启动交互式终端。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cli
from chatbot import Chatbot


def test_parse_command_known():
    for cmd in ("help", "history", "clear", "status", "about", "exit"):
        assert cli.parse_command(f"/{cmd}") == cmd, f"/{cmd} 应解析为 {cmd}"
        assert cli.parse_command(f"/{cmd.upper()}") == cmd, "命令应大小写不敏感"


def test_parse_command_non_command():
    assert cli.parse_command("你好") is None
    assert cli.parse_command("help") is None        # 不带斜杠视为普通消息
    assert cli.parse_command("ModuleNotFoundError") is None


def test_parse_command_unknown():
    assert cli.parse_command("/foo") == "unknown"
    assert cli.parse_command("/") == "unknown"


def test_render_welcome():
    text = cli.render_welcome()
    assert "IT 智能技术支持助手" in text
    assert "版本" in text
    assert "/help" in text and "/exit" in text


def test_render_status():
    s = {
        "rules": 45, "knowledge_entries": 72,
        "retrieval_mode": "Hybrid", "vector_index": "Available",
        "llm": "deepseek-flash", "messages": 4,
    }
    text = cli.render_status(s)
    assert "Rule Engine" in text and "Hybrid" in text
    assert "72 条知识" in text


def test_render_history():
    msgs = [
        {"role": "user", "content": "torch 检测不到 cuda"},
        {"role": "assistant", "content": "检测到 PyTorch CUDA 问题..."},
    ]
    text = cli.render_history(msgs)
    assert "[1] 用户" in text and "[2] 助手" in text


def test_handle_command_dispatch():
    bot = Chatbot()
    assert "命令" in cli.handle_command(bot, "help")[0]
    assert "IT Support Bot" in cli.handle_command(bot, "about")[0]
    assert "未知命令" in cli.handle_command(bot, "unknown")[0]
    out, should_exit = cli.handle_command(bot, "exit")
    assert should_exit is True and out == "再见！"


def test_clear_command():
    bot = Chatbot()
    bot.reply("你好")           # 命中规则，不触发向量加载
    assert len(bot.get_history()) == 2
    out, _ = cli.handle_command(bot, "clear")
    assert out == "当前会话已清空。"
    assert bot.get_history() == []


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
