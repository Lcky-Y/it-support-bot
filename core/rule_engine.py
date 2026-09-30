"""
规则引擎模块（多层级匹配）
不再单纯依赖 difflib 模糊相似度，而是按信号强度分层打分：

    第一层  错误类型精确匹配（依赖 error_parser 解析结果）    1.00
    第二层  错误代码 / 特征短语子串命中                        0.95
    第三层  关键词组合命中                                     0.90 / 0.80 / 0.70
    第四层  difflib 模糊匹配（降权，仅作兜底）                 动态（≤ 0.60）

分数相同的规则通过“关键词命中数 → 优先级”进一步打破平局，
保证更具体的规则（如 pip SSL 错误）优先于宽泛规则（如通用网络 SSL）。
"""
import json
import difflib

from config import RULES_PATH


class RuleEngine:
    def __init__(self, rules_path: str = RULES_PATH):
        with open(rules_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.rules = data["rules"]

    # ------------------------------------------------------------------
    # 内部打分
    # ------------------------------------------------------------------
    def _error_type_match(self, rule: dict, parsed_error: dict) -> bool:
        if not parsed_error or not parsed_error.get("error_type"):
            return False
        rule_et = (rule.get("error_type") or "").lower()
        return bool(rule_et) and rule_et == parsed_error["error_type"].lower()

    def _keyword_hits(self, text_lower: str, rule: dict) -> int:
        kws = rule.get("keywords") or []
        return sum(1 for k in kws if k and k.lower() in text_lower)

    def _score_rule(self, text_lower: str, rule: dict, parsed_error: dict) -> float:
        # 第一层：错误类型精确匹配
        if self._error_type_match(rule, parsed_error):
            return 1.00

        # 第二层：错误代码 / 特征短语子串命中
        for pattern in rule.get("patterns") or []:
            if pattern and pattern.lower() in text_lower:
                return 0.95

        # 第三层：关键词组合命中
        kws = rule.get("keywords") or []
        if kws:
            hits = self._keyword_hits(text_lower, rule)
            ratio = hits / len(kws)
            if ratio >= 1.0:
                return 0.90
            if ratio >= 0.5:
                return 0.80
            if hits >= 2:
                return 0.70
            if hits == 1:
                # 单个关键词命中不足以触发规则，避免通用词（如 "git"、"torch"）误命中
                return 0.55
            # hits == 0 时继续落入第四层模糊匹配

        # 第四层：difflib 模糊匹配（降权，仅作弱信号，不使其单独触发命中）
        best = 0.0
        for pattern in rule.get("patterns") or []:
            if not pattern:
                continue
            best = max(best, difflib.SequenceMatcher(None, text_lower, pattern.lower()).ratio())
        if best >= 0.80:
            return 0.58
        return best * 0.5

    # ------------------------------------------------------------------
    # 对外匹配
    # ------------------------------------------------------------------
    def match(self, user_text: str, parsed_error: dict = None):
        """
        返回 (命中的规则 dict, 匹配分数)；未达到阈值时规则为 None。
        """
        text_lower = (user_text or "").lower().strip()

        best_rule = None
        best_score = 0.0
        best_hits = -1
        best_priority = -1

        for rule in self.rules:
            score = self._score_rule(text_lower, rule, parsed_error)
            hits = self._keyword_hits(text_lower, rule)
            priority = rule.get("priority", 0)
            # 元组比较：先比分数，再比关键词命中数（更具体），最后比优先级
            if (score, hits, priority) > (best_score, best_hits, best_priority):
                best_score, best_hits, best_priority = score, hits, priority
                best_rule = rule

        if best_score >= 0.60:
            return best_rule, best_score
        return None, best_score
