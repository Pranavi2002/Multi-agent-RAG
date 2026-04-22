# reranking and summarization included

from agents.document_fetcher import DocumentFetcher
from agents.chunking_agent import ChunkingAgent
from agents.embedding_agent import EmbeddingAgent
from agents.vector_store_agent import VectorStoreAgent
from agents.llm_agent import LLMAgent
from agents.evaluation_agent import EvaluationAgent
from agents.observability_agent import ObservabilityAgent
from agents.rerank_summarize_agent import RerankSummarizeAgent
# import torch
import time

def main():
    # 1. Fetch documents
    fetcher = DocumentFetcher(folder_path="data")
    docs = fetcher.fetch_documents()
    if not docs:
        print("No documents found in data/ folder!")
        return
    
    # 2. Chunk documents
    chunker = ChunkingAgent()
    all_chunks = []
    for doc in docs:
        chunks = chunker.chunk(doc)
        all_chunks.extend(chunks)

    print(f"Loaded {len(docs)} docs → {len(all_chunks)} chunks")

    # 3. Embed documents
    embedder = EmbeddingAgent()
    embeddings = embedder.embed(all_chunks)

    # 3. Store embeddings in vector DB
    dimension = embedder.get_sentence_embedding_dimension()
    vector_store = VectorStoreAgent(dimension=dimension)
    vector_store.add(embeddings, all_chunks)

    # Agents
    reranker = RerankSummarizeAgent(embedder)
    llm = LLMAgent()
    evaluator = EvaluationAgent()
    observability = ObservabilityAgent()

    # 4. Query loop
    while True:
        query = input("\n Enter your query (or 'exit'): ")
        if query.lower() == "exit":
            break

        # start_time = torch.cuda.Event(enable_timing=True) if torch.cuda.is_available() else None
        start_time = time.time()

        # 5. Retrieve top docs
        query_embedding = embedder.embed([query])
        top_docs = vector_store.query(query_embedding, top_k=3)

        # 6a. Rerank
        reranked_docs = reranker.rerank(query_embedding, top_docs)

        # 6b. Summarize
        summary_context = reranker.summarize(reranked_docs)

        # 6c. Generate answer
        answer = llm.generate_answer(query, summary_context)

        # 7. Evaluate
        score = evaluator.evaluate(query, top_docs, embedder)

        # 8. Log
        observability.log(query, top_docs, score, start_time)

        print("\nAnswer:\n", answer)

if __name__ == "__main__":
    main()