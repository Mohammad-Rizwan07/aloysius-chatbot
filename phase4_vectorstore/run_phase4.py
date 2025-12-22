from phase4_vectorstore.load_chunks import load_chunks
from phase4_vectorstore.embed_chunks import embed_texts
from phase4_vectorstore.create_collection import get_collection
import os

CHUNKS_PATH = os.path.abspath("data/processed_chunks/chunks.json")
VECTOR_DB_DIR = os.path.abspath("data/vector_db")
COLLECTION_NAME = "aloysius_knowledge"

BATCH_SIZE = 500

def main():
    print("🔹 Loading processed chunks...")
    chunks = load_chunks(CHUNKS_PATH)

    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [c["id"] for c in chunks]

    print("🔹 Generating embeddings...")
    embeddings = embed_texts(texts)

    print("🔹 Creating persistent vector store...")
    collection = get_collection(VECTOR_DB_DIR, COLLECTION_NAME)

    print("🔹 Adding documents to vector store in batches...")
    total = len(texts)

    for start in range(0, total, BATCH_SIZE):
        end = start + BATCH_SIZE

        collection.add(
            documents=texts[start:end],
            embeddings=embeddings[start:end].tolist(),
            metadatas=metadatas[start:end],
            ids=ids[start:end]
        )

        print(f"   ✔ Inserted {min(end, total)}/{total}")

    print("✅ Phase 4 completed successfully.")
    print(f"📦 Total vectors stored: {collection.count()}")

if __name__ == "__main__":
    main()
