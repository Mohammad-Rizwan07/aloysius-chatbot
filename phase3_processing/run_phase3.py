import json
from config.settings import OUTPUT_REGISTRY_PATH
from phase3_processing.load_markdown import load_markdown_files
from phase3_processing.clean_text import clean_markdown
from phase3_processing.simple_chunk import chunk_and_score

RAW_MD_DIR = "data/raw_markdown"
OUTPUT_PATH = "data/processed_chunks/chunks.json"

def main():
    print("[*] Loading markdown files...")
    markdown_files = load_markdown_files(RAW_MD_DIR)

    print("[*] Loading URL registry...")
    with open(OUTPUT_REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = { 
            e["url"].split("/")[-1] + ".md": e 
            for e in json.load(f)
        }

    all_chunks = []
    chunk_id = 0
    total_quality_chunks = 0

    for file, content in markdown_files.items():
        print(f"[*] Processing: {file}")

        # Don't clean - just chunk raw markdown
        scored_chunks = chunk_and_score(content)
        
        # Filter and enrich
        quality_chunks = [c for c in scored_chunks if c['valid']]
        
        for chunk in quality_chunks:
            all_chunks.append({
                "id": f"{file}_{chunk_id}",
                "text": chunk["text"],
                "metadata": {
                    "source_file": file,
                    "url": registry.get(file, {}).get("url", ""),
                    "lastmod": registry.get(file, {}).get("lastmod", ""),
                    "quality_score": chunk["score"]
                }
            })
            chunk_id += 1
        
        total_quality_chunks += len(quality_chunks)
        print(f"    OK {len(quality_chunks)} chunks")

    print(f"\nQuality Report:")
    print(f"   Total chunks: {len(all_chunks)}")
    if all_chunks:
        avg_score = sum(c['metadata']['quality_score'] for c in all_chunks) / len(all_chunks)
        print(f"   Average score: {avg_score:.2f}")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"\nDone. Output: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
