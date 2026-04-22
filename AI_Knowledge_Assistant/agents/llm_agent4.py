# not aligned with reranking and summarization

class LLMAgent:
    """
    LLM Agent (local / dummy version).
    Focuses on:
    - Strong RAG-style prompt
    - Ranked + truncated context
    - Cleaner answer simulation
    """

    def generate_answer(self, query, context_docs):
        if not context_docs:
            return "No relevant documents found to answer the query."

        MAX_CHARS_PER_DOC = 300
        MAX_DOCS = 3  # top-k control at LLM level

        # ---- Step 1: Limit number of docs (top-k control) ----
        context_docs = context_docs[:MAX_DOCS]

        # ---- Step 2: Format + truncate context ----
        formatted_context = []

        for idx, (doc, score) in enumerate(context_docs, start=1):
            cleaned_doc = doc[:MAX_CHARS_PER_DOC]

            formatted_context.append(
                f"[{idx}] (similarity: {round(score, 3)})\n{cleaned_doc}"
            )

        context_block = "\n\n".join(formatted_context)

        # ---- Step 3: Strong RAG prompt ----
        prompt = f"""
You are a precise and helpful AI assistant.

Rules:
- Use ONLY the context provided below.
- If the answer is not in the context, say "I don't know".
- Do not use external knowledge.

Context:
{context_block}

Question:
{query}

Provide a clear and accurate answer:
"""

        # ---- Step 4: Dummy response (simulating LLM) ----
        # In real system, this prompt goes to GPT / Llama / Mistral etc.

        best_doc = context_docs[0][0]

        return (
            "Answer (based on retrieved context):\n\n"
            + best_doc[:400]
            + "..."
        )