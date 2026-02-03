# 模板使用指南

## 模板文件说明

### 1. 每日日志模板

**文件位置**: `assets/templates/daily_log_template.md`

**用途**: 记录当天的活动、决策、学习笔记等。

**字段说明**:
- `date`: 记录日期（YYYY-MM-DD 格式）
- `time`: 记录时间（HH:MM 格式）
- `type`: 固定为"每日日志"
- `title`: 记录标题
- `tags`: 相关标签（多选）
- `importance`: 重要程度（1-5 星）
- `project`: 相关项目（可选）
- `status`: 当前状态
- `updated`: 最后更新时间

**使用场景**:
- 记录每日工作会议
- 记录技术讨论
- 记录学习笔记
- 记录灵感想法
- 记录待办事项

**示例**:
```markdown
---
date: 2026-02-02
time: "14:30"
type: "每日日志"
title: "API 设计讨论"
tags: ["#技术", "#决策", "#项目-A"]
importance: 5
project: "Acme Dashboard"
status: "已完成"
updated: 2026-02-02 14:30
---

## 14:30 - API 设计讨论

### 背景
需要设计用户认证 API。

### 决策
选择 JWT 认证方案。

### 原因
- 无状态，易于扩展
- 标准化方案
- 支持跨域请求

### 下一步
[ ] 实现 token 生成逻辑
[ ] 实现 token 验证中间件
```

### 2. 长期记忆模板

**文件位置**: `assets/templates/long_term_memory_template.md`

**用途**: 存储重要的决策、用户偏好、长期知识等。

**字段说明**:
- `date`: 创建日期
- `type`: 固定为"长期记忆"
- `title`: 记忆类别标题
- `tags`: 分类标签
- `importance**: 通常为 4-5 星
- `project`: 通常为空
- `status**: 固定为"已归档"

**使用场景**:
- 重要决策记录
- 用户偏好和习惯
- 技术选型决策
- 项目里程碑
- 重要的学到的教训

**示例**:
```markdown
---
date: 2026-01-15
type: "长期记忆"
title: "技术栈决策"
tags: ["#长期记忆", "#技术", "#决策"]
importance: 5
project: ""
status: "已归档"
---

# 技术栈决策

## 数据库选择

### 决策: PostgreSQL
**日期**: 2026-01-15
**理由**:
- ACID 特性保证数据一致性
- 优秀的 JSON 支持
- 成熟的生态系统

**影响**: 所有后端服务

## API 风格选择

### 决策: REST API
**日期**: 2026-01-20
**理由**:
- 实现简单
- 更好的缓存支持
- 团队更熟悉

**影响**: 前后端接口设计
```

## 创建模板的脚本

### 使用 init_memory_system.py

```bash
python scripts/init_memory_system.py <笔记库路径>
```

这将创建:
- MEMORY.md（长期记忆文件）
- memory/ 文件夹
- 今日每日日志

### 使用 create_daily_log.py

```bash
python scripts/create_daily_log.py <笔记库路径> [标题]
```

示例:
```bash
python scripts/create_daily_log.py ~/Obsidian/Vault "API 设计讨论"
```

## Templater 集成

如果使用 Templater 插件，可以创建自动化模板：

### 每日日志命令

创建文件 `templates/Daily Log Template.md`:

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
time: "<% tp.date.now("HH:mm") %>"
type: "每日日志"
title: "<% await tp.system.prompt('请输入标题') %>"
tags: ["#daily-log"]
importance: 3
project: ""
status: "进行中"
updated: <% tp.date.now("YYYY-MM-DD HH:mm") %>
---

# <% tp.date.now("YYYY-MM-DD") %>

## <% tp.date.now("HH:mm") %> - <% await tp.system.prompt('标题') %>

<% tp.file.cursor() %>
```

### Templater 配置

在 Obsidian 设置中添加命令:

```javascript
{
  "name": "创建每日日志",
  "template_file": "templates/Daily Log Template.md",
  "file_name_format": "memory/{{date}}.md"
}
```

## Dataview 查询

### 查询今天的记录

```dataview
TABLE
  time as "时间",
  title as "标题",
  type as "类型",
  importance as "重要程度",
  status as "状态"
FROM #daily-log
WHERE date = date(today)
SORT date DESC, time DESC
```

### 查询重要事项

```dataview
TABLE
  title as "标题",
  type as "类型",
  date as "日期",
  project as "相关项目"
FROM #daily-log OR #长期记忆
WHERE importance >= 4
SORT importance DESC, date DESC
```

### 按项目统计

```dataview
TABLE
  rows.title AS "记录数"
FROM #daily-log
WHERE project != ""
GROUP BY project
SORT rows.title DESC
```

## 最佳实践

### 1. 命名规范
- 每日日志: `YYYY-MM-DD.md`
- 长期记忆: `MEMORY.md`
- 模板文件: `*_template.md`

### 2. 标签使用
- 使用层次化标签: `#技术/API`, `#项目-A/前端`
- 避免过多标签（3-5 个最佳）
- 保持标签一致性

### 3. 重要程度
- 5 星: 紧急重要，需要立即处理
- 4 星: 重要，但不是紧急
- 3 星: 中等优先级
- 2 星: 较低优先级
- 1 星: 极低优先级

### 4. 定期整理
- 每周回顾重要事项
- 将重要决策升级为长期记忆
- 归档已完成的任务
- 清理过期的临时记录

### 5. 项目关联
- 始终填写相关项目字段
- 使用统一的项目名称
- 便于按项目视图查看所有相关记录

## 常见问题

### Q: 如何修改模板?
A: 直接编辑 `assets/templates/` 目录下的模板文件，或者使用 Obsidian 的模板编辑器。

### Q: 可以添加自定义字段吗?
A: 可以，在配置文件中添加新的列定义，然后在模板中添加对应的 YAML 字段。

### Q: 如何批量更新记录?
A: 可以使用 Dataview 批量查询，或者编写脚本批量修改 YAML 字段。

### Q: 模板支持变量吗?
A: 支持，使用 Templater 或其他模板插件可以添加变量和动态内容。
