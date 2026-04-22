# no RAGAS, no DeepEval
# embedding-based + retrieval-based metrics

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class EvaluationAgent:
    """
    Offline evaluation (NO LLM, NO OpenAI)

    Measures:
    - Avg similarity between query and retrieved chunks
    - Coverage score
    """

    def evaluate(self, query, context_docs, embedder):
        """
        context_docs: List[(doc_text, similarity_score)]
        """

        if not context_docs:
            return {"avg_similarity": 0.0}

        # Embed query
        query_emb = embedder.embed([query]).cpu().numpy()

        # Embed retrieved docs
        doc_texts = [doc for doc, _ in context_docs]
        doc_embs = embedder.embed(doc_texts).cpu().numpy()

        similarities = cosine_similarity(query_emb, doc_embs)[0]

        return {
            "avg_similarity": round(float(np.mean(similarities)), 3),
            "max_similarity": round(float(np.max(similarities)), 3),
            "num_chunks": len(context_docs)
        }