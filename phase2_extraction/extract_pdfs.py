import os
import json
import requests
from pathlib import Path
from PyPDF2 import PdfReader

PDF_REGISTRY_PATH = os.path.join('data', 'pdf_registry.json')
OUTPUT_DIR = os.path.join('data', 'pdf_text')


def safe_filename(url: str) -> str:
    name = url.replace('https://', '').replace('http://', '')
    name = ''.join(c if c.isalnum() or c in '-_.' else '_' for c in name)
    return name[:150] + '.txt'


def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        reader = PdfReader(pdf_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ''


def download_pdf(url: str, dest_path: str) -> bool:
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    temp_pdf_dir = os.path.join('data', 'temp_pdfs')
    os.makedirs(temp_pdf_dir, exist_ok=True)

    with open(PDF_REGISTRY_PATH, 'r', encoding='utf-8') as f:
        pdf_entries = json.load(f)

    for entry in pdf_entries:
        url = entry['pdf_url']
        filename = safe_filename(url)
        pdf_path = os.path.join(temp_pdf_dir, filename.replace('.txt', '.pdf'))
        txt_path = os.path.join(OUTPUT_DIR, filename)

        if not os.path.exists(pdf_path):
            print(f"Downloading: {url}")
            if not download_pdf(url, pdf_path):
                continue
        else:
            print(f"Already downloaded: {url}")

        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
            print(f"No text extracted from {url}")
            continue

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Saved extracted text to {txt_path}")

if __name__ == '__main__':
    main()
