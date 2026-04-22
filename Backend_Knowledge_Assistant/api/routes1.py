# no database integration

from fastapi import APIRouter
from models.schemas import QueryRequest
from services.rag_service import RAGService

router = APIRouter()

# Create singleton service
rag_service = RAGService()

# 🔥 IMPORTANT: initialize vector store at startup
rag_service.initialize_vector_store()


@router.post("/query")
def query(request: QueryRequest):
    return rag_service.query(request.question)