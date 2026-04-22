from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from db.database import Base

class QueryHistory(Base):
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    avg_similarity = Column(Float)
    max_similarity = Column(Float)
    latency = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())