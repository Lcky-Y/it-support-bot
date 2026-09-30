"""
IT 技术支持助手 —— Streamlit UI（纯展示层）

只调用现有核心（chatbot.reply / get_history / clear / status 与 knowledge.retrieve），
不包含任何诊断 / 检索 / 规则逻辑，保证与 CLI 共用同一套核心，避免逻辑分叉。

启动：streamlit run ui/app.py
"""
import sys
from pathlib import Path

# 让 ui/ 能导入项目根目录的 core / services / chatbot / config 等模块
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from chatbot import Chatbot

# 来源类型 -> 展示标签
SOURCE_LABELS = {
    "rule": "Rule（规则引擎）",
    "rule+llm": "Rule + LLM",
    "llm": "Hybrid RAG",
}

st.set_page_config(page_title="IT 技术支持助手", page_icon="🛠️", layout="wide")


# ----------------------------------------------------------------------
# 会话状态：每个浏览器会话一个 Chatbot（含对话历史与诊断上下文）
# ----------------------------------------------------------------------
if "bot" not in st.session_state:
    st.session_state.bot = Chatbot()
if "messages" not in st.session_state:
    st.session_state.messages = []

bot: Chatbot = st.session_state.bot


# ----------------------------------------------------------------------
# 侧边栏：系统状态 + 清空会话 + 检索详情开关
# ----------------------------------------------------------------------
def render_sidebar() -> None:
    with st.sidebar:
        st.header("系统状态")

        status = bot.status()
        vector_ok = status["vector_index"] == "Available"

        st.markdown(
            f"- **Rule Engine**：OK（{status['rules']} 条规则）\n"
            f"- **Knowledge Base**：{status['knowledge_entries']} 条知识\n"
            f"- **Retrieval**：{status['retrieval_mode']}\n"
            f"- **Vector Model**：{'Local' if vector_ok else '未构建（关键词兜底）'}\n"
            f"- **LLM**：{status['llm']}\n"
            f"- **Conversation**：{status['messages']} 条消息"
        )

        st.divider()
        st.session_state.show_retrieval = st.toggle(
            "显示检索详情", value=st.session_state.get("show_retrieval", True)
        )

        st.divider()
        if st.button("清空会话", type="secondary"):
            bot.clear()
            st.session_state.messages = []
            st.rerun()


def render_retrieval_detail(hits: list) -> None:
    """折叠展示 Top-K 命中知识（标题 / 分类 / 来源）。"""
    if not hits:
        st.caption("（未命中相关知识）")
        return
    for i, h in enumerate(hits, 1):
        st.markdown(
            f"**{i}. {h.get('title', '')}**\n\n"
            f"· 分类：`{h.get('category', '')}`　· 来源：`{h.get('source', '')}`"
        )


def render_assistant_message(msg: dict) -> None:
    """渲染一条助手消息，附来源类型与可折叠的命中知识。"""
    with st.chat_message("assistant"):
        st.markdown(msg["content"])

        source = msg.get("source", "llm")
        label = SOURCE_LABELS.get(source, source)

        with st.expander(f"参考来源 · {label}", expanded=False):
            if source in ("rule", "rule+llm"):
                st.markdown(
                    f"- **检索方式**：{label}\n"
                    f"- **分类**：`{msg.get('category', '')}`\n"
                    f"- **规则**：`{msg.get('rule_id', '')}`\n"
                    f"- **置信度**：{msg.get('confidence', 0):.2f}"
                )
            else:
                st.markdown(
                    f"- **检索方式**：{label}\n"
                    f"- **分类**：`{msg.get('category', '')}`"
                )
                if msg.get("references"):
                    st.markdown("- **参考来源**：" + "、".join(msg["references"]))
                if st.session_state.get("show_retrieval", True):
                    st.markdown("**命中知识**")
                    render_retrieval_detail(msg.get("hits", []))


# ----------------------------------------------------------------------
# 主区域
# ----------------------------------------------------------------------
render_sidebar()

st.title("🛠️ IT 技术支持助手")
st.caption("规则引擎 · 错误解析 · Hybrid RAG · LLM 兜底")

# 渲染历史
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        render_assistant_message(msg)

# 处理新输入
if prompt := st.chat_input("描述你遇到的报错或问题……"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("正在诊断……"):
        try:
            result = bot.reply(prompt)
        except Exception:
            result = {
                "text": "本次请求处理失败，请稍后重试。",
                "source": "llm",
                "category": "",
                "confidence": 0.0,
                "references": [],
            }

        assistant_msg = {
            "role": "assistant",
            "content": result["text"],
            "source": result.get("source", "llm"),
            "category": result.get("category", ""),
            "confidence": result.get("confidence", 0.0),
            "rule_id": result.get("rule_id"),
            "references": result.get("references", []),
            "hits": [],
        }

        if result.get("source") == "llm":
            try:
                assistant_msg["hits"] = bot.engine.knowledge.retrieve(prompt, top_k=3)
            except Exception:
                assistant_msg["hits"] = []

        st.session_state.messages.append(assistant_msg)

    st.rerun()
