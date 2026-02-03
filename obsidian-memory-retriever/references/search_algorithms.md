# 搜索算法详解

## 1. 关键词搜索

### 算法原理
```python
def keyword_search(query, database):
    results = []

    for record in database:
        score = 0
        query_lower = query.lower()

        # 标题匹配（权重 10）
        if query_lower in record.title.lower():
            score += 10

        # 内容匹配（权重 5）
        if query_lower in record.content.lower():
            score += 5

        # 标签匹配（权重 3）
        for tag in record.tags:
            if query_lower in tag.lower():
                score += 3

        if score > 0:
            results.append((record, score))

    return sorted(results, key=lambda x: x[1], reverse=True)
```

### 权重说明

| 匹配位置 | 权重 | 说明 |
|----------|--------|------|
| 标题 | 10 | 标题是最重要的信息 |
| 内容 | 5 | 内容中的匹配 |
| 标签 | 3 | 标签的辅助信息 |

### 优缺点
**优点**:
- 快速高效
- 精确匹配
- 易于理解和调试

**缺点**:
- 依赖完全匹配
- 无法理解语义
- 同义词无法匹配

### 使用场景
- 搜索具体的术语
- 查找包含特定词的记录
- 精确关键词查询

---

## 2. 语义搜索

### 算法原理

#### 步骤 1: 生成嵌入向量
```python
def generate_embedding(text):
    # 使用预训练模型
    embedding = model.encode(text)
    return embedding  # 例如: [0.12, -0.34, 0.56, ...]
```

#### 步骤 2: 计算相似度
```python
def cosine_similarity(vec1, vec2):
    # 点积
    dot_product = sum(a * b for a, b in zip(vec1, vec2))

    # 向量长度
    magnitude1 = sqrt(sum(a * a for a in vec1))
    magnitude2 = sqrt(sum(b * b for b in vec2))

    # 余弦相似度
    similarity = dot_product / (magnitude1 * magnitude2)

    return similarity  # 范围: 0-1
```

#### 步骤 3: 匹配和排序
```python
def semantic_search(query, database, threshold=0.7):
    query_vector = generate_embedding(query)
    results = []

    for record in database:
        record_vector = record.embedding

        # 计算相似度
        similarity = cosine_similarity(query_vector, record_vector)

        # 超过阈值则添加到结果
        if similarity >= threshold:
            results.append((record, similarity))

    # 按相似度排序
    return sorted(results, key=lambda x: x[1], reverse=True)
```

### 嵌入模型选择

#### 生产环境推荐

1. **sentence-transformers** (开源)
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode("你的文本")
```

2. **OpenAI Embeddings API**
```python
import openai

response = openai.Embedding.create(
    model="text-embedding-3-small",
    input="你的文本"
)
embedding = response['data'][0]['embedding']
```

3. **Cohere Embeddings**
```python
import cohere

co = cohere.Client('your-api-key')
response = co.embed(texts=["你的文本"])
embedding = response.embeddings[0]
```

#### 开发/测试环境

简化实现（当前脚本使用）:
```python
def simple_embedding(text):
    # 基于 TF-IDF 的简化版本
    words = text.split()
    word_freq = {}

    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1

    # 生成固定大小的向量
    vocab_size = 1000
    embedding = [0.0] * vocab_size

    for word, freq in word_freq.items():
        word_hash = hash(word) % vocab_size
        embedding[word_hash] = float(freq)

    # 归一化
    magnitude = sqrt(sum(v * v for v in embedding))
    if magnitude > 0:
        embedding = [v / magnitude for v in embedding]

    return embedding
```

### 相似度阈值

| 阈值 | 说明 | 使用场景 |
|--------|------|----------|
| 0.9 | 高度相关 | 精确查询 |
| 0.7 | 相关（默认）| 一般查询 |
| 0.5 | 较弱相关 | 广泛查询 |
| 0.3 | 弱相关 | 探索性查询 |

### 优缺点

**优点**:
- 理解语义含义
- 同义词可以匹配
- 不依赖完全匹配

**缺点**:
- 计算资源消耗大
- 需要预训练模型
- 可能返回不精确的结果

### 使用场景
- 搜索概念和想法
- 查找相关但关键词不匹配的记录
- 自然语言查询

---

## 3. 混合搜索

### 算法原理

```python
def hybrid_search(query, database, keyword_weight=0.3, semantic_weight=0.7):
    # 步骤 1: 执行关键词搜索
    keyword_results = keyword_search(query, database)

    # 步骤 2: 执行语义搜索
    semantic_results = semantic_search(query, database)

    # 步骤 3: 合并结果
    combined = {}

    # 处理关键词结果
    for record, score in keyword_results:
        file_id = record.file.id
        if file_id not in combined:
            combined[file_id] = {
                "record": record,
                "keyword_score": score,
                "semantic_score": 0.0
            }
        else:
            combined[file_id]["keyword_score"] = score

    # 处理语义结果
    for record, similarity in semantic_results:
        file_id = record.file.id
        if file_id not in combined:
            combined[file_id] = {
                "record": record,
                "keyword_score": 0.0,
                "semantic_score": similarity
            }
        else:
            combined[file_id]["semantic_score"] = similarity

    # 步骤 4: 计算加权总分
    results = []
    for file_id, data in combined.items():
        # 归一化分数
        normalized_keyword = data["keyword_score"] / 10.0
        normalized_semantic = data["semantic_score"]

        # 加权计算
        total_score = (keyword_weight * normalized_keyword) + \
                    (semantic_weight * normalized_semantic)

        results.append((data["record"], total_score,
                     data["keyword_score"], data["semantic_score"]))

    # 步骤 5: 按总分排序
    return sorted(results, key=lambda x: x[1], reverse=True)
```

### 权重配置

| 权重 | 默认 | 说明 |
|--------|--------|------|
| keyword_weight | 0.3 | 关键词匹配权重（30%） |
| semantic_weight | 0.7 | 语义相似度权重（70%） |

#### 调整建议

**查询包含精确术语**:
```python
keyword_weight = 0.7  # 增加关键词权重
semantic_weight = 0.3
```

**查询是自然语言**:
```python
keyword_weight = 0.2  # 降低关键词权重
semantic_weight = 0.8  # 增加语义权重
```

### 优缺点

**优点**:
- 结合两种方法的优势
- 关键词精确匹配
- 语义理解概念
- 结果更准确

**缺点**:
- 计算复杂度高
- 需要调整权重
- 资源消耗大

### 使用场景
- 综合查询（"找到技术决策，特别是关于 API 的"）
- 复杂查询
- 需要高准确度的查询

---

## 性能优化

### 1. 索引构建

```python
# 预构建标题索引
title_index = {}
for record in database:
    title = record.title.lower()
    if title not in title_index:
        title_index[title] = []
    title_index[title].append(record)

# 查询时快速查找
if query.lower() in title_index:
    results = title_index[query.lower()]
```

### 2. 嵌入缓存

```python
embedding_cache = {}

def get_embedding(text):
    if text not in embedding_cache:
        embedding_cache[text] = generate_embedding(text)
    return embedding_cache[text]
```

### 3. 结果限制

```python
# 限制返回数量
max_results = 10
results = results[:max_results]
```

### 4. 去重

```python
# 使用集合去重
seen = set()
unique_results = []

for record, score in results:
    if record.id not in seen:
        seen.add(record.id)
        unique_results.append((record, score))
```

---

## 算法选择指南

### 何时使用关键词搜索

✅ 查询包含精确术语
✅ 搜索特定名称或ID
✅ 需要快速结果
✅ 查询短而具体

### 何时使用语义搜索

✅ 查询是自然语言
✅ 搜索概念和想法
✅ 关键词不完全匹配
✅ 查询较长且复杂

### 何时使用混合搜索

✅ 需要最高准确度
✅ 查询包含精确术语和概念
✅ 综合查询
✅ 初期不确定最佳方法
