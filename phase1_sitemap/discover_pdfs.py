"""
PDF Discovery Script for Phase 1
Scans sitemap and HTML pages for PDF links, classifies, and records metadata.
"""

import os
import re
import json
import requests
from urllib.parse import urljoin, urlparse, quote
from bs4 import BeautifulSoup
import string
import datetime


URL_REGISTRY_PATH = os.path.join('data', 'url_registry.json')
PDF_REGISTRY_PATH = os.path.join('data', 'pdf_registry.json')
BASE_URL = 'https://staloysius.edu.in/'

# Heuristic patterns for document type and year
DOC_TYPE_PATTERNS = {
    'prospectus': re.compile(r'prospectus', re.I),
    'handbook': re.compile(r'handbook', re.I),
    'syllabus': re.compile(r'syllabus', re.I),
    'fees': re.compile(r'fee|fees', re.I),
}
YEAR_PATTERN = re.compile(r'(20\d{2})')



def load_url_registry(registry_path):
    with open(registry_path, 'r', encoding='utf-8') as f:
        entries = json.load(f)
    # Use all URLs as seeds, regardless of ending
    urls = [entry['url'] for entry in entries if 'url' in entry]
    return urls


def fetch_html(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None



def sanitize_string(s):
    return s  # Revert to original behavior, preserving URLs and metadata

def classify_pdf(url, link_text):
    doc_type = None
    for dtype, pattern in DOC_TYPE_PATTERNS.items():
        if pattern.search(url) or (link_text and pattern.search(link_text)):
            doc_type = dtype
            break
    year = None
    for target in [url, link_text]:
        if target:
            m = YEAR_PATTERN.search(target)
            if m:
                year = m.group(1)
                break
    return doc_type, year


def discover_pdfs_from_html(html, page_url):
    soup = BeautifulSoup(html, 'html.parser')
    pdfs = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.lower().endswith('.pdf'):
            pdf_url = urljoin(page_url, href)
            pdf_url = quote(pdf_url, safe=':/')  # Encode spaces and unsafe chars
            link_text = a.get_text(strip=True)
            doc_type, year = classify_pdf(pdf_url, link_text)
            source_domain = urlparse(pdf_url).netloc
            date_discovered = datetime.datetime.utcnow().isoformat() + 'Z'
            pdfs.append({
                'pdf_url': pdf_url,
                'source_page': page_url,
                'source_domain': source_domain,
                'link_text': link_text,
                'document_type': doc_type,
                'year': year,
                'date_discovered': date_discovered
            })
    return pdfs




from collections import deque
from urllib.parse import urldefrag

def is_internal_link(href):
    if not href:
        return False
    parsed = urlparse(href)
    # Accept relative or same-domain links only
    return (not parsed.netloc) or (parsed.netloc == urlparse(BASE_URL).netloc)

def normalize_url(url):
    # Remove fragments, normalize
    url, _ = urldefrag(url)
    if url.endswith('/'):
        url = url[:-1]
    return url

def deep_crawl_and_discover_pdfs(start_urls):
    visited = set()
    pdfs = []
    queue = deque(start_urls)
    while queue:
        page_url = queue.popleft()
        norm_url = normalize_url(page_url)
        if norm_url in visited:
            continue
        visited.add(norm_url)
        html = fetch_html(page_url)
        if not html:
            continue
        # Find PDFs on this page
        pdfs.extend(discover_pdfs_from_html(html, page_url))
        # Find new internal HTML links to crawl
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.lower().endswith('.pdf'):
                continue
            if is_internal_link(href):
                next_url = urljoin(page_url, href)
                next_url = normalize_url(next_url)
                if next_url not in visited and next_url.startswith(BASE_URL):
                    # Only crawl .html or directory pages
                    if next_url.endswith('.html') or next_url.endswith('/'):
                        queue.append(next_url)
    return pdfs

def main():
    html_urls = load_url_registry(URL_REGISTRY_PATH)
    print(f"Starting deep crawl from {len(html_urls)} seed URLs...")
    all_pdfs = deep_crawl_and_discover_pdfs(html_urls)
    # Deduplicate by pdf_url
    seen = set()
    unique_pdfs = []
    for pdf in all_pdfs:
        if pdf['pdf_url'] not in seen:
            unique_pdfs.append(pdf)
            seen.add(pdf['pdf_url'])
    os.makedirs(os.path.dirname(PDF_REGISTRY_PATH), exist_ok=True)
    with open(PDF_REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(unique_pdfs, f, indent=2, ensure_ascii=False)
    print(f"Discovered {len(unique_pdfs)} PDFs. Saved to {PDF_REGISTRY_PATH}")

if __name__ == '__main__':
    main()
