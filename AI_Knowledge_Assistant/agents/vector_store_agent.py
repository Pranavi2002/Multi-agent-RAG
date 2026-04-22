# aligning query() code with ranked retrieved context llm_agent,
# to retrieve top-k most similar chunks WITH similarity scores

# also ensured that the code is compatible with backend, 
# near Tensor and ndarray

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

        # ✅ FIX: handle both torch.Tensor and numpy.ndarray safely
        # (backend/embedding layer inconsistency fix)
        if hasattr(embeddings, "cpu"):
            embeddings = embeddings.cpu().detach().numpy()

        embeddings = np.array(embeddings).astype("float32")

        # ✅ Normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.documents.extend(docs)

    def query(self, query_embedding, top_k=3):
        """
        Retrieve top-k most similar chunks WITH similarity scores
        """

        # ✅ FIX: handle both torch.Tensor and numpy.ndarray safely
        # (ensures FAISS always receives numpy float32 input)
        if hasattr(query_embedding, "cpu"):
            query_embedding = query_embedding.cpu().detach().numpy()

        query_embedding = np.array(query_embedding).astype("float32")

        # Ensure correct shape (1, dim)
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)

        # Normalize query for cosine similarity
        faiss.normalize_L2(query_embedding)

        # Search
        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            # ✅ FIX: guard against invalid FAISS index (-1)
            if idx == -1:
                continue

            results.append((self.documents[idx], float(score)))

        return results