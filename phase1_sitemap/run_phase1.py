from config.settings import (
    SITEMAP_URL,
    SKIP_KEYWORDS,
    OUTPUT_REGISTRY_PATH
)

from phase1_sitemap.fetch_sitemap import fetch_sitemap_xml
from phase1_sitemap.parse_sitemap import parse_sitemap
from phase1_sitemap.filter_urls import filter_urls
from phase1_sitemap.save_registry import save_registry


def main():
    print("🔹 Fetching sitemap...")
    xml = fetch_sitemap_xml(SITEMAP_URL)

    print("🔹 Parsing sitemap...")
    entries = parse_sitemap(xml)

    print(f"🔹 Total URLs found: {len(entries)}")

    print("🔹 Filtering URLs...")
    filtered_entries = filter_urls(entries, SKIP_KEYWORDS)

    print(f"🔹 URLs after filtering: {len(filtered_entries)}")

    print("🔹 Saving URL registry...")
    save_registry(filtered_entries, OUTPUT_REGISTRY_PATH)

    print("✅ Phase 1 completed successfully.")


if __name__ == "__main__":
    main()
