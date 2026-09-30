"""
全局配置文件
统一管理路径、匹配阈值、大模型、日志等配置，保证整个项目共用同一套参数。
"""
import os
from dotenv import load_dotenv

# 项目根目录（本文件所在目录），保证相对路径不受运行时工作目录影响
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 项目版本
VERSION = "1.2"

# 加载 .env 文件中的环境变量（如 API Key）
load_dotenv(os.path.join(BASE_DIR, ".env"))

# ------------------ 路径配置 ------------------
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")          # 知识库目录
RULES_PATH = os.path.join(KNOWLEDGE_DIR, "rules.json")       # 故障诊断规则库
FAQ_PATH = os.path.join(KNOWLEDGE_DIR, "faq.json")           # 补充 FAQ
DOCUMENTS_DIR = os.path.join(KNOWLEDGE_DIR, "documents")     # 技术知识库 Markdown 文档
EMBEDDINGS_DIR = os.path.join(KNOWLEDGE_DIR, "embeddings")   # 向量索引与元数据目录
FAISS_INDEX_PATH = os.path.join(EMBEDDINGS_DIR, "index.faiss")
METADATA_PATH = os.path.join(EMBEDDINGS_DIR, "metadata.json")

DATABASE_DIR = os.path.join(KNOWLEDGE_DIR, "database")          # SQLite 知识库目录
KNOWLEDGE_DB_PATH = os.path.join(DATABASE_DIR, "knowledge.db")  # 运行时知识库（由 Markdown 导入）

LOGS_DIR = os.path.join(BASE_DIR, "logs")
FALLBACK_LOG_PATH = os.path.join(LOGS_DIR, "fallback_queries.csv")   # 未命中规则、转交 LLM 的问题
CONVERSATION_LOG_PATH = os.path.join(LOGS_DIR, "conversations.csv")  # 完整对话流水

# ------------------ 规则引擎匹配阈值 ------------------
# 匹配分数达到 MATCH_THRESHOLD 才认为命中规则，否则转交 LLM 兜底
MATCH_THRESHOLD = 0.60
# 分数达到该阈值时直接返回规则答案（高置信度）；介于两者之间则“规则 + LLM 解释”
RULE_CONFIDENT_THRESHOLD = 0.80

# ------------------ 大模型兜底配置 ------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "deepseek-flash")
LLM_TIMEOUT = 30
# 未配置 API Key 时自动关闭 LLM，系统退化为纯规则引擎，便于本地测试
LLM_ENABLED = bool(OPENAI_API_KEY)

# ------------------ 对话历史配置 ------------------
MAX_HISTORY_TURNS = 6   # 传给大模型的最近对话轮数上限，避免上下文无限增长、增加成本

# ------------------ 向量检索（RAG）配置 ------------------
# 多语言 embedding 模型，中英文 IT 文本均可处理
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "paraphrase-multilingual-MiniLM-L12-v2")
RAG_TOP_K = 3   # 检索返回的知识片段数量

# 本地 embedding 模型目录（完全离线加载，不访问 Hugging Face）
MODELS_DIR = os.path.join(KNOWLEDGE_DIR, "models")
EMBEDDING_MODEL_PATH = os.getenv(
    "EMBEDDING_MODEL_PATH",
    os.path.join(MODELS_DIR, EMBEDDING_MODEL_NAME),
)

# ------------------ Hybrid 融合检索（RRF）配置 ------------------
FUSION_TOP_N = 10   # 融合前各检索器取的前 N 条
RRF_K = 60          # Reciprocal Rank Fusion 平滑常数
EXACT_BOOST = 0.5   # 技术错误精确命中时的额外排名加成
TECH_BOOST = 0.2    # 查询命中的技术栈与条目技术栈匹配时的加成（Metadata Boost）
PLATFORM_BOOST = 0.15   # 平台匹配加成（Metadata Boost）
