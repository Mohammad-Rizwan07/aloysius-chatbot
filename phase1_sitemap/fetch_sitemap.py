import requests

def fetch_sitemap_xml(sitemap_url: str) -> str:
    response = requests.get(sitemap_url, timeout=30)
    response.raise_for_status()
    return response.text
