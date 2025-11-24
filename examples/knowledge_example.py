import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from knowledge import KnowledgeBase
from dotenv import load_dotenv

load_dotenv()


def main():
    print("=== ChromaDB 知识库示例 ===\n")
    
    kb = KnowledgeBase(
        persist_directory="./data/chroma",
        collection_name="test_knowledge",
        chunk_size=500,
        chunk_overlap=50
    )
    
    print(f"当前知识库文档数: {kb.count()}\n")
    
    documents = [
        "Agno是一个强大的AI Agent框架，支持构建智能助手和自动化工作流。",
        "ChromaDB是一个开源的向量数据库，专为AI应用设计，支持高效的相似度搜索。",
        "智谱AI提供了embedding-3模型，可以将文本转换为2048维的向量表示。",
        "RAG（检索增强生成）是一种结合知识检索和大语言模型的技术，可以提供更准确的答案。"
    ]
    
    metadatas = [
        {"source": "agno_docs", "category": "framework"},
        {"source": "chromadb_docs", "category": "database"},
        {"source": "zhipu_docs", "category": "embedding"},
        {"source": "ai_concepts", "category": "technique"}
    ]
    
    print("添加文档到知识库...")
    ids = kb.add_documents(documents, metadatas=metadatas)
    print(f"成功添加 {len(ids)} 个文档块\n")
    
    print(f"更新后文档数: {kb.count()}\n")
    
    query = "什么是RAG技术"
    print(f"搜索查询: {query}")
    results = kb.search(query, n_results=3)
    
    print(f"\n找到 {len(results)} 个相关结果:\n")
    for i, result in enumerate(results, 1):
        print(f"结果 {i}:")
        print(f"内容: {result['content']}")
        print(f"来源: {result['metadata'].get('source', 'unknown')}")
        print(f"分类: {result['metadata'].get('category', 'unknown')}")
        print(f"相似度: {1 - result['distance']:.3f}")
        print()


if __name__ == "__main__":
    main()
