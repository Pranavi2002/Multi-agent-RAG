from sentence_transformers import SentenceTransformer

class EmbeddingAgent:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        return self.model.encode(texts, convert_to_tensor=True)
    
    def get_sentence_embedding_dimension(self):
        return self.model.get_embedding_dimension()