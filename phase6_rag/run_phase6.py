from phase6_rag.embed_query import embed_query
from phase6_rag.retrieve_context import retrieve_context
from phase6_rag.prompt_template import build_prompt
from phase6_rag.gemini_llm import get_llm

def main():
    print("[*] Testing RAG System with Google Gemini")
    print("[*] Type 'exit' to quit\n")

    llm = get_llm()

    while True:
        user_question = input("Question: ")
        if user_question.lower() in ["exit", "quit"]:
            break

        print("\n[*] Retrieving context...")
        query_embedding = embed_query(user_question)
        context_chunks, metadatas = retrieve_context(query_embedding)
        print(f"    Found {len(context_chunks)} relevant chunks")

        prompt = build_prompt(context_chunks, user_question)
        
        print("[*] Generating answer with Gemini...")
        system_prompt = """You are a helpful assistant for St. Aloysius University. 
Answer questions based on the provided context about the university. 
Be concise and accurate."""
        answer = llm.generate_with_context(user_question, context_chunks, system_prompt)

        print("\nAnswer:", answer)
        print("\n--- Sources ---")
        urls_shown = set()
        for meta in metadatas:
            url = meta.get("url", "")
            if url and url not in urls_shown:
                print(f"  - {url}")
                urls_shown.add(url)
        print()

if __name__ == "__main__":
    main()
