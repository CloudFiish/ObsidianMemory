"""
Obsidian Memory Manager - Intent Detector
智能识别用户意图
"""
import json
import sys
import re


# 意图识别规则
INTENT_PATTERNS = {
    "initialize": {
        "keywords": [
            "初始化", "设置", "配置", "第一次用", "开始使用",
            "init", "setup", "configure", "start"
        ],
        "patterns": [
            r"初始化.*记忆",
            r"设置.*记忆系统",
            r"开始使用.*记忆",
        ]
    },
    "record": {
        "keywords": [
            "记录", "保存", "记下来", "写入", "添加",
            "record", "save", "write", "add", "note"
        ],
        "patterns": [
            r"记录.*",
            r"保存.*",
            r".*记录下来",
        ]
    },
    "retrieve": {
        "keywords": [
            "搜索", "查找", "检索", "回顾", "查看", "找到",
            "search", "find", "lookup", "retrieve", "review"
        ],
        "patterns": [
            r"搜索.*",
            r"查找.*",
            r".*在哪里",
            r"之前.*说过",
        ]
    },
    "config": {
        "keywords": [
            "配置", "设置", "修改", "调整", "更改",
            "config", "setting", "modify", "change"
        ],
        "patterns": [
            r"配置.*",
            r"设置.*路径",
            r"修改.*配置",
        ]
    },
    "status": {
        "keywords": [
            "状态", "检查", "查看", "怎么样", "情况",
            "status", "check", "state", "condition"
        ],
        "patterns": [
            r".*状态",
            r"检查.*系统",
            r"查看.*配置",
        ]
    }
}

# 自动记录触发词（当用户陈述中包含这些词时，可能想要记录）
AUTO_RECORD_INDICATORS = [
    "决定", "决策", "选择", "采用", "使用", "放弃", "转向",
    "偏好", "喜欢", "习惯", "重要", "关键", "主要",
    "确定", "选定", "确认", "同意", "否决"
]


def detect_intent(text):
    """
    检测用户意图
    
    返回:
    {
        "primary_intent": "initialize|record|retrieve|config|status|unknown",
        "confidence": 0.0-1.0,
        "suggested_action": "描述建议的操作",
        "auto_record_suggested": true/false,
        "details": { ... }
    }
    """
    text_lower = text.lower()
    scores = {}
    
    # 计算每种意图的匹配分数
    for intent, rules in INTENT_PATTERNS.items():
        score = 0
        
        # 关键词匹配
        for keyword in rules["keywords"]:
            if keyword.lower() in text_lower:
                score += 1
        
        # 模式匹配
        for pattern in rules["patterns"]:
            if re.search(pattern, text, re.IGNORECASE):
                score += 2
        
        scores[intent] = score
    
    # 找出最高分的意图
    if scores:
        max_intent = max(scores, key=scores.get)
        max_score = scores[max_intent]
        total_score = sum(scores.values())
        
        # 计算置信度
        confidence = max_score / (total_score + 1) if total_score > 0 else 0
        
        # 如果最高分太低，认为是未知意图
        if max_score < 1:
            primary_intent = "unknown"
            confidence = 0
        else:
            primary_intent = max_intent
    else:
        primary_intent = "unknown"
        confidence = 0
    
    # 检查是否建议自动记录
    auto_record_suggested = False
    if primary_intent == "unknown":
        for indicator in AUTO_RECORD_INDICATORS:
            if indicator in text:
                auto_record_suggested = True
                break
    
    # 生成建议操作
    suggested_actions = {
        "initialize": "初始化记忆系统",
        "record": "记录信息到记忆系统",
        "retrieve": "从记忆系统检索信息",
        "config": "修改系统配置",
        "status": "检查系统状态",
        "unknown": "需要更多信息或澄清"
    }
    
    return {
        "primary_intent": primary_intent,
        "confidence": round(confidence, 2),
        "suggested_action": suggested_actions.get(primary_intent, "未知操作"),
        "auto_record_suggested": auto_record_suggested,
        "all_scores": scores,
        "details": {
            "input_text": text,
            "matched_keywords": [
                kw for intent, rules in INTENT_PATTERNS.items()
                for kw in rules["keywords"]
                if kw.lower() in text_lower
            ]
        }
    }


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: python detect_intent.py '<用户输入文本>'")
        sys.exit(1)
    
    text = sys.argv[1]
    result = detect_intent(text)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
