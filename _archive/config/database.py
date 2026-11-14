import os
from sqlmodel import create_engine, Session, SQLModel

# v0.6 Production Database Configuration
DB_URL = os.getenv("DATABASE_URL", "sqlite:///agentic_core/data/workstation.db")

engine = create_engine(
    DB_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
