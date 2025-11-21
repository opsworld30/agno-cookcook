#!/usr/bin/env python3
"""
Markdown Knowledge Base Importer - 智能分块版本
 
按照文档结构对markdown文件进行智能分块，支持文件夹批量导入
"""
 
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import re
from dotenv import load_dotenv
 
load_dotenv()
 
# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))
 
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.lancedb import LanceDb, SearchType
 
 
class MarkdownChunker:
    """Markdown智能分块器"""
    
    def __init__(self, max_chunk_size: int = 400, overlap: int = 50):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    
    def chunk_by_headers(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """按照标题层级进行分块"""
        chunks = []
        
        # 提取文件基本信息
        file_name = Path(file_path).name
        
        # 分割内容，保持标题和内容的关联
        sections = re.split(r'(^#{1,6}\s+.+$)', content, flags=re.MULTILINE)
        
        current_hierarchy = []  # 保存当前标题层级
        current_content = ""
        
        for i, section in enumerate(sections):
            if not section.strip():
                continue
                
            # 检查是否是标题
            header_match = re.match(r'^(#{1,6})\s+(.+)$', section.strip())
            
            if header_match:
                # 保存之前的内容块
                if current_content.strip():
                    chunks.append(self._create_chunk(
                        current_content.strip(),
                        current_hierarchy.copy(),
                        file_name,
                        file_path
                    ))
                
                # 更新标题层级
                header_level = len(header_match.group(1))
                header_text = header_match.group(2)
                
                # 清理层级（移除同级和更深层级的标题）
                current_hierarchy = [h for h in current_hierarchy if h['level'] < header_level]
                current_hierarchy.append({
                    'level': header_level,
                    'text': header_text
                })
                
                current_content = section + "\n"
            else:
                current_content += section
                
                # 如果内容过长，进行分割
                if len(current_content) > self.max_chunk_size:
                    chunks.extend(self._split_long_content(
                        current_content,
                        current_hierarchy.copy(),
                        file_name,
                        file_path
                    ))
                    current_content = ""
        
        # 处理最后一块内容
        if current_content.strip():
            chunks.append(self._create_chunk(
                current_content.strip(),
                current_hierarchy.copy(),
                file_name,
                file_path
            ))
        
        return chunks
    
    def _create_chunk(self, content: str, hierarchy: List[Dict], file_name: str, file_path: str) -> Dict[str, Any]:
        """创建内容块"""
        # 构建层级标题路径
        title_path = " > ".join([h['text'] for h in hierarchy])
        
        # 构建完整上下文
        context_content = content
        if hierarchy:
            # 在内容前添加标题上下文
            headers = "\n".join([f"{'#' * h['level']} {h['text']}" for h in hierarchy])
            context_content = f"{headers}\n\n{content}"
        
        return {
            'content': context_content,
            'metadata': {
                'file_name': file_name,
                'file_path': file_path,
                'title_path': title_path,
                'hierarchy_level': len(hierarchy),
                'chunk_type': 'markdown_section',
                'content_length': len(content)
            }
        }
    
    def _split_long_content(self, content: str, hierarchy: List[Dict], file_name: str, file_path: str) -> List[Dict[str, Any]]:
        """分割过长的内容"""
        chunks = []
        content_lines = content.split('\n')
        
        current_chunk_lines = []
        current_length = 0
        
        for line in content_lines:
            line_length = len(line) + 1  # +1 for newline
            
            if current_length + line_length > self.max_chunk_size and current_chunk_lines:
                # 保存当前块
                chunk_content = '\n'.join(current_chunk_lines)
                chunks.append(self._create_chunk(chunk_content, hierarchy, file_name, file_path))
                
                # 开始新块，保留重叠内容
                overlap_lines = current_chunk_lines[-self.overlap:] if len(current_chunk_lines) > self.overlap else current_chunk_lines
                current_chunk_lines = overlap_lines + [line]
                current_length = sum(len(l) + 1 for l in current_chunk_lines)
            else:
                current_chunk_lines.append(line)
                current_length += line_length
        
        # 处理最后一块
        if current_chunk_lines:
            chunk_content = '\n'.join(current_chunk_lines)
            chunks.append(self._create_chunk(chunk_content, hierarchy, file_name, file_path))
        
        return chunks
 
 
class KnowledgeImporter:
    """知识库导入器"""
    
    def __init__(self):
        self.chunker = MarkdownChunker()
        
        db_path = os.getenv("KNOWLEDGE_DIR", "tmp/lancedb")
        table_name = os.getenv("KNOWLEDGE_TABLE", "knowledge_documents")
        embedding_model = os.getenv("KNOWLEDGE_EMBEDDING_MODEL", "BAAI/bge-large-zh-v1.5")
        embedding_api_key = os.getenv("KNOWLEDGE_EMBEDDING_API_KEY", "")
        embedding_base_url = os.getenv("KNOWLEDGE_EMBEDDING_BASE_URL", "")
        
        embedder_params = {
            "id": embedding_model,
            "api_key": embedding_api_key,
            "enable_batch": False
        }
        if embedding_base_url:
            embedder_params["base_url"] = embedding_base_url
        
        self.knowledge = Knowledge(
            vector_db=LanceDb(
                uri=db_path,
                table_name=table_name,
                search_type=SearchType.hybrid,
                embedder=OpenAIEmbedder(**embedder_params),  
            ),
        )
        
    def import_file(self, file_path: str) -> Dict[str, Any]:
        """导入单个markdown文件"""
        print(f"📄 处理文件: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                return {'status': 'skipped', 'reason': 'empty_file'}
            
            # 分块处理
            chunks = self.chunker.chunk_by_headers(content, file_path)
            
            success_count = 0
            for i, chunk in enumerate(chunks):
                print(f"  [{i+1}/{len(chunks)}] 添加分块...", end='\r')
                
                try:
                    self.knowledge.add_content(
                        text_content=chunk['content'],
                        metadata=chunk['metadata']
                    )
                    success_count += 1
                except Exception as e:
                    print(f"\n  ⚠️  分块 {i+1} 添加失败: {str(e)}")
            
            print(f"\n  ✅ 成功添加 {success_count}/{len(chunks)} 个分块")
            return {
                'status': 'success',
                'total_chunks': len(chunks),
                'success_chunks': success_count
            }
            
        except Exception as e:
            print(f"  ❌ 错误: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def import_directory(self, dir_path: str, recursive: bool = True) -> Dict[str, Any]:
        """批量导入目录中的markdown文件"""
        print(f"📁 处理目录: {dir_path}")
        
        path = Path(dir_path)
        if not path.exists():
            print(f"  ❌ 目录不存在")
            return {'status': 'error', 'error': 'directory_not_found'}
        
        # 查找所有markdown文件
        if recursive:
            markdown_files = list(path.rglob('*.md'))
        else:
            markdown_files = list(path.glob('*.md'))
        
        if not markdown_files:
            print(f"  ⚠️  未找到markdown文件")
            return {'status': 'warning', 'message': 'no_markdown_files'}
        
        print(f"  📊 找到 {len(markdown_files)} 个markdown文件")
        
        results = {
            'total_files': len(markdown_files),
            'success_files': 0,
            'error_files': 0,
            'total_chunks': 0,
            'success_chunks': 0,
            'file_results': {}
        }
        
        for file_path in markdown_files:
            result = self.import_file(str(file_path))
            results['file_results'][str(file_path)] = result
            
            if result['status'] == 'success':
                results['success_files'] += 1
                results['total_chunks'] += result['total_chunks']
                results['success_chunks'] += result['success_chunks']
            elif result['status'] == 'error':
                results['error_files'] += 1
        
        print(f"\n📊 导入统计:")
        print(f"  文件: {results['success_files']}/{results['total_files']} 成功")
        print(f"  分块: {results['success_chunks']}/{results['total_chunks']} 成功")
        
        return results
 
 
def main():
    print("=" * 60)
    print("📚 Markdown Knowledge Importer - 智能分块版本")
    print("=" * 60)
    print()
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ 请设置 OPENAI_API_KEY 环境变量")
        return
    
    importer = KnowledgeImporter()
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python markdown_importer.py <文件或目录路径>")
        print()
        print("示例:")
        print("  python markdown_importer.py docs/")
        print("  python markdown_importer.py README.md")
        print("  python markdown_importer.py docs/ --no-recursive")
        return
    
    target_path = sys.argv[1]
    recursive = '--no-recursive' not in sys.argv
    
    path = Path(target_path)
    
    if path.is_file():
        if target_path.endswith('.md'):
            importer.import_file(target_path)
        else:
            print("❌ 请指定markdown文件 (.md)")
    elif path.is_dir():
        importer.import_directory(target_path, recursive=recursive)
    else:
        print(f"❌ 路径不存在: {target_path}")
    
    print("\n✅ 导入完成!")
 
 
if __name__ == "__main__":
    main()