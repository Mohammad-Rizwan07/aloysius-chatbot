import os
import re
import json

CLEAN_MARKDOWN_DIR = 'data/clean_markdown'
PROCESSED_CHUNKS_DIR = 'data/processed_chunks_pdfs'
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 200  # Overlap between chunks for context

os.makedirs(PROCESSED_CHUNKS_DIR, exist_ok=True)

def split_by_headings(content):
    """Split markdown by headings to preserve structure."""
    sections = []
    current_section = ""
    
    lines = content.split('\n')
    for line in lines:
        if re.match(r'^#{1,6}\s', line):  # Heading
            if current_section.strip():
                sections.append(current_section.strip())
            current_section = line
        else:
            current_section += '\n' + line
    
    if current_section.strip():
        sections.append(current_section.strip())
    
    return sections

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into chunks with overlap for better context."""
    chunks = []
    
    if len(text) <= chunk_size:
        return [text]
    
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
        if i + chunk_size >= len(text):
            break
    
    return chunks

def main():
    all_chunks = []
    chunk_id = 0
    
    for md_file in sorted(os.listdir(CLEAN_MARKDOWN_DIR)):
        if not md_file.endswith('.md'):
            continue
        
        md_path = os.path.join(CLEAN_MARKDOWN_DIR, md_file)
        
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by headings first
            sections = split_by_headings(content)
            
            for section in sections:
                # Then chunk each section
                chunks = chunk_text(section)
                
                for chunk_text_content in chunks:
                    all_chunks.append({
                        'id': chunk_id,
                        'source_file': md_file,
                        'content': chunk_text_content,
                        'char_length': len(chunk_text_content)
                    })
                    chunk_id += 1
            
            print(f"Chunked: {md_file} → {len(sections)} sections")
        
        except Exception as e:
            print(f"Error chunking {md_file}: {e}")
    
    # Save all chunks to JSON
    chunks_output_path = os.path.join(PROCESSED_CHUNKS_DIR, 'chunks.json')
    with open(chunks_output_path, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Phase 4 (Chunking) completed.")
    print(f"Total chunks created: {chunk_id}")
    print(f"Chunks saved to: {chunks_output_path}")

if __name__ == '__main__':
    main()
