import chromadb
from chromadb.config import Settings
import os

VECTOR_DB_DIR = os.path.abspath("data/vector_db")
COLLECTION_NAME = "aloysius_knowledge"

def retrieve_context(query_embedding, top_k=5):
    client = chromadb.Client(
        Settings(
            persist_directory=VECTOR_DB_DIR,
            anonymized_telemetry=False,
            is_persistent=True
        )
    )

    collection = client.get_or_create_collection(COLLECTION_NAME)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    return documents, metadatas
