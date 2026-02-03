---
name: obsidian-bases-memory
description: Obsidian Bases 记忆数据库核心架构初始化工具 - 专注于创建标准化的数据存储结构。仅生成 'memory/' 文件夹、'MEMORY.md' 长期记忆文件和 '记忆数据库.base' 配置文件。不包含任何具体的记录或检索逻辑，这些功能完全委托给 Recorder 和 Retriever 技能。
---

# Obsidian Bases 记忆数据库核心架构

## 概述

这个 skill 是记忆系统的**基础设施层**。它不负责具体的业务逻辑（如怎么写日记、怎么搜内容），只负责在你的 Obsidian 库中“铺路”——建立标准化的数据结构，让其他高级技能有地放矢。

**核心职责**:
- 建立 `memory/` 数据目录
- 初始化 `MEMORY.md` 长期记忆入口
- 部署 `记忆数据库.base` 数据库 Schema

## 快速开始

在 Obsidian 笔记库根目录执行：

```bash
python scripts/init_memory_system.py <笔记库路径>
```

这将生成以下纯净的结构：

```
[你的 Obsidian 库]/
├── 记忆数据库.base       # 数据库 Schema 定义 (Single Source of Truth)
├── MEMORY.md           # 长期记忆入口文件
└── memory/             # 空文件夹，用于存放 Recorder 生成的日志
```

## 职责边界

为了保持系统的模块化和低耦合，本技能严格遵守以下边界：

- **❌ 不做**: 创建 `scripts/`、`config/` 或 `templates/` 等逻辑目录。
- **❌ 不做**: 提供写文件的 Python 脚本（这是 **Recorder** 的工作）。
- **❌ 不做**: 提供搜索或索引功能（这是 **Retriever** 的工作）。
- **✅ 只做**: 确保数据存放在正确的位置，并且数据库能正确读取这些数据。

## 配合其他技能使用

本技能只负责“建房子”，而“装修”和“入住”需要配合以下技能：

1.  **obsidian-memory-recorder**:
    *   负责向 `memory/` 目录写入每日日志。
    *   负责读取 `记忆数据库.base` 中的字段定义来生成正确的 Frontmatter。

2.  **obsidian-memory-retriever**:
    *   负责读取 `memory/` 和 `MEMORY.md` 中的内容。
    *   负责建立索引并提供语义搜索。

## 资产文件

- **[assets/config/记忆数据库.base](assets/config/记忆数据库.base)**: 
  这是整个系统的核心 Schema。Recorder 依据它来决定记录什么字段，Retriever 依据它来决定检索什么字段。
