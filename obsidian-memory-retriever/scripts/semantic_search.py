#!/usr/bin/env python3
"""
语义搜索脚本

使用嵌入向量进行语义相似度搜索
"""

import sys
import re
from pathlib import Path
from datetime import datetime
import yaml
import math


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


def cosine_similarity(vec1, vec2):
    """
    计算余弦相似度

    Args:
        vec1: 向量1
        vec2: 向量2

    Returns:
        相似度分数 (0-1)
    """
    if not vec1 or not vec2:
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def generate_simple_embedding(text):
    """
    生成简单的文本嵌入（基于TF-IDF的简化版本）

    注意: 这是简化实现。生产环境应使用专业的嵌入模型
    如 sentence-transformers, OpenAI embeddings, 等

    Args:
        text: 输入文本

    Returns:
        嵌入向量
    """
    # 分词（简单按空格和标点分割）
    words = re.findall(r'\w+', text.lower())

    if not words:
        return []

    # 计算词频
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1

    # 生成向量（使用固定大小的词汇表）
    # 这是一个简化版本，实际应该使用预训练的嵌入模型
    vocab_size = 1000
    embedding = [0.0] * vocab_size

    for word, freq in word_freq.items():
        # 使用简单的哈希函数将词映射到索引
        word_hash = hash(word) % vocab_size
        embedding[word_hash] = float(freq)

    # 归一化
    magnitude = math.sqrt(sum(v * v for v in embedding))
    if magnitude > 0:
        embedding = [v / magnitude for v in embedding]

    return embedding


def semantic_search(query, database_path, threshold=0.7, filters=None):
    """
    语义搜索

    Args:
        query: 搜索查询
        database_path: 数据库路径
        threshold: 相似度阈值
        filters: 过滤条件

    Returns:
        结果列表 [(record, similarity), ...]
    """
    vault = Path(database_path)
    memory_folder = vault / "memory"

    if not memory_folder.exists():
        print("❌ 错误: memory 文件夹不存在")
        return []

    # 生成查询向量
    query_vector = generate_simple_embedding(query)

    results = []

    # 遍历所有记忆文件
    for md_file in memory_folder.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            frontmatter, body = parse_frontmatter(content)

            # 生成记录向量（标题 + 内容）
            text_to_embed = frontmatter.get("title", "") + " " + body[:500]
            record_vector = generate_simple_embedding(text_to_embed)

            # 计算相似度
            similarity = cosine_similarity(query_vector, record_vector)

            # 如果相似度超过阈值，添加到结果
            if similarity >= threshold:
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
                    "similarity": similarity
                }
                results.append(record)

        except Exception as e:
            print(f"⚠️  跳过文件 {md_file}: {e}")
            continue

    # 按相似度排序
    results.sort(key=lambda x: x["similarity"], reverse=True)

    return results


def display_results(results, query, max_results=10):
    """
    显示语义搜索结果

    Args:
        results: 结果列表
        query: 搜索查询
        max_results: 最大显示数量
    """
    if not results:
        print(f"\n🔍 未找到与 \"{query}\" 语义相关的记录")
        print("\n建议:")
        print("  - 尝试更具体的查询")
        print("  - 降低相似度阈值")
        print("  - 使用关键词搜索: /search [关键词]")
        return

    print(f"\n🔍 语义搜索: \"{query}\"")
    print(f"找到 {len(results)} 条相关记录\n")

    display_count = min(len(results), max_results)

    for i, record in enumerate(results[:display_count], 1):
        fm = record["frontmatter"]
        similarity = record["similarity"]
        stars = "⭐" * fm.get("importance", 3)
        similarity_percent = int(similarity * 100)

        print(f"[{i}] {stars} {fm.get('title', '无标题')}")
        print(f"    📅 {fm.get('date', '')} | {fm.get('time', '')}")
        print(f"    🏷️ {' '.join(fm.get('tags', []))}")
        print(f"    🔗 项目: {fm.get('project', '未指定')}")
        print(f"    📊 状态: {fm.get('status', '')}")
        print(f"    💡 相似度: {similarity_percent}%")
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
        print("用法: python semantic_search.py <笔记库路径> <查询> [选项]")
        print("\n选项:")
        print("  --threshold <数字>    设置相似度阈值 (0-1, 默认: 0.7)")
        print("  --type <类型>         仅搜索指定类型")
        print("  --date <日期>         仅搜索指定日期")
        print("  --importance <数字>   仅搜索重要程度>=N的记录")
        print("  --max <数字>          最多显示N条结果")
        print("\n示例:")
        print("  python semantic_search.py ~/Obsidian/Vault \"我们之前讨论过数据库吗？\"")
        print("  python semantic_search.py ~/Obsidian/Vault 技术决策 --threshold 0.6")
        print("  python semantic_search.py ~/Obsidian/Vault API --type decision")
        sys.exit(1)

    vault_path = sys.argv[1]
    query = sys.argv[2]

    # 解析选项
    threshold = 0.7
    filters = {}
    max_results = 10

    i = 3
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg == "--threshold" and i + 1 < len(sys.argv):
            threshold = float(sys.argv[i + 1])
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
    results = semantic_search(query, vault_path, threshold, filters)

    # 显示结果
    display_results(results, query, max_results)

    print("\n⚠️  注意: 当前使用简化的嵌入算法")
    print("建议在生产环境中使用专业的嵌入模型:")
    print("  - sentence-transformers (Hugging Face)")
    print("  - OpenAI Embeddings API")
    print("  - Cohere Embeddings")
