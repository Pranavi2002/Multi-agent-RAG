import os

# ===============================
# RAG CONFIG
# ===============================
TOP_K = 3
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ===============================
# DATABASE CONFIG
# ===============================
DATABASE_URL = os.getenv("DATABASE_URL") # from .env file