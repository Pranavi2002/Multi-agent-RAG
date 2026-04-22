# no LLM prompt and not good retreived context format

class LLMAgent:
    """
    Dummy LLM Agent for testing the RAG pipeline.
    Simply returns the first document as the 'answer'.
    """
    def generate_answer(self, query, context_docs):
        if not context_docs:
            return "No relevant documents found."
        # Combine the first top doc as a placeholder answer
        return f"Based on retrieved context, here's a placeholder answer:\n{context_docs[0][:300]}..."