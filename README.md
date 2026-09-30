# IT 技术支持机器人

基于 **规则引擎 + 错误解析 + 知识库 + 大模型** 的 IT 故障诊断与技术支持系统。

不再是“遇到问题就丢给大模型随便回答”的普通 ChatBot，而是先由规则引擎做高频故障的快速精确匹配，
未命中/低置信度时再交给 DeepSeek 做综合诊断。规则命中零成本、响应快、答案可控，LLM 兜底处理开放式问题。

## 支持的领域

| 分类 | 示例 |
|---|---|
| Python | ModuleNotFoundError、ImportError、SyntaxError、venv 等 |
| pip | 安装失败、依赖冲突、SSL、超时、权限、镜像源 |
| Conda | 创建/激活环境、依赖冲突、channel、命令未找到 |
| Git | 认证失败、仓库不存在、合并冲突、推送被拒绝 |
| Windows | 命令未找到、PATH、权限、DLL 缺失 |
| PyTorch | CUDA 不可用、显存不足、模型加载、版本匹配 |
| 网络 | SSL、超时、连接错误、代理、DNS |
| Docker | daemon、镜像拉取、容器退出、端口/网络、数据卷、compose、WSL2 |

规则库共 **45 条**，技术知识库文档 **109 条**（`knowledge/documents/`，含 Docker 37 条），测试问题 **98 条**，规则识别准确率目标 ≥ 85%（当前 100%）。RAG 检索 benchmark（56 精确 + 14 语义改写）：Hybrid Recall@1=71.4% / Recall@3=97.1% / Recall@5=100%。

## 架构

```
用户输入
  → 错误解析 (core/error_parser.py)        提取标准错误类型/分类/模块
  → 规则匹配 (core/rule_engine.py)         多层打分：错误类型 > 特征短语 > 关键词组合 > 模糊
  → 置信度分派 (core/diagnostic_engine.py)
       ≥ 0.80  规则答案
       ≥ 0.60  规则答案 + LLM 补充解释
       <  0.60 意图分类 → 知识检索(RAG) → LLM 综合诊断
  → 结构化回复 (core/response_formatter.py)
```

## 目录结构

```
├── main.py                    # CLI 入口
├── cli.py                     # CLI 交互层（命令解析 / 展示 / REPL）
├── chatbot.py                 # 会话编排（历史 + 诊断上下文 + 日志）
├── config.py                  # 全局配置
├── core/                      # 核心引擎
│   ├── error_parser.py        # 错误信息解析
│   ├── rule_engine.py         # 多层规则匹配
│   ├── intent_classifier.py   # 技术领域粗分类
│   ├── query_analyzer.py      # 检索前 Query 理解（技术 token / 平台 / 技术栈）
│   ├── diagnostic_engine.py   # 诊断流程编排
│   └── response_formatter.py  # 结构化回复
├── llm/                       # 大模型
│   ├── client.py              # DeepSeek 客户端
│   └── prompts.py             # 提示词
├── knowledge/                  # 知识库
│   ├── __init__.py
│   ├── document_loader.py      # Markdown 文档加载（导入源）
│   ├── text_splitter.py        # 知识条目切块
│   ├── repository.py           # SQLite 知识仓库（运行时读取）
│   ├── importer.py             # Markdown -> SQLite 导入脚本
│   ├── schema.sql              # SQLite 表结构
│   ├── embedding_model.py      # embedding 模型（本地离线加载）
│   ├── vector_store.py         # FAISS 向量存储（构建/保存/检索）
│   ├── build_index.py          # 向量索引构建脚本
│   ├── rules.json             # 故障诊断规则库（45 条）
│   ├── faq.json               # 补充 FAQ
│   ├── documents/             # 技术知识库文档（109 条，导入源）
│   │   ├── python.md
│   │   ├── pip.md
│   │   ├── conda.md
│   │   ├── git.md
│   │   ├── windows.md
│   │   ├── pytorch.md
│   │   ├── cuda.md
│   │   ├── network.md
│   │   └── docker.md
│   ├── database/              # SQLite 知识库（importer.py 生成）
│   │   └── knowledge.db
│   ├── models/                # 本地 embedding 模型（离线，需手动放置）
│   │   └── paraphrase-multilingual-MiniLM-L12-v2/
│   └── embeddings/            # 向量索引（build_index.py 生成）
│       ├── index.faiss
│       └── metadata.json
├── services/
│   ├── logger.py              # 日志（fallback_queries.csv / conversations.csv）
│   ├── history.py             # 对话历史 + 诊断上下文
│   └── knowledge_service.py   # RAG 检索（向量优先 + 关键词降级）
├── logs/                      # 运行日志（自动生成）
└── tests/                     # 测试
    ├── test_rule_engine.py
    ├── test_error_parser.py
    ├── test_chatbot.py
    ├── test_documents.py
    ├── test_vector_retrieval.py
    ├── test_cli.py
    ├── test_e2e.py
    ├── test_cases.json        # 98 条标注问题集
    └── test_cases_rag.json    # 56 精确 + 14 语义改写 RAG benchmark
```

## 快速开始

```bash
# 1. 安装基础依赖（规则引擎 + LLM）
pip install -r requirements.txt

# 2. 导入知识库到 SQLite（Markdown 仅作数据源，运行时从 SQLite 读取）
python knowledge/importer.py

# 3.（可选）安装向量检索依赖，启用 RAG
pip install -r requirements-rag.txt
#    a) 将 embedding 模型放置到 knowledge/models/paraphrase-multilingual-MiniLM-L12-v2/
#       （完全离线加载，不再联网下载；本地缺失时自动降级为关键词检索）
#    b) 构建 FAISS 向量索引
python knowledge/build_index.py

# 4. 配置 .env（填入 DeepSeek API Key；不填则退化为纯规则引擎）
#    OPENAI_API_KEY=sk-xxx
#    OPENAI_BASE_URL=https://api.deepseek.com
#    LLM_MODEL_NAME=deepseek-flash

# 5. 运行
python main.py
```

> 未安装 RAG 依赖、未放置本地模型或未构建索引时，系统自动降级为关键词检索，功能不受影响。
> 除 LLM API 调用外，系统全程本地离线运行（规则 / SQLite / 向量检索 / embedding 均不联网）。

## 环境变量

复制 `.env.example` 为 `.env` 并按需填写：

| 变量 | 说明 | 默认值 |
|---|---|---|
| `OPENAI_API_KEY` | DeepSeek / 兼容服务 API Key | 无（不填则禁用 LLM） |
| `OPENAI_BASE_URL` | API 服务地址 | `https://api.deepseek.com` |
| `LLM_MODEL_NAME` | 兜底大模型名称 | `deepseek-flash` |
| `EMBEDDING_MODEL_NAME` | RAG 多语言 embedding 模型 | `paraphrase-multilingual-MiniLM-L12-v2` |
| `EMBEDDING_MODEL_PATH` | 本地 embedding 模型路径（离线加载） | `knowledge/models/<EMBEDDING_MODEL_NAME>` |

## CLI 命令

| 命令 | 说明 |
|---|---|
| `/help` | 显示帮助 |
| `/history` | 查看当前会话历史 |
| `/clear` | 清空当前会话上下文（不影响日志/知识库/索引） |
| `/status` | 显示系统状态（规则、知识库、检索模式、向量索引、LLM） |
| `/about` | 显示版本与能力 |
| `/exit` 或 `exit` | 退出 |

Ctrl+C / EOF 会优雅退出；单次回答异常不会导致程序崩溃。

## 运行测试

```bash
python tests/test_rule_engine.py      # 规则识别准确率
python tests/test_error_parser.py     # 错误解析单元测试
python tests/test_chatbot.py          # 会话集成测试（离线，不联网）
python tests/test_documents.py        # 知识库文档与检索测试
python tests/test_vector_retrieval.py # RAG 向量/Hybrid 检索 + Recall 基准
python tests/test_cli.py              # CLI 命令解析与分派测试
python tests/test_e2e.py              # 端到端场景测试
```

## 匹配打分

| 层级 | 依据 | 分数 |
|---|---|---|
| 第一层 | 错误类型精确匹配（error_parser） | 1.00 |
| 第二层 | 错误代码/特征短语子串命中 | 0.95 |
| 第三层 | 关键词组合命中 | 0.90 / 0.80 / 0.70 |
| 第四层 | difflib 模糊匹配（降权） | ≤ 0.58 |

分数相同的规则按“关键词命中数 → 优先级”打破平局，保证更具体的规则（如 pip SSL）优先于宽泛规则（如通用 SSL）。

## 如何新增规则

在 `knowledge/rules.json` 的 `rules` 数组中新增一条：

```json
{
  "id": "my_new_rule",
  "category": "python",
  "error_type": "SomeError",
  "priority": 0,
  "patterns": ["SomeError", "特征短语"],
  "keywords": ["关键词1", "关键词2"],
  "response": {
    "title": "问题标题",
    "causes": ["可能原因1", "可能原因2"],
    "checks": ["检查步骤1", "检查步骤2"],
    "solution": "解决命令或方法",
    "further": "仍无法解决时需用户提供的信息"
  }
}
```

同时在 `tests/test_cases.json` 中补充对应问题即可纳入准确率统计。

## 知识库文档

`knowledge/documents/` 下的 Markdown 按“故障知识条目”组织，格式如下（一个文件可含多条）：

```markdown
## 条目标题

### 关键词
空格分隔的检索关键词

### 症状
- ...

### 常见原因
- ...

### 检查命令
- ...

### 解决思路
- ...
```

可选小节（V1.2 新增，用于检索增强，缺失时为空）：

```markdown
### 别名      空格/逗号分隔的常见口语化说法（提升中文改写召回）
### 平台      windows / linux / macos（可多个，用于 Metadata Boost）
### 技术栈    docker、compose 等相关技术（用于 Metadata Boost）
### 故障类型  安装失败 / 权限问题 / 网络问题 等
### 错误类型  标准化错误标识（如 docker_daemon_not_running）
### 子类      更细粒度分类
```

规则未命中时，系统会从这些文档中检索 top-3 相关条目，拼入 LLM 提示词综合诊断，并在回复中附带【参考来源】。

## 检索（RAG / Hybrid Retrieval）

`KnowledgeService` 对外接口统一为 `retrieve(query, top_k, mode)`，内部按 `mode` 分派：

```
retrieve(query, top_k, mode)
   → mode = "auto"（默认）
        ├─ 向量可用 → Hybrid（Query 分析 → 关键词 + 向量 → RRF → 精确命中 + Metadata Boost）
        └─ 不可用   → Lexical（关键词 + 别名 + 字符 n-gram）
   → mode = "lexical" / "vector" / "fts" / "hybrid" 可显式指定
```

- **模型**：`paraphrase-multilingual-MiniLM-L12-v2`（中英文多语言，384 维）
- **模型加载**：从 `knowledge/models/` 本地目录离线加载（`local_files_only`），禁止访问 Hugging Face
- **知识存储**：SQLite（`knowledge/database/knowledge.db`），Markdown 仅作导入源
- **Query Analyzer**：检索前提取技术栈 / 平台 / 错误 token / 版本号，驱动 Metadata Boost
- **别名（Aliases）**：口语化说法进入词法打分，提升中文改写（paraphrase）召回
- **FTS5**：SQLite `trigram` 全文索引（BM25），通过 `mode="fts"` 可用；因 trigram 对中文分词有限，默认 Hybrid 不混入以避免通用词稀释精确命中
- **向量相似度**：L2 归一化 + `IndexFlatIP`（等价余弦相似度）
- **融合**：Reciprocal Rank Fusion（k=60），Lexical Top-10 + Vector Top-10
- **Exact Match Boost**：技术错误精确命中按命中强度加权
- **Metadata Boost**：技术栈 / 平台匹配给予额外加成
- **惰性加载**：仅首次触发检索时才加载 torch + 模型，规则命中的常规对话零开销
- **索引持久化**：`knowledge/embeddings/`（`index.faiss` + `metadata.json`）

修改 `knowledge/documents/` 后需重新导入并重建索引：

```bash
python knowledge/importer.py && python knowledge/build_index.py
```

### Benchmark 对比（56 精确 + 14 语义改写）

| 检索器 | Recall@1 | Recall@3 | Recall@5 |
|---|---|---|---|
| Lexical（关键词） | 55.7% | 97.1% | 97.1% |
| Vector（向量） | 61.4% | 82.9% | 87.1% |
| **Hybrid（融合）** | **71.4%** | **97.1%** | **100%** |

语义改写问题上 Hybrid 的 Recall@1 从 Lexical 的 14.3% 提升到 28.6%，同时 Recall@3 不低于 Lexical。

## 已知限制

- 仅提供 CLI 交互，无 Web / GUI 界面（后续可加 FastAPI）。
- 知识库文档变更后需手动重建向量索引（`python knowledge/build_index.py`）。
- 向量检索依赖 `sentence-transformers`（含 torch）等重型依赖，未安装时自动降级为关键词检索。
- embedding 为单个多语言模型，未做 rerank；对“驱动正常但仍不用 GPU”这类强语义推理仍有边界。
- LLM 兜底依赖外部 API，无 Key 时退化为“规则 + 知识片段直出”。

## 日志

- `logs/fallback_queries.csv`：记录转交 LLM 或需 LLM 增强的问题（含分类、分数、是否解决、反馈），供后续 review 补充规则。
- `logs/conversations.csv`：完整对话流水，用于分析高频问题与解决率。
