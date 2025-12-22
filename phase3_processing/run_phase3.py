import json
from config.settings import OUTPUT_REGISTRY_PATH
from phase3_processing.load_markdown import load_markdown_files
from phase3_processing.clean_text import clean_markdown
from phase3_processing.chunk_text import chunk_text
from phase3_processing.attach_metadata import attach_metadata

RAW_MD_DIR = "data/raw_markdown"
OUTPUT_PATH = "data/processed_chunks/chunks.json"

def main():
    print("🔹 Loading markdown files...")
    markdown_files = load_markdown_files(RAW_MD_DIR)

    print("🔹 Loading URL registry...")
    with open(OUTPUT_REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = { 
            e["url"].split("/")[-1] + ".md": e 
            for e in json.load(f)
        }

    all_chunks = []

    for file, content in markdown_files.items():
        print(f"🔹 Processing: {file}")

        cleaned = clean_markdown(content)
        chunks = chunk_text(cleaned)

        reg = registry.get(file, {})
        url = reg.get("url", "")
        lastmod = reg.get("lastmod", "")

        enriched = attach_metadata(
            chunks,
            source_file=file,
            url=url,
            lastmod=lastmod
        )

        all_chunks.extend(enriched)

    print(f"🔹 Total chunks created: {len(all_chunks)}")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print("✅ Phase 3 completed successfully.")

if __name__ == "__main__":
    main()
