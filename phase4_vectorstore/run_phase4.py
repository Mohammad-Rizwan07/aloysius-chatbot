from phase4_vectorstore.load_chunks import load_chunks
from phase4_vectorstore.embed_chunks import embed_texts
from phase4_vectorstore.create_collection import get_collection

CHUNKS_PATH = "data/processed_chunks/chunks.json"
VECTOR_DB_DIR = "data/vector_db"
COLLECTION_NAME = "aloysius_knowledge"

BATCH_SIZE = 500  # Safe batch size for ChromaDB

def main():
    print("🔹 Loading processed chunks...")
    chunks = load_chunks(CHUNKS_PATH)

    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [c["id"] for c in chunks]

    print("🔹 Generating embeddings...")
    embeddings = embed_texts(texts)

    print("🔹 Creating vector store...")
    collection = get_collection(VECTOR_DB_DIR, COLLECTION_NAME)

    print("🔹 Adding documents to vector store in batches...")

    total = len(texts)
    for start in range(0, total, BATCH_SIZE):
        end = start + BATCH_SIZE

        batch_texts = texts[start:end]
        batch_embeddings = embeddings[start:end]
        batch_metadatas = metadatas[start:end]
        batch_ids = ids[start:end]

        collection.add(
            documents=batch_texts,
            embeddings=batch_embeddings.tolist(),
            metadatas=batch_metadatas,
            ids=batch_ids
        )

        batch_no = start // BATCH_SIZE + 1
        print(f"   ✔ Inserted batch {batch_no} ({end if end < total else total}/{total})")

    print("✅ Phase 4 completed successfully.")
    print(f"📦 Total vectors stored: {collection.count()}")

if __name__ == "__main__":
    main()
