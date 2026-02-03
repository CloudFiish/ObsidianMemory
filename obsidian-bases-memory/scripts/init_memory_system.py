#!/usr/bin/env python3
"""
初始化 Obsidian Bases 记忆系统 - 纯净版
仅生成核心数据结构：memory/ 文件夹、MEMORY.md 文件和 .base 配置文件
"""

import sys
from datetime import datetime
from pathlib import Path

# 内嵌 .base 配置文件内容 (作为 Single Source of Truth)
BASE_CONFIG_CONTENT = """version: 1
id: "记忆数据库-uuid-001"
name: "记忆数据库"
description: "基于 CLAWDBOT 架构的个人记忆系统，管理每日日志和长期记忆"
source: "笔记根目录"
icon: "🧠"
defaultView: "按时间线"

tags:
  include: ["#daily-log", "#长期记忆", "#记忆"]
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
"""


def create_memory_system(vault_path: str):
    """
    初始化记忆系统数据结构

    Args:
        vault_path: Obsidian 笔记库根目录
    """
    vault = Path(vault_path)

    print(f"🚀 开始初始化记忆系统数据结构...")
    print(f"📂 目标路径: {vault}")

    # 1. 创建 memory 文件夹（数据层）
    memory_folder = vault / "memory"
    memory_folder.mkdir(parents=True, exist_ok=True)
    print(f"✓ 创建文件夹: memory/ (用于存储每日日志)")

    # 2. 创建 MEMORY.md（长期记忆入口）
    memory_file = vault / "MEMORY.md"
    if not memory_file.exists():
        memory_content = """---
日期: {today}
类型: "长期记忆"
标题: "长期记忆"
参与者: []
摘要: "系统初始化"
tags: ["#长期记忆", "#核心"]
重要程度: 5
相关项目: ""
状态: "已归档"
---

# 长期记忆

## 用户偏好
- 预留位置：记录用户的工作偏好、习惯等

## 重要决策历史
### {today}: 初始化记忆系统
- 决策：使用 Obsidian Bases 作为记忆数据库
- 理由：可视化、结构化、易于搜索
- 影响：所有个人知识和决策管理
"""
        memory_file.write_text(memory_content.format(today=datetime.now().strftime("%Y-%m-%d")), encoding="utf-8")
        print(f"✓ 创建文件: MEMORY.md (长期记忆入口)")

    # 3. 创建 .base 配置文件（架构层）
    base_config_file = vault / "记忆数据库.base"
    base_config_file.write_text(BASE_CONFIG_CONTENT, encoding="utf-8")
    print(f"✓ 创建文件: 记忆数据库.base (数据库结构定义)")

    print("\n✅ 初始化完成！")
    print("现在你可以集成以下技能来增强系统：")
    print("- obsidian-memory-recorder: 用于自动化记录")
    print("- obsidian-memory-retriever: 用于智能检索")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python init_memory_system.py <笔记库路径>")
        sys.exit(1)

    vault_path = sys.argv[1]
    create_memory_system(vault_path)
