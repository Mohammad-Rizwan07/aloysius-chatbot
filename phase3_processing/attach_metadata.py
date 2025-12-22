from typing import List, Dict

def attach_metadata(
    chunks: List[str],
    source_file: str,
    url: str,
    lastmod: str
) -> List[Dict]:

    results = []
    for idx, chunk in enumerate(chunks):
        results.append({
            "id": f"{source_file}_{idx}",
            "text": chunk,
            "metadata": {
                "source_file": source_file,
                "url": url,
                "lastmod": lastmod
            }
        })
    return results
