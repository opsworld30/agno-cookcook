import os
from typing import Optional
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from utils.logger import get_logger

logger = get_logger()


class KnowledgeManager:
    _instance: Optional['KnowledgeManager'] = None
    _knowledge: Optional[Knowledge] = None
    
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
            
            logger.info(f"初始化Knowledge: dir={knowledge_dir}, table={table_name}")
            
            self._knowledge = Knowledge(
                vector_db=LanceDb(
                    table_name=table_name,
                    uri=knowledge_dir
                )
            )
            
            logger.info("Knowledge初始化成功")
            
        except Exception as e:
            logger.error(f"Knowledge初始化失败: {str(e)}", exc_info=True)
            self._knowledge = None
    
    def get_knowledge(self) -> Optional[Knowledge]:
        return self._knowledge
    
    def is_available(self) -> bool:
        return self._knowledge is not None
    
    def add_content(self, content: str = None, path: str = None, url: str = None):
        if not self.is_available():
            logger.warning("Knowledge未初始化,无法添加内容")
            return False
        
        try:
            if content:
                self._knowledge.add_content(content=content)
                logger.info("成功添加文本内容到Knowledge")
            elif path:
                self._knowledge.add_content(path=path)
                logger.info(f"成功添加文件到Knowledge: {path}")
            elif url:
                self._knowledge.add_content(url=url)
                logger.info(f"成功添加URL到Knowledge: {url}")
            return True
        except Exception as e:
            logger.error(f"添加内容到Knowledge失败: {str(e)}", exc_info=True)
            return False


def get_knowledge_manager() -> KnowledgeManager:
    return KnowledgeManager()
