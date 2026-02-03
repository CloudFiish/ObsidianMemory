import re
from pathlib import Path

def sync_to_core_memory(vault_path, record_type, title, content, date_str, source_file):
    """
    将重要记录同步到 MEMORY.md
    
    Args:
        vault_path: 笔记库路径
        record_type: 记录类型 (如 "用户偏好", "决策")
        title: 记录标题
        content: 记录内容
        date_str: 日期字符串 (YYYY-MM-DD)
        source_file: 源文件名 (如 2026-02-03.md)
    """
    vault = Path(vault_path)
    memory_file = vault / "MEMORY.md"

    if not memory_file.exists():
        print(f"⚠️ 警告: MEMORY.md 不存在，跳过同步")
        return

    existing_content = memory_file.read_text(encoding="utf-8")
    new_content = existing_content
    
    source_link = f"[[memory/{source_file}]]"

    if record_type == "用户偏好":
        # 寻找 "## 用户偏好" 章节
        pattern = r"(## 用户偏好\s*\n)"
        match = re.search(pattern, existing_content)
        if match:
            # 构造要插入的行
            insertion = f"- {title} (来源于 {source_link})\n"
            # 插入到章节标题下方
            insert_pos = match.end()
            new_content = existing_content[:insert_pos] + insertion + existing_content[insert_pos:]
            print(f"✓ 已同步到 MEMORY.md: 用户偏好")
        else:
             print(f"⚠️ 警告: 未在 MEMORY.md 中找到 '## 用户偏好' 章节")

    elif record_type == "决策":
        # 寻找 "## 重要决策历史" 章节
        pattern = r"(## 重要决策历史\s*\n)"
        match = re.search(pattern, existing_content)
        if match:
             # 构造要插入的块
             # 提取内容摘要，去掉换行符，限制长度
             summary = content.strip().split('\n')[0][:100]
             insertion = f"### {date_str}: {title}\n- 决策内容: {summary}\n- 来源: {source_link}\n\n"
             insert_pos = match.end()
             new_content = existing_content[:insert_pos] + insertion + existing_content[insert_pos:]
             print(f"✓ 已同步到 MEMORY.md: 决策")
        else:
             print(f"⚠️ 警告: 未在 MEMORY.md 中找到 '## 重要决策历史' 章节")

    if new_content != existing_content:
        memory_file.write_text(new_content, encoding="utf-8")
