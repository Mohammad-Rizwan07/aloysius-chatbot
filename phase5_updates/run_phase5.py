import json
import os
from phase5_updates.load_previous_state import load_previous_state, save_state
from phase5_updates.compute_hash import compute_content_hash
from phase5_updates.detect_changes import detect_change
from phase4_vectorstore.create_collection import get_collection

URL_REGISTRY = "data/url_registry.json"
RAW_MD_DIR = "data/raw_markdown"
VECTOR_DB_DIR = "data/vector_db"
COLLECTION_NAME = "aloysius_knowledge"

def main():
    print("🔹 Loading previous state...")
    old_state = load_previous_state()
    new_state = {}

    print("🔹 Loading URL registry...")
    with open(URL_REGISTRY, "r", encoding="utf-8") as f:
        urls = json.load(f)

    collection = get_collection(VECTOR_DB_DIR, COLLECTION_NAME)

    for entry in urls:
        url = entry["url"]
        lastmod = entry.get("lastmod", "")

        filename = url.replace("https://", "").replace("/", "_") + ".md"
        path = os.path.join(RAW_MD_DIR, filename)

        if not os.path.exists(path):
            continue

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        content_hash = compute_content_hash(content)
        status = detect_change(url, lastmod, content_hash, old_state)

        if status == "NEW":
            print(f"🆕 New page: {url}")

        elif status == "UPDATED":
            print(f"♻️ Updated page: {url}")
            collection.delete(where={"url": url})

        else:
            continue

        new_state[url] = {
            "lastmod": lastmod,
            "hash": content_hash
        }

    save_state(new_state)
    print("✅ Phase 5 completed successfully.")

if __name__ == "__main__":
    main()
