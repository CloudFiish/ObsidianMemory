import os
import json
from datetime import datetime
from pathlib import Path

# Try import yaml, else use simple dump
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

class MarkdownManager:
    """Manages local Markdown memory files."""
    
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.memory_dir = self.root_path / "memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
    def get_daily_file(self, date_str=None):
        """Get the path to the daily memory file."""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        return self.memory_dir / f"{date_str}.md"
        
    def append_entry(self, content, importance=3, tags=None):
        """Append a new entry to the daily log."""
        if tags is None:
            tags = []
            
        file_path = self.get_daily_file()
        timestamp = datetime.now().strftime("%H:%M")
        
        entry_text = f"\n## {timestamp} - Memory Entry\n"
        entry_text += f"**Importance**: {'⭐' * importance}\n"
        if tags:
            entry_text += f"**Tags**: {' '.join(tags)}\n"
        entry_text += f"\n{content}\n"
        entry_text += "\n---\n"
        
        # Ensure file exists with frontmatter
        if not file_path.exists():
            self._init_daily_file(file_path)
            
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(entry_text)
            
        return str(file_path)
        
    def _init_daily_file(self, file_path):
        """Initialize a new daily file with frontmatter."""
        date_str = file_path.stem
        frontmatter = {
            "date": date_str,
            "type": "daily-log",
            "tags": ["memory"]
        }
        
        content = "---\n"
        if HAS_YAML:
            content += yaml.dump(frontmatter, allow_unicode=True)
        else:
            # Simple manual YAML dump
            for key, value in frontmatter.items():
                if isinstance(value, list):
                    val_str = "[" + ", ".join(f'"{v}"' for v in value) + "]"
                    content += f"{key}: {val_str}\n"
                else:
                    content += f"{key}: {value}\n"
        content += "---\n\n"
        content += f"# Daily Memory: {date_str}\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def read_file(self, file_path):
        """Read file content."""
        if Path(file_path).exists():
            return Path(file_path).read_text(encoding='utf-8')
        return ""

    def list_memory_files(self):
        """List all markdown files in memory directory."""
        return list(self.memory_dir.glob("*.md"))
