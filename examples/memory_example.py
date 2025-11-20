from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAILike
import os
from dotenv import load_dotenv

load_dotenv()

api_keys = os.getenv("OPENROUTER_API_KEYS", "").split(",")
api_key = api_keys[0].strip() if api_keys else ""

model = OpenAILike(
    id=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o"),
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

agent = Agent(
    name="记忆助手",
    model=model,
    db=SqliteDb(db_file="agno.db"),
    enable_user_memories=True,
    add_history_to_context=True,
    instructions=[
        "你是一个具有记忆功能的AI助手",
        "你会记住用户告诉你的重要信息",
        "在后续对话中使用这些记忆提供个性化服务"
    ]
)

print("=== Memory示例 ===\n")
print("第一次对话 - 告诉Agent一些信息:")
agent.print_response(
    "我叫张三,我喜欢Python编程,最喜欢的颜色是蓝色",
    markdown=True
)

print("\n第二次对话 - 测试记忆:")
agent.print_response(
    "你还记得我的名字和喜好吗?",
    markdown=True
)

print("\n第三次对话 - 基于记忆的个性化回复:")
agent.print_response(
    "推荐一个适合我的项目",
    markdown=True
)
