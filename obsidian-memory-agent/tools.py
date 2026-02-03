import os
import json
import hashlib
from pathlib import Path
from core.zvec_adapter import ZvecAdapter
from core.markdown_manager import MarkdownManager

# Configuration
CONFIG_PATH = Path(__file__).parent / "config.json"
DEFAULT_ROOT = str(Path(__file__).parent.parent.parent)

def load_config():
    config = {
        "memory_root": DEFAULT_ROOT,
        "zvec_db_path": os.path.join(DEFAULT_ROOT, ".zvec_db")
    }
    
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                
                # Resolve memory_root relative to config file if it's relative
                mem_root = user_config.get("memory_root", ".")
                if not os.path.isabs(mem_root):
                    # If ./memory, it means relative to SKILL root, but we usually want vault root
                    # Let's assume if user sets ./memory in config inside obsidian-memory-agent,
                    # they might mean obsidian-memory-agent/memory OR project_root/memory
                    # To be safe and consistent with previous logic:
                    # Let's interpret paths relative to the PROJECT ROOT (parent of obsidian-memory-agent)
                    project_root = Path(__file__).parent.parent
                    mem_root = str(project_root / mem_root)
                
                config["memory_root"] = mem_root
                
                # Resolve zvec_db_path
                zvec_path = user_config.get("zvec_db_path", ".zvec_db")
                if not os.path.isabs(zvec_path):
                    project_root = Path(__file__).parent.parent
                    zvec_path = str(project_root / zvec_path)
                
                config["zvec_db_path"] = zvec_path
                
        except Exception as e:
            print(f"Warning: Failed to load config.json: {e}")
            
    # Environment variables override config
    if "OBSIDIAN_VAULT_ROOT" in os.environ:
        config["memory_root"] = os.environ["OBSIDIAN_VAULT_ROOT"]
        config["zvec_db_path"] = os.path.join(config["memory_root"], ".zvec_db")
        
    return config

CFG = load_config()

# Initialize Singletons
md_manager = MarkdownManager(CFG["memory_root"])
zvec_adapter = ZvecAdapter(CFG["zvec_db_path"])

def configure_memory_path(path: str) -> str:
    """
    Update the memory storage path in config.json.
    
    Args:
        path: The new absolute or relative path for memory storage.
    
    Returns:
        Status message.
    """
    try:
        current_config = {}
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                current_config = json.load(f)
        
        current_config["memory_root"] = path
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(current_config, f, indent=2)
            
        return f"Configuration updated. New memory root: {path}. Please restart the agent/skill to apply changes."
    except Exception as e:
        return f"Failed to update configuration: {e}"

def remember_event(content: str, importance: int = 3, tags: list = None) -> str:
    """
    Store a new memory event.
    
    Args:
        content: The text content of the memory.
        importance: Integer 1-5 indicating importance.
        tags: List of string tags (e.g. ["work", "python"]).
        
    Returns:
        Status message.
    """
    # 1. Write to Markdown (Source of Truth)
    file_path = md_manager.append_entry(content, importance, tags)
    
    # 2. Add to Vector DB (Index)
    doc_id = hashlib.md5(content.encode('utf-8')).hexdigest()
    metadata = {
        "source_file": file_path,
        "importance": importance,
        "tags": tags or []
    }
    
    success = zvec_adapter.add_memory(doc_id, content, metadata)
    
    if success:
        return f"Memory stored in {file_path} and indexed in Zvec."
    else:
        return f"Memory stored in {file_path} but failed to index."

def recall_context(query: str, top_k: int = 5) -> str:
    """
    Retrieve relevant context based on a query.
    
    Args:
        query: The search query.
        top_k: Number of results to return.
        
    Returns:
        Formatted string of relevant memories.
    """
    results = zvec_adapter.search(query, top_k)
    
    if not results:
        return "No relevant memories found."
        
    output = f"Found {len(results)} relevant memories for '{query}':\n\n"
    for i, res in enumerate(results, 1):
        content = res.get('content', 'No content')
        meta = res.get('metadata', {})
        score = res.get('score', 0)
        
        output += f"[{i}] (Score: {score:.2f})\n"
        output += f"Content: {content}\n"
        output += f"Source: {meta.get('source_file', 'Unknown')}\n"
        output += "---\n"
        
    return output

def sync_memory() -> str:
    """
    Force synchronization of all Markdown files to Zvec index.
    Useful if files were edited manually.
    """
    files = md_manager.list_memory_files()
    count = 0
    
    for file_path in files:
        content = md_manager.read_file(file_path)
        # Simple chunking: split by "---" separator used in append_entry
        entries = content.split("\n---\n")
        
        for entry in entries:
            if not entry.strip() or entry.startswith("---"): # Skip frontmatter
                continue
                
            # Extract content (removing headers if possible, simplified here)
            clean_content = entry.strip()
            
            doc_id = hashlib.md5(clean_content.encode('utf-8')).hexdigest()
            metadata = {"source_file": str(file_path), "sync": True}
            
            zvec_adapter.add_memory(doc_id, clean_content, metadata)
            count += 1
            
    return f"Synced {count} memory entries from {len(files)} files."

if __name__ == "__main__":
    # Simple CLI test
    print(f"Using config: {CFG}")
    print(remember_event("Today I learned about Zvec vector database.", 5, ["learning"]))
    print(recall_context("Zvec"))
