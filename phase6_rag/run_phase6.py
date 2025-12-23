from phase6_rag.embed_query import embed_query
from phase6_rag.retrieve_context import retrieve_context
from phase6_rag.prompt_template import build_prompt
from phase6_rag.gemini_llm import get_llm

def main():
    print("[*] Testing RAG System with Google Gemini")
    print("[*] Type 'exit' to quit\n")

    llm = get_llm()

    while True:
        user_question = input("Question: ").strip()
        if user_question.lower() in ["exit", "quit"]:
            break

        print("\n[*] Retrieving context...")
        query_embedding = embed_query(user_question)
        context_chunks, metadatas = retrieve_context(query_embedding)
        print(f"    Found {len(context_chunks)} relevant chunks")

        # Build RAG prompt (NO system prompt here)
        prompt = build_prompt(context_chunks, user_question)

        print("[*] Generating answer with Gemini...")
        answer = llm.generate(prompt)

        print("\nAnswer:\n")
        print(answer)

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
