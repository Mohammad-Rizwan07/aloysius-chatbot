from typing import List, Dict

def filter_urls(entries: List[Dict], skip_keywords: List[str]) -> List[Dict]:
    filtered = []

    for entry in entries:
        url = entry["url"].lower()

        if any(keyword in url for keyword in skip_keywords):
            continue

        filtered.append(entry)

    return filtered
