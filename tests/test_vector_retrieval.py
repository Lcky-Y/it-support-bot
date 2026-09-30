"""
向量 / Hybrid 检索测试（Stage 5）
覆盖：向量后端可用性、索引构建/保存/加载、来源引用、依赖缺失自动降级、
空知识库不崩溃，以及 Lexical / Vector / Hybrid 三路检索的 Recall 对比 benchmark。
"""
import os
import sys
import json
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.knowledge_service import KnowledgeService
from knowledge.embedding_model import dependencies_available

CASES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_cases_rag.json")


def _load_cases():
    with open(CASES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("benchmark_cases", []), data.get("paraphrase_cases", [])


def _recall(ks, cases, mode, top_k=5):
    hits = {1: 0, 3: 0, 5: 0}
    for c in cases:
        top = ks.retrieve(c["query"], top_k=top_k, mode=mode)
        titles = [t["title"] for t in top]
        for k in (1, 3, 5):
            if c["expected_title"] in titles[:k]:
                hits[k] += 1
    n = len(cases) if cases else 1
    return {k: hits[k] / n for k in (1, 3, 5)}


def test_fallback_without_vector():
    ks = KnowledgeService(use_vector=False)   # 强制走关键词兜底
    r = ks.retrieve("No module named torch", top_k=3)
    assert r, "关键词兜底检索不应为空"
    assert all("title" in x and "source" in x for x in r)


def test_source_citation():
    ks = KnowledgeService(use_vector=False)
    top = ks.retrieve("CERTIFICATE_VERIFY_FAILED", top_k=3)
    assert top and top[0]["source"].endswith(".md")


def test_empty_knowledge():
    with tempfile.TemporaryDirectory() as d:
        ks = KnowledgeService(documents_dir=d, use_vector=False)
        assert ks.retrieve("任何问题") == []


def test_index_build_save_load():
    if not dependencies_available():
        print("  (skip) 未安装 sentence-transformers / faiss")
        return "skip"
    from knowledge.document_loader import load_documents
    from knowledge.text_splitter import split_entries
    from knowledge.embedding_model import get_embedder
    from knowledge.vector_store import VectorStore

    embedder = get_embedder()
    if not embedder.available:
        print("  (skip) embedding 模型加载失败")
        return "skip"

    chunks = split_entries(load_documents())
    texts = [c["content"] for c in chunks]
    vecs = embedder.encode(texts)

    with tempfile.TemporaryDirectory() as d:
        idx = os.path.join(d, "index.faiss")
        meta = os.path.join(d, "metadata.json")
        store = VectorStore(idx, meta)
        store.build(vecs, chunks)
        assert store.save(), "索引保存应成功"

        store2 = VectorStore(idx, meta)
        assert store2.load(), "索引加载应成功"
        qvec = embedder.encode(["No module named torch"])[0]
        res = store2.search(qvec, top_k=3)
        assert res, "向量检索应返回结果"
        assert res[0]["source"].endswith(".md")


def _fmt(recalls):
    return f"R@1={recalls[1]:.1%}  R@3={recalls[3]:.1%}  R@5={recalls[5]:.1%}"


def test_benchmark_recall():
    exact, paraphrase = _load_cases()
    all_cases = exact + paraphrase

    ks = KnowledgeService()
    vector_available = ks.using_vector

    print(f"\n  benchmark：{len(exact)} 条精确问题 + {len(paraphrase)} 条语义改写")
    for mode in ("lexical", "vector", "hybrid"):
        r = _recall(ks, all_cases, mode)
        print(f"    {mode:8s} 全部  -> {_fmt(r)}")

    if vector_available and paraphrase:
        print("  —— 仅语义改写问题（向量检索优势场景）——")
        for mode in ("lexical", "vector", "hybrid"):
            r = _recall(ks, paraphrase, mode)
            print(f"    {mode:8s} 改写  -> {_fmt(r)}")

    lex = _recall(ks, all_cases, "lexical")
    hyb = _recall(ks, all_cases, "hybrid")
    assert hyb[3] >= 0.90, f"Hybrid Recall@3 应 >= 90%，实际 {hyb[3]:.1%}"
    assert hyb[3] >= lex[3], f"Hybrid Recall@3 应 >= Lexical（{lex[3]:.1%}），实际 {hyb[3]:.1%}"
    assert hyb[1] >= lex[1], f"Hybrid Recall@1 应 >= Lexical（{lex[1]:.1%}），实际 {hyb[1]:.1%}"


def main():
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
            import traceback
            print(f"✗ {fn.__name__} 异常:")
            traceback.print_exc()
    print(f"\n通过 {passed}/{len(tests)}（跳过 {skipped}）")


if __name__ == "__main__":
    main()
