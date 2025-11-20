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
