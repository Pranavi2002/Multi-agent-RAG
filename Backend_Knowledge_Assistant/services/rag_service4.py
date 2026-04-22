# includes smart deduplication (sentence-level)
# includes database integration
# no observability metrics and logging
# no optional agents

import time
import os
import numpy as np
import torch  # tensor conversion helper
import re   # for sentence-level dedupe

from AI_Knowledge_Assistant.agents.embedding_agent import EmbeddingAgent
from AI_Knowledge_Assistant.agents.vector_store_agent import VectorStoreAgent
from AI_Knowledge_Assistant.agents.rerank_summarize_agent import RerankSummarizeAgent
from AI_Knowledge_Assistant.agents.llm_agent import LLMAgent
from AI_Knowledge_Assistant.agents.evaluation_agent import EvaluationAgent
from AI_Knowledge_Assistant.agents.observability_agent import ObservabilityAgent

from AI_Knowledge_Assistant.agents.document_fetcher import DocumentFetcher
from AI_Knowledge_Assistant.agents.chunking_agent import ChunkingAgent

from AI_Knowledge_Assistant.agents.observability_agent import ObservabilityAgent

from observability.metrics import rag_query_count, rag_query_latency
from observability.logger import logger

# ==============================
# DB IMPORT (NEW)
# ==============================
from db.history_repo import save_query


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

        base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "AI_Knowledge_Assistant")
        )

        fetcher = DocumentFetcher(folder_path=os.path.join(base_dir, "data"))
        chunker = ChunkingAgent()

        docs = fetcher.fetch_documents()

        if not docs:
            raise RuntimeError("No documents found in data folder")

        chunks = []

        for doc in docs:
            chunks.extend(chunker.chunk(doc))

        chunks = [str(c).strip() for c in chunks if c and str(c).strip()]

        if not chunks:
            raise RuntimeError("Chunking failed: no valid text chunks")

        embeddings = self.embedder.embed(chunks)
        embeddings = self._to_numpy(embeddings)

        self.vector_store.add(embeddings, chunks)

        self._initialized = True

        print(f"✅ Vector store ready: {len(chunks)} chunks indexed")

    # ----------------------------
    # QUERY PIPELINE updated with observability
    # ----------------------------
    def query(self, user_query: str, db):
        """
        Main RAG pipeline + DB logging + observability
        """
        if not self._initialized:
            raise RuntimeError("Vector store not initialized")

        start_time = time.time()
        rag_query_count.inc()

        try:
            # 1. Embed
            query_embedding = self.embedder.embed([user_query])
            query_embedding_np = self._to_numpy(query_embedding)

            if query_embedding_np.ndim == 1:
                query_embedding_np = query_embedding_np.reshape(1, -1)

            # 2. Retrieve
            retrieved_docs = self.vector_store.query(
                query_embedding=query_embedding_np,
                top_k=3
            )

            # 3. Rerank
            query_embedding_torch = torch.tensor(query_embedding_np, dtype=torch.float32)
            reranked_docs = self.reranker.rerank(query_embedding_torch, retrieved_docs)

            # 4. Context
            context = self._smart_deduplicate_context(reranked_docs)

            # 5. LLM
            answer = self.llm.generate_answer(user_query, context)

            # 6. Evaluation
            safe_context_docs = (
                retrieved_docs if retrieved_docs and isinstance(retrieved_docs[0], tuple)
                else [(doc, 1.0) for doc in reranked_docs]
            )

            eval_score = self.evaluator.evaluate(
                user_query, safe_context_docs, self.embedder
            )

            return_payload = {
                "answer": answer,
                "retrieved_docs": retrieved_docs,
                "reranked_docs": reranked_docs,
                "context": context,
                "evaluation_score": eval_score
            }

            return return_payload

        finally:
            latency = time.time() - start_time
            rag_query_latency.observe(latency)

            logger.info(
                "RAG_QUERY_PROCESSED",
                extra={
                    "query": user_query,
                    "latency": latency,
                    "num_retrieved": len(retrieved_docs) if 'retrieved_docs' in locals() else 0
                }
            )

            try:
                save_query(
                    db=db,
                    question=user_query,
                    answer=answer if 'answer' in locals() else None,
                    avg_similarity=eval_score.get("avg_similarity", 0.0) if 'eval_score' in locals() else 0.0,
                    max_similarity=eval_score.get("max_similarity", 0.0) if 'eval_score' in locals() else 0.0,
                    latency=latency
                )
            except Exception as e:
                logger.error(f"DB insert failed: {e}")

    # ----------------------------
    # SAFE CONVERTER
    # ----------------------------
    def _to_numpy(self, x):
        if isinstance(x, torch.Tensor):
            return x.detach().cpu().numpy().astype("float32")
        return np.array(x, dtype="float32")

    # ----------------------------
    # SMART DEDUPLICATION
    # ----------------------------
    def _smart_deduplicate_context(self, docs):
        """
        Removes duplicate sentences across retrieved chunks
        """

        seen = set()
        final_text = []

        for doc in docs:

            sentences = re.split(r'(?<=[.!?])\s+', doc)

            cleaned_sentences = []

            for s in sentences:
                norm = s.strip().lower()

                if not norm or norm in seen:
                    continue

                seen.add(norm)
                cleaned_sentences.append(s)

            if cleaned_sentences:
                final_text.append(" ".join(cleaned_sentences))

        return "\n\n".join(final_text)