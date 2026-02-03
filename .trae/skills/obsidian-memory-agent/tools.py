import os
import hashlib
from pathlib import Path
from core.zvec_adapter import ZvecAdapter
from core.markdown_manager import MarkdownManager

# Configuration
VAULT_ROOT = os.environ.get("OBSIDIAN_VAULT_ROOT", str(Path(__file__).parent.parent.parent))
ZVEC_DB_PATH = os.path.join(VAULT_ROOT, ".zvec_db")

# Initialize Singletons
md_manager = MarkdownManager(VAULT_ROOT)
zvec_adapter = ZvecAdapter(ZVEC_DB_PATH)

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
    print(remember_event("Today I learned about Zvec vector database.", 5, ["learning"]))
    print(recall_context("Zvec"))
