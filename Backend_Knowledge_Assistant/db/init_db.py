# correct approach for ORM tables, if Base is already created

from db.database import engine, Base

def init_db():
    Base.metadata.create_all(bind=engine)