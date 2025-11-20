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
    print("📚 知识库状态")
    print("=" * 60)
    print()
    
    km = get_knowledge_manager()
    
    if not km.is_available():
        print("❌ Knowledge未初始化")
        print("\n请检查配置:")
        print("  1. ENABLE_KNOWLEDGE=true")
        print("  2. KNOWLEDGE_EMBEDDING_API_KEY已设置")
        return
    
    print("✅ Knowledge已初始化")
    
    import os
    knowledge_dir = os.getenv("KNOWLEDGE_DIR", "tmp/lancedb")
    knowledge_table = os.getenv("KNOWLEDGE_TABLE", "knowledge_documents")
    
    print(f"\n📁 存储位置: {knowledge_dir}")
    print(f"📋 表名: {knowledge_table}")
    
    db_path = f"{knowledge_dir}/{knowledge_table}.lance"
    if os.path.exists(db_path):
        import subprocess
        try:
            result = subprocess.run(
                ['du', '-sh', db_path],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                size = result.stdout.split()[0]
                print(f"💾 数据库大小: {size}")
        except:
            pass
        
        print("\n✅ 知识库已创建")
        print("\n💡 提示:")
        print("  - 添加内容: python scripts/add_knowledge.py file <文件>")
        print("  - 初始化: python scripts/init_knowledge.py")
        print("  - 测试查询: curl -X POST http://localhost:9001/agents/general-assistant/runs \\")
        print("               -d 'message=你的问题' -d 'user_id=user123'")
    else:
        print("\n⚠️  知识库为空（未添加任何内容）")
        print("\n使用以下命令添加内容:")
        print("  python scripts/add_knowledge.py file README.md")
        print("  python scripts/init_knowledge.py")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
