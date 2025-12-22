import os
from typing import Dict

def load_markdown_files(directory: str) -> Dict[str, str]:
    data = {}
    for file in os.listdir(directory):
        if file.endswith(".md"):
            path = os.path.join(directory, file)
            with open(path, "r", encoding="utf-8") as f:
                data[file] = f.read()
    return data
