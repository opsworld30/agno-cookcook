# Memory 和 Knowledge 功能使用指南

## Memory (记忆功能)

### 功能说明

所有Agent都已启用自动记忆功能(`enable_user_memories=True`),可以:
- 自动记住用户的偏好和重要信息
- 记住历史对话内容
- 在后续交互中使用这些记忆提供个性化服务

### 使用方式

Memory功能**默认启用**,无需额外配置。只需正常使用Agent即可:

```bash
curl -X POST http://localhost:9001/agents/general-assistant/runs \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "message=我叫张三,我喜欢Python编程" \
  -d "user_id=user123" \
  -d "session_id=session_abc"
```

在后续对话中,Agent会记住这些信息:

```bash
curl -X POST http://localhost:9001/agents/general-assistant/runs \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "message=你还记得我的名字吗?" \
  -d "user_id=user123" \
  -d "session_id=session_abc"
```

### 支持的Agents

✅ 所有7个Agents都支持Memory:
- general-assistant (通用助手)
- web-search-expert (DuckDuckGo搜索)
- baidu-search-expert (百度搜索)
- searxng-expert (Searxng搜索)
- exa-search-expert (Exa搜索)
- data-analyst (数据分析师)
- code-assistant (代码助手)

✅ 研究工作流的所有步骤也支持Memory

### 数据存储

- Memory数据存储在SQLite数据库中(`agno.db`)
- 按`user_id`和`session_id`隔离
- 自动管理,无需手动维护

---

## Knowledge (知识库功能)

### 功能说明

Knowledge功能让Agent能够:
- 基于文档内容回答问题
- 提供准确的信息引用
- 支持PDF、文本、URL等多种内容源

### 启用方式

Knowledge功能**默认禁用**,需要手动启用:

#### 1. 安装依赖

```bash
uv sync
```

或手动安装:

```bash
pip install lancedb>=0.5.0
```

#### 2. 配置环境变量

编辑`.env`文件:

```env
# 启用Knowledge功能
ENABLE_KNOWLEDGE=true

# 可选: 自定义存储路径
KNOWLEDGE_DIR=tmp/lancedb
KNOWLEDGE_TABLE=knowledge_documents
```

#### 3. 添加知识内容

启动Python交互式环境:

```python
from utils.knowledge_manager import get_knowledge_manager

km = get_knowledge_manager()

# 添加文本内容
km.add_content(content="""
你的知识库内容...
可以是产品文档、技术文档、FAQ等
""")

# 添加本地文件
km.add_content(path="docs/readme.pdf")

# 添加整个目录
km.add_content(path="docs/")

# 添加URL
km.add_content(url="https://example.com/article")
```

#### 4. 使用知识库

启用Knowledge后,通用助手会自动搜索知识库:

```bash
curl -X POST http://localhost:9001/agents/general-assistant/runs \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "message=Agno CookCook有哪些功能?" \
  -d "user_id=user123"
```

### 支持的Agents

目前只有**通用助手**(general-assistant)支持Knowledge功能。

### 数据存储

- Knowledge数据存储在LanceDB向量数据库中
- 默认路径: `tmp/lancedb/`
- 支持语义搜索和相似度匹配

---

## 最佳实践

### Memory

1. **使用固定的user_id和session_id**
   - 同一用户使用相同的`user_id`
   - 同一会话使用相同的`session_id`
   - 这样Agent才能正确关联记忆

2. **告诉Agent重要信息**
   - 明确告诉Agent你的偏好
   - 例如: "我喜欢简洁的代码风格"
   - Agent会记住并在后续交互中使用

3. **定期清理**
   - Memory数据会持续累积
   - 可以定期清理`agno.db`中的旧数据

### Knowledge

1. **结构化内容**
   - 使用清晰的标题和段落
   - 包含关键词和术语
   - 便于Agent检索

2. **定期更新**
   - 保持知识库内容最新
   - 删除过时信息
   - 添加新的文档

3. **测试检索**
   - 添加内容后测试检索效果
   - 调整内容结构以提高准确性

---

## 故障排查

### Memory不工作

1. 检查是否使用了相同的`user_id`和`session_id`
2. 查看`agno.db`是否存在
3. 检查日志文件`logs/`

### Knowledge不工作

1. 确认`ENABLE_KNOWLEDGE=true`
2. 确认已安装`lancedb`
3. 检查`tmp/lancedb/`目录是否存在
4. 查看日志文件确认Knowledge是否初始化成功

### 性能问题

1. Memory数据过多: 定期清理旧数据
2. Knowledge检索慢: 减少知识库大小或优化内容结构
3. 数据库锁定: 确保没有多个进程同时访问数据库

---

## 示例代码

完整的示例代码在`examples/`目录:
- `memory_example.py` - Memory功能演示
- `knowledge_example.py` - Knowledge功能演示

运行示例:

```bash
python examples/memory_example.py
python examples/knowledge_example.py
```
