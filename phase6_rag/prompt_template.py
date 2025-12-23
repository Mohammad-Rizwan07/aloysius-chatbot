def build_prompt(context_chunks, user_question):
    context_text = "\n\n".join(
        [f"- {chunk}" for chunk in context_chunks]
    )

    prompt = f"""
Answer the question using ONLY the context below.

CONTEXT:
{context_text}

QUESTION:
{user_question}

INSTRUCTIONS:
- Follow the structured response format.
- Use headings and bullet points.
- Do not include information outside the context.

ANSWER:
"""
    return prompt.strip()
