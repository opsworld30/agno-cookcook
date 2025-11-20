import os
from typing import Optional
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.chunking.fixed import FixedSizeChunking
from utils.logger import get_logger

logger = get_logger()


class KnowledgeManager:
    _instance: Optional['KnowledgeManager'] = None
    _knowledge: Optional[Knowledge] = None
    _chunking_strategy = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._knowledge is None:
            self._initialize_knowledge()
    
    def _initialize_knowledge(self):
        try:
            knowledge_dir = os.getenv("KNOWLEDGE_DIR", "tmp/lancedb")
            table_name = os.getenv("KNOWLEDGE_TABLE", "knowledge_documents")
            
            embedding_model_id = os.getenv("KNOWLEDGE_EMBEDDING_MODEL", "openai/text-embedding-3-small")
            embedding_api_key = os.getenv("KNOWLEDGE_EMBEDDING_API_KEY", "")
            embedding_base_url = os.getenv("KNOWLEDGE_EMBEDDING_BASE_URL", "")
            
            chunk_size = int(os.getenv("KNOWLEDGE_CHUNK_SIZE", "800"))
            chunk_overlap = int(os.getenv("KNOWLEDGE_CHUNK_OVERLAP", "80"))
            
            logger.info(f"初始化Knowledge: dir={knowledge_dir}, table={table_name}")
            logger.info(f"Embedding模型: {embedding_model_id}")
            logger.info(f"分块策略: FixedSize(size={chunk_size}, overlap={chunk_overlap})")
            
            from agno.knowledge.embedder.openai import OpenAIEmbedder
            
            embedder = None
            if embedding_api_key:
                embedder_params = {
                    "id": embedding_model_id,
                    "api_key": embedding_api_key
                }
                if embedding_base_url:
                    embedder_params["base_url"] = embedding_base_url
                
                embedder = OpenAIEmbedder(**embedder_params)
                logger.info(f"使用自定义Embedding模型: {embedding_model_id}")
            
            self._chunking_strategy = FixedSizeChunking(
                chunk_size=chunk_size,
                overlap=chunk_overlap
            )
            
            vector_db_params = {
                "table_name": table_name,
                "uri": knowledge_dir
            }
            
            if embedder:
                vector_db_params["embedder"] = embedder
            
            self._knowledge = Knowledge(
                vector_db=LanceDb(**vector_db_params)
            )
            
            logger.info("Knowledge初始化成功")
            
        except Exception as e:
            logger.error(f"Knowledge初始化失败: {str(e)}", exc_info=True)
            self._knowledge = None
    
    def get_knowledge(self) -> Optional[Knowledge]:
        return self._knowledge
    
    def is_available(self) -> bool:
        return self._knowledge is not None
    
    def add_content(self, content: str = None, path: str = None, url: str = None, 
                   skip_if_exists: bool = True, upsert: bool = False):
        if not self.is_available():
            logger.warning("Knowledge未初始化,无法添加内容")
            return False
        
        try:
            add_params = {
                "skip_if_exists": skip_if_exists,
                "upsert": upsert
            }
            
            if self._chunking_strategy:
                add_params["chunking_strategy"] = self._chunking_strategy
            
            if content:
                self._knowledge.add_content(content=content, **add_params)
                logger.info("成功添加文本内容到Knowledge")
            elif path:
                self._knowledge.add_content(path=path, **add_params)
                logger.info(f"成功添加文件到Knowledge: {path}")
            elif url:
                self._knowledge.add_content(url=url, **add_params)
                logger.info(f"成功添加URL到Knowledge: {url}")
            return True
        except Exception as e:
            logger.error(f"添加内容到Knowledge失败: {str(e)}", exc_info=True)
            return False


def get_knowledge_manager() -> KnowledgeManager:
    return KnowledgeManager()
