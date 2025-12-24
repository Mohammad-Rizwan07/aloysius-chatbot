import os
import re
import json

PDF_MARKDOWN_DIR = 'data/pdf_markdown'
CLEAN_MARKDOWN_DIR = 'data/clean_markdown'
FILTERED_PDF_REGISTRY_PATH = 'data/filtered_pdf_registry.json'

os.makedirs(CLEAN_MARKDOWN_DIR, exist_ok=True)

def clean_markdown(content):
    """Clean and standardize markdown content."""
    
    # Remove page numbers (e.g., "- 5 -" or "Page 5")
    content = re.sub(r'[-\s]*Page\s+\d+[-\s]*', ' ', content, flags=re.IGNORECASE)
    content = re.sub(r'-\s*\d+\s*-', '', content)
    
    # Remove header/footer artifacts (common patterns)
    content = re.sub(r'^.*?www\..*?\..*?$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^.*?Copyright.*?$', '', content, flags=re.MULTILINE | re.IGNORECASE)
    
    # Fix multiple spaces to single space (but preserve markdown formatting)
    content = re.sub(r' {2,}', ' ', content)
    
    # Fix multiple blank lines to max 2 blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Remove trailing whitespace on each line
    lines = [line.rstrip() for line in content.split('\n')]
    content = '\n'.join(lines)
    
    # Remove leading/trailing whitespace
    content = content.strip()
    
    return content

def main():
    with open(FILTERED_PDF_REGISTRY_PATH, 'r', encoding='utf-8') as f:
        pdfs = json.load(f)
    
    processed_count = 0
    for entry in pdfs:
        url = entry['pdf_url']
        filename = os.path.basename(url).replace(' ', '_')
        # Match the naming convention from extract_with_gemini.py
        for md_file in os.listdir(PDF_MARKDOWN_DIR):
            md_path = os.path.join(PDF_MARKDOWN_DIR, md_file)
            clean_path = os.path.join(CLEAN_MARKDOWN_DIR, md_file)
            
            if os.path.exists(clean_path):
                print(f"Skipping {md_file} (already cleaned)")
                continue
            
            try:
                with open(md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                cleaned_content = clean_markdown(content)
                
                with open(clean_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                
                print(f"Cleaned: {md_file}")
                processed_count += 1
            except Exception as e:
                print(f"Error cleaning {md_file}: {e}")
    
    print(f"✅ Phase 3 (Cleaning) completed. Processed {processed_count} files.")

if __name__ == '__main__':
    main()
