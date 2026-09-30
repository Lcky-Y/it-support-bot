"""
CLI 交互层
负责命令行命令解析、欢迎/帮助/状态/历史/关于等展示，以及带异常兜底的 REPL 循环。
纯展示与调度逻辑，不涉及核心算法，方便单独测试。
"""
from config import VERSION

# 支持的命令
COMMANDS = ("help", "history", "clear", "status", "about", "exit")

_SOURCE_TAG = {"rule": "[规则]", "rule+llm": "[规则+LLM]", "llm": "[LLM]"}

_LINE = "=" * 44
_THIN = "-" * 40


def parse_command(text: str):
    """解析用户输入，返回命令名；非命令返回 None，未知命令返回 'unknown'。"""
    t = (text or "").strip()
    if not t.startswith("/"):
        return None
    body = t[1:].strip().lower()
    cmd = body.split()[0] if body else ""
    if cmd in COMMANDS:
        return cmd
    return "unknown"


def render_welcome() -> str:
    return (
        f"{_LINE}\n"
        f"          IT 智能技术支持助手\n"
        f"{_LINE}\n"
        f"版本：V{VERSION}\n\n"
        f"支持：Python / pip / Conda / Git\n"
        f"      Windows / PyTorch / CUDA / 网络\n\n"
        f"输入 /help 查看命令\n"
        f"输入 /exit 退出\n"
        f"{_LINE}"
    )


def render_help() -> str:
    return (
        "可用命令：\n"
        "  /help     显示本帮助\n"
        "  /history  查看当前会话历史\n"
        "  /clear    清空当前会话上下文\n"
        "  /status   显示系统状态\n"
        "  /about    显示版本与能力\n"
        "  /exit     退出程序（也可输入 exit / quit）\n\n"
        "直接输入问题即可，支持粘贴完整报错信息（traceback）。"
    )


def render_status(s: dict) -> str:
    return (
        "系统状态\n"
        f"{_THIN}\n"
        f"Rule Engine       OK（{s['rules']} 条规则）\n"
        f"Error Parser      OK\n"
        f"Knowledge Base    {s['knowledge_entries']} 条知识\n"
        f"Retrieval Mode    {s['retrieval_mode']}\n"
        f"Vector Index      {s['vector_index']}\n"
        f"LLM               {s['llm']}\n"
        f"Conversation      {s['messages']} 条消息\n"
        f"{_THIN}"
    )


def render_about(knowledge_entries: int) -> str:
    return (
        f"IT Support Bot V{VERSION}\n\n"
        "核心能力：\n"
        "  - 规则故障识别（45 条）\n"
        "  - 错误解析 Error Parser\n"
        "  - Hybrid RAG（关键词 + 向量 + RRF）\n"
        "  - DeepSeek LLM 兜底\n"
        "  - 多轮会话 + 诊断上下文\n"
        "  - 来源引用\n\n"
        f"知识库：{knowledge_entries} 条故障知识\n"
        "覆盖：Python / pip / Conda / Git / Windows / PyTorch / CUDA / 网络"
    )


def render_history(messages: list, max_len: int = 100) -> str:
    if not messages:
        return "（暂无对话历史）"
    lines = []
    for i, m in enumerate(messages, 1):
        role = "用户" if m["role"] == "user" else "助手"
        content = m["content"].replace("\n", " ")
        if len(content) > max_len:
            content = content[:max_len] + "…"
        lines.append(f"[{i}] {role}：{content}")
    return "\n".join(lines)


def handle_command(bot, cmd: str):
    """执行命令，返回 (展示文本, 是否退出)。"""
    if cmd == "help":
        return render_help(), False
    if cmd == "history":
        return render_history(bot.get_history()), False
    if cmd == "clear":
        bot.clear()
        return "当前会话已清空。", False
    if cmd == "status":
        return render_status(bot.status()), False
    if cmd == "about":
        return render_about(len(bot.engine.knowledge)), False
    if cmd == "exit":
        return "再见！", True
    if cmd == "unknown":
        return "未知命令，输入 /help 查看可用命令。", False
    return "", False


def run():
    """启动交互式 REPL，带异常兜底：单次失败不退出程序。"""
    from chatbot import Chatbot

    bot = Chatbot()
    print(render_welcome())

    while True:
        try:
            raw = input("\n你 > ")
        except (KeyboardInterrupt, EOFError):
            print("\n再见！")
            break

        text = raw.strip()
        if not text:
            continue
        if text.lower() in ("exit", "quit"):
            print("再见！")
            break

        cmd = parse_command(text)
        if cmd is not None:
            out, should_exit = handle_command(bot, cmd)
            print(out)
            if should_exit:
                break
            continue

        # 正常聊天，外层兜底，避免单次异常导致程序崩溃
        try:
            result = bot.reply(text)
        except Exception:
            print("\n[错误] 本次请求处理失败，请重试。")
            continue

        tag = _SOURCE_TAG.get(result["source"], "[?]")
        print(f"\n助手 {tag}：\n{result['text']}")

        if result["source"] != "llm":
            try:
                fb = input("这个方案解决你的问题了吗？(y=解决 / n=未解决 / 回车跳过)：").strip().lower()
                if fb in ("y", "yes", "是"):
                    bot.record_feedback(resolved=True)
                elif fb in ("n", "no", "否"):
                    bot.record_feedback(resolved=False)
            except (KeyboardInterrupt, EOFError):
                pass

    print("")
