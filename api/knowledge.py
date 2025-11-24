from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from knowledge import KnowledgeBase
import os

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

kb = None

def get_kb():
    global kb
    if kb is None:
        try:
            kb = KnowledgeBase(
                persist_directory=os.getenv("KNOWLEDGE_DB_PATH", "./data/chroma"),
                collection_name=os.getenv("KNOWLEDGE_COLLECTION_NAME", "agno_knowledge")
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"知识库初始化失败: {str(e)}")
    return kb


class AddTextRequest(BaseModel):
    text: str
    metadata: Optional[dict] = None


class SearchRequest(BaseModel):
    query: str
    n_results: int = 5


class SearchResult(BaseModel):
    content: str
    metadata: dict
    distance: Optional[float]
    id: Optional[str]


class StatsResponse(BaseModel):
    total_documents: int
    collection_name: str
    persist_directory: str


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    try:
        knowledge_base = get_kb()
        return StatsResponse(
            total_documents=knowledge_base.count(),
            collection_name=knowledge_base.collection_name,
            persist_directory=knowledge_base.persist_directory
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-text")
async def add_text(request: AddTextRequest):
    try:
        knowledge_base = get_kb()
        ids = knowledge_base.add_documents(
            [request.text],
            metadatas=[request.metadata] if request.metadata else None
        )
        return {
            "success": True,
            "message": f"成功添加 {len(ids)} 个文本块",
            "ids": ids
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-file")
async def add_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = content.decode('utf-8')
        
        knowledge_base = get_kb()
        metadata = {
            "source": file.filename,
            "file_type": file.content_type
        }
        
        ids = knowledge_base.add_documents([text], metadatas=[metadata])
        
        return {
            "success": True,
            "message": f"成功添加文件 {file.filename}，生成 {len(ids)} 个文本块",
            "ids": ids
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=List[SearchResult])
async def search(request: SearchRequest):
    try:
        knowledge_base = get_kb()
        results = knowledge_base.search(request.query, n_results=request.n_results)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear")
async def clear():
    try:
        knowledge_base = get_kb()
        knowledge_base.clear()
        return {
            "success": True,
            "message": "知识库已清空"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents")
async def get_documents(limit: int = 100):
    try:
        knowledge_base = get_kb()
        documents = knowledge_base.get_all_documents(limit=limit)
        return {
            "success": True,
            "documents": documents,
            "total": len(documents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class DeleteDocumentRequest(BaseModel):
    id: str


@router.delete("/document")
async def delete_document(request: DeleteDocumentRequest):
    try:
        knowledge_base = get_kb()
        knowledge_base.delete([request.id])
        return {
            "success": True,
            "message": f"成功删除文档 {request.id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
