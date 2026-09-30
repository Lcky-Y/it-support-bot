"""
规则引擎测试脚本
加载 tests/test_cases.json 中的标注问题集，评估“错误解析 + 规则匹配”的整体识别准确率。
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.rule_engine import RuleEngine
from core import error_parser

TEST_CASES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_cases.json")


def load_cases():
    with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["test_cases"]


def run(verbose: bool = True):
    engine = RuleEngine()
    cases = load_cases()
    correct = 0
    failures = []

    for case in cases:
        query = case["query"]
        expected = case["expected"]
        parsed = error_parser.parse(query)
        rule, score = engine.match(query, parsed)
        actual = rule["id"] if rule else None
        ok = (actual == expected)
        correct += int(ok)
        if not ok:
            failures.append((query, expected, actual, score))

        if verbose:
            status = "✓" if ok else "✗"
            print(f"{status} {query!r}  期望={expected}  实际={actual}  score={score:.2f}")

    accuracy = correct / len(cases) if cases else 0.0
    print(f"\n规则识别准确率：{accuracy:.2%}（{correct}/{len(cases)}）")

    if failures:
        print(f"\n失败 {len(failures)} 条：")
        for q, exp, act, sc in failures:
            print(f"  - {q!r} 期望={exp} 实际={act} score={sc:.2f}")

    return accuracy, failures


if __name__ == "__main__":
    run()
