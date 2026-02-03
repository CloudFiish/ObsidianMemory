#!/usr/bin/env python3
"""
关键词搜索脚本

在记忆系统中执行基于关键词的搜索
"""

import sys
import re
from pathlib import Path
from datetime import datetime
import yaml


def load_config(config_path):
    """
    加载配置文件

    Args:
        config_path: 配置文件路径

    Returns:
        配置字典
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ 加载配置失败: {e}")
        return {}


def parse_frontmatter(content):
    """
    解析 YAML frontmatter

    Args:
        content: 文件内容

    Returns:
        (frontmatter, body)
    """
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 2:
            frontmatter_text = parts[1]
            body = parts[2] if len(parts) > 2 else ''
            try:
                frontmatter = yaml.safe_load(frontmatter_text)
                return frontmatter, body
            except:
                return {}, body
    return {}, content


def keyword_search(query, database_path, filters=None):
    """
    关键词搜索

    Args:
        query: 搜索查询
        database_path: 数据库路径
        filters: 过滤条件字典

    Returns:
        结果列表 [(record, score), ...]
    """
    vault = Path(database_path)
    memory_folder = vault / "memory"

    if not memory_folder.exists():
        print("❌ 错误: memory 文件夹不存在")
        return []

    results = []
    query_lower = query.lower()

    # 遍历所有记忆文件
    for md_file in memory_folder.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            frontmatter, body = parse_frontmatter(content)

            # 计算匹配分数
            score = 0
            match_details = []

            # 标题匹配（权重 10）
            title = frontmatter.get("title", "")
            if query_lower in title.lower():
                score += 10
                match_details.append("标题")

            # 内容匹配（权重 5）
            if query_lower in body.lower():
                score += 5
                match_details.append("内容")

            # 标签匹配（权重 3）
            tags = frontmatter.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]
            for tag in tags:
                if query_lower in tag.lower():
                    score += 3
                    match_details.append(f"标签: {tag}")

            # 如果有匹配，添加到结果
            if score > 0:
                # 应用过滤条件
                if filters:
                    if "date" in filters:
                        record_date = frontmatter.get("date", "")
                        if record_date != filters["date"]:
                            continue
                    if "type" in filters:
                        record_type = frontmatter.get("type", "")
                        if record_type != filters["type"]:
                            continue
                    if "importance" in filters:
                        record_importance = frontmatter.get("importance", 0)
                        if record_importance < filters["importance"]:
                            continue

                record = {
                    "file": md_file,
                    "frontmatter": frontmatter,
                    "body": body,
                    "score": score,
                    "matches": match_details
                }
                results.append(record)

        except Exception as e:
            print(f"⚠️  跳过文件 {md_file}: {e}")
            continue

    # 按分数排序
    results.sort(key=lambda x: x["score"], reverse=True)

    return results


def display_results(results, query, max_results=10):
    """
    显示搜索结果

    Args:
        results: 结果列表
        query: 搜索查询
        max_results: 最大显示数量
    """
    if not results:
        print(f"\n🔍 未找到与 \"{query}\" 相关的记录")
        print("\n建议:")
        print("  - 尝试不同的关键词")
        print("  - 使用语义搜索: /semantic [查询]")
        print("  - 扩大时间范围")
        return

    print(f"\n🔍 找到 {len(results)} 条相关记录")
    print(f"查询: \"{query}\"\n")

    display_count = min(len(results), max_results)

    for i, record in enumerate(results[:display_count], 1):
        fm = record["frontmatter"]
        score = record["score"]
        matches = record["matches"]
        stars = "⭐" * fm.get("importance", 3)

        print(f"[{i}] {stars} {fm.get('title', '无标题')}")
        print(f"    📅 {fm.get('date', '')} | {fm.get('time', '')}")
        print(f"    🏷️ {' '.join(fm.get('tags', []))}")
        print(f"    🔗 项目: {fm.get('project', '未指定')}")
        print(f"    📊 状态: {fm.get('status', '')}")
        print(f"    💡 匹配: {', '.join(matches)} (得分: {score})")
        print(f"    📁 文件: {record['file'].name}")

        # 提取摘要
        body = record["body"]
        snippet_start = body.find(query)
        if snippet_start >= 0:
            snippet = body[max(0, snippet_start-20):snippet_start+100]
            snippet = snippet.replace("\n", " ")
            print(f"    📄 摘要: ...{snippet}...")

        print()

    if len(results) > max_results:
        print(f"ℹ️  还有 {len(results) - max_results} 条记录未显示")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python search.py <笔记库路径> <搜索关键词> [选项]")
        print("\n选项:")
        print("  --type <类型>        仅搜索指定类型")
        print("  --date <日期>        仅搜索指定日期")
        print("  --importance <数字>  仅搜索重要程度>=N的记录")
        print("  --max <数字>         最多显示N条结果")
        print("\n示例:")
        print("  python search.py ~/Obsidian/Vault PostgreSQL")
        print("  python search.py ~/Obsidian/Vault API --type decision")
        print("  python search.py ~/Obsidian/Vault 决策 --importance 4")
        sys.exit(1)

    vault_path = sys.argv[1]
    query = sys.argv[2]

    # 解析选项
    filters = {}
    max_results = 10

    i = 3
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg == "--type" and i + 1 < len(sys.argv):
            filters["type"] = sys.argv[i + 1]
            i += 2
        elif arg == "--date" and i + 1 < len(sys.argv):
            filters["date"] = sys.argv[i + 1]
            i += 2
        elif arg == "--importance" and i + 1 < len(sys.argv):
            filters["importance"] = int(sys.argv[i + 1])
            i += 2
        elif arg == "--max" and i + 1 < len(sys.argv):
            max_results = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    # 执行搜索
    results = keyword_search(query, vault_path, filters)

    # 显示结果
    display_results(results, query, max_results)
