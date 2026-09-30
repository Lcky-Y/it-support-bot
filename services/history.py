"""
对话历史与诊断上下文
1. 保留最近 N 轮对话，供 LLM 多轮上下文使用；
2. 维护一个轻量“诊断上下文”，在多轮排查中逐步累积关键信息
   （如分类、操作系统、GPU、Python 版本、错误类型），让后续回答更精准。
"""
import uuid
from collections import deque

from config import MAX_HISTORY_TURNS


class HistoryManager:
    def __init__(self, max_turns: int = MAX_HISTORY_TURNS):
        self.max_turns = max_turns
        self.messages = deque(maxlen=max_turns * 2)   # 每轮 1 问 1 答
        self.diagnostic_context = {}

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def clear(self):
        """清空对话历史与诊断上下文（不影响日志、知识库与向量索引）。"""
        self.messages.clear()
        self.diagnostic_context = {}

    def as_list(self) -> list:
        return list(self.messages)

    def update_context(self, **kwargs):
        """用非空值更新诊断上下文。"""
        for k, v in kwargs.items():
            if v:
                self.diagnostic_context[k] = v

    def context_summary(self) -> str:
        if not self.diagnostic_context:
            return ""
        items = [f"{k}={v}" for k, v in self.diagnostic_context.items()]
        return "；".join(items)


def new_session_id() -> str:
    return uuid.uuid4().hex[:12]
