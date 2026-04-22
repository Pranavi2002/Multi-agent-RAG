from prometheus_client import Counter, Histogram

# total queries
rag_query_count = Counter(
    "rag_queries_total",
    "Total number of RAG queries"
)

# latency tracking
rag_query_latency = Histogram(
    "rag_query_latency_seconds",
    "Latency for RAG pipeline"
)