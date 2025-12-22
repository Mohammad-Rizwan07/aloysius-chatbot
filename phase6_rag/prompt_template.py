def build_prompt(context_chunks, user_question):
    context_text = "\n\n".join(context_chunks)

    prompt = f"""
You are an official AI assistant for St. Aloysius University.
Answer the question strictly using the provided context.
If the answer is not found in the context, say:
"I do not have this information from the official website."

Context:
{context_text}

Question:
{user_question}

Answer:
"""
    return prompt.strip()
