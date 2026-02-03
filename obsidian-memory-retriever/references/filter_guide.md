# 过滤器使用指南

## 可用过滤器

### 1. 日期过滤器

#### 指定日期
```bash
--date 2026-02-02
```

**说明**: 仅搜索指定日期的记录

#### 相对日期（快捷命令）
```bash
/today      # 今天
/this-week  # 本周
/this-month # 本月
```

#### 相对日期（脚本选项）
```bash
--after 2026-01-01
--before 2026-12-31
```

**示例**:
```bash
python search.py ~/Obsidian/Vault PostgreSQL --date 2026-02-02
python search.py ~/Obsidian/Vault 决策 --after 2026-01-01
```

---

### 2. 类型过滤器

#### 类型选项
```bash
--type <类型>
```

**可用类型**:
- `daily-log` - 每日日志
- `决策` - 决策记录
- `任务` - 任务
- `学习笔记` - 学习笔记
- `会议记录` - 会议记录
- `用户偏好` - 用户偏好

**示例**:
```bash
python search.py ~/Obsidian/Vault API --type 决策
python search.py ~/Obsidian/Vault 学习 --type 学习笔记
```

---

### 3. 重要程度过滤器

#### 最小重要程度
```bash
--importance <数字>
```

**说明**: 仅搜索重要程度 >= N 的记录

**重要程度级别**:
- 5 - 紧急重要
- 4 - 重要
- 3 - 中等（默认）
- 2 - 较低
- 1 - 极低

**示例**:
```bash
python search.py ~/Obsidian/Vault 决策 --importance 4
python search.py ~/Obsidian/Vault 重要 --importance 5
```

#### 快捷命令
```bash
/important   # 4 星及以上
/urgent     # 5 星
```

---

### 4. 状态过滤器

#### 状态选项
```bash
--status <状态>
```

**可用状态**:
- `进行中` - 正在进行
- `已完成` - 已完成
- `暂停` - 暂停
- `已归档` - 已归档

**示例**:
```bash
python search.py ~/Obsidian/Vault 任务 --status 进行中
python search.py ~/Obsidian/Vault 决策 --status 已完成
```

#### 快捷命令
```bash
/pending    # 进行中
/completed  # 已完成
```

---

### 5. 项目过滤器

#### 按项目搜索
```bash
--project <项目名>
```

**说明**: 仅搜索指定项目的记录

**示例**:
```bash
python search.py ~/Obsidian/Vault API --project "Acme Dashboard"
python search.py ~/Obsidian/Vault 决策 --project "API Gateway"
```

#### 快捷命令
```bash
/project <项目名>
```

---

## 组合过滤器

### 多个过滤器

```bash
python search.py ~/Obsidian/Vault PostgreSQL \
  --type 决策 \
  --importance 4 \
  --after 2026-01-01
```

### 常用组合

**本周重要决策**:
```bash
python search.py ~/Obsidian/Vault 决策 \
  --this-week \
  --importance 4
```

**今日进行中任务**:
```bash
python search.py ~/Obsidian/Vault 任务 \
  --today \
  --status 进行中
```

**某项目的所有记录**:
```bash
python search.py ~/Obsidian/Vault "" \
  --project "Acme Dashboard"
```

---

## 过滤器操作符

| 操作符 | 说明 | 示例 |
|--------|------|------|
| `--type` | 等于类型 | `--type 决策` |
| `--date` | 等于日期 | `--date 2026-02-02` |
| `--after` | 日期之后 | `--after 2026-01-01` |
| `--before` | 日期之前 | `--before 2026-12-31` |
| `--importance` | 大于等于 | `--importance 4` |
| `--status` | 等于状态 | `--status 进行中` |
| `--project` | 等于项目 | `--project "Acme Dashboard"` |

---

## 快捷过滤器

### 内置快捷过滤

在支持的命令环境中使用：

```bash
# 今天的记录
/today

# 本周的记录
/this-week

# 本月的记录
/this-month

# 待处理
/pending

# 高优先级
/important

# 紧急
/urgent

# 按项目
/project <项目名>
```

### 组合使用

```bash
# 本周的高优先级决策
/this-week /important /decision

# 今天的待办任务
/today /pending /task
```

---

## 过滤器最佳实践

### 1. 从宽到窄

```bash
# 步骤 1: 宽泛搜索
python search.py ~/Obsidian/Vault 决策

# 步骤 2: 添加时间过滤
python search.py ~/Obsidian/Vault 决策 --this-week

# 步骤 3: 添加重要程度过滤
python search.py ~/Obsidian/Vault 决策 --this-week --importance 4

# 步骤 4: 添加类型过滤
python search.py ~/Obsidian/Vault 决策 --this-week --importance 4 --type 决策
```

### 2. 使用相对日期

```bash
# 推荐
/this-week
/this-month
/after 2026-01-01

# 不推荐
--date 2026-02-02  # 除非知道确切日期
```

### 3. 优先使用语义

```bash
# 宽泛查询使用语义
/semantic 我们之前讨论过数据库吗？

# 精确查询使用关键词
/search PostgreSQL
```

### 4. 组合类型和重要程度

```bash
# 查找重要决策
python search.py ~/Obsidian/Vault "" --type 决策 --importance 4

# 查找学习笔记
python search.py ~/Obsidian/Vault "" --type 学习笔记
```

---

## 过滤器实现

### 在脚本中使用

```python
def apply_filters(results, filters):
    filtered_results = []

    for record in results:
        include = True

        # 日期过滤
        if "date" in filters:
            record_date = record.frontmatter.get("date", "")
            if record_date != filters["date"]:
                include = False

        # 类型过滤
        if "type" in filters and include:
            record_type = record.frontmatter.get("type", "")
            if record_type != filters["type"]:
                include = False

        # 重要程度过滤
        if "importance" in filters and include:
            record_importance = record.frontmatter.get("importance", 0)
            if record_importance < filters["importance"]:
                include = False

        # 状态过滤
        if "status" in filters and include:
            record_status = record.frontmatter.get("status", "")
            if record_status != filters["status"]:
                include = False

        # 项目过滤
        if "project" in filters and include:
            record_project = record.frontmatter.get("project", "")
            if record_project != filters["project"]:
                include = False

        if include:
            filtered_results.append(record)

    return filtered_results
```

---

## 性能考虑

### 过滤器顺序

1. **先过滤，后搜索**（推荐）
```python
# 先缩小数据范围
filtered_database = [r for r in database if r.type == "决策"]
# 再在缩小后的范围内搜索
results = search(query, filtered_database)
```

2. **先搜索，后过滤**（灵活但慢）
```python
# 先搜索整个数据库
all_results = search(query, database)
# 再应用过滤器
results = apply_filters(all_results, filters)
```

### 过滤器优化

```python
# 使用索引加速
if "type" in filters:
    if filters["type"] in type_index:
        filtered = type_index[filters["type"]]
    else:
        filtered = []

# 使用缓存
if filters in filter_cache:
    return filter_cache[filters]
```

---

## 常见使用场景

### 场景 1: 查找本周重要决策

```bash
python hybrid_search.py ~/Obsidian/Vault "" \
  --this-week \
  --type 决策 \
  --importance 4
```

### 场景 2: 查找某项目的所有记录

```bash
python search.py ~/Obsidian/Vault "" \
  --project "Acme Dashboard"
```

### 场景 3: 查找今天的待办任务

```bash
python search.py ~/Obsidian/Vault 任务 \
  --today \
  --status 进行中
```

### 场景 4: 查找特定日期的所有记录

```bash
python search.py ~/Obsidian/Vault "" \
  --date 2026-02-02
```

### 场景 5: 查找重要的技术决策

```bash
python hybrid_search.py ~/Obsidian/Vault "技术决策" \
  --type 决策 \
  --importance 4
```
