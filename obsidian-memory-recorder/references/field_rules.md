# 字段自动填充规则

## 标题生成

### 决策类
```python
def generate_decision_title(content):
    # 提取决策对象
    match = re.search(r'(选择|决定|使用|采用|确定)\s*([^，。！？\n]+)', content)
    if match:
        object = match.group(1).strip()
        return f"决策 - {object}"
    return content[:50]
```

**示例**:
```
输入: "我们决定使用 PostgreSQL 作为数据库"
输出: "决策 - PostgreSQL"

输入: "选择了 REST API"
输出: "决策 - REST API"
```

### 会议类
```python
def generate_meeting_title(participants, topic):
    return f"会议 - {topic} ({participants})"
```

**示例**:
```
输入: 参与者: Alice, Bob; 主题: API 设计
输出: "会议 - API 设计 (Alice, Bob)"
```

### 默认
```python
def generate_default_title(content):
    return content[:50]  # 前 50 个字符
```

## 标签推断

### 关键词映射
```python
KEYWORD_MAPPINGS = {
    "数据库": ["#技术", "#数据库"],
    "API": ["#技术", "#API"],
    "决策": ["#技术", "#决策"],
    "决定": ["#技术", "#决策"],
    "选择": ["#技术", "#决策"],
    "会议": ["#会议"],
    "学习": ["#学习"],
    "重要": ["#重要"],
    "紧急": ["#重要"],
    "技术": ["#技术"],
    "前端": ["#技术", "#前端"],
    "后端": ["#技术", "#后端"]
}
```

### 推断逻辑
```python
def infer_tags(content):
    tags = set(["#daily-log"])  # 默认标签

    for keyword, tag_list in KEYWORD_MAPPINGS.items():
        if keyword in content:
            for tag in tag_list:
                tags.add(tag)

    return list(tags)
```

**示例**:
```
输入: "我们决定使用 PostgreSQL 作为数据库"
输出: ["#daily-log", "#技术", "#决策", "#数据库"]

输入: "学习 React 框架"
输出: ["#daily-log", "#学习", "#技术", "#前端"]
```

## 重要程度规则

### 优先级映射
```python
IMPORTANCE_RULES = {
    "决策": 4,
    "决定": 4,
    "选择": 4,
    "重要": 5,
    "紧急": 5,
    "完成": 3,
    "讨论": 3,
    "学习": 3,
    "默认": 3
}
```

### 推断逻辑
```python
def infer_importance(content):
    for keyword, importance in IMPORTANCE_RULES.items():
        if keyword in content:
            return importance
    return IMPORTANCE_RULES["默认"]
```

**示例**:
```
输入: "重要的决策：使用 PostgreSQL"
输出: 5  # 因为包含"重要"和"决策"

输入: "学习 React"
输出: 3  # 学习类的默认值
```

### 重要性级别
| 星级 | 含义 | 使用场景 |
|------|------|----------|
| ⭐⭐⭐⭐ | 5 | 紧急重要、关键决策 |
| ⭐⭐⭐ | 4 | 重要、主要决策 |
| ⭐⭐ | 3 | 中等、常规记录 |
| ⭐ | 2 | 较低、次要内容 |
| ⭐ | 1 | 极低、临时记录 |

## 类型推断

### 类型映射
```python
TYPE_MAPPINGS = {
    "决定": "决策",
    "决策": "决策",
    "选择": "决策",
    "会议": "会议记录",
    "学习": "学习笔记",
    "记录": "每日日志",
    "默认": "每日日志"
}
```

### 推断逻辑
```python
def infer_type(content):
    for keyword, type_name in TYPE_MAPPINGS.items():
        if keyword in content:
            return type_name
    return TYPE_MAPPINGS["默认"]
```

**示例**:
```
输入: "决定使用 PostgreSQL"
输出: "决策"

输入: "学习了 React"
输出: "学习笔记"

输入: "记录今天的会议"
输出: "会议记录"
```

### 类型选项
| 类型 | 说明 | 默认重要程度 |
|------|------|--------------|
| 每日日志 | 日常活动记录 | 3 |
| 决策 | 重要决策记录 | 4 |
| 任务 | 待办事项 | 3 |
| 学习笔记 | 学习内容 | 3 |
| 会议记录 | 会议内容 | 3 |
| 用户偏好 | 个人偏好和习惯 | 5 |

## 日期和时间

### 自动填充
```python
from datetime import datetime

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")  # 2026-02-02
time_str = now.strftime("%H:%M")      # 14:30
datetime_str = now.strftime("%Y-%m-%d %H:%M")  # 2026-02-02 14:30
```

## 状态默认值

### 状态规则
```python
STATUS_DEFAULTS = {
    "决策": "已完成",
    "任务": "进行中",
    "学习笔记": "进行中",
    "会议记录": "已完成",
    "用户偏好": "已归档"
}
```

### 推断逻辑
```python
def infer_status(record_type):
    return STATUS_DEFAULTS.get(record_type, "进行中")
```

## 内容格式化

### 结构化内容
```python
def format_content(title, content):
    return f"""

## {time} - {title}

{content}

---
"""
```

### 决策类内容
```python
def format_decision_content(title, content):
    return f"""

## {time} - {title}

### 决策
{content}

### 理由
<% 请填写决策理由 %>

### 影响
<% 请填写决策影响 %>

### 下一步
- [ ] <% 待办事项 1 %>
- [ ] <% 待办事项 2 %>

---
"""
```

### 会议类内容
```python
def format_meeting_content(title, participants):
    return f"""

## {time} - {title}

### 参与者
{participants}

### 讨论内容
<% 请填写讨论内容 %>

### 行动项
- [ ] <% 行动项 1 %>
- [ ] <% 行动项 2 %>

---
"""
```
