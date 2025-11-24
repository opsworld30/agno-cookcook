import os
from typing import List
import requests
from dotenv import load_dotenv

load_dotenv()


class ZhipuEmbeddings:
    
    def __init__(self, api_key: str = None, model: str = "embedding-3"):
        self.api_key = api_key or os.getenv("ZHIPU_API_KEY")
        if not self.api_key:
            raise ValueError("需要设置 ZHIPU_API_KEY")
        
        self.model = model
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/embeddings"
        self.dimension = 2048
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            embedding = self._get_embedding(text)
            embeddings.append(embedding)
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        return self._get_embedding(text)
    
    def _get_embedding(self, text: str) -> List[float]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "input": text
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            if "data" in result and len(result["data"]) > 0:
                return result["data"][0]["embedding"]
            else:
                raise ValueError(f"智谱API返回格式错误: {result}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"调用智谱Embedding API失败: {str(e)}")
