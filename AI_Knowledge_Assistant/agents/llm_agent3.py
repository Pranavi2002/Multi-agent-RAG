#includes LLM agent prompt
# no truncated context

class LLMAgent:
    """
    LLM Agent (local / dummy).
    Focuses on:
    - Proper RAG-style prompt
    - Using ranked retrieved context
    """

    def generate_answer(self, query, context_docs):
        if not context_docs:
            return "No relevant documents found to answer the query."

        # context_docs is expected as: [(doc_text, score), ...]
        formatted_context = []
        for idx, (doc, score) in enumerate(context_docs, start=1):
            formatted_context.append(
                f"[{idx}] (similarity: {round(score, 3)})\n{doc}"
            )

        context_block = "\n\n".join(formatted_context)

        prompt = f"""
You are an AI assistant. Answer the question using ONLY the context below.
If the answer is not present in the context, say "I don't know".

Context:
{context_block}

Question:
{query}

Answer:
"""

        # Dummy generation logic (for now)
        # In real LLMs, this prompt would be sent to a model
        return (
            "Answer based on retrieved context:\n"
            + context_docs[0][0][:400]
            + "..."
        )