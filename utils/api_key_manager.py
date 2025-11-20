import threading
from typing import List
from utils.logger import get_logger


class APIKeyManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, api_keys: List[str] = None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, api_keys: List[str] = None):
        if self._initialized:
            return
            
        self.logger = get_logger()
        self.api_keys = [key.strip() for key in api_keys if key.strip()] if api_keys else []
        self.current_index = 0
        self.lock = threading.Lock()
        self._initialized = True
        
        if self.api_keys:
            self.logger.info(f"API Key管理器初始化成功,共 {len(self.api_keys)} 个Key")
        else:
            self.logger.warning("API Key管理器初始化,但没有可用的Key")
    
    def get_next_key(self) -> str:
        if not self.api_keys:
            self.logger.error("没有可用的API Key")
            raise ValueError("没有配置API Key")
        
        with self.lock:
            key = self.api_keys[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.api_keys)
            
            masked_key = f"{key[:10]}...{key[-4:]}" if len(key) > 14 else "***"
            self.logger.debug(f"使用API Key: {masked_key} (索引: {self.current_index - 1})")
            
            return key
    
    def get_all_keys(self) -> List[str]:
        return self.api_keys.copy()
    
    def get_key_count(self) -> int:
        return len(self.api_keys)
    
    def reset_index(self):
        with self.lock:
            self.current_index = 0
            self.logger.info("API Key索引已重置")
