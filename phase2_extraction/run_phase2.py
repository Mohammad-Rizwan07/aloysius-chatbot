import asyncio
from config.settings import OUTPUT_REGISTRY_PATH
from phase2_extraction.load_registry import load_url_registry
from phase2_extraction.crawl_page import crawl_single_page
from phase2_extraction.save_markdown import save_markdown

OUTPUT_MD_DIR = "data/raw_markdown"

async def main():
    print("🔹 Loading URL registry...")
    entries = load_url_registry(OUTPUT_REGISTRY_PATH)

    print(f"🔹 URLs to crawl: {len(entries)}")

    for idx, entry in enumerate(entries, start=1):
        url = entry["url"]
        print(f"({idx}/{len(entries)}) Crawling → {url}")

        try:
            markdown = await crawl_single_page(url)
            if markdown.strip():
                save_markdown(markdown, url, OUTPUT_MD_DIR)
            else:
                print(f"⚠️ Empty content: {url}")

        except Exception as e:
            print(f"❌ Failed: {url} → {e}")

    print("✅ Phase 2 completed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
