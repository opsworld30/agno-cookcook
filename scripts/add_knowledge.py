import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.knowledge_manager import get_knowledge_manager
from utils.logger import get_logger

logger = get_logger()


def split_markdown_by_sections(file_path: str, max_chars: int = 300):
    """按照Markdown标题分段切割文件"""
    import re
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = re.split(r'(^#{1,6}\s+.+$)', content, flags=re.MULTILINE)
    
    chunks = []
    current_chunk = ""
    
    for i, section in enumerate(sections):
        if not section.strip():
            continue
        
        if len(current_chunk) + len(section) > max_chars and current_chunk:
            chunks.append(current_chunk)
            current_chunk = section
        else:
            current_chunk += section
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def add_file(km, file_path: str):
    print(f"📄 添加文件: {file_path}")
    
    file_size = Path(file_path).stat().st_size
    
    if file_size > 50000:
        print(f"  ⚠️  文件较大 ({file_size} bytes)，将自动分段处理...")
        
        if file_path.endswith('.md'):
            chunks = split_markdown_by_sections(file_path, max_chars=300)
            print(f"  📊 已分割为 {len(chunks)} 个段落")
            
            success_count = 0
            for i, chunk in enumerate(chunks, 1):
                print(f"  [{i}/{len(chunks)}] 处理中...", end='\r')
                if km.add_content(content=chunk):
                    success_count += 1
            
            print(f"\n  ✅ 成功添加 {success_count}/{len(chunks)} 个段落")
        else:
            print(f"  ⚠️  非Markdown文件，尝试直接添加...")
            if km.add_content(path=file_path):
                print(f"  ✅ 成功")
            else:
                print(f"  ❌ 失败")
    else:
        if km.add_content(path=file_path):
            print(f"  ✅ 成功")
        else:
            print(f"  ❌ 失败")


def add_directory(km, dir_path: str, recursive: bool = True):
    print(f"📁 添加目录: {dir_path}")
    
    path = Path(dir_path)
    if not path.exists():
        print(f"  ❌ 目录不存在")
        return
    
    supported_extensions = {'.md', '.txt', '.pdf', '.doc', '.docx', '.html', '.json', '.py'}
    
    if recursive:
        files = list(path.rglob('*'))
    else:
        files = list(path.glob('*'))
    
    added_count = 0
    skipped_count = 0
    
    for file in files:
        if file.is_file() and file.suffix.lower() in supported_extensions:
            if km.add_content(path=str(file)):
                added_count += 1
                print(f"  ✅ {file.name}")
            else:
                skipped_count += 1
                print(f"  ⏭️  {file.name} (已存在或失败)")
    
    print(f"\n📊 统计: 成功 {added_count} 个, 跳过 {skipped_count} 个")


def add_text(km, text: str):
    print(f"📝 添加文本内容 ({len(text)} 字符)")
    if km.add_content(content=text):
        print(f"  ✅ 成功")
    else:
        print(f"  ❌ 失败")


def add_url(km, url: str):
    print(f"🌐 添加URL: {url}")
    if km.add_content(url=url):
        print(f"  ✅ 成功")
    else:
        print(f"  ❌ 失败")


def main():
    print("=" * 60)
    print("📚 Agno CookCook - 知识库管理工具")
    print("=" * 60)
    print()
    
    km = get_knowledge_manager()
    
    if not km.is_available():
        print("❌ Knowledge未初始化，请检查配置:")
        print("  1. ENABLE_KNOWLEDGE=true")
        print("  2. KNOWLEDGE_EMBEDDING_API_KEY已设置")
        return
    
    print("✅ Knowledge已就绪\n")
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python scripts/add_knowledge.py <类型> <路径/内容>")
        print()
        print("类型:")
        print("  file <文件路径>        - 添加单个文件")
        print("  dir <目录路径>         - 添加整个目录(递归)")
        print("  url <URL>             - 添加网页内容")
        print("  text <文本内容>        - 添加文本")
        print()
        print("示例:")
        print("  python scripts/add_knowledge.py file README.md")
        print("  python scripts/add_knowledge.py dir docs/")
        print("  python scripts/add_knowledge.py url https://docs.agno.com")
        print("  python scripts/add_knowledge.py text '这是一段知识库内容'")
        print()
        
        print("快速初始化:")
        print("  添加项目文档到知识库")
        response = input("是否添加 README.md 到知识库? (y/n): ")
        if response.lower() == 'y':
            add_file(km, "README.md")
        return
    
    cmd_type = sys.argv[1].lower()
    
    if cmd_type == "file":
        if len(sys.argv) < 3:
            print("❌ 请指定文件路径")
            return
        add_file(km, sys.argv[2])
    
    elif cmd_type == "dir":
        if len(sys.argv) < 3:
            print("❌ 请指定目录路径")
            return
        add_directory(km, sys.argv[2])
    
    elif cmd_type == "url":
        if len(sys.argv) < 3:
            print("❌ 请指定URL")
            return
        add_url(km, sys.argv[2])
    
    elif cmd_type == "text":
        if len(sys.argv) < 3:
            print("❌ 请指定文本内容")
            return
        add_text(km, sys.argv[2])
    
    else:
        print(f"❌ 未知类型: {cmd_type}")
        print("支持的类型: file, dir, url, text")
    
    print("\n✅ 完成!")


if __name__ == "__main__":
    main()
