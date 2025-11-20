# Agno CookCook 示例

本目录包含Agno CookCook系统的各种功能示例。

## Memory (记忆功能)

### 运行Memory示例

```bash
python examples/memory_example.py
```

**功能演示**:
- Agent自动记住用户告诉它的信息
- 在后续对话中使用这些记忆
- 提供个性化的回复

**实现原理**:
```python
agent = Agent(
    enable_user_memories=True,  # 启用自动记忆
    db=SqliteDb(db_file="agno.db")
)
```

## Knowledge (知识库)

### 安装依赖

```bash
pip install lancedb
```

### 运行Knowledge示例

```bash
python examples/knowledge_example.py
```

**功能演示**:
- 向知识库添加文档内容
- Agent基于知识库回答问题
- 提供准确的引用来源

**实现原理**:
```python
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb

knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="knowledge_documents",
        uri="tmp/lancedb"
    )
)

knowledge.add_content(content="...")

agent = Agent(
    knowledge=knowledge,
    search_knowledge=True
)
```

## 其他示例

### 添加文档到知识库

```python
# 添加本地文件
knowledge.add_content(path="docs/readme.pdf")

# 添加整个目录
knowledge.add_content(path="docs/")

# 添加URL
knowledge.add_content(url="https://example.com/article")

# 添加文本内容
knowledge.add_content(content="你的文本内容...")
```

### Agentic Memory (主动记忆)

```python
agent = Agent(
    enable_agentic_memory=True,  # Agent主动决定记忆内容
    db=SqliteDb(db_file="agno.db")
)
```

## 注意事项

1. **Memory**: 需要配置数据库(SQLite)
2. **Knowledge**: 需要安装向量数据库(LanceDB)
3. **API Key**: 确保.env文件中配置了有效的API Key
4. **模型选择**: 某些功能可能需要更强大的模型

## 下一步

- 尝试将Memory和Knowledge结合使用
- 在实际项目中集成这些功能
- 探索更多Agno框架的高级特性
