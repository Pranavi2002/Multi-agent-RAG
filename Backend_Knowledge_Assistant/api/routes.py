# includes database integration
# includes history route

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.schemas import QueryRequest
from services.rag_service import RAGService

from db.database import SessionLocal
from db.history_repo import get_all_history

router = APIRouter()

rag_service = RAGService()

# 🔥 initialize vector store once at startup (ok for now)
rag_service.initialize_vector_store()


# ============================
# DB Dependency (BEST PRACTICE)
# ============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================
# QUERY ENDPOINT
# ============================
@router.post("/query")
def query(request: QueryRequest, db: Session = Depends(get_db)):

    # 🔥 pass DB into RAG service for logging
    return rag_service.query(request.question, db)


# ============================
# HISTORY ENDPOINT
# ============================
@router.get("/history")
def history(db: Session = Depends(get_db)):

    records = get_all_history(db)

    return [
        {
            "id": r.id,
            "question": r.question,
            "answer": r.answer,
            "avg_similarity": r.avg_similarity,
            "max_similarity": r.max_similarity,
            "latency": r.latency,
            "created_at": r.created_at
        }
        for r in records
    ]