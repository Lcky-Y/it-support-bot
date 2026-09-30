"""
Streamlit UI 冒烟测试（AppTest，无浏览器/无服务器）

验证 ui/app.py 展示层：初始渲染、规则命中回答、Hybrid RAG 命中与来源、
清空会话、侧边栏系统状态。仅断言 UI 行为，不重复覆盖核心诊断逻辑
（核心已由 test_e2e / test_vector_retrieval 等覆盖）。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit.testing.v1 import AppTest

APP_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ui", "app.py")


def _new_app():
    # default_timeout 调大：首次 run 会懒加载 embedding 模型 + FAISS 索引，较慢
    return AppTest.from_file(APP_PATH, default_timeout=180)


def _all_markdown(at):
    return [m.value for m in at.markdown]


def test_initial_render():
    at = _new_app().run()
    assert not at.exception, f"初始渲染异常: {[e.value for e in at.exception]}"
    assert at.title, "应渲染标题"
    assert "IT 技术支持助手" in at.title[0].value, "标题应包含应用名"


def test_rule_hit():
    at = _new_app().run()
    at.chat_input[0].set_value("No module named torch").run()
    assert not at.exception, f"规则命中异常: {[e.value for e in at.exception]}"
    texts = _all_markdown(at)
    assert any("ModuleNotFoundError" in t or "模块" in t for t in texts), "规则命中应展示回答"
    labels = [e.label for e in at.expander]
    assert any("Rule" in l for l in labels), f"应展示 Rule 来源标签，实际 {labels}"


def test_hybrid_rag_hit():
    at = _new_app().run()
    at.chat_input[0].set_value("数据库提示 database is locked").run()
    assert not at.exception, f"RAG 命中异常: {[e.value for e in at.exception]}"
    labels = [e.label for e in at.expander]
    assert any("参考来源" in l for l in labels), f"应展示参考来源折叠，实际 {labels}"
    texts = _all_markdown(at)
    assert any("database is locked" in t for t in texts), "命中知识应包含 database is locked"


def test_clear_button():
    at = _new_app().run()
    at.chat_input[0].set_value("No module named torch").run()
    assert at.session_state["messages"], "发送消息后应存在会话消息"
    at.sidebar.button[0].click().run()
    assert not at.exception, f"清空会话异常: {[e.value for e in at.exception]}"
    assert at.session_state["messages"] == [], "清空后消息列表应为空"


def test_sidebar_status():
    at = _new_app().run()
    assert not at.exception
    sidebar_text = " ".join([m.value for m in at.sidebar.markdown])
    for key in ("Rule Engine", "Knowledge Base", "Retrieval", "LLM"):
        assert key in sidebar_text, f"侧边栏应显示 {key}"


def main():
    import traceback
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = skipped = 0
    for fn in tests:
        try:
            status = fn()
            if status == "skip":
                skipped += 1
                print(f"- {fn.__name__} (skip)")
            else:
                passed += 1
                print(f"✓ {fn.__name__}")
        except AssertionError as e:
            print(f"✗ {fn.__name__}: {e}")
        except Exception:
            print(f"✗ {fn.__name__} 异常:")
            traceback.print_exc()
    print(f"\n通过 {passed}/{len(tests)}（跳过 {skipped}）")


if __name__ == "__main__":
    main()
