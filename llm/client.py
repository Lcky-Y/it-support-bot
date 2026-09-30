"""
大模型客户端
封装 DeepSeek（兼容 OpenAI 协议）调用，统一异常处理与超时控制。
"""
from openai import OpenAI, APIError, APITimeoutError

from config import (
    OPENAI_API_KEY, OPENAI_BASE_URL, LLM_MODEL_NAME,
    LLM_TIMEOUT, LLM_ENABLED, MAX_HISTORY_TURNS,
)
from llm.prompts import SYSTEM_PROMPT

_client = None
if LLM_ENABLED:
    _client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, timeout=LLM_TIMEOUT)


def is_available() -> bool:
    return LLM_ENABLED and _client is not None


def generate_reply(user_text: str, history: list, system_prompt: str = None) -> str:
    """
    调用大模型生成回复。
    history: [{"role": "user"/"assistant", "content": "..."}, ...]
    返回生成的文本；失败时抛出异常由上层兜底。
    """
    if not is_available():
        raise RuntimeError("LLM 未配置（缺少 OPENAI_API_KEY）")

    recent = history[-MAX_HISTORY_TURNS * 2:]
    messages = [{"role": "system", "content": system_prompt or SYSTEM_PROMPT}]
    messages.extend(recent)
    messages.append({"role": "user", "content": user_text})

    response = _client.chat.completions.create(
        model=LLM_MODEL_NAME,
        messages=messages,
        temperature=0.3,
        # DeepSeek 默认开启“思考模式”；技术支持场景不需要长推理，关闭以降低延迟与成本
        extra_body={"thinking": {"type": "disabled"}},
    )
    return response.choices[0].message.content


def generate_with_prompt(user_text: str, prompt: str, history: list) -> str:
    """用自定义 user 提示词（如 RAG / 规则解释）调用大模型。"""
    if not is_available():
        raise RuntimeError("LLM 未配置（缺少 OPENAI_API_KEY）")

    recent = history[-MAX_HISTORY_TURNS * 2:]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(recent)
    messages.append({"role": "user", "content": prompt})

    response = _client.chat.completions.create(
        model=LLM_MODEL_NAME,
        messages=messages,
        temperature=0.3,
        extra_body={"thinking": {"type": "disabled"}},
    )
    return response.choices[0].message.content
