from sentence_transformers import SentenceTransformer
from typing import List

def embed_texts(texts: List[str]):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True
    )
    return embeddings
