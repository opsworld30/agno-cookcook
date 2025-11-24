import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from .embeddings import ZhipuEmbeddings
from .text_splitter import RecursiveCharacterTextSplitter
from utils.logger import get_logger


class KnowledgeBase:
    
    def __init__(
        self,
        persist_directory: str = "./data/chroma",
        collection_name: str = "agno_knowledge",
        embedding_model: str = "embedding-3",
        chunk_size: int = 800,
        chunk_overlap: int = 80
    ):
        self.logger = get_logger()
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        os.makedirs(persist_directory, exist_ok=True)
        
        self.embeddings = ZhipuEmbeddings(model=embedding_model)
        
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        self.logger.info(f"知识库初始化完成: {collection_name}")
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        if not texts:
            return []
        
        import uuid
        import time
        
        chunks = []
        chunk_metadatas = []
        chunk_ids = []
        
        for i, text in enumerate(texts):
            text_chunks = self.text_splitter.split_text(text)
            
            base_id = ids[i] if ids and i < len(ids) else f"doc_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"
            
            for j, chunk in enumerate(text_chunks):
                chunks.append(chunk)
                
                metadata = metadatas[i].copy() if metadatas and i < len(metadatas) else {}
                metadata["chunk_index"] = j
                metadata["total_chunks"] = len(text_chunks)
                chunk_metadatas.append(metadata)
                
                chunk_id = f"{base_id}_chunk_{j}"
                chunk_ids.append(chunk_id)
        
        self.logger.info(f"开始向量化 {len(chunks)} 个文本块...")
        embeddings = self.embeddings.embed_documents(chunks)
        
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=chunk_metadatas,
            ids=chunk_ids
        )
        
        self.logger.info(f"成功添加 {len(chunks)} 个文本块到知识库")
        return chunk_ids
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        query_embedding = self.embeddings.embed_query(query)
        
        search_kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": n_results
        }
        
        if where:
            search_kwargs["where"] = where
        
        results = self.collection.query(**search_kwargs)
        
        formatted_results = []
        if results and results["documents"] and len(results["documents"]) > 0:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else None,
                    "id": results["ids"][0][i] if results["ids"] else None
                })
        
        return formatted_results
    
    def delete(self, ids: List[str]) -> None:
        self.collection.delete(ids=ids)
        self.logger.info(f"删除了 {len(ids)} 个文档")
    
    def clear(self) -> None:
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        self.logger.info("知识库已清空")
    
    def count(self) -> int:
        return self.collection.count()
    
    def get_all_documents(self, limit: int = 100) -> List[Dict[str, Any]]:
        results = self.collection.get(limit=limit)
        
        documents = []
        if results and results["documents"]:
            for i in range(len(results["documents"])):
                documents.append({
                    "id": results["ids"][i] if results["ids"] else None,
                    "content": results["documents"][i],
                    "metadata": results["metadatas"][i] if results["metadatas"] else {}
                })
        
        return documents
