from phase6_rag.embed_query import embed_query
from phase6_rag.retrieve_context import retrieve_context
from phase6_rag.prompt_template import build_prompt
from phase6_rag.call_llm import call_llm

def run_rag(question: str):
    query_embedding = embed_query(question)
    context_chunks, metadatas = retrieve_context(query_embedding)

    prompt = build_prompt(context_chunks, question)
    answer = call_llm(prompt)

    sources = list({
        meta.get("url", "")
        for meta in metadatas
        if meta.get("url")
    })

    return answer, sources
