"""
Obsidian Memory Manager - Configuration Manager
统一管理配置文件
"""
import json
import sys
from pathlib import Path


def get_config_path():
    """获取配置文件路径"""
    script_dir = Path(__file__).parent.parent
    return script_dir / "assets" / "config" / "manager_config.json"


def get_default_config():
    """获取默认配置"""
    return {
        "vault_path": str(Path.home() / "ObsidianVault"),
        "auto_initialize": True,
        "auto_detect_intent": True,
        "components": {
            "bases_memory": {
                "enabled": True,
                "path": "obsidian-bases-memory",
                "init_script": "scripts/init_memory_system.py"
            },
            "recorder": {
                "enabled": True,
                "path": "obsidian-memory-recorder",
                "time_script": "scripts/get_time.py",
                "auto_record_keywords": [
                    "决定", "选择", "偏好", "重要", "采用", "使用", "放弃", "转向"
                ],
                "min_importance_auto_record": 3
            },
            "retriever": {
                "enabled": True,
                "path": "obsidian-memory-retriever",
                "default_search_mode": "hybrid",
                "search_scripts": {
                    "keyword": "scripts/search.py",
                    "semantic": "scripts/semantic_search.py",
                    "hybrid": "scripts/hybrid_search.py"
                }
            }
        },
        "memory_rules": {
            "min_importance_for_summary": 3,
            "auto_sync_to_memory_md": ["决策", "用户偏好"],
            "retention_days": 365,
            "daily_log_format": "{Date}.md",
            "memory_md_path": "MEMORY.md",
            "memory_folder": "memory"
        },
        "ui_preferences": {
            "show_confirmations": True,
            "default_output_format": "detailed",
            "max_search_results": 10,
            "enable_shortcuts": True
        }
    }


def load_config():
    """加载配置文件"""
    config_path = get_config_path()
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    return None


def save_config(config):
    """保存配置文件"""
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    return True


def get_config_value(config, key_path):
    """
    获取配置值
    key_path: 点分隔的路径，如 "components.recorder.enabled"
    """
    keys = key_path.split('.')
    value = config
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None
    
    return value


def set_config_value(config, key_path, value):
    """
    设置配置值
    key_path: 点分隔的路径，如 "components.recorder.enabled"
    """
    keys = key_path.split('.')
    target = config
    
    for key in keys[:-1]:
        if key not in target:
            target[key] = {}
        target = target[key]
    
    target[keys[-1]] = value
    return config


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: python config_manager.py <command> [args]")
        print("Commands:")
        print("  show                    - 显示当前配置")
        print("  get <key_path>          - 获取配置值")
        print("  set <key_path> <value>  - 设置配置值")
        print("  reset                   - 重置为默认配置")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "show":
        config = load_config()
        if config:
            print(json.dumps(config, ensure_ascii=False, indent=2))
        else:
            print("{}\n配置文件不存在，使用默认配置")
            print(json.dumps(get_default_config(), ensure_ascii=False, indent=2))
    
    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: python config_manager.py get <key_path>")
            sys.exit(1)
        
        key_path = sys.argv[2]
        config = load_config() or get_default_config()
        value = get_config_value(config, key_path)
        
        if value is not None:
            if isinstance(value, (dict, list)):
                print(json.dumps(value, ensure_ascii=False, indent=2))
            else:
                print(value)
        else:
            print(f"Key '{key_path}' not found")
            sys.exit(1)
    
    elif command == "set":
        if len(sys.argv) < 4:
            print("Usage: python config_manager.py set <key_path> <value>")
            sys.exit(1)
        
        key_path = sys.argv[2]
        value_str = sys.argv[3]
        
        # 尝试解析值
        try:
            value = json.loads(value_str)
        except json.JSONDecodeError:
            # 作为字符串处理
            value = value_str
        
        config = load_config() or get_default_config()
        config = set_config_value(config, key_path, value)
        
        if save_config(config):
            print(f"✅ 配置已更新: {key_path} = {value}")
        else:
            print("❌ 保存配置失败")
            sys.exit(1)
    
    elif command == "reset":
        default_config = get_default_config()
        if save_config(default_config):
            print("✅ 配置已重置为默认值")
        else:
            print("❌ 重置配置失败")
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
