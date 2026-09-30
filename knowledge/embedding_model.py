"""
Embedding 模型封装
按需加载 sentence-transformers 多语言模型；未安装或加载失败时优雅降级，
返回的编码结果均做 L2 归一化（配合 FAISS IndexFlatIP 实现余弦相似度）。

模型完全离线加载：优先读取本地目录 knowledge/models/<model>，并通过环境变量
禁止 Hugging Face 联网（不再自动下载、不再发起 HEAD/Retry 请求）。
本地模型缺失时立即降级为关键词检索。
"""
import os

from config import EMBEDDING_MODEL_NAME, EMBEDDING_MODEL_PATH

# 在导入 sentence-transformers 之前强制离线，避免任何隐式联网行为
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")


def dependencies_available() -> bool:
    """检查向量检索所需依赖是否可导入（不加载模型，代价很低）。"""
    try:
        import sentence_transformers  # noqa: F401
        import faiss  # noqa: F401
        import numpy  # noqa: F401
        return True
    except ImportError:
        return False


class Embedder:
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME,
                 model_path: str = EMBEDDING_MODEL_PATH):
        self.model_name = model_name
        self.model_path = model_path
        self.model = None
        if not dependencies_available():
            return
        try:
            from sentence_transformers import SentenceTransformer
            # 优先从本地目录加载；本地缺失时仅允许离线使用 HF 缓存，禁止联网下载
            if self.model_path and os.path.isdir(self.model_path):
                self.model = SentenceTransformer(str(self.model_path), local_files_only=True)
            else:
                self.model = SentenceTransformer(model_name, local_files_only=True)
        except Exception:
            self.model = None

    @property
    def available(self) -> bool:
        return self.model is not None

    def encode(self, texts, normalize: bool = True):
        """把文本列表编码为 float32 向量数组，并做 L2 归一化。"""
        import numpy as np
        if self.model is None:
            raise RuntimeError("embedding 模型不可用（缺少依赖或加载失败）")
        vectors = self.model.encode(
            list(texts), normalize_embeddings=normalize, show_progress_bar=False
        )
        return np.asarray(vectors, dtype="float32")


_embedder = None


def get_embedder() -> Embedder:
    """获取全局单例 Embedder（惰性加载，避免重复初始化模型）。"""
    global _embedder
    if _embedder is None:
        _embedder = Embedder()
    return _embedder
