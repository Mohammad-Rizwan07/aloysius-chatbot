import json
from typing import List, Dict

def save_registry(entries: List[Dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
