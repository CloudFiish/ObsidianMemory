#!/usr/bin/env python3
"""
对话中实时记录脚本

自动提取关键信息并创建记录
"""

import sys
import re
from datetime import datetime
from pathlib import Path
try:
    from sync_utils import sync_to_core_memory
except ImportError:
    # 如果直接运行脚本失败，尝试添加当前目录到路径
    sys.path.append(str(Path(__file__).parent))
    from sync_utils import sync_to_core_memory


# 字段自动填充规则
KEYWORD_MAPPINGS = {
    "数据库": ["#技术", "#数据库"],
    "API": ["#技术", "#API"],
    "接口": ["#技术", "#API"],
    "决策": ["#技术", "#决策"],
    "决定": ["#技术", "#决策"],
    "选择": ["#技术", "#决策"],
    "会议": ["#会议"],
    "学习": ["#学习"],
    "重要": ["#重要"],
    "紧急": ["#重要"],
    "偏好": ["#用户偏好"],
    "习惯": ["#用户偏好"],
    "常用": ["#用户偏好"]
}

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

TYPE_MAPPINGS = {
    "决定": "决策",
    "决策": "决策",
    "选择": "决策",
    "会议": "会议记录",
    "学习": "学习笔记",
    "记录": "每日日志",
    "偏好": "用户偏好",
    "习惯": "用户偏好",
    "常用": "用户偏好",
    "默认": "每日日志"
}


def extract_keywords(content):
    """
    从内容中提取关键词

    Args:
        content: 用户输入的内容

    Returns:
        提取的关键词列表
    """
    keywords = []
    for keyword, tags in KEYWORD_MAPPINGS.items():
        if keyword in content:
            keywords.append(keyword)
    return keywords


def infer_type(content):
    """
    推断记录类型

    Args:
        content: 用户输入的内容

    Returns:
        推断的类型
    """
    for keyword, type_name in TYPE_MAPPINGS.items():
        if keyword in content:
            return type_name
    return TYPE_MAPPINGS["默认"]


def infer_importance(content):
    """
    推断重要程度

    Args:
        content: 用户输入的内容

    Returns:
        推断的重要程度（1-5）
    """
    for keyword, importance in IMPORTANCE_RULES.items():
        if keyword in content:
            return importance
    return IMPORTANCE_RULES["默认"]


def generate_title(content):
    """
    生成标题

    Args:
        content: 用户输入的内容

    Returns:
        生成的标题
    """
    # 提取前 50 个字符
    short_content = content[:50]

    # 尝试识别主语
    type_inferred = infer_type(content)
    if type_inferred == "决策":
        # 提取决策对象
        match = re.search(r'(选择|决定|使用|采用|确定)\s*([^，。！？\n]+)', content)
        if match:
            object = match.group(1).strip()
            return f"决策 - {object}"
        else:
            return short_content

    return short_content


def infer_tags(content):
    """
    推断标签

    Args:
        content: 用户输入的内容

    Returns:
        推断的标签列表
    """
    tags = set()

    # 从关键词映射中提取标签
    for keyword, tag_list in KEYWORD_MAPPINGS.items():
        if keyword in content:
            for tag in tag_list:
                tags.add(tag)

    # 添加默认标签
    tags.add("#daily-log")

    return list(tags)


def generate_frontmatter(content, custom_fields=None):
    """
    生成 YAML frontmatter

    Args:
        content: 用户输入的内容
        custom_fields: 自定义字段字典

    Returns:
        YAML frontmatter 字符串
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    # 自动推断字段
    title = custom_fields.get("title") if custom_fields else generate_title(content)
    record_type = custom_fields.get("type") if custom_fields else infer_type(content)
    tags = custom_fields.get("tags") if custom_fields else infer_tags(content)
    importance = custom_fields.get("importance") if custom_fields else infer_importance(content)
    project = custom_fields.get("project", "")
    status = custom_fields.get("status", "进行中")

    # 生成 YAML
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

    return frontmatter, title, record_type, tags, importance


def create_daily_log(vault_path, content, custom_fields=None):
    """
    创建或更新每日日志

    Args:
        vault_path: 笔记库路径
        content: 记录内容
        custom_fields: 自定义字段

    Returns:
        创建的文件路径
    """
    vault = Path(vault_path)
    memory_folder = vault / "memory"

    if not memory_folder.exists():
        print("❌ 错误: memory 文件夹不存在")
        print("请先使用 obsidian-bases-memory skill 初始化系统")
        sys.exit(1)

    # 生成文件名
    today_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today_str}.md"
    filepath = memory_folder / filename

    # 生成 frontmatter
    frontmatter, title, record_type, tags, importance = generate_frontmatter(content, custom_fields)

    # 构建完整内容
    now = datetime.now()
    time_str = now.strftime("%H:%M")

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
        header = f"# {today_str}\n"
        new_content = frontmatter + header + section
        filepath.write_text(new_content, encoding="utf-8")
        print(f"✓ 已创建新文件: {filename}")

    # 同步到 MEMORY.md
    if record_type in ["用户偏好", "决策"]:
        sync_to_core_memory(vault_path, record_type, title, content, today_str, filename)

    return filepath, title, record_type, tags, importance


def display_confirmation(title, record_type, tags, importance):
    """
    显示确认信息

    Args:
        title: 生成的标题
        record_type: 记录类型
        tags: 标签列表
        importance: 重要程度
    """
    tags_str = " ".join(tags)
    stars = "⭐" * importance

    print(f"\n{'='*60}")
    print(f"📝 记录信息预览")
    print(f"{'='*60}")
    print(f"✓ 标题: {title}")
    print(f"✓ 类型: {record_type}")
    print(f"✓ 标签: {tags_str}")
    print(f"✓ 重要程度: {stars}")
    print(f"{'='*60}")
    print("\n修改建议：")
    print("  [1] 修改标题")
    print("  [2] 修改重要程度")
    print("  [3] 修改标签")
    print("  [4] 添加相关项目")
    print("  [5] 确认创建")
    print("  [0] 取消")
    print(f"{'='*60}\n")


def get_user_modification(original_title, original_type, original_tags, original_importance):
    """
    获取用户修改

    Returns:
        修改后的字段字典
    """
    fields = {
        "title": original_title,
        "type": original_type,
        "tags": original_tags,
        "importance": original_importance
    }

    while True:
        choice = input("请选择操作 (0-5): ").strip()

        if choice == "0":
            return None  # 取消
        elif choice == "1":
            new_title = input(f"新标题 [{fields['title']}]: ").strip()
            if new_title:
                fields["title"] = new_title
        elif choice == "2":
            new_importance = input(f"新重要程度 (1-5) [{fields['importance']}]: ").strip()
            if new_importance and new_importance.isdigit() and 1 <= int(new_importance) <= 5:
                fields["importance"] = int(new_importance)
        elif choice == "3":
            print("当前标签:", " ".join(fields["tags"]))
            new_tags = input(f"新标签 (空格分隔，如 #技术 #决策): ").strip()
            if new_tags:
                fields["tags"] = new_tags.split()
        elif choice == "4":
            new_project = input(f"相关项目: ").strip()
            if new_project:
                fields["project"] = new_project
        elif choice == "5":
            return fields
        else:
            print("❌ 无效选择")

        # 显示更新后的信息
        display_confirmation(
            fields["title"],
            fields["type"],
            fields["tags"],
            fields.get("importance", fields["importance"])
        )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python record.py <笔记库路径> <记录内容>")
        print("示例: python record.py ~/Obsidian/Vault \"我们决定使用 PostgreSQL 作为数据库\"")
        sys.exit(1)

    vault_path = sys.argv[1]
    content = sys.argv[2]

    # 生成信息
    frontmatter, title, record_type, tags, importance = generate_frontmatter(content)

    # 显示确认
    display_confirmation(title, record_type, tags, importance)

    # 获取用户修改
    custom_fields = get_user_modification(title, record_type, tags, importance)

    if custom_fields:
        # 创建记录
        filepath, final_title, final_type, final_tags, final_importance = create_daily_log(
            vault_path,
            content,
            custom_fields
        )

        print(f"\n✓ 记录已成功创建")
        print(f"📁 文件: {filepath}")
        print(f"📝 标题: {final_title}")
        print(f"🏷️ 标签: {' '.join(final_tags)}")
        print(f"⭐ 重要程度: {'⭐' * final_importance}")
        print(f"\n查看记录: [[{filepath.name}]]")
    else:
        print("\n❌ 已取消记录")
