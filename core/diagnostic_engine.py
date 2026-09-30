"""
诊断引擎
编排完整诊断流程：

    用户输入
      → 错误解析（error_parser）
      → 规则匹配（rule_engine）
      → 按置信度分派：
            ≥ 0.80  规则答案
            ≥ 0.60  规则答案 + LLM 补充解释
            <  0.60 意图分类 → 知识检索 → LLM 综合诊断

统一返回结构化结果，供 chatbot / 未来 Web 层直接消费。
"""
from config import MATCH_THRESHOLD, RULE_CONFIDENT_THRESHOLD

from core import error_parser
from core.rule_engine import RuleEngine
from core.intent_classifier import classify
from core import response_formatter
from services.knowledge_service import KnowledgeService
from llm import client as llm_client
from llm import prompts as llm_prompts


class DiagnosticEngine:
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.knowledge = KnowledgeService()

    def diagnose(self, user_text: str, history: list = None) -> dict:
        history = history or []

        parsed_error = error_parser.parse(user_text)
        rule, score = self.rule_engine.match(user_text, parsed_error)

        # 高置信度：直接返回规则答案
        if rule and score >= RULE_CONFIDENT_THRESHOLD:
            return self._result(
                text=response_formatter.format_rule_response(rule, parsed_error),
                source="rule", category=rule.get("category"),
                rule_id=rule.get("id"), confidence=score, error=parsed_error,
            )

        # 中等置信度：规则答案 + LLM 补充解释
        if rule and score >= MATCH_THRESHOLD:
            base_text = response_formatter.format_rule_response(rule, parsed_error)
            text = base_text
            if llm_client.is_available():
                try:
                    prompt = llm_prompts.RULE_LLM_PROMPT.format(
                        rule_answer=base_text, user_text=user_text)
                    extra = llm_client.generate_with_prompt(user_text, prompt, history)
                    if extra and extra.strip():
                        text = f"{base_text}\n【补充说明】\n{extra.strip()}\n"
                except Exception:
                    pass
            return self._result(
                text=text, source="rule+llm", category=rule.get("category"),
                rule_id=rule.get("id"), confidence=score, error=parsed_error,
            )

        # 未命中：意图分类 + 知识检索 + LLM 综合诊断
        category, _ = classify(user_text)
        snippets = self.knowledge.retrieve(user_text, top_k=3)
        text = self._llm_diagnose(user_text, history, snippets)
        references = [s["title"] for s in snippets]

        return self._result(
            text=text, source="llm", category=category,
            rule_id=None, confidence=score, error=parsed_error,
            references=references,
        )

    @staticmethod
    def _format_knowledge(snippets) -> str:
        parts = []
        for s in snippets:
            parts.append(f"【{s['title']}】(来源: {s['source']})\n{s['content']}")
        return "\n\n".join(parts)

    def _llm_diagnose(self, user_text, history, snippets) -> str:
        if llm_client.is_available():
            try:
                knowledge = self._format_knowledge(snippets) if snippets else "（无相关知识片段）"
                prompt = llm_prompts.RAG_PROMPT_TEMPLATE.format(
                    user_text=user_text, knowledge=knowledge)
                return response_formatter.format_llm_response(
                    llm_client.generate_with_prompt(user_text, prompt, history))
            except Exception:
                pass

        if snippets:
            return "【问题判断】\n已为你匹配到以下相关知识，请参考：\n\n" + \
                   self._format_knowledge(snippets) + \
                   "\n\n【参考来源】\n" + "\n".join(f"- {s['source']}" for s in snippets) + "\n"
        return (
            "【问题判断】\n暂时无法确定问题类型，也没有命中相关知识。\n\n"
            "请补充：\n1. 完整报错信息（可直接粘贴 traceback）\n"
            "2. 你的操作系统与 Python/工具版本\n"
            "3. 已经尝试过的操作\n"
        )

    @staticmethod
    def _result(**kwargs) -> dict:
        return kwargs
