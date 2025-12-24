import os
import json
import time
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)

FILTERED_PDF_REGISTRY_PATH = 'data/filtered_pdf_registry.json'
PDF_DOWNLOAD_DIR = 'data/temp_pdfs'
PDF_MARKDOWN_DIR = 'data/pdf_markdown'
RATE_LIMIT_PER_MIN = 60
MAX_CHARS_PER_CHUNK = 8000  # Conservative chunk size for Gemini

os.makedirs(PDF_DOWNLOAD_DIR, exist_ok=True)
os.makedirs(PDF_MARKDOWN_DIR, exist_ok=True)

def safe_filename(url: str) -> str:
    name = url.replace('https://', '').replace('http://', '')
    name = ''.join(c if c.isalnum() or c in '-_.' else '_' for c in name)
    return name[:150] + '.md'

def download_pdf(url: str, dest_path: str) -> bool:
    import requests
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def extract_pdf_text(pdf_path: str):
    try:
        reader = PdfReader(pdf_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ''

def split_text(text, max_chars=MAX_CHARS_PER_CHUNK):
    for i in range(0, len(text), max_chars):
        yield text[i:i+max_chars]

def gemini_extract_markdown(text):
    model = genai.GenerativeModel('gemini-2.5-pro')
    prompt = (
        "Convert the following PDF text to markdown, preserving layout, tables, and structure as much as possible:\n\n"
        + text
    )
    try:
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        print(f"Gemini API error: {e}")
        return ''

def main():
    with open(FILTERED_PDF_REGISTRY_PATH, 'r', encoding='utf-8') as f:
        pdfs = json.load(f)
    for entry in pdfs:
        url = entry['pdf_url']
        filename = safe_filename(url)
        pdf_path = os.path.join(PDF_DOWNLOAD_DIR, filename.replace('.md', '.pdf'))
        md_path = os.path.join(PDF_MARKDOWN_DIR, filename)
        if os.path.exists(md_path):
            print(f"Skipping {filename} (already processed)")
            continue
        if not os.path.exists(pdf_path):
            print(f"Downloading: {url}")
            if not download_pdf(url, pdf_path):
                continue
        else:
            print(f"Already downloaded: {url}")
        text = extract_pdf_text(pdf_path)
        if not text.strip():
            print(f"No text extracted from {url}")
            continue
        print(f"Extracting markdown for {filename}")
        markdown_chunks = []
        for idx, chunk in enumerate(split_text(text)):
            print(f"  Sending chunk {idx+1}")
            md = gemini_extract_markdown(chunk)
            markdown_chunks.append(md)
            time.sleep(60.0 / RATE_LIMIT_PER_MIN)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(markdown_chunks))
        print(f"Saved markdown for {filename}")

if __name__ == '__main__':
    main()