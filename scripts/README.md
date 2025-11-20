# 知识库管理脚本

这个目录包含用于管理Agno CookCook知识库的工具脚本。

## 📋 脚本列表

### 1. init_knowledge.py - 快速初始化

快速初始化知识库，自动添加项目文档。

```bash
python scripts/init_knowledge.py
```

**自动添加的内容:**
- README.md
- docs/ 目录下的所有Markdown文件
- 系统信息（Agents、Teams、Workflows列表）

---

### 2. add_knowledge.py - 添加内容

灵活添加各种类型的内容到知识库。

#### 添加单个文件

```bash
python scripts/add_knowledge.py file <文件路径>
```

**示例:**
```bash
python scripts/add_knowledge.py file README.md
python scripts/add_knowledge.py file docs/PERFORMANCE.md
```

**支持的文件格式:**
- Markdown (.md)
- 文本 (.txt)
- PDF (.pdf)
- Word (.doc, .docx)
- HTML (.html)
- JSON (.json)
- Python (.py)

#### 添加整个目录

```bash
python scripts/add_knowledge.py dir <目录路径>
```

**示例:**
```bash
python scripts/add_knowledge.py dir docs/
python scripts/add_knowledge.py dir examples/
```

**特性:**
- 递归扫描子目录
- 自动过滤支持的文件类型
- 跳过已存在的文件

#### 添加URL

```bash
python scripts/add_knowledge.py url <URL>
```

**示例:**
```bash
python scripts/add_knowledge.py url https://docs.agno.com
python scripts/add_knowledge.py url https://github.com/agno-agi/agno
```

#### 添加文本

```bash
python scripts/add_knowledge.py text "<文本内容>"
```

**示例:**
```bash
python scripts/add_knowledge.py text "这是一段知识库内容"
```

---

### 3. list_knowledge.py - 查看内容

查看知识库中的所有文档。

```bash
python scripts/list_knowledge.py
```

**显示信息:**
- 文档总数
- 每个文档的名称、ID、类型
- 处理状态

---

## 🚀 快速开始

### 第一次使用

1. **确保Knowledge已启用**

编辑 `.env`:
```env
ENABLE_KNOWLEDGE=true
KNOWLEDGE_EMBEDDING_MODEL=embedding-3
KNOWLEDGE_EMBEDDING_API_KEY=your_zhipuai_api_key
KNOWLEDGE_EMBEDDING_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
```

2. **初始化知识库**

```bash
python scripts/init_knowledge.py
```

3. **查看内容**

```bash
python scripts/list_knowledge.py
```

4. **测试查询**

```bash
curl -X POST http://localhost:9001/agents/general-assistant/runs \
  -d "message=Agno CookCook有哪些Agent?" \
  -d "user_id=user123"
```

---

## 📚 使用场景

### 场景1: 添加项目文档

```bash
# 初始化基础文档
python scripts/init_knowledge.py

# 添加更多文档
python scripts/add_knowledge.py dir docs/
```

### 场景2: 添加外部资料

```bash
# 添加Agno官方文档
python scripts/add_knowledge.py url https://docs.agno.com

# 添加自定义说明
python scripts/add_knowledge.py text "
项目部署说明:
1. 配置.env文件
2. 运行./run.sh
3. 访问http://localhost:9001
"
```

### 场景3: 更新知识库

```bash
# 查看当前内容
python scripts/list_knowledge.py

# 添加新文档
python scripts/add_knowledge.py file new_doc.md

# 再次查看
python scripts/list_knowledge.py
```

---

## ⚠️ 注意事项

1. **首次添加会创建向量数据库**
   - 位置: `tmp/lancedb/`
   - 自动使用智谱Embedding-3模型

2. **重复添加会自动跳过**
   - 默认 `skip_if_exists=True`
   - 避免重复处理相同文件

3. **大文件处理需要时间**
   - PDF、长文档会分块处理
   - 请耐心等待

4. **向量维度一致性**
   - 使用相同的Embedding模型
   - 更换模型需要清空数据库: `rm -rf tmp/lancedb/`

---

## 🔧 故障排查

### 问题: Knowledge未初始化

**检查:**
```bash
grep ENABLE_KNOWLEDGE .env
grep KNOWLEDGE_EMBEDDING .env
```

**解决:**
确保配置正确并重启服务。

### 问题: 向量维度不匹配

**解决:**
```bash
# 清空数据库
rm -rf tmp/lancedb/

# 重新初始化
python scripts/init_knowledge.py
```

### 问题: 文件添加失败

**检查日志:**
```bash
tail -f logs/$(date +%Y-%m-%d).log | grep Knowledge
```

---

## 📖 更多信息

- [Memory和Knowledge使用指南](../docs/MEMORY_KNOWLEDGE.md)
- [性能优化指南](../docs/PERFORMANCE.md)
- [项目README](../README.md)
