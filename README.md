# Agno CookCook - 多功能AI Agent系统

基于Agno框架构建的多功能AI Agent系统,支持独立Agent、Team协作和Workflow编排。

## ✨ 功能特性

### 🤖 Agents (7个)
- **通用助手**: 处理日常对话和基本任务
- **DuckDuckGo搜索**: 国际信息搜索
- **百度搜索**: 中文信息搜索
- **Searxng搜索**: 隐私友好的元搜索
- **Exa搜索**: AI驱动的语义搜索
- **数据分析师**: 数据处理和分析
- **代码助手**: 代码编写、审查和调试

### 👥 Teams (4个)
- **研究团队**: 多语言信息搜索 + 数据分析 + 报告生成
- **开发团队**: 代码开发 + 性能分析 + 技术文档
- **内容团队**: 多源素材收集 + 内容创作
- **全功能团队**: 包含所有Agent的综合服务

### 🔄 Workflows (4个)
- **研究工作流**: 中文搜索 → 数据分析 → 报告生成
- **开发工作流**: 需求分析 → 代码实现 → 性能测试
- **内容工作流**: 多源收集 → 中文补充 → 内容创作
- **数据流水线**: 数据收集 → 聚合 → 分析 → 代码 → 报告

### 🚀 核心功能
- ✅ **多API Key轮询**: 自动轮换API Key,防止限流
- ✅ **完整日志系统**: 按日期记录所有操作和错误
- ✅ **日期时间上下文**: 所有Agent知道当前时间,搜索更准确
- ✅ **可配置端口**: 通过环境变量自定义服务地址

## 快速开始

### 环境要求
- Python 3.11+
- OpenRouter API Key (或其他兼容OpenAI的API)

### 安装依赖

```bash
uv sync
```

### 配置环境变量

复制 `.env.example` 到 `.env` 并配置:

```bash
cp .env.example .env
```

编辑 `.env`:

```env
# 支持多个API Key,用逗号分隔
OPENROUTER_API_KEYS=your_key_1,your_key_2,your_key_3
OPENROUTER_MODEL=alibaba/tongyi-deepresearch-30b-a3b:free
SERVER_PORT=9001
```

### 启动服务

```bash
./run.sh
```

或直接运行:

```bash
python main.py
```

服务将在配置的端口启动(默认 `http://0.0.0.0:9001`)。

## API使用

### 1. 使用独立Agent

```bash
curl -X POST http://localhost:9001/agents/{agent_id}/runs \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "message=你的问题" \
  -d "stream=True" \
  -d "user_id=user@example.com" \
  -d "session_id=session_123"
```

可用的 agent_id:
- `general-assistant` - 通用助手
- `web-search-expert` - 搜索专家
- `data-analyst` - 数据分析师
- `code-assistant` - 代码助手

### 2. 使用Team协作

```bash
curl -X POST http://localhost:9001/teams/cookcook-ai-team/runs \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "message=你的问题" \
  -d "stream=True" \
  -d "user_id=user@example.com" \
  -d "session_id=session_123"
```

### 3. 使用Workflow

```bash
curl -X POST http://localhost:9001/workflows/cookcook-ai-workflow/runs \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "message=你的问题" \
  -d "stream=True" \
  -d "user_id=user@example.com" \
  -d "session_id=session_123"
```

## 📋 开发计划

### ✅ 已完成
- [x] 7个专业Agents(通用、搜索、分析、代码)
- [x] 4个Teams(研究、开发、内容、全功能)
- [x] 4个Workflows(研究、开发、内容、数据流水线)
- [x] 多API Key轮询机制
- [x] 完整日志记录系统
- [x] 日期时间上下文支持
- [x] 可配置服务端口

### 🚧 进行中
- [ ] **Memory (记忆功能)** - 让Agent记住用户偏好和历史交互
  - [ ] Automatic Memory: 自动记忆管理
  - [ ] Agentic Memory: Agent主动决定记忆内容
  - [ ] 记忆检索和更新机制

- [ ] **Knowledge (知识库)** - 让Agent基于文档回答问题
  - [ ] 向量数据库集成(LanceDB)
  - [ ] 文档加载和索引
  - [ ] 知识检索和引用
  - [ ] 支持PDF、文本、URL等多种内容

### 📅 计划中
- [ ] **Multimodal (多模态)** - 图片、音频、视频处理
- [ ] **Advanced Workflow Patterns** - 条件分支、并行执行、循环
- [ ] **Reasoning Tools** - 推理增强
- [ ] **Human-in-the-Loop** - 人机协作
- [ ] **Evals** - Agent性能评估

## 项目结构

```
agno-cookcook/
├── agents/                 # Agent模块
│   ├── agents.py          # 所有Agent定义
│   ├── config.py          # 配置管理
│   └── factory.py         # Agent工厂
├── teams/                  # Team配置
│   └── teams.py           # 所有Team定义
├── workflows/              # Workflow配置
│   └── workflows.py       # 所有Workflow定义
├── utils/                  # 工具模块
│   ├── logger.py          # 日志系统
│   ├── api_key_manager.py # API Key轮询
│   └── datetime_helper.py # 日期时间工具
├── logs/                   # 日志文件(自动生成)
├── main.py                 # 主程序入口
├── .env                    # 环境变量配置
└── README.md               # 项目文档
```

## 技术栈

- **Agno**: 多Agent框架
- **OpenRouter**: LLM API服务
- **DuckDuckGo / 百度 / Searxng / Exa**: 多源搜索
- **SQLite**: 数据存储
- **LanceDB**: 向量数据库(计划中)
- **FastAPI**: Web服务
- **Uvicorn**: ASGI服务器

## 许可证

MIT License
