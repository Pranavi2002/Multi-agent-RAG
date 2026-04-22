from sentence_transformers import util

class RerankSummarizeAgent:
    def __init__(self, embedder, max_chunks=2, max_chars=1200):
        self.embedder = embedder
        self.max_chunks = max_chunks
        self.max_chars = max_chars

    def rerank(self, query_embedding, retrieved_docs):
        texts = [doc for doc, _ in retrieved_docs]

        doc_embeddings = self.embedder.embed(texts)

        # ensure CPU tensors
        query_embedding = query_embedding.cpu().detach()
        doc_embeddings = doc_embeddings.cpu().detach()

        scores = util.cos_sim(query_embedding, doc_embeddings)[0]

        ranked = sorted(
            zip(texts, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [text for text, _ in ranked[:self.max_chunks]]

    def summarize(self, ranked_texts):
        context = ""
        for text in ranked_texts:
            if len(context) + len(text) > self.max_chars:
                break
            context += text.strip() + "\n\n"

        return context.strip()