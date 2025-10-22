from sqlmodel import SQLModel, Session, create_engine
from contextlib import contextmanager
from typing import Generator
from app.config import settings



DATABASE_URL = settings.database_url


engine = create_engine(DATABASE_URL, echo=True)


def get_db() -> Session:
    session = Session(engine)
    try:
        yield session 
    finally:
        session.close()

# Function to create tables
def create_tables():
    SQLModel.metadata.create_all(engine)
