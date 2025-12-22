import chromadb
from chromadb.config import Settings

def get_collection(persist_dir: str, name: str):
    client = chromadb.Client(
        Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False
        )
    )

    return client.get_or_create_collection(name=name)
