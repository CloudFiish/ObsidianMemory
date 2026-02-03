# Obsidian Bases 配置 Schema

## 配置文件结构

Obsidian Bases 使用 JSON 格式的配置文件（.base 扩展名）。

### 根级字段

```json
{
  "version": 1,                    // 配置版本
  "id": "unique-id",              // 唯一标识符
  "name": "数据库名称",            // 显示名称
  "description": "描述",            // 数据库描述
  "source": "路径",                // 数据源路径
  "icon": "🧠",                   // 图标
  "defaultView": "默认视图ID"       // 默认视图
}
```

### Tags 配置

```json
{
  "tags": {
    "include": ["#tag1", "#tag2"],  // 包含的标签
    "exclude": ["#excluded"]          // 排除的标签
  }
}
```

### Views 配置

每个视图包含以下字段：

```json
{
  "id": "view-id",          // 唯一标识符
  "name": "视图名称",        // 显示名称
  "type": "table",          // 视图类型: table, summary, kanban, calendar
  "icon": "📅",            // 图标
  "columns": ["列1", "列2"], // 显示的列
  "groupBy": "分组列",      // 分组列 (null = 不分组)
  "sortBy": [              // 排序规则
    {"column": "日期", "direction": "DESC"}
  ],
  "filters": [             // 过滤器
    {"column": "状态", "operator": "=", "value": "进行中"}
  ],
  "pageSize": 20          // 每页行数
}
```

### 列类型

#### Date 类型

```json
{
  "id": "date",
  "name": "日期",
  "type": "date",
  "path": "date",
  "format": "YYYY-MM-DD",    // 日期格式
  "required": true,
  "sortable": true,
  "filterable": true,
  "groupable": true
}
```

#### Select 类型

```json
{
  "id": "type",
  "name": "类型",
  "type": "select",
  "path": "type",
  "options": [
    {"value": "选项1", "color": "#3498db", "icon": "📝"},
    {"value": "选项2", "color": "#e74c3c", "icon": "✅"}
  ]
}
```

#### Rating 类型

```json
{
  "id": "importance",
  "name": "重要程度",
  "type": "rating",
  "path": "importance",
  "max": 5,                // 最大评分
  "emoji": "⭐",           // 评分图标
  "default": 3              // 默认值
}
```

#### Multiselect 类型

```json
{
  "id": "tags",
  "name": "标签",
  "type": "multiselect",
  "path": "tags",
  "options": [
    {"value": "#tag1", "color": "#3498db"},
    {"value": "#tag2", "color": "#e74c3c"}
  ]
}
```

#### Actions 类型

```json
{
  "id": "actions",
  "name": "操作",
  "type": "actions",
  "actions": [
    {"label": "查看", "type": "open", "icon": "📖"},
    {"label": "编辑", "type": "edit", "icon": "✏️"},
    {"label": "删除", "type": "delete", "icon": "🗑️"}
  ]
}
```

### 过滤器操作符

| 操作符 | 说明 | 示例 |
|--------|------|------|
| `=` | 等于 | `{"column": "状态", "operator": "=", "value": "进行中"}` |
| `!=` | 不等于 | `{"column": "状态", "operator": "!=", "value": "已归档"}` |
| `>` | 大于 | `{"column": "重要程度", "operator": ">", "value": 3}` |
| `>=` | 大于等于 | `{"column": "重要程度", "operator": ">=", "value": 4}` |
| `<` | 小于 | `{"column": "日期", "operator": "<", "value": "2026-01-01"}` |
| `<=` | 小于等于 | `{"column": "日期", "operator": "<=", "value": "2026-12-31"}` |
| `contains` | 包含 | `{"column": "标题", "operator": "contains", "value": "API"}` |
| `starts_with` | 开头是 | `{"column": "标签", "operator": "starts_with", "value": "#技术"}` |
| `ends_with` | 结尾是 | `{"column": "文件名", "operator": "ends_with", "value": ".md"}` |
| `is_empty` | 为空 | `{"column": "相关项目", "operator": "is_empty", "value": true}` |
| `is_not_empty` | 不为空 | `{"column": "相关项目", "operator": "is_not_empty", "value": true}` |

### 快速过滤函数

```json
{
  "quickFilters": [
    {
      "id": "today",
      "name": "今天",
      "filter": {
        "column": "日期",
        "operator": "=",
        "value": "TODAY()"           // 今天
      }
    },
    {
      "id": "this-week",
      "name": "本周",
      "filter": {
        "column": "日期",
        "operator": ">=",
        "value": "THIS_WEEK_START()"  // 本周开始
      }
    },
    {
      "id": "this-month",
      "name": "本月",
      "filter": {
        "column": "日期",
        "operator": ">=",
        "value": "THIS_MONTH_START()" // 本月开始
      }
    }
  ]
}
```

### 全局设置

```json
{
  "settings": {
    "autoSave": true,                // 自动保存
    "autoIndex": true,               // 自动索引
    "watchFiles": true,              // 监视文件变化
    "indexDebounce": 1500,           // 索引入口延迟（毫秒）
    "enableSearchHighlight": true,    // 启用搜索高亮
    "enableContextMenu": true,         // 启用右键菜单
    "defaultPageSize": 20,           // 默认每页行数
    "showRowNumbers": true,           // 显示行号
    "enableCompactMode": false        // 启用紧凑模式
  }
}
```

## 完整示例

参见 [assets/config/记忆数据库.base](../assets/config/记忆数据库.base) 获取完整配置示例。
