"""
统一日志服务
记录两类日志：
1. fallback_queries.csv —— 未命中规则、转交 LLM 的问题，便于人工 review 后补充规则；
2. conversations.csv   —— 完整对话流水，便于后续分析高频问题与解决率。
"""
import os
import csv
from datetime import datetime

from config import FALLBACK_LOG_PATH, CONVERSATION_LOG_PATH

_FALLBACK_HEADER = [
    "timestamp", "query", "category", "matched_rule", "score", "used_llm",
    "resolved", "feedback",
]
_CONVERSATION_HEADER = ["timestamp", "session_id", "role", "content"]


def _append(path, header, row):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file_exists = os.path.exists(path) and os.path.getsize(path) > 0
        with open(path, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header)
            writer.writerow(row)
    except Exception:
        # 日志写入失败不应影响主流程
        pass


def log_fallback(query, category="unknown", matched_rule=None, score=0.0,
                 used_llm=True, resolved="", feedback=""):
    """记录一条未命中规则（或需 LLM 增强）的查询。"""
    _append(
        FALLBACK_LOG_PATH, _FALLBACK_HEADER,
        [
            datetime.now().isoformat(timespec="seconds"),
            query, category, matched_rule or "", f"{score:.3f}",
            "True" if used_llm else "False", resolved, feedback,
        ],
    )


def log_conversation(session_id, role, content):
    """记录一条对话消息（user / assistant）。"""
    _append(
        CONVERSATION_LOG_PATH, _CONVERSATION_HEADER,
        [datetime.now().isoformat(timespec="seconds"), session_id, role, content],
    )
