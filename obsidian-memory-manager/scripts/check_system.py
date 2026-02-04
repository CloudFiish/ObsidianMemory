"""
Obsidian Memory Manager - System Status Checker
检测记忆系统的当前状态
"""
import os
import json
import sys
from pathlib import Path


def get_config_path():
    """获取配置文件路径"""
    script_dir = Path(__file__).parent.parent
    return script_dir / "assets" / "config" / "manager_config.json"


def load_config():
    """加载配置文件"""
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def check_system_status(vault_path):
    """
    检查记忆系统的状态
    
    返回状态:
    - "uninitialized": 完全未初始化
    - "partial": 部分初始化（缺少某些组件）
    - "ready": 完全就绪
    """
    vault = Path(vault_path)
    
    # 检查关键组件
    memory_folder = vault / "memory"
    memory_md = vault / "MEMORY.md"
    base_config = vault / "记忆数据库.base"
    
    checks = {
        "memory_folder_exists": memory_folder.exists(),
        "memory_md_exists": memory_md.exists(),
        "base_config_exists": base_config.exists(),
        "vault_path_valid": vault.exists()
    }
    
    # 判断状态
    if all(checks.values()):
        status = "ready"
    elif any(checks.values()):
        status = "partial"
    else:
        status = "uninitialized"
    
    return {
        "status": status,
        "checks": checks,
        "vault_path": str(vault),
        "missing_components": [
            k.replace("_exists", "").replace("_", " ")
            for k, v in checks.items()
            if not v and k != "vault_path_valid"
        ]
    }


def main():
    """主函数"""
    # 尝试从命令行参数获取路径，否则使用配置
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        config = load_config()
        if config:
            vault_path = config.get("vault_path", ".")
        else:
            vault_path = "."
    
    # 检查状态
    result = check_system_status(vault_path)
    
    # 输出 JSON 结果
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return 0 if result["status"] == "ready" else 1


if __name__ == "__main__":
    sys.exit(main())
