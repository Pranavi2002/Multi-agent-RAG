# don't run it

# this does:
# using raw SQL
# ignoring ORM models
# duplicating schema definition

# 👉 This creates two sources of truth:
# ORM model (models.py)
# raw SQL table (init_db.py)

# That leads to:
# mismatched columns
# confusion
# bugs later when you update schema

from sqlalchemy import create_engine, text
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS query_history (
            id SERIAL PRIMARY KEY,
            query TEXT,
            response TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """))
        conn.commit()