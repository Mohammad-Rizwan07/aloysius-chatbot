import json
import re

# Keywords for relevant PDFs (add/remove as needed)
KEYWORDS = [
    'fee', 'fees', 'course', 'syllabus', 'prospectus', 'admission', 'program', 'structure', 'curriculum'
]

PDF_REGISTRY_PATH = 'data/pdf_registry.json'
FILTERED_PDF_REGISTRY_PATH = 'data/filtered_pdf_registry.json'

def is_relevant(entry):
    url = entry.get('pdf_url', '').lower()
    doc_type = (entry.get('document_type') or '').lower()
    for kw in KEYWORDS:
        if kw in url or kw in doc_type:
            return True
    return False

def main():
    with open(PDF_REGISTRY_PATH, 'r', encoding='utf-8') as f:
        pdfs = json.load(f)
    relevant = [entry for entry in pdfs if is_relevant(entry)]
    print(f"Filtered {len(relevant)} relevant PDFs out of {len(pdfs)} total.")
    with open(FILTERED_PDF_REGISTRY_PATH, 'w', encoding='utf-8') as f:
        json.dump(relevant, f, indent=2, ensure_ascii=False)
    print(f"Saved to {FILTERED_PDF_REGISTRY_PATH}")

if __name__ == '__main__':
    main()
