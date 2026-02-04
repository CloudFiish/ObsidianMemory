# Obsidian Memory Manager - 使用指南

## 快速开始

### 1. 初始化记忆系统

```
用户: 初始化记忆系统

AI: 检测到记忆系统尚未初始化。我可以在 D:\JF\Note\ObsidianMemory 为您初始化吗？

用户: 是的

AI: ✅ 记忆系统初始化完成！
   - 创建了 memory/ 目录
   - 创建了 MEMORY.md
   - 创建了 记忆数据库.base
   - 生成了默认配置
```

### 2. 记录信息

```
用户: 记录一下，我决定使用 Python 作为主要开发语言

AI: 检测到重要决策。是否记录到记忆系统？

用户: 是的

AI: ✅ 已记录决策到 [[memory/2026-02-04.md]]
   类型: 决策
   重要程度: ⭐⭐⭐⭐
   已同步到 MEMORY.md
```

### 3. 检索信息

```
用户: 搜索之前的技术决策

AI: 请选择搜索模式：
   [1] 关键词搜索
   [2] 语义搜索
   [3] 混合搜索 ← 推荐

用户: 3

AI: 🔍 找到 2 条相关记录：
   [1] ⭐⭐⭐⭐ 使用 Python 作为主要开发语言
       📅 2026-02-04 | 🏷️ #技术 #决策
   
   [2] ⭐⭐⭐⭐ 选择 PostgreSQL 作为数据库
       📅 2026-01-15 | 🏷️ #技术 #决策
```

## 命令参考

### 系统管理命令

| 命令 | 说明 | 示例 |
|-----|------|------|
| `/memory init` | 初始化记忆系统 | `/memory init` |
| `/memory status` | 查看系统状态 | `/memory status` |
| `/memory config show` | 显示当前配置 | `/memory config show` |
| `/memory config set` | 修改配置项 | `/memory config set vault_path "D:\\Notes"` |
| `/memory config reset` | 重置为默认配置 | `/memory config reset` |

### 记录命令

| 命令 | 说明 | 示例 |
|-----|------|------|
| `/memory record` | 交互式记录 | `/memory record` |
| `/memory decision` | 快速记录决策 | `/memory decision "选择 React"` |
| `/memory meeting` | 快速记录会议 | `/memory meeting "周会讨论"` |
| `/memory learn` | 快速记录学习 | `/memory learn "学习了 Docker"` |
| `/remember` | 快捷记录 | `/remember 今天完成了登录功能` |

### 检索命令

| 命令 | 说明 | 示例 |
|-----|------|------|
| `/memory search` | 关键词搜索 | `/memory search Python` |
| `/memory find` | 混合搜索 | `/memory find "技术决策"` |
| `/memory today` | 查看今日记录 | `/memory today` |
| `/memory this-week` | 查看本周记录 | `/memory this-week` |
| `/memory important` | 查看重要记录 | `/memory important` |
| `/recall` | 快捷检索 | `/recall "之前的讨论"` |

## 自然语言使用

### 初始化相关

- "我想开始使用记忆系统"
- "帮我设置一下记忆功能"
- "初始化 Obsidian 记忆"
- "配置记忆系统"

### 记录相关

- "记录一下这个决定"
- "保存这个信息"
- "把这个记下来"
- "写入记忆系统"
- "我决定使用 Vue.js"（自动检测）
- "我的偏好是深色主题"（自动检测）

### 检索相关

- "搜索之前的讨论"
- "查找关于 API 的记录"
- "回顾上周的决策"
- "之前说过什么关于数据库的"
- "查看本周的重要事项"

### 管理相关

- "检查记忆系统状态"
- "修改配置"
- "设置 Obsidian 路径"
- "重置配置"

## 配置管理

### 查看配置

```bash
# 查看完整配置
python scripts/config_manager.py show

# 查看特定配置项
python scripts/config_manager.py get vault_path
python scripts/config_manager.py get components.recorder.enabled
```

### 修改配置

```bash
# 设置 Obsidian 库路径
python scripts/config_manager.py set vault_path "D:\\MyNotes"

# 启用/禁用自动初始化
python scripts/config_manager.py set auto_initialize true

# 修改搜索模式
python scripts/config_manager.py set components.retriever.default_search_mode "semantic"

# 添加自动记录关键词
python scripts/config_manager.py set components.recorder.auto_record_keywords '["决定", "选择", "偏好"]'
```

### 重置配置

```bash
python scripts/config_manager.py reset
```

## 意图识别

### 支持的意图类型

1. **initialize** - 初始化系统
   - 触发词："初始化"、"设置"、"配置"、"第一次用"

2. **record** - 记录信息
   - 触发词："记录"、"保存"、"记下来"、"写入"

3. **retrieve** - 检索信息
   - 触发词："搜索"、"查找"、"检索"、"回顾"

4. **config** - 配置管理
   - 触发词："配置"、"修改"、"调整"、"更改"

5. **status** - 状态检查
   - 触发词："状态"、"检查"、"查看"、"怎么样"

### 自动记录检测

当用户陈述中包含以下词汇时，系统会建议自动记录：

- 决策类："决定"、"决策"、"选择"、"采用"、"使用"、"放弃"
- 偏好类："偏好"、"喜欢"、"习惯"
- 重要类："重要"、"关键"、"主要"
- 确认类："确定"、"选定"、"确认"、"同意"

## 工作流程示例

### 场景 1：首次使用

```
用户: 我想开始使用记忆系统

AI: [触发 manager 技能]
   1. 检测系统状态 → 未初始化
   2. 询问用户确认
   3. 执行初始化
   4. 反馈结果

AI: ✅ 记忆系统初始化完成！
   您现在可以：
   - 说"记录"来保存信息
   - 说"搜索"来查找历史记录
```

### 场景 2：日常记录

```
用户: 今天学习了 FastAPI

AI: [触发 manager 技能]
   1. 意图识别 → record
   2. 分析内容
      - 类型: 学习笔记
      - 标题: "学习 FastAPI"
      - 标签: #学习 #FastAPI
      - 重要程度: 3⭐
   3. 调用 recorder
   4. 反馈结果

AI: ✅ 已记录学习笔记到 [[memory/2026-02-04.md]]
```

### 场景 3：智能检测

```
用户: 我决定放弃使用 MongoDB，转向 PostgreSQL

AI: [触发 manager 技能]
   1. 意图识别 → unknown（无明确指令）
   2. 检测自动记录触发词 → "决定"、"放弃"、"转向"
   3. 建议自动记录

AI: 检测到重要决策。是否记录到记忆系统？

用户: 是的

AI: ✅ 已记录决策到 [[memory/2026-02-04.md]]
   类型: 决策
   重要程度: ⭐⭐⭐⭐⭐
   已同步到 MEMORY.md
```

### 场景 4：信息检索

```
用户: 搜索之前关于数据库的讨论

AI: [触发 manager 技能]
   1. 意图识别 → retrieve
   2. 询问搜索模式
   3. 执行搜索
   4. 格式化结果

AI: 🔍 找到 3 条相关记录：
   [1] ⭐⭐⭐⭐⭐ 放弃 MongoDB，转向 PostgreSQL
   [2] ⭐⭐⭐⭐ 选择 PostgreSQL 作为数据库
   [3] ⭐⭐ 学习了 MongoDB 基础
```

## 故障排查

### 系统未初始化

**现象**: 提示 "记忆系统未初始化"

**解决**:
```
用户: 初始化记忆系统
AI: [执行初始化]
```

### 配置错误

**现象**: 无法找到 Obsidian 库路径

**解决**:
```bash
python scripts/config_manager.py set vault_path "<正确路径>"
```

### 权限问题

**现象**: 无法写入文件

**解决**:
1. 检查目录权限
2. 更换 Obsidian 库路径
3. 以管理员身份运行

### 意图识别失败

**现象**: AI 无法理解用户意图

**解决**:
- 使用更明确的表达
- 使用命令格式：`/memory <操作>`
- 参考支持的意图类型

## 最佳实践

### 1. 首次使用

- 先执行初始化
- 验证配置正确
- 测试记录和检索功能

### 2. 日常记录

- 善用自动检测功能
- 及时记录重要决策
- 使用合适的标签

### 3. 定期回顾

- 使用 `/memory this-week` 回顾本周
- 使用 `/memory important` 查看重要事项
- 定期整理 MEMORY.md

### 4. 配置管理

- 保持配置更新
- 定期备份配置
- 根据使用习惯调整设置

### 5. 自然语言使用

- 不需要记忆复杂命令
- 直接描述需求
- 利用自动检测功能

## 与其他技能的关系

```
obsidian-memory-manager (调度层)
        │
        ├── 自动检测系统状态
        ├── 智能识别用户意图
        ├── 统一配置管理
        └── 协调子技能调用
        │
        ▼
┌───────┴───────┐
│               │
▼               ▼
bases-memory  recorder    retriever
(基础设施)    (记录)      (检索)
│               │           │
▼               ▼           ▼
创建目录      写入日志    搜索内容
创建文件      更新索引    返回结果
```

**注意**: 
- Manager 不替代原有技能，而是作为统一入口
- 原有技能仍可独立使用
- Manager 提供智能调度和配置管理
