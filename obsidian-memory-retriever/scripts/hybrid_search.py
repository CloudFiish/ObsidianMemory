#!/usr/bin/env python3
"""
混合搜索脚本

结合关键词和语义搜索，提供更准确的结果
"""

import sys
from pathlib import Path
import yaml


# 导入搜索脚本中的函数
# 注意: 在实际使用中，这些函数应该在共享模块中
from search import keyword_search, parse_frontmatter
from semantic_search import semantic_search, cosine_similarity


def hybrid_search(query, database_path, keyword_weight=0.3, semantic_weight=0.7, filters=None):
    """
    混合搜索

    Args:
        query: 搜索查询
        database_path: 数据库路径
        keyword_weight: 关键词权重
        semantic_weight: 语义权重
        filters: 过滤条件

    Returns:
        结果列表 [(record, total_score, keyword_score, semantic_score), ...]
    """
    vault = Path(database_path)
    memory_folder = vault / "memory"

    if not memory_folder.exists():
        print("❌ 错误: memory 文件夹不存在")
        return []

    # 执行关键词搜索
    keyword_results = keyword_search(query, database_path, filters)

    # 执行语义搜索
    semantic_results = semantic_search(query, database_path, threshold=0.5, filters=filters)

    # 合并结果
    combined_results = {}

    # 处理关键词搜索结果
    for record in keyword_results:
        file_path = str(record["file"])
        if file_path not in combined_results:
            combined_results[file_path] = {
                "file": record["file"],
                "frontmatter": record["frontmatter"],
                "body": record["body"],
                "keyword_score": record["score"],
                "semantic_score": 0.0
            }
        else:
            combined_results[file_path]["keyword_score"] = record["score"]

    # 处理语义搜索结果
    for record in semantic_results:
        file_path = str(record["file"])
        if file_path not in combined_results:
            combined_results[file_path] = {
                "file": record["file"],
                "frontmatter": record["frontmatter"],
                "body": record["body"],
                "keyword_score": 0.0,
                "semantic_score": record["similarity"]
            }
        else:
            combined_results[file_path]["semantic_score"] = record["similarity"]

    # 计算总分
    results = []
    for file_path, record_data in combined_results.items():
        # 归一化分数
        normalized_keyword = record_data["keyword_score"] / 10.0  # 假设最大关键词分为10
        normalized_semantic = record_data["semantic_score"]  # 已经是0-1

        # 计算加权总分
        total_score = (keyword_weight * normalized_keyword) + (semantic_weight * normalized_semantic)

        record_data["total_score"] = total_score
        results.append(record_data)

    # 按总分排序
    results.sort(key=lambda x: x["total_score"], reverse=True)

    return results


def display_results(results, query, max_results=10):
    """
    显示混合搜索结果

    Args:
        results: 结果列表
        query: 搜索查询
        max_results: 最大显示数量
    """
    if not results:
        print(f"\n🔍 未找到与 \"{query}\" 相关的记录")
        print("\n建议:")
        print("  - 尝试不同的关键词")
        print("  - 降低搜索条件")
        print("  - 仅使用关键词搜索: /search [关键词]")
        print("  - 仅使用语义搜索: /semantic [查询]")
        return

    print(f"\n🔍 混合搜索: \"{query}\"")
    print(f"找到 {len(results)} 条相关记录\n")

    display_count = min(len(results), max_results)

    for i, record in enumerate(results[:display_count], 1):
        fm = record["frontmatter"]
        total_score = record["total_score"]
        keyword_score = record["keyword_score"]
        semantic_score = record["semantic_score"]
        stars = "⭐" * fm.get("importance", 3)

        # 显示得分
        keyword_percent = int((keyword_score / 10.0) * 100)
        semantic_percent = int(semantic_score * 100)
        total_percent = int(total_score * 100)

        print(f"[{i}] {stars} {fm.get('title', '无标题')}")
        print(f"    📅 {fm.get('date', '')} | {fm.get('time', '')}")
        print(f"    🏷️ {' '.join(fm.get('tags', []))}")
        print(f"    🔗 项目: {fm.get('project', '未指定')}")
        print(f"    📊 状态: {fm.get('status', '')}")
        print(f"    💡 总分: {total_percent}%")
        print(f"       - 关键词分: {keyword_percent}% (权重: 30%)")
        print(f"       - 语义分: {semantic_percent}% (权重: 70%)")
        print(f"    📁 文件: {record['file'].name}")

        # 提取摘要
        body = record["body"]
        if len(body) > 100:
            snippet = body[:100]
            print(f"    📄 摘要: {snippet}...")

        print()

    if len(results) > max_results:
        print(f"ℹ️  还有 {len(results) - max_results} 条记录未显示")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python hybrid_search.py <笔记库路径> <查询> [选项]")
        print("\n选项:")
        print("  --keyword-weight <数字>  设置关键词权重 (默认: 0.3)")
        print("  --semantic-weight <数字>  设置语义权重 (默认: 0.7)")
        print("  --type <类型>          仅搜索指定类型")
        print("  --date <日期>          仅搜索指定日期")
        print("  --importance <数字>    仅搜索重要程度>=N的记录")
        print("  --max <数字>           最多显示N条结果")
        print("\n示例:")
        print("  python hybrid_search.py ~/Obsidian/Vault \"找到技术决策，特别是关于 API 的\"")
        print("  python hybrid_search.py ~/Obsidian/Vault 决策 --keyword-weight 0.4")
        print("  python hybrid_search.py ~/Obsidian/Vault API --type decision --importance 4")
        sys.exit(1)

    vault_path = sys.argv[1]
    query = sys.argv[2]

    # 解析选项
    keyword_weight = 0.3
    semantic_weight = 0.7
    filters = {}
    max_results = 10

    i = 3
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg == "--keyword-weight" and i + 1 < len(sys.argv):
            keyword_weight = float(sys.argv[i + 1])
            i += 2
        elif arg == "--semantic-weight" and i + 1 < len(sys.argv):
            semantic_weight = float(sys.argv[i + 1])
            i += 2
        elif arg == "--type" and i + 1 < len(sys.argv):
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
    results = hybrid_search(query, vault_path, keyword_weight, semantic_weight, filters)

    # 显示结果
    display_results(results, query, max_results)
