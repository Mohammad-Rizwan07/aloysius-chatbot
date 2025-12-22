from phase6_rag.embed_query import embed_query
from phase6_rag.retrieve_context import retrieve_context
from phase6_rag.prompt_template import build_prompt
from phase6_rag.call_llm import call_llm

def main():
    print("🎓 St. Aloysius University Chatbot (Phase 6)")
    print("Type 'exit' to quit\n")

    while True:
        user_question = input("You: ")
        if user_question.lower() in ["exit", "quit"]:
            break

        query_embedding = embed_query(user_question)
        context_chunks, metadatas = retrieve_context(query_embedding)

        prompt = build_prompt(context_chunks, user_question)
        answer = call_llm(prompt)

        print("\nBot:", answer)
        print("\n--- Sources ---")
        for meta in metadatas:
            print(meta.get("url", ""))
        print("\n")

if __name__ == "__main__":
    main()
