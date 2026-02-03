---
title: "记忆数据库配置文件"
created: "2026-02-02"
tags: [Obsidian, Bases, 配置, 记忆系统]
---

# Obsidian Bases 记忆数据库配置指南

## 配置文件结构

Obsidian Bases 使用 `.base` 文件格式来定义数据库结构。下面是一个完整的记忆数据库配置示例。

---

## 完整配置文件示例

### 文件名：`记忆数据库.base`

```yaml
version: 1
id: "记忆数据库-uuid-001"
name: "记忆数据库"
description: "基于 CLAWDBOT 架构的个人记忆系统，管理每日日志和长期记忆"
source: "笔记根目录"
icon: "🧠"
defaultView: "按时间线"

tags:
  include: ["#记忆", "#daily-log", "#长期记忆"]
  exclude: ["#归档", "#删除"]

views:
  - id: "cards-view"
    name: "卡片视图"
    type: "cards"
    icon: "🖼️"
    order:
      - "标题"
      - "类型"
      - "摘要"
      - "tags"
      - "重要程度"
    limit: 20

  - id: "timeline-view"
    name: "按时间线"
    type: "table"
    icon: "📅"
    order:
      - "日期"
      - "时间"
      - "类型"
      - "标题"
      - "tags"
      - "重要程度"
      - "相关项目"
      - "状态"
      - "最后更新"
    limit: 20

  - id: "by-type-view"
    name: "按类型"
    type: "table"
    icon: "📂"
    order:
      - "类型"
      - "标题"
      - "日期"
      - "重要程度"
      - "相关项目"
      - "tags"
      - "状态"
    groupBy:
      property: "类型"
      direction: "ASC"
    limit: 50

  - id: "important-view"
    name: "重要事项"
    type: "table"
    icon: "⭐"
    order:
      - "重要程度"
      - "标题"
      - "类型"
      - "日期"
      - "相关项目"
      - "状态"
    groupBy:
      property: "重要程度"
      direction: "DESC"
    filters:
      and:
        - "重要程度 >= 3"
    limit: 20

  - id: "by-project-view"
    name: "按项目"
    type: "table"
    icon: "🚀"
    order:
      - "相关项目"
      - "标题"
      - "类型"
      - "日期"
      - "状态"
      - "重要程度"
    groupBy:
      property: "相关项目"
      direction: "ASC"
    filters:
      and:
        - "相关项目 != ''"
    limit: 50

properties:
  日期:
    displayName: "日期"
    type: "date"
    format: "YYYY-MM-DD"
  
  时间:
    displayName: "时间"
    type: "text"
  
  类型:
    displayName: "类型"
    type: "select"
    options:
      - value: "每日日志"
        color: "#3498db"
        icon: "📝"
      - value: "长期记忆"
        color: "#9b59b6"
        icon: "🧠"
      - value: "决策"
        color: "#e74c3c"
        icon: "✅"
      - value: "任务"
        color: "#f39c12"
        icon: "📋"
      - value: "学习笔记"
        color: "#2ecc71"
        icon: "📚"
      - value: "会议记录"
        color: "#1abc9c"
        icon: "💬"
      - value: "对话记录"
        color: "#34495e"
        icon: "🗨️"
      - value: "摘要"
        color: "#8e44ad"
        icon: "📝"
      - value: "用户偏好"
        color: "#e91e63"
        icon: "👤"
  
  标题:
    displayName: "标题"
    type: "text"
  
  内容:
    displayName: "内容"
    type: "text"
  
  tags:
    displayName: "标签"
    type: "multiselect"
  
  重要程度:
    displayName: "重要程度"
    type: "number"
    max: 5
  
  相关项目:
    displayName: "相关项目"
    type: "text"
  
  状态:
    displayName: "状态"
    type: "select"
    options:
      - value: "进行中"
        color: "#3498db"
        icon: "🔄"
      - value: "已完成"
        color: "#2ecc71"
        icon: "✅"
      - value: "暂停"
        color: "#f39c12"
        icon: "⏸️"
      - value: "已归档"
        color: "#95a5a6"
        icon: "📦"
  
  最后更新:
    displayName: "最后更新"
    type: "date"
  
  参与者:
    displayName: "参与者"
    type: "multiselect"
  
  摘要:
    displayName: "摘要"
    type: "text"

quickFilters:
  - id: "today"
    name: "今天"
    filter:
      column: "日期"
      operator: "="
      value: "TODAY()"
  - id: "this-week"
    name: "本周"
    filter:
      column: "日期"
      operator: ">="
      value: "THIS_WEEK_START()"
  - id: "this-month"
    name: "本月"
    filter:
      column: "日期"
      operator: ">="
      value: "THIS_MONTH_START()"
  - id: "pending"
    name: "待处理"
    filter:
      column: "状态"
      operator: "="
      value: "进行中"
  - id: "important"
    name: "高优先级"
    filter:
      column: "重要程度"
      operator: ">="
      value: 4

settings:
  autoSave: true
  autoIndex: true
  watchFiles: true
  indexDebounce: 1500
  enableSearchHighlight: true
  enableContextMenu: true
  defaultPageSize: 20
  showRowNumbers: true
  enableCompactMode: false
```

---

## 配置详解

### 1. 元数据部分

```yaml
version: 1                          # 配置文件版本
id: "记忆数据库-uuid-001"           # 唯一标识符
name: "记忆数据库"                  # 数据库显示名称
description: "基于 CLAWDBOT 架构的个人记忆系统"
source: "笔记根目录"                # 数据源路径
icon: "🧠"                          # 数据库图标
defaultView: "按时间线"             # 默认视图
```

### 2. 标签过滤

```yaml
tags:
  include: ["#记忆", "#daily-log", "#长期记忆"]
  exclude: ["#归档", "#删除"]
```

### 3. 视图配置

#### 3.1 表格视图

```yaml
- id: "timeline-view"
  name: "按时间线"
  type: "table"
  icon: "📅"
  order:
    - "日期"
    - "时间"
    - "类型"
    - "标题"
    - "tags"
    - "重要程度"
    - "相关项目"
    - "状态"
    - "最后更新"
  limit: 20
```

#### 3.2 分组视图

```yaml
- id: "by-type-view"
  name: "按类型"
  type: "table"
  groupBy:
    property: "类型"
    direction: "ASC"
  order:
    - "类型"
    - "重要程度"
```

#### 3.3 过滤视图

```yaml
- id: "important-view"
  name: "重要事项"
  filters:
    and:
      - "重要程度 >= 3"
```

### 4. 列配置（Properties）

```yaml
properties:
  日期:
    displayName: "日期"
    type: "date"
    format: "YYYY-MM-DD"
  
  类型:
    displayName: "类型"
    type: "select"
    options:
      - value: "每日日志"
        color: "#3498db"
        icon: "📝"
```

**注意**：`tags` 字段建议保持英文键名，以确保与 Obsidian 系统标签功能的兼容性。

### 5. 笔记模板示例

#### 每日日志模板

```markdown
---
日期: {{date}}
时间: "{{time}}"
类型: "每日日志"
标题: "{{title}}"
tags: ["#daily-log"]
重要程度: 3
相关项目: ""
状态: "进行中"
---
```

#### 长期记忆模板

```markdown
---
日期: {{date}}
类型: "长期记忆"
标题: "{{title}}"
tags: ["#长期记忆"]
重要程度: 5
相关项目: ""
状态: "已归档"
---
```
