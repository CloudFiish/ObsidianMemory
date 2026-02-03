---
name: obsidian-memory-agent
description: 一个通用的 Agent 记忆 Skill，结合了 Markdown 本地存储的可读性和 Zvec 向量数据库的高性能检索。
version: 0.1.0
---

# Obsidian Memory Agent Skill

这个 Skill 为任何 AI Agent 赋予了持久化记忆能力。它遵循 "Local-First" 原则，将数据存储在本地 Markdown 文件中，同时利用 Zvec 向量数据库提供语义搜索。

## 核心特性

1.  **双层存储架构**：
    *   **Source of Truth**: Markdown 文件 (`memory/YYYY-MM-DD.md`)，人类可读，Git 友好。
    *   **Index Layer**: Zvec 嵌入式向量数据库，提供毫秒级语义检索。
2.  **通用 Agent 接口**：提供标准的 JSON Schema，支持 OpenAI/Anthropic 等 Function Calling 协议。
3.  **零依赖启动**：内置 Mock 模式，即使没有安装 Zvec 或 Embedding 模型也能跑通流程。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 在 Agent 中使用

将 `tools_schema.json` 中的定义注册给你的 Agent。当 Agent 决定调用工具时，执行 `tools.py` 中对应的函数。

#### Python 示例

```python
from obsidian_memory_agent.tools import remember_event, recall_context

# 存记忆
print(remember_event("用户喜欢使用 Python 进行数据分析", importance=5, tags=["user-preference", "python"]))

# 查记忆
print(recall_context("用户常用的编程语言"))
```

## 工具列表

### `remember_event`
记录一件事情。
- **content**: 内容文本。
- **importance**: 重要程度 (1-5)。
- **tags**: 标签列表。

### `recall_context`
回忆相关上下文。
- **query**: 查询语句。
- **top_k**: 返回条数。

### `sync_memory`
强制同步。扫描所有 Markdown 文件并重建向量索引。

## 配置

默认情况下，记忆文件存储在当前 Vault 根目录的 `memory/` 文件夹下。
你可以通过设置环境变量 `OBSIDIAN_VAULT_ROOT` 来修改存储路径。

## 架构说明

```
obsidian-memory-agent/
├── core/
│   ├── zvec_adapter.py    # Zvec 适配器 (含 Mock 实现)
│   └── markdown_manager.py # Markdown 文件操作
├── tools.py               # Agent 工具实现
├── tools_schema.json      # Agent 工具定义 (Schema)
└── SKILL.md               # 本文档
```
