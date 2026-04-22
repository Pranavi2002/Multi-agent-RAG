# no chunking

from agents.document_fetcher import DocumentFetcher
from agents.embedding_agent import EmbeddingAgent
from agents.vector_store_agent import VectorStoreAgent
from agents.llm_agent import LLMAgent
from agents.evaluation_agent import EvaluationAgent
from agents.observability_agent import ObservabilityAgent
# import torch
import time

def main():
    # 1. Fetch documents
    fetcher = DocumentFetcher(folder_path="data")
    docs = fetcher.fetch_documents()
    if not docs:
        print("No documents found in data/ folder!")
        return

    # 2. Embed documents
    embedder = EmbeddingAgent()
    doc_embeddings = embedder.embed(docs)

    # 3. Store embeddings in vector DB
    # vector_store = VectorStoreAgent(dimension=doc_embeddings.shape[1])
    dimension = embedder.get_sentence_embedding_dimension()
    vector_store = VectorStoreAgent(dimension=dimension)
    vector_store.add(doc_embeddings, docs)

    # Agents
    llm = LLMAgent()
    evaluator = EvaluationAgent()
    observability = ObservabilityAgent()

    while True:
        query = input("Enter your query (or 'exit'): ")
        if query.lower() == "exit":
            break

        # start_time = torch.cuda.Event(enable_timing=True) if torch.cuda.is_available() else None
        start_time = time.time()
        
        # 4. Embed query
        query_embedding = embedder.embed([query])

        # 5. Retrieve top docs
        top_docs = vector_store.query(query_embedding, top_k=3)

        # 6. Generate answer
        answer = llm.generate_answer(query, top_docs)

        # 7. Evaluate
        score = evaluator.evaluate(query, answer)

        # 8. Log
        observability.log(query, top_docs, score, start_time)

        print("\nAnswer:\n", answer)
        print("-" * 50)

if __name__ == "__main__":
    main()