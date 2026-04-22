# includes database integration
# no history route

from fastapi import APIRouter
from models.schemas import QueryRequest
from services.rag_service import RAGService
from db.database import SessionLocal   # ✅ ADD THIS

router = APIRouter()

rag_service = RAGService()
rag_service.initialize_vector_store()


@router.post("/query")
def query(request: QueryRequest):

    db = SessionLocal()   # ✅ CREATE DB SESSION PER REQUEST

    try:
        response = rag_service.query(request.question, db)  # ✅ PASS DB
        return response
    finally:
        db.close()  # ✅ ALWAYS CLOSE