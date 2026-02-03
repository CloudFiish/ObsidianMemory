# 结果格式化指南

## 输出格式规范

### 简洁格式

用于快速浏览结果，显示核心信息。

```python
def display_compact(results):
    print(f"\n🔍 找到 {len(results)} 条相关记录\n")

    for i, record in enumerate(results, 1):
        fm = record.frontmatter
        stars = "⭐" * fm.importance

        print(f"[{i}] {stars} {fm.title}")
        print(f"    📅 {fm.date} | 🏷️ {' '.join(fm.tags)}")
```

**输出示例**:
```
🔍 找到 3 条相关记录

[1] ⭐⭐⭐⭐ 数据库选择 - PostgreSQL
    📅 2026-01-15 | 🏷️ #技术 #决策

[2] ⭐⭐⭐ API 设计 - REST 选择
    📅 2026-01-20 | 🏷️ #技术 #决策

[3] ⭐⭐ 技术选型 - Redis 缓存
    📅 2026-01-25 | 🏷️ #技术
```

---

### 详细格式

用于查看详细信息，显示所有字段和摘要。

```python
def display_detailed(results):
    print(f"\n{'='*60}")
    print(f"🔍 搜索结果（共 {len(results)} 条）")
    print(f"{'='*60}\n")

    for i, record in enumerate(results, 1):
        fm = record.frontmatter
        stars = "⭐" * fm.importance

        print(f"[{i}] {stars} {fm.title}")
        print(f"    📁 文件: {record.file.name}")
        print(f"    📅 日期: {fm.date} | ⏰ 时间: {fm.time}")
        print(f"    🏷️ 类型: {fm.type} | 标签: {' '.join(fm.tags)}")
        print(f"    ⭐ 重要程度: {fm.importance} | 🔗 项目: {fm.project}")
        print(f"    📊 状态: {fm.status}")

        # 摘要
        if len(record.body) > 100:
            snippet = record.body[:100]
            print(f"    📄 摘要: {snippet}...")

        print(f"{'='*60}\n")
```

**输出示例**:
```
============================================================
🔍 搜索结果（共 3 条）
============================================================

[1] ⭐⭐⭐⭐ 数据库选择 - PostgreSQL
    📁 文件: 2026-01-15.md
    📅 日期: 2026-01-15 | ⏰ 时间: 14:30
    🏷️ 类型: 决策 | 标签: #技术 #决策 #重要
    ⭐ 重要程度: 4 | 🔗 项目: Acme Dashboard
    📊 状态: 已完成
    📄 摘要: 决策: 选择 PostgreSQL 作为数据库...

============================================================

[2] ⭐⭐⭐ API 设计 - REST 选择
    ...
```

---

### 表格格式

使用表格形式展示，便于比较。

```python
def display_table(results):
    print(f"\n🔍 搜索结果（共 {len(results)} 条）\n")
    print(f"{'序号':<5} {'标题':<30} {'日期':<12} {'类型':<10} {'重要':<6}")
    print(f"{'-'*60}")

    for i, record in enumerate(results, 1):
        fm = record.frontmatter
        stars = str(fm.importance) + "⭐"

        print(f"{i:<5} {fm.title:<30} {fm.date:<12} {fm.type:<10} {stars:<6}")
```

**输出示例**:
```
🔍 搜索结果（共 3 条）

序号  标题                          日期         类型       重要
------------------------------------------------------------
1      数据库选择 - PostgreSQL      2026-01-15  决策      4⭐
2      API 设计 - REST 选择         2026-01-20  决策      4⭐
3      技术选型 - Redis 缓存      2026-01-25  技术选型  3⭐
```

---

## 分数显示

### 关键词搜索分数

```python
def display_keyword_score(score):
    print(f"💡 关键词分: {score}")
    print(f"   - 标题匹配: {'✅' if score >= 10 else '❌'}")
    print(f"   - 内容匹配: {'✅' if score >= 5 else '❌'}")
    print(f"   - 标签匹配: {'✅' if score >= 3 else '❌'}")
```

**输出示例**:
```
💡 关键词分: 15
   - 标题匹配: ✅
   - 内容匹配: ✅
   - 标签匹配: ✅
```

### 语义搜索分数

```python
def display_semantic_score(similarity):
    similarity_percent = int(similarity * 100)

    print(f"💡 语义相似度: {similarity_percent}%")

    if similarity >= 0.9:
        print(f"   - 相关性: 高度相关")
    elif similarity >= 0.7:
        print(f"   - 相关性: 相关")
    elif similarity >= 0.5:
        print(f"   - 相关性: 较弱相关")
    else:
        print(f"   - 相关性: 弱相关")
```

**输出示例**:
```
💡 语义相似度: 85%
   - 相关性: 相关
```

### 混合搜索分数

```python
def display_hybrid_score(total, keyword, semantic):
    total_percent = int(total * 100)
    keyword_percent = int((keyword / 10.0) * 100)
    semantic_percent = int(semantic * 100)

    print(f"💡 总分: {total_percent}%")
    print(f"   - 关键词分: {keyword_percent}% (权重: 30%)")
    print(f"   - 语义分: {semantic_percent}% (权重: 70%)")
```

**输出示例**:
```
💡 总分: 82%
   - 关键词分: 60% (权重: 30%)
   - 语义分: 90% (权重: 70%)
```

---

## 摘要生成

### 简单摘要

```python
def generate_snippet(body, query, max_length=100):
    # 查找查询词在内容中的位置
    pos = body.lower().find(query.lower())

    if pos >= 0:
        # 提取前后文本
        start = max(0, pos - 20)
        end = min(len(body), pos + max_length)
        snippet = body[start:end]

        # 添加省略号
        if start > 0:
            snippet = "..." + snippet
        if end < len(body):
            snippet = snippet + "..."

        return snippet

    # 未找到查询词，返回开头
    return body[:max_length] + "..."
```

**输出示例**:
```
📄 摘要: ...决定使用 PostgreSQL 作为数据库，因为它的 ACID 特性...
```

### 高亮摘要

```python
def generate_highlighted_snippet(body, query, max_length=100):
    # 查找查询词
    pos = body.lower().find(query.lower())

    if pos >= 0:
        # 提取前后文本
        start = max(0, pos - 20)
        end = min(len(body), pos + len(query) + 80)

        before = body[start:pos]
        match = body[pos:pos+len(query)]
        after = body[pos+len(query):end]

        # 添加高亮标记
        snippet = f"...{before}[{match}]{after}..."

        return snippet

    return body[:max_length] + "..."
```

**输出示例**:
```
📄 摘要: ...决定使用 [PostgreSQL] 作为数据库...
```

---

## 无结果处理

### 无结果输出

```python
def display_no_results(query):
    print(f"\n🔍 未找到与 \"{query}\" 相关的记录")
    print("\n💡 建议:")
    print("  1. 尝试不同的关键词")
    print("  2. 使用语义搜索: /semantic [查询]")
    print("  3. 扩大时间范围")
    print("  4. 降低重要程度要求")
    print("  5. 搜索相关项目: /project [项目名]")
```

**输出示例**:
```
🔍 未找到与 "XYZ" 相关的记录

💡 建议:
  1. 尝试不同的关键词
  2. 使用语义搜索: /semantic [查询]
  3. 扩大时间范围
  4. 降低重要程度要求
  5. 搜索相关项目: /project [项目名]
```

---

## 操作选项

### 结果操作菜单

```python
def display_action_menu(results):
    print(f"\n操作选项:")

    for i in range(1, len(results) + 1):
        print(f"  [{i}] 查看记录 {i}")

    print(f"  [n] 新建搜索")
    print(f"  [q] 退出")

    while True:
        choice = input("\n请选择: ").strip()

        if choice.lower() == 'q':
            return None
        elif choice.lower() == 'n':
            return 'new_search'
        elif choice.isdigit() and 1 <= int(choice) <= len(results):
            return int(choice) - 1

        print("❌ 无效选择")
```

**输出示例**:
```
操作选项:
  [1] 查看记录 1
  [2] 查看记录 2
  [3] 查看记录 3
  [n] 新建搜索
  [q] 退出

请选择:
```

---

## 颜色和图标

### 推荐颜色编码

```python
# 终端颜色（ANSI）
class Colors:
    HEADER = '\033[95m'      # 紫色
    OKBLUE = '\033[94m'         # 蓝色
    OKCYAN = '\033[96m'         # 青色
    OKGREEN = '\033[92m'        # 绿色
    WARNING = '\033[93m'        # 黄色
    FAIL = '\033[91m'          # 红色
    ENDC = '\033[0m'          # 结束
```

### 图标使用

| 图标 | 用途 | 示例 |
|------|------|------|
| 🔍 | 搜索 | "找到 3 条记录" |
| 📁 | 文件 | "文件: 2026-02-02.md" |
| 📅 | 日期 | "日期: 2026-02-02" |
| 🏷️ | 标签 | "标签: #技术 #决策" |
| ⭐ | 重要程度 | "重要程度: 4⭐" |
| 🔗 | 链接/项目 | "项目: Acme Dashboard" |
| 📊 | 状态 | "状态: 已完成" |
| 💡 | 信息/提示 | "建议: ..." |
| ✅ | 成功 | "记录已创建" |
| ❌ | 错误 | "记录失败" |
| ⚠️ | 警告 | "跳过文件" |
| ℹ️ | 信息 | "还有 5 条记录" |

---

## 导出格式

### 导出为 Markdown

```python
def export_markdown(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 搜索结果\n\n")
        f.write(f"查询: {query}\n\n")
        f.write(f"找到: {len(results)} 条记录\n\n")

        for i, record in enumerate(results, 1):
            f.write(f"## {i}. {record.frontmatter.title}\n\n")
            f.write(f"- 日期: {record.frontmatter.date}\n")
            f.write(f"- 类型: {record.frontmatter.type}\n")
            f.write(f"- 重要程度: {record.frontmatter.importance}⭐\n")
            f.write(f"\n")
```

### 导出为 CSV

```python
def export_csv(results, output_file):
    import csv

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['标题', '日期', '类型', '重要程度', '标签', '项目', '状态'])

        for record in results:
            fm = record.frontmatter
            writer.writerow([
                fm.title,
                fm.date,
                fm.type,
                fm.importance,
                ' '.join(fm.tags),
                fm.project,
                fm.status
            ])
```

---

## 最佳实践

### 1. 根据结果数量选择格式

- 少量结果 (<5): 详细格式
- 中量结果 (5-10): 简洁格式
- 大量结果 (>10): 表格格式

### 2. 始终显示分数

让用户理解为什么结果这样排序

### 3. 提供摘要

不要只显示标题，显示内容摘要

### 4. 提供操作选项

允许用户查看、编辑、导出结果

### 5. 处理无结果情况

给出有用的建议，帮助用户改进查询
