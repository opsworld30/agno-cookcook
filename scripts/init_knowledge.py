import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.knowledge_manager import get_knowledge_manager
from utils.logger import get_logger

logger = get_logger()


def main():
    print("=" * 60)
    print("📚 初始化知识库")
    print("=" * 60)
    print()
    
    km = get_knowledge_manager()
    
    if not km.is_available():
        print("❌ Knowledge未初始化，请检查配置:")
        print("  1. ENABLE_KNOWLEDGE=true")
        print("  2. KNOWLEDGE_EMBEDDING_API_KEY已设置")
        print("  3. KNOWLEDGE_EMBEDDING_BASE_URL已设置")
        return
    
    print("✅ Knowledge已就绪\n")
    
    print("📄 添加项目文档...")
    
    readme_path = "README.md"
    if Path(readme_path).exists():
        print(f"  - {readme_path}")
        km.add_content(path=readme_path)
    else:
        print(f"  ⚠️  {readme_path} 不存在")
    
    docs_dir = Path("docs")
    if docs_dir.exists():
        print(f"\n📁 添加 docs/ 目录...")
        for doc_file in docs_dir.glob("*.md"):
            print(f"  - {doc_file.name}")
            km.add_content(path=str(doc_file))
    else:
        print(f"\n⚠️  docs/ 目录不存在")
    
    print("\n📝 添加系统信息...")
    system_info = """
# Agno CookCook 系统信息

## Agents (7个)
1. general-assistant - 通用助手
2. web-search-expert - DuckDuckGo搜索专家
3. baidu-search-expert - 百度搜索专家
4. searxng-expert - Searxng搜索专家
5. exa-search-expert - Exa搜索专家
6. data-analyst - 数据分析师
7. code-assistant - 代码助手

## Teams (4个)
1. research-team - 研究团队
2. dev-team - 开发团队
3. content-team - 内容团队
4. full-service-team - 全功能团队

## Workflows (4个)
1. research-workflow - 研究工作流
2. dev-workflow - 开发工作流
3. content-workflow - 内容工作流
4. data-pipeline-workflow - 数据流水线

## 核心功能
- 多API Key轮询
- Memory记忆功能
- Knowledge知识库
- 日期时间上下文
- 完整日志系统
"""
    km.add_content(content=system_info)
    print("  ✅ 系统信息已添加")
    
    print("\n" + "=" * 60)
    print("✅ 知识库初始化完成!")
    print("=" * 60)
    print("\n现在可以向通用助手提问，它会从知识库中检索信息。")
    print("\n示例:")
    print("  curl -X POST http://localhost:9001/agents/general-assistant/runs \\")
    print("    -d 'message=Agno CookCook有哪些Agent?' \\")
    print("    -d 'user_id=user123'")


if __name__ == "__main__":
    main()
