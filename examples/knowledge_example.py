from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.models.openai import OpenAILike
import os
from dotenv import load_dotenv

load_dotenv()

api_keys = os.getenv("OPENROUTER_API_KEYS", "").split(",")
api_key = api_keys[0].strip() if api_keys else ""

knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="knowledge_documents",
        uri="tmp/lancedb"
    )
)

knowledge.add_content(
    content="""
    # Agno CookCook 项目介绍
    
    Agno CookCook是一个基于Agno框架的多功能AI Agent系统。
    
    ## 主要功能
    1. 7个专业Agents: 通用助手、搜索专家、数据分析师、代码助手等
    2. 4个Teams: 研究团队、开发团队、内容团队、全功能团队
    3. 4个Workflows: 研究工作流、开发工作流、内容工作流、数据流水线
    
    ## 核心特性
    - 多API Key轮询机制,防止限流
    - 完整的日志记录系统
    - 日期时间上下文支持
    - 可配置的服务端口
    
    ## 技术栈
    - Agno框架
    - OpenRouter API
    - 多种搜索引擎(DuckDuckGo、百度、Searxng、Exa)
    - SQLite数据库
    - FastAPI Web服务
    """
)

model = OpenAILike(
    id=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o"),
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

agent = Agent(
    name="知识库助手",
    model=model,
    knowledge=knowledge,
    search_knowledge=True,
    instructions=[
        "你是一个具有知识库的AI助手",
        "在回答问题前,先搜索知识库",
        "基于知识库内容提供准确的答案",
        "引用知识库来源"
    ]
)

print("=== Knowledge示例 ===\n")
print("问题1: Agno CookCook有哪些功能?")
agent.print_response(
    "Agno CookCook有哪些功能?",
    markdown=True
)

print("\n问题2: 这个项目使用了什么技术栈?")
agent.print_response(
    "这个项目使用了什么技术栈?",
    markdown=True
)
