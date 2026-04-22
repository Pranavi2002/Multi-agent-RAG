from sqlalchemy.orm import Session
from db.models import QueryHistory

# save query and output
def save_query(
    db: Session,
    question: str,
    answer: str,
    avg_similarity: float,
    max_similarity: float,
    latency: float
):
    record = QueryHistory(
        question=question,
        answer=answer,
        avg_similarity=avg_similarity,
        max_similarity=max_similarity,
        latency=latency
    )
    db.add(record)
    db.commit()

# 🔥 NEW: fetch all history
def get_all_history(db: Session):
    return db.query(QueryHistory).order_by(QueryHistory.created_at.desc()).all()