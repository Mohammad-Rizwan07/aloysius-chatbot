from bs4 import BeautifulSoup
from typing import List, Dict

def parse_sitemap(xml_content: str) -> List[Dict]:
    soup = BeautifulSoup(xml_content, "xml")
    entries = []

    for url in soup.find_all("url"):
        loc = url.find("loc")
        lastmod = url.find("lastmod")

        if not loc:
            continue

        entries.append({
            "url": loc.text.strip(),
            "lastmod": lastmod.text.strip() if lastmod else None,
            "status": "active"
        })

    return entries
