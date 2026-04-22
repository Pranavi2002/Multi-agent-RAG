# rerank and summarization are moved to another file
# so, LLMAgent should ONLY generate answers

class LLMAgent:
    """
    LLM Agent (local / dummy version).
    Assumes context is already:
    - reranked
    - summarized
    """

    def generate_answer(self, query, context):
        if not context:
            return "No relevant documents found to answer the query."

        prompt = f"""
You are a precise and helpful AI assistant.

Rules:
- Use ONLY the context below.
- Do NOT hallucinate.
- If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{query}

Provide a clear and accurate answer:
"""

        # Dummy response (offline-safe)
        return (
            "Answer (based on retrieved context):\n\n"
            + context
        )