# basic add and query methods

import faiss
import numpy as np

class VectorStoreAgent:
    def __init__(self, dimension):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add(self, embeddings, docs):
        self.index.add(embeddings.cpu().detach().numpy())
        self.documents.extend(docs)

    def query(self, query_embedding, top_k=3):
        D, I = self.index.search(query_embedding.cpu().detach().numpy(), top_k)
        return [self.documents[i] for i in I[0]]