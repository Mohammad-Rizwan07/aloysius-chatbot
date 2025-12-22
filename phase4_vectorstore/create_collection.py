import chromadb
from chromadb.config import Settings
import os

def get_collection(persist_dir: str, name: str):
    persist_dir = os.path.abspath(persist_dir)
    os.makedirs(persist_dir, exist_ok=True)

    print(f"📦 Using persistent Chroma DB at: {persist_dir}")

    client = chromadb.Client(
        Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False,
            is_persistent=True   # 🔑 THIS IS CRITICAL
        )
    )

    collection = client.get_or_create_collection(name=name)
    return collection
