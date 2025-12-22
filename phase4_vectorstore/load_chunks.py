import json
from typing import List, Dict

def load_chunks(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
