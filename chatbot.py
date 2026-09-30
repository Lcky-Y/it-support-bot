"""
聊天机器人主类
负责会话编排：调用诊断引擎生成回复，维护对话历史与诊断上下文，并记录日志。
优先走规则引擎（零成本、可控、响应快），未命中/低置信度时转交大模型兜底。
"""
from core.diagnostic_engine import DiagnosticEngine
from services.history import HistoryManager, new_session_id
from services import logger


class Chatbot:
    def __init__(self, session_id: str = None):
        self.engine = DiagnosticEngine()
        self.history = HistoryManager()
        self.session_id = session_id or new_session_id()
        self._last_query = ""
        self._last_result = None

    def reply(self, user_text: str) -> dict:
        """生成回复，返回结构化的诊断结果。"""
        result = self.engine.diagnose(user_text, self.history.as_list())

        # 更新诊断上下文（多轮排查中逐步累积关键信息）
        self._update_context(user_text, result)

        # 记录对话历史与日志
        self.history.add("user", user_text)
        self.history.add("assistant", result["text"])
        logger.log_conversation(self.session_id, "user", user_text)
        logger.log_conversation(self.session_id, "assistant", result["text"])

        # 规则未完全接管（需要 LLM 参与）的问题，记录到 fallback 日志供后续 review
        if result["source"] != "rule":
            logger.log_fallback(
                user_text,
                category=result.get("category", "unknown"),
                matched_rule=result.get("rule_id"),
                score=result.get("confidence", 0.0),
                used_llm=(result["source"] == "llm"),
            )

        self._last_query = user_text
        self._last_result = result
        return result

    def record_feedback(self, resolved: bool, feedback: str = ""):
        """记录用户反馈（是否解决了问题），用于后续统计解决率。"""
        if self._last_result is None:
            return
        logger.log_fallback(
            self._last_query,
            category=self._last_result.get("category", "unknown"),
            matched_rule=self._last_result.get("rule_id"),
            score=self._last_result.get("confidence", 0.0),
            used_llm=(self._last_result.get("source") == "llm"),
            resolved="True" if resolved else "False",
            feedback=feedback,
        )

    # ------------------------------------------------------------------
    # CLI 支持接口（供 cli.py / 未来前端调用）
    # ------------------------------------------------------------------
    def get_history(self) -> list:
        """返回当前会话对话历史 [{role, content}, ...]。"""
        return self.history.as_list()

    def clear(self):
        """清空对话历史与诊断上下文（不影响日志/知识库/向量索引）。"""
        self.history.clear()
        self._last_query = ""
        self._last_result = None

    def status(self) -> dict:
        """返回系统运行状态，供 /status 展示。"""
        from config import LLM_MODEL_NAME
        from llm import client as llm_client

        using_vector = self.engine.knowledge.using_vector
        return {
            "rules": len(self.engine.rule_engine.rules),
            "knowledge_entries": len(self.engine.knowledge),
            "retrieval_mode": "Hybrid" if using_vector else "Lexical",
            "vector_index": "Available" if using_vector else "Not built (keyword fallback)",
            "llm": LLM_MODEL_NAME if llm_client.is_available() else "未配置",
            "messages": len(self.history.as_list()),
        }

    def _update_context(self, user_text: str, result: dict):
        self.history.update_context(category=result.get("category"))
        error = result.get("error")
        if error:
            self.history.update_context(error_type=error.get("error_type"))
            if error.get("module"):
                self.history.update_context(module=error.get("module"))
