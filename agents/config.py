import os
from typing import List
from dotenv import load_dotenv
from utils.api_key_manager import APIKeyManager

load_dotenv()


class AgentConfig:
    def __init__(self):
        api_keys_str = os.getenv("OPENROUTER_API_KEYS", "")
        self.api_keys = [key.strip() for key in api_keys_str.split(",") if key.strip()]
        
        self.api_key_manager = APIKeyManager(self.api_keys) if self.api_keys else None
        
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")
        self.base_url = "https://openrouter.ai/api/v1"
        self.site_url = os.getenv("SITE_URL", "")
        self.site_name = os.getenv("SITE_NAME", "")
        self.db_file = "agno.db"
        
        self.server_host = os.getenv("SERVER_HOST", "0.0.0.0")
        self.server_port = int(os.getenv("SERVER_PORT", "9001"))
        
        self.searxng_host = os.getenv("SEARXNG_HOST", "http://localhost:53153")
        self.exa_api_key = os.getenv("EXA_API_KEY")
        
        self.enable_knowledge = os.getenv("ENABLE_KNOWLEDGE", "false").lower() == "true"
        self.knowledge_db_path = os.getenv("KNOWLEDGE_DB_PATH", "./data/chroma")
        self.knowledge_collection_name = os.getenv("KNOWLEDGE_COLLECTION_NAME", "agno_knowledge")
        self.knowledge_chunk_size = int(os.getenv("KNOWLEDGE_CHUNK_SIZE", "800"))
        self.knowledge_chunk_overlap = int(os.getenv("KNOWLEDGE_CHUNK_OVERLAP", "80"))
        self.knowledge_max_results = int(os.getenv("KNOWLEDGE_MAX_RESULTS", "5"))
        
        self.zhipu_api_key = os.getenv("ZHIPU_API_KEY", "")
        self.zhipu_embedding_model = os.getenv("ZHIPU_EMBEDDING_MODEL", "embedding-3")
        
        self.enable_memory = os.getenv("ENABLE_MEMORY", "true").lower() == "true"
        
        self.enable_reasoning = os.getenv("ENABLE_REASONING", "false").lower() == "true"
        self.reasoning_model = os.getenv("REASONING_MODEL", "")
        self.reasoning_min_steps = int(os.getenv("REASONING_MIN_STEPS", "1"))
        self.reasoning_max_steps = int(os.getenv("REASONING_MAX_STEPS", "10"))

    def validate(self):
        if not self.api_keys:
            raise ValueError("请在.env文件中设置OPENROUTER_API_KEYS")
        return True
    
    def get_api_key(self) -> str:
        if self.api_key_manager:
            return self.api_key_manager.get_next_key()
        raise ValueError("API Key管理器未初始化")

    def get_headers(self) -> dict:
        return {
            "HTTP-Referer": self.site_url,
            "X-Title": self.site_name
        }
