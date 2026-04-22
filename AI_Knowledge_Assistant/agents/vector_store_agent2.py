# Correct similarity metric - Cosine similarity (best for embeddings)
# Stable FAISS usage - float32 everywhere, normalized vectors
# Safe query handling- supports both (dim,) and (1, dim)
# Clean RAG behavior- chunk → embed → retrieve works properly

# ✅ Cosine similarity (FAISS IndexFlatIP)
# ✅ L2 normalization for docs
# ✅ L2 normalization for query
# ✅ Correct FAISS search

# no similarity score chunks retrieval

import faiss
import numpy as np

class VectorStoreAgent:
    def __init__(self, dimension):
        self.dimension = dimension

        # ✅ Cosine similarity via Inner Product
        self.index = faiss.IndexFlatIP(dimension)

        self.documents = []

    def add(self, embeddings, docs):
        """
        Store document embeddings in FAISS index
        """
        embeddings = embeddings.cpu().detach().numpy().astype("float32")

        # ✅ Normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.documents.extend(docs)

    def query(self, query_embedding, top_k=3):
        """
        Retrieve top-k most similar chunks
        """
        query_embedding = query_embedding.cpu().detach().numpy().astype("float32")

        # Ensure correct shape (1, dim)
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)

        # ✅ Normalize query for cosine similarity
        faiss.normalize_L2(query_embedding)

        D, I = self.index.search(query_embedding, top_k)

        return [self.documents[i] for i in I[0]]