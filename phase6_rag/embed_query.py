from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_query(query: str):
    return _model.encode([query])[0]
