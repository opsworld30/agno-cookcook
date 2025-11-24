from agno.tools import Toolkit
from agno.utils.log import logger
from typing import Optional
from .knowledge_base import KnowledgeBase
import os


class KnowledgeTool(Toolkit):
    
    def __init__(
        self,
        persist_directory: str = None,
        collection_name: str = None,
        max_results: int = 5
    ):
        super().__init__(name="knowledge_search")
        
        self.persist_directory = persist_directory or os.getenv("KNOWLEDGE_DB_PATH", "./data/chroma")
        self.collection_name = collection_name or os.getenv("KNOWLEDGE_COLLECTION_NAME", "agno_knowledge")
        self.max_results = max_results
        
        try:
            self.kb = KnowledgeBase(
                persist_directory=self.persist_directory,
                collection_name=self.collection_name
            )
            self.available = True
        except Exception as e:
            logger.error(f"知识库初始化失败: {str(e)}")
            self.available = False
        
        self.register(self.search_knowledge)
    
    def search_knowledge(self, query: str, top_k: int = None) -> str:
        if not self.available:
            return "知识库不可用，请检查配置"
        
        if not query or not query.strip():
            return "请提供搜索关键词"
        
        try:
            n_results = top_k if top_k and top_k > 0 else self.max_results
            results = self.kb.search(query, n_results=n_results)
            
            if not results:
                return f"未找到与 '{query}' 相关的知识"
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                content = result["content"]
                metadata = result.get("metadata", {})
                distance = result.get("distance")
                
                result_text = f"[结果 {i}]\n{content}"
                
                if metadata:
                    meta_info = []
                    for key, value in metadata.items():
                        if key not in ["chunk_index", "total_chunks"]:
                            meta_info.append(f"{key}: {value}")
                    if meta_info:
                        result_text += f"\n来源: {', '.join(meta_info)}"
                
                if distance is not None:
                    result_text += f"\n相似度: {1 - distance:.3f}"
                
                formatted_results.append(result_text)
            
            return "\n\n".join(formatted_results)
            
        except Exception as e:
            logger.error(f"知识库搜索失败: {str(e)}")
            return f"搜索失败: {str(e)}"
