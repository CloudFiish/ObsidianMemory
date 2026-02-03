#!/usr/bin/env python3
"""
快捷记录决策脚本

专门用于快速记录决策类型的信息
"""

import sys
from datetime import datetime
from pathlib import Path
try:
    from sync_utils import sync_to_core_memory
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from sync_utils import sync_to_core_memory


def create_decision_record(vault_path, decision_content, importance=None, project=None):
    """
    创建决策记录

    Args:
        vault_path: 笔记库路径
        decision_content: 决策内容
        importance: 重要程度（可选）
        project: 相关项目（可选）

    Returns:
        创建的文件路径
    """
    vault = Path(vault_path)
    memory_folder = vault / "memory"

    if not memory_folder.exists():
        print("❌ 错误: memory 文件夹不存在")
        print("请先使用 obsidian-bases-memory skill 初始化系统")
        sys.exit(1)

    # 生成标题
    title = f"决策 - {decision_content[:30]}"

    # 生成文件名
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    filename = f"{date_str}.md"
    filepath = memory_folder / filename

    # 设置字段
    tags = ["#技术", "#决策", "#重要"]
    record_type = "决策"
    importance = importance or 4  # 决策默认为 4 星
    status = "已完成"
    project = project or ""

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
    content = f"""

## {time_str} - {title}

### 决策
{decision_content}

### 理由
<% 请填写决策理由 %>

### 影响
<% 请填写决策影响 %>

### 下一步
- [ ] <% 待办事项 1 %>
- [ ] <% 待办事项 2 %>

---
"""

    # 检查是否已存在
    if filepath.exists():
        # 读取现有内容
        existing_content = filepath.read_text(encoding="utf-8")

        # 追加新记录
        new_content = existing_content + content
        filepath.write_text(new_content, encoding="utf-8")
        print(f"⚠️  已追加到现有文件: {filename}")
    else:
        # 创建新文件
        header = f"# {date_str}\n"
        new_content = frontmatter + header + content
        filepath.write_text(new_content, encoding="utf-8")
        print(f"✓ 已创建新文件: {filename}")

    # 同步到 MEMORY.md
    sync_to_core_memory(vault_path, "决策", title, decision_content, date_str, filename)

    return filepath


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python record_decision.py <笔记库路径> <决策内容> [重要程度] [项目]")
        print("示例:")
        print("  python record_decision.py ~/Obsidian/Vault \"使用 PostgreSQL 作为数据库\"")
        print("  python record_decision.py ~/Obsidian/Vault \"使用 REST API\" 5 \"Acme Dashboard\"")
        sys.exit(1)

    vault_path = sys.argv[1]
    decision_content = sys.argv[2]
    importance = int(sys.argv[3]) if len(sys.argv) > 3 else None
    project = sys.argv[4] if len(sys.argv) > 4 else None

    # 验证重要程度
    if importance is not None and (importance < 1 or importance > 5):
        print("❌ 错误: 重要程度必须是 1-5 的整数")
        sys.exit(1)

    # 创建记录
    filepath = create_decision_record(vault_path, decision_content, importance, project)

    stars = "⭐" * (importance or 4)
    print(f"\n✓ 决策已成功记录")
    print(f"📁 文件: {filepath}")
    print(f"📝 决策: {decision_content}")
    print(f"⭐ 重要程度: {stars}")
    if project:
        print(f"🔗 项目: {project}")
    print(f"\n查看记录: [[{filepath.name}]]")
