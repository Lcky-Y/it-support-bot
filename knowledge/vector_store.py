"""
FAISS 向量存储
封装索引的构建、持久化（保存/加载）与检索。
向量统一做 L2 归一化 + IndexFlatIP，等价于余弦相似度。
所有 faiss / numpy 依赖均在方法内部懒加载，缺少时优雅返回 False / 空结果。
"""
import os
import json

from config import FAISS_INDEX_PATH, METADATA_PATH


def _import_faiss():
    try:
        import faiss
        return faiss
    except ImportError:
        return None


class VectorStore:
    def __init__(self, index_path: str = FAISS_INDEX_PATH, metadata_path: str = METADATA_PATH):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.index = None
        self.metadata = []

    @property
    def available(self) -> bool:
        return self.index is not None

    def build(self, vectors, chunks: list) -> None:
        """用向量与对应 chunk 构建索引（vectors 需与 chunks 顺序一致）。"""
        import numpy as np
        faiss = _import_faiss()
        if faiss is None:
            raise RuntimeError("faiss 未安装，无法构建索引")

        vectors = np.asarray(vectors, dtype="float32")
        faiss.normalize_L2(vectors)
        dim = int(vectors.shape[1])
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(vectors)
        self.metadata = [
            {
                "source": c.get("source", ""),
                "category": c.get("category", ""),
                "title": c.get("title", ""),
                "content": c.get("content", ""),
            }
            for c in chunks
        ]

    def save(self) -> bool:
        faiss = _import_faiss()
        if faiss is None or self.index is None:
            return False
        try:
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
            # 用 serialize_index 得到字节后再由 Python 写文件，
            # 避免 faiss 的 C++ 文件接口在含中文的路径下 fopen 失败
            data = faiss.serialize_index(self.index)
            with open(self.index_path, "wb") as f:
                f.write(data)
            with open(self.metadata_path, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def load(self) -> bool:
        faiss = _import_faiss()
        if faiss is None:
            return False
        if not (os.path.exists(self.index_path) and os.path.exists(self.metadata_path)):
            return False
        try:
            import numpy as np
            with open(self.index_path, "rb") as f:
                raw = f.read()
            # faiss.deserialize_index 需要 numpy uint8 数组，而不是 bytes
            self.index = faiss.deserialize_index(np.frombuffer(raw, dtype="uint8"))
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
            return True
        except Exception:
            self.index = None
            self.metadata = []
            return False

    def search(self, query_vector, top_k: int = 3) -> list:
        """按余弦相似度检索，返回带 score 的 chunk 列表。"""
        import numpy as np
        faiss = _import_faiss()
        if faiss is None or self.index is None:
            return []

        vec = np.asarray([query_vector], dtype="float32")
        faiss.normalize_L2(vec)
        scores, indices = self.index.search(vec, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            chunk = dict(self.metadata[idx])
            chunk["score"] = float(score)
            results.append(chunk)
        return results
