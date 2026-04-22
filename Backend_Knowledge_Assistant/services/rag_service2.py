# includes smart deduplication (sentence-level)
# no database integration

import time
import os
import numpy as np
import torch  # ✅ tensor conversion helper
import re  # ✅ NEW: for sentence-level dedupe

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
    # QUERY PIPELINE
    # ----------------------------
    def query(self, user_query: str):

        if not self._initialized:
            raise RuntimeError("Vector store not initialized")

        start_time = time.time()

        query_embedding = self.embedder.embed([user_query])
        query_embedding_np = self._to_numpy(query_embedding)

        if query_embedding_np.ndim == 1:
            query_embedding_np = query_embedding_np.reshape(1, -1)

        retrieved_docs = self.vector_store.query(
            query_embedding=query_embedding_np,
            top_k=3
        )

        query_embedding_torch = torch.tensor(query_embedding_np, dtype=torch.float32)

        reranked_docs = self.reranker.rerank(
            query_embedding_torch,
            retrieved_docs
        )

        # ==============================
        # 🔥 NEW: SMART DEDUP BEFORE LLM
        # ==============================
        context = self._smart_deduplicate_context(reranked_docs)

        answer = self.llm.generate_answer(user_query, context)

        safe_context_docs = []

        if retrieved_docs and isinstance(retrieved_docs[0], tuple):
            safe_context_docs = retrieved_docs
        else:
            safe_context_docs = [(doc, 1.0) for doc in reranked_docs]

        eval_score = self.evaluator.evaluate(
            user_query,
            safe_context_docs,
            self.embedder
        )

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
    # SAFE CONVERTER
    # ----------------------------
    def _to_numpy(self, x):
        if isinstance(x, torch.Tensor):
            return x.detach().cpu().numpy().astype("float32")
        return np.array(x, dtype="float32")

    # ==============================
    # 🔥 NEW SMART DEDUP FUNCTION
    # ==============================
    def _smart_deduplicate_context(self, docs):
        """
        Removes overlap + repeated sentences while preserving meaning
        """

        seen = set()
        final_text = []

        for doc in docs:

            sentences = re.split(r'(?<=[.!?])\s+', doc)

            cleaned_sentences = []

            for s in sentences:
                norm = s.strip().lower()

                # skip empty or duplicates
                if not norm or norm in seen:
                    continue

                seen.add(norm)
                cleaned_sentences.append(s)

            if cleaned_sentences:
                final_text.append(" ".join(cleaned_sentences))

        return "\n\n".join(final_text)