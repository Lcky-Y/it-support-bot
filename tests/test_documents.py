"""
知识库文档与检索测试
验证文档加载、切块与关键词检索（来源引用）是否正常工作。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from knowledge.document_loader import load_documents
from knowledge.text_splitter import split_entries
from services.knowledge_service import KnowledgeService


def test_entry_count():
    entries = load_documents()
    assert len(entries) >= 60, f"知识条目数量应 >= 60，实际 {len(entries)}"
    categories = {e["category"] for e in entries}
    assert "python" in categories and "git" in categories and "network" in categories


def test_chunk_structure():
    chunks = split_entries(load_documents())
    assert chunks, "切块结果不应为空"
    for c in chunks:
        for key in ("source", "category", "title", "content"):
            assert key in c, f"chunk 缺少字段 {key}"
        assert c["content"].strip(), f"{c['title']} 正文为空"


def test_retrieve_python():
    ks = KnowledgeService()
    top = ks.retrieve("No module named torch", top_k=3)
    titles = [c["title"] for c in top]
    assert any("ModuleNotFoundError" in t for t in titles), f"应命中模块缺失知识，实际 {titles}"


def test_retrieve_cuda():
    ks = KnowledgeService()
    top = ks.retrieve("torch.cuda.is_available() 返回 false", top_k=3)
    titles = [c["title"] for c in top]
    assert any("is_available" in t for t in titles), f"应命中 CUDA 检测知识，实际 {titles}"


def test_retrieve_git():
    ks = KnowledgeService()
    top = ks.retrieve("git 合并冲突", top_k=3)
    titles = [c["title"] for c in top]
    assert any("合并冲突" in t for t in titles), f"应命中合并冲突知识，实际 {titles}"


def test_retrieve_pip():
    ks = KnowledgeService()
    top = ks.retrieve("pip 换源", top_k=3)
    titles = [c["title"] for c in top]
    assert any("镜像" in t for t in titles), f"应命中镜像源知识，实际 {titles}"


def test_source_citation():
    ks = KnowledgeService()
    top = ks.retrieve("CERTIFICATE_VERIFY_FAILED", top_k=3)
    if top:
        assert top[0]["source"].endswith(".md"), "来源应指向 Markdown 文件"


def main():
    import traceback
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for fn in tests:
        try:
            fn()
            print(f"✓ {fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {fn.__name__}: {e}")
        except Exception:
            print(f"✗ {fn.__name__} 异常:")
            traceback.print_exc()
    print(f"\n通过 {passed}/{len(tests)}")


if __name__ == "__main__":
    main()
