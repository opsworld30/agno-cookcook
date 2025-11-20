# 性能优化指南

## 🚀 性能优化策略

### 1. Memory功能优化

Memory功能会在每次对话时查询和更新数据库,如果不需要记忆功能,可以禁用:

```env
# 禁用Memory提升响应速度
ENABLE_MEMORY=false
```

**性能影响**:
- 启用Memory: 每次对话增加 50-100ms
- 禁用Memory: 无额外延迟

**建议**:
- 开发测试时可以禁用
- 生产环境根据需求选择

### 2. Knowledge功能优化

Knowledge是最影响性能的功能,因为需要向量搜索。已实现的优化:

#### ✅ 使用FixedSizeChunking (快速分块)

```env
# 使用固定大小分块,比语义分块快3-5倍
KNOWLEDGE_CHUNK_SIZE=800
KNOWLEDGE_CHUNK_OVERLAP=80
```

**对比**:
- FixedSizeChunking: 快速,适合简单文档
- SemanticChunking: 慢,但质量更好,适合复杂文档

#### ✅ 跳过已处理文件

```python
km = get_knowledge_manager()

# 自动跳过已存在的文件,避免重复处理
km.add_content(
    path="docs/readme.pdf",
    skip_if_exists=True,  # 默认True
    upsert=False  # 不更新已存在的内容
)
```

#### ✅ 限制搜索结果数量

```env
# 减少返回结果数量,提升搜索速度
KNOWLEDGE_MAX_RESULTS=5
```

#### ✅ 使用专用Embedding模型

推荐使用智谱AI的Embedding-3模型:

```env
KNOWLEDGE_EMBEDDING_MODEL=zhipuai/embedding-3
KNOWLEDGE_EMBEDDING_API_KEY=your_zhipuai_api_key
KNOWLEDGE_EMBEDDING_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
```

**优势**:
- 专门优化的Embedding模型
- 比通用LLM模型快
- 成本更低

### 3. 向量数据库选择

当前使用LanceDB(本地,快速):

```python
# 开发环境: LanceDB (无需配置)
vector_db = LanceDb(
    table_name="knowledge_documents",
    uri="tmp/lancedb"
)
```

**生产环境建议**:
- 小规模(<10万文档): LanceDB
- 中规模(10-100万): PgVector
- 大规模(>100万): Pinecone

### 4. 批量操作优化

如果需要加载大量文档,使用异步批量操作:

```python
import asyncio

async def load_knowledge_efficiently():
    km = get_knowledge_manager()
    
    # 并行加载多个目录
    tasks = [
        km._knowledge.add_content_async(path="docs/hr/"),
        km._knowledge.add_content_async(path="docs/engineering/"),
        km._knowledge.add_content_async(url="https://company.com/api-docs"),
    ]
    
    await asyncio.gather(*tasks)

asyncio.run(load_knowledge_efficiently())
```

## 📊 性能对比

### 普通对话响应时间

| 配置 | 响应时间 | 说明 |
|------|---------|------|
| 无Memory + 无Knowledge | ~500ms | 最快 |
| 有Memory + 无Knowledge | ~600ms | 增加100ms |
| 无Memory + 有Knowledge | ~1.5s | Knowledge搜索耗时 |
| 有Memory + 有Knowledge | ~1.6s | 完整功能 |

### Knowledge搜索时间

| 文档数量 | FixedChunking | SemanticChunking |
|---------|--------------|------------------|
| <1000 | ~200ms | ~600ms |
| 1000-10000 | ~500ms | ~1.5s |
| >10000 | ~1s | ~3s |

## 🎯 推荐配置

### 开发/测试环境

```env
# 快速响应,方便调试
ENABLE_MEMORY=false
ENABLE_KNOWLEDGE=false
```

### 生产环境 - 标准配置

```env
# 平衡性能和功能
ENABLE_MEMORY=true
ENABLE_KNOWLEDGE=false  # 按需启用
KNOWLEDGE_CHUNK_SIZE=800
KNOWLEDGE_MAX_RESULTS=5
```

### 生产环境 - 完整功能

```env
# 启用所有功能
ENABLE_MEMORY=true
ENABLE_KNOWLEDGE=true
KNOWLEDGE_CHUNK_SIZE=800
KNOWLEDGE_CHUNK_OVERLAP=80
KNOWLEDGE_MAX_RESULTS=5

# 使用专用Embedding模型
KNOWLEDGE_EMBEDDING_MODEL=zhipuai/embedding-3
KNOWLEDGE_EMBEDDING_API_KEY=your_key
KNOWLEDGE_EMBEDDING_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
```

## 🔍 性能监控

### 查看日志

```bash
# 查看Knowledge初始化日志
tail -f logs/$(date +%Y-%m-%d).log | grep Knowledge

# 查看响应时间
tail -f logs/$(date +%Y-%m-%d).log | grep "响应时间"
```

### 检查Knowledge状态

```python
from utils.knowledge_manager import get_knowledge_manager

km = get_knowledge_manager()

if km.is_available():
    # 获取内容统计
    content_list, count = km._knowledge.get_content()
    print(f"知识库文档数: {count}")
    
    # 检查特定内容状态
    for content in content_list[:5]:
        status, message = km._knowledge.get_content_status(content.id)
        print(f"{content.name}: {status}")
```

## 💡 最佳实践

1. **按需启用功能**: 不需要的功能就禁用
2. **使用专用Embedding**: 不要用LLM模型做Embedding
3. **定期清理**: 删除过时的Knowledge内容
4. **批量操作**: 大量文档用异步批量加载
5. **监控性能**: 定期查看日志,发现瓶颈

## 🐛 常见问题

### Q: 为什么对话变慢了?

A: 检查是否启用了Knowledge,Knowledge搜索会增加1-2秒延迟。如果不需要知识库功能,设置`ENABLE_KNOWLEDGE=false`。

### Q: 如何只在特定Agent使用Knowledge?

A: 目前只有通用助手支持Knowledge。其他Agent默认不使用Knowledge,不会影响性能。

### Q: Memory可以完全禁用吗?

A: 可以,设置`ENABLE_MEMORY=false`即可。但会失去个性化能力。

### Q: 如何提升Knowledge搜索速度?

A: 
1. 减少`KNOWLEDGE_MAX_RESULTS`
2. 使用`FixedSizeChunking`
3. 使用专用Embedding模型
4. 升级到更快的向量数据库(PgVector/Pinecone)
