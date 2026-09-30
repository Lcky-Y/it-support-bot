"""
回复格式化器
将规则命中结果 / LLM 输出统一成结构化的专业诊断答复，而非一大段散文。

结构：
    【问题判断】
    【可能原因】
    【检查步骤】
    【解决方法】
    【仍无法解决】
"""
from core.error_parser import ERROR_TYPE_LABELS


def _section(lines, title, content):
    if not content:
        return
    lines.append(f"【{title}】")
    lines.append("")
    if isinstance(content, str):
        lines.append(content)
    else:
        for i, item in enumerate(content, 1):
            lines.append(f"{i}. {item}")
    lines.append("")


def format_rule_response(rule: dict, parsed_error: dict = None) -> str:
    """将一条命中的规则格式化为结构化诊断答复。"""
    resp = rule.get("response", {})
    lines = []

    # 问题判断
    title = resp.get("title") or rule.get("id")
    lines.append("【问题判断】")
    lines.append("")
    lines.append(title)
    if parsed_error and parsed_error.get("module"):
        lines.append("")
        lines.append(f"涉及模块：{parsed_error['module']}")
    lines.append("")

    # 可能原因
    _section(lines, "可能原因", resp.get("causes"))

    # 检查步骤
    _section(lines, "检查步骤", resp.get("checks"))

    # 解决方法
    solution = resp.get("solution")
    if solution:
        lines.append("【解决方法】")
        lines.append("")
        if isinstance(solution, str):
            lines.append(solution)
        else:
            for cmd in solution:
                lines.append(f"    {cmd}")
        lines.append("")

    # 仍无法解决
    further = resp.get("further")
    if further:
        lines.append("【仍无法解决】")
        lines.append("")
        lines.append(further)
        lines.append("")
    else:
        lines.append("【仍无法解决】")
        lines.append("")
        lines.append("请提供：python --version、python -m pip --version、where python 的输出，以便进一步定位。")

    return "\n".join(lines).strip() + "\n"


def format_llm_response(text: str) -> str:
    """LLM 兜底回复：原样返回（提示词已要求其按结构化格式输出）。"""
    return (text or "").strip() + "\n"


def error_banner(parsed_error: dict) -> str:
    """为命中错误时生成一句简短判断语，便于日志与调试。"""
    if not parsed_error:
        return ""
    label = ERROR_TYPE_LABELS.get(parsed_error["error_type"], parsed_error["error_type"])
    return f"检测到错误类型：{label}"
