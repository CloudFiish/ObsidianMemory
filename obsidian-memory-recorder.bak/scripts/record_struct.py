#!/usr/bin/env python3
"""
结构化记录脚本

用户提供完整的结构化数据，创建标准化记录
"""

import sys
from datetime import datetime
from pathlib import Path
try:
    from sync_utils import sync_to_core_memory
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from sync_utils import sync_to_core_memory


def validate_fields(fields):
    """
    验证必填字段

    Args:
        fields: 字段字典

    Returns:
        (是否有效, 错误消息)
    """
    required = ["title", "type"]

    for field in required:
        if not fields.get(field):
            return False, f"缺少必填字段: {field}"

    # 验证重要程度
    if "importance" in fields:
        importance = fields["importance"]
        if isinstance(importance, str) and importance.isdigit():
            fields["importance"] = int(importance)
        if not isinstance(importance, int) or not 1 <= importance <= 5:
            return False, "重要程度必须是 1-5 的整数"

    # 验证类型
    valid_types = ["每日日志", "决策", "任务", "学习笔记", "会议记录", "用户偏好"]
    if "type" in fields and fields["type"] not in valid_types:
        return False, f"无效的类型: {fields['type']}"

    # 验证状态
    valid_statuses = ["进行中", "已完成", "暂停", "已归档"]
    if "status" in fields and fields["status"] not in valid_statuses:
        return False, f"无效的状态: {fields['status']}"

    return True, ""


def create_structured_record(vault_path, fields):
    """
    创建结构化记录

    Args:
        vault_path: 笔记库路径
        fields: 字段字典

    Returns:
        创建的文件路径
    """
    vault = Path(vault_path)
    memory_folder = vault / "memory"

    if not memory_folder.exists():
        print("❌ 错误: memory 文件夹不存在")
        print("请先使用 obsidian-bases-memory skill 初始化系统")
        sys.exit(1)

    # 获取字段
    title = fields.get("title", "")
    record_type = fields.get("type", "每日日志")
    content = fields.get("content", "")
    tags = fields.get("tags", ["#daily-log"])
    importance = fields.get("importance", 3)
    project = fields.get("project", "")
    status = fields.get("status", "进行中")

    # 生成文件名
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    filename = f"{date_str}.md"
    filepath = memory_folder / filename

    # 生成 frontmatter
    frontmatter = f"""---
date: {date_str}
time: "{time_str}"
type: "{record_type}"
title: "{title}"
tags: {tags}
importance: {importance}
project: "{project}"
status: "{status}"
updated: {date_str} {time_str}
---
"""

    # 构建内容
    section = f"""

## {time_str} - {title}

{content}

---
"""

    # 检查是否已存在
    if filepath.exists():
        # 读取现有内容
        existing_content = filepath.read_text(encoding="utf-8")

        # 追加新记录
        new_content = existing_content + section
        filepath.write_text(new_content, encoding="utf-8")
        print(f"⚠️  已追加到现有文件: {filename}")
    else:
        # 创建新文件
        header = f"# {date_str}\n"
        new_content = frontmatter + header + section
        filepath.write_text(new_content, encoding="utf-8")
        print(f"✓ 已创建新文件: {filename}")

    # 同步到 MEMORY.md
    if record_type in ["用户偏好", "决策"]:
        sync_to_core_memory(vault_path, record_type, title, content, date_str, filename)

    return filepath


def interactive_input():
    """
    交互式输入字段

    Returns:
        字段字典
    """
    print("\n" + "="*60)
    print("📝 创建结构化记录")
    print("="*60 + "\n")

    fields = {}

    # 标题（必填）
    while True:
        title = input("标题*: ").strip()
        if title:
            fields["title"] = title
            break
        print("❌ 标题不能为空")

    # 类型（必填）
    print("\n类型选项:")
    print("  1. 每日日志")
    print("  2. 决策")
    print("  3. 任务")
    print("  4. 学习笔记")
    print("  5. 会议记录")
    print("  6. 用户偏好")

    type_map = {
        "1": "每日日志",
        "2": "决策",
        "3": "任务",
        "4": "学习笔记",
        "5": "会议记录",
        "6": "用户偏好"
    }

    while True:
        type_choice = input("类型*: [1-6] ").strip()
        if type_choice in type_map:
            fields["type"] = type_map[type_choice]
            break
        print("❌ 无效选择")

    # 内容（必填）
    while True:
        content = input("\n内容*: ").strip()
        if content:
            fields["content"] = content
            break
        print("❌ 内容不能为空")

    # 标签（可选）
    tags_input = input("\n标签 (空格分隔，如 #技术 #决策): ").strip()
    if tags_input:
        fields["tags"] = tags_input.split()
    else:
        fields["tags"] = ["#daily-log"]

    # 重要程度（可选）
    while True:
        importance_input = input("重要程度 (1-5) [默认: 3]: ").strip()
        if not importance_input:
            fields["importance"] = 3
            break
        if importance_input.isdigit() and 1 <= int(importance_input) <= 5:
            fields["importance"] = int(importance_input)
            break
        print("❌ 请输入 1-5 的数字")

    # 相关项目（可选）
    fields["project"] = input("\n相关项目 (可选): ").strip()

    # 状态（可选）
    print("\n状态选项:")
    print("  1. 进行中")
    print("  2. 已完成")
    print("  3. 暂停")
    print("  4. 已归档")

    status_map = {
        "1": "进行中",
        "2": "已完成",
        "3": "暂停",
        "4": "已归档"
    }

    status_choice = input("状态 [默认: 1]: ").strip()
    fields["status"] = status_map.get(status_choice, "进行中")

    return fields


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # 交互式输入
        fields = interactive_input()

        # 验证
        valid, error = validate_fields(fields)
        if not valid:
            print(f"\n❌ 验证失败: {error}")
            sys.exit(1)

        # 确认
        print("\n" + "="*60)
        print("📋 记录信息")
        print("="*60)
        for key, value in fields.items():
            stars = "⭐" * value if key == "importance" and isinstance(value, int) else value
            print(f"  {key}: {stars}")
        print("="*60)

        confirm = input("\n确认创建？[y/N]: ").strip().lower()
        if confirm != "y":
            print("❌ 已取消")
            sys.exit(0)

        # 获取笔记库路径
        vault_path = input("\n请输入 Obsidian 笔记库路径: ").strip()

        # 创建记录
        filepath = create_structured_record(vault_path, fields)

        print(f"\n✓ 记录已成功创建")
        print(f"📁 文件: {filepath}")

    else:
        print("用法: python record_struct.py --interactive")
        print("\n或者直接提供字段:")
        print("  title=标题 type=类型 content=内容 tags='#技术 #决策'")
        sys.exit(1)
