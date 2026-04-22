# no smart deduplication (sentence-level)

import time
import os
import numpy as np
import torch  # ✅ tensor conversion helper

from AI_Knowledge_Assistant.agents.embedding_agent import EmbeddingAgent
from AI_Knowledge_Assistant.agents.vector_store_agent import VectorStoreAgent
from AI_Knowledge_Assistant.agents.rerank_summarize_agent import RerankSummarizeAgent
from AI_Knowledge_Assistant.agents.llm_agent import LLMAgent
from AI_Knowledge_Assistant.agents.evaluation_agent import EvaluationAgent
from AI_Knowledge_Assistant.agents.observability_agent import ObservabilityAgent

from AI_Knowledge_Assistant.agents.document_fetcher import DocumentFetcher
from AI_Knowledge_Assistant.agents.chunking_agent import ChunkingAgent


class RAGService:

    def __init__(self):
        # AI components
        self.embedder = EmbeddingAgent()
        dimension = self.embedder.get_sentence_embedding_dimension()

        self.vector_store = VectorStoreAgent(dimension)
        self.reranker = RerankSummarizeAgent(self.embedder)
        self.llm = LLMAgent()
        self.evaluator = EvaluationAgent()
        self.logger = ObservabilityAgent()

        self._initialized = False

    # ----------------------------
    # INIT VECTOR STORE
    # ----------------------------
    def initialize_vector_store(self):

        if self._initialized:
            return
        
        # fetcher = DocumentFetcher()
        # this tries to fetch documents from Backend_Knowledge_Assistant/data folder

        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "AI_Knowledge_Assistant")
        )

        fetcher = DocumentFetcher(folder_path=os.path.join(base_dir, "data"))
        chunker = ChunkingAgent()

        # 1. Load docs
        docs = fetcher.fetch_documents()

        if not docs:
            raise RuntimeError("No documents found in data folder")

        # ==============================
        # ✅ FIX: correct chunking input
        # ==============================
        chunks = []

        for doc in docs:
            chunks.extend(chunker.chunk(doc))

        chunks = [str(c).strip() for c in chunks if c and str(c).strip()]

        if not chunks:
            raise RuntimeError("Chunking failed: no valid text chunks")

        # 2. Embeddings (torch → numpy conversion)
        embeddings = self.embedder.embed(chunks)
        embeddings = self._to_numpy(embeddings)  # ✅ changed: centralized conversion

        # 3. Store in FAISS
        self.vector_store.add(embeddings, chunks)

        self._initialized = True

        print(f"✅ Vector store ready: {len(chunks)} chunks indexed")

    # ----------------------------
    # QUERY PIPELINE
    # ----------------------------
    def query(self, user_query: str):

        if not self._initialized:
            raise RuntimeError("Vector store not initialized")

        start_time = time.time()

        # 1. Embed query (torch)
        query_embedding = self.embedder.embed([user_query])

        # ==============================
        # ✅ FIX: ensure FAISS-ready numpy
        # ==============================
        query_embedding_np = self._to_numpy(query_embedding)

        # ensure 2D shape for FAISS
        if query_embedding_np.ndim == 1:
            query_embedding_np = query_embedding_np.reshape(1, -1)

        # 2. Retrieve
        retrieved_docs = self.vector_store.query(
            query_embedding=query_embedding_np,
            top_k=3
        )

        # ==============================
        # ✅ FIX: reranker expects torch
        # ==============================
        query_embedding_torch = torch.tensor(query_embedding_np, dtype=torch.float32)

        reranked_docs = self.reranker.rerank(
            query_embedding_torch,
            retrieved_docs
        )

        # 4. Context
        context = self.reranker.summarize(reranked_docs)

        # 5. Answer
        answer = self.llm.generate_answer(user_query, context)

        # 6. Evaluate
        # ==============================
        # FIX: evaluation expects (doc, score) tuples
        # ==============================
        safe_context_docs = []

        if isinstance(retrieved_docs[0], tuple):
            # already in (doc, score) format
            safe_context_docs = retrieved_docs
        else:
            # reranked output is list of strings → convert safely
            safe_context_docs = [(doc, 1.0) for doc in reranked_docs]

        eval_score = self.evaluator.evaluate(
            user_query,
            safe_context_docs,
            self.embedder
        )

        # 7. Log
        self.logger.log(
            query=user_query,
            retrieved_docs=retrieved_docs,
            eval_score=eval_score,
            start_time=start_time
        )

        return {
            "answer": answer,
            "retrieved_docs": retrieved_docs,
            "reranked_docs": reranked_docs,
            "context": context,
            "evaluation_score": eval_score,
            "latency": time.time() - start_time
        }

    # ----------------------------
    # SAFE CONVERTER (FIXED + CLEAN)
    # ----------------------------
    def _to_numpy(self, x):
        # ==============================
        # ✅ FIX: handles torch, numpy, list safely
        # ==============================
        if isinstance(x, torch.Tensor):
            return x.detach().cpu().numpy().astype("float32")

        return np.array(x, dtype="float32")