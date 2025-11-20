# Agno CookCook - 多功能AI Agent系统

基于Agno框架构建的多功能AI Agent系统,同时支持独立Agent、Team协作和Workflow编排三种模式。

## 功能特性

### 1. 独立Agents
系统包含4个专业Agent,可独立使用:

- **通用助手** (`general`): 处理日常对话和基本任务
- **搜索专家** (`search`): 实时网络搜索和信息收集
- **数据分析师** (`analyst`): 数据处理和分析
- **代码助手** (`coder`): 代码编写、审查和调试

### 2. Team协作
**CookCook AI Team** - 多个Agent组成团队协同工作:
- **成员**: 搜索专家、数据分析师、代码助手
- **协调者**: 使用独立的模型协调团队成员
- **工作方式**: 根据任务需求自动选择合适的成员完成任务

### 3. Workflow编排
**CookCook AI Workflow** - 智能任务处理工作流:
- **步骤1**: 搜索专家 - 收集相关信息
- **步骤2**: 数据分析师 - 分析处理数据
- **步骤3**: 通用助手 - 生成最终总结
- **特点**: 线性执行,数据在步骤间自动传递

## 快速开始

### 环境要求
- Python 3.11+
- OpenAI API Key

### 安装依赖

```bash
uv sync
```

### 配置环境变量

创建 `.env` 文件并配置:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL_NAME=gpt-4o-mini
```

### 启动服务

```bash
python main.py
```

或使用脚本:

```bash
./run.sh
```

服务将在 `http://0.0.0.0:9001` 启动。

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

## 项目结构

```
agno-cookcook/
├── agents/                    # Agent模块
│   ├── general/              # 通用助手
│   ├── web_search/           # 搜索专家
│   ├── data_analysis/        # 数据分析师
│   ├── code_assistant/       # 代码助手
│   ├── config/               # 配置管理
│   └── factory.py            # Agent工厂
├── examples/                  # 示例代码
│   ├── examples.py           # Agent基础示例
│   ├── examples_team.py      # Team协作示例
│   └── examples_workflow.py  # Workflow编排示例
├── main.py                    # 主程序入口
├── .env                       # 环境变量配置
└── README.md                  # 项目文档
```

## 架构设计

### Agent工厂模式
使用工厂模式统一管理Agent的创建,支持:
- 创建单个Agent
- 创建指定类型的多个Agent
- 创建所有Agent

### 配置管理
集中管理所有配置,包括:
- API密钥
- 模型选择
- 数据库连接
- 工具配置

### 三种模式共存
在同一个AgentOS实例中同时注册:
- **agents**: 4个独立Agent可直接调用
- **teams**: 1个Team(包含3个成员Agent)
- **workflows**: 1个Workflow(包含3个步骤)

用户可以根据任务特点选择最合适的方式:
- 简单任务 → 使用独立Agent
- 需要协作 → 使用Team
- 复杂流程 → 使用Workflow

## 示例

### 运行Agent示例

```bash
python examples/examples.py
```

### 运行Team示例

```bash
python examples/examples_team.py
```

### 运行Workflow示例

```bash
python examples/examples_workflow.py
```

## 技术栈

- **Agno**: 多Agent框架
- **OpenAI**: LLM模型
- **DuckDuckGo**: 网络搜索
- **SQLite**: 数据存储
- **FastAPI**: Web服务
- **Uvicorn**: ASGI服务器

## 开发建议

1. **简单任务**: 使用独立Agent
2. **需要协作**: 使用Team模式
3. **复杂流程**: 使用Workflow编排
4. **混合使用**: 根据具体场景灵活选择

## 许可证

MIT License
