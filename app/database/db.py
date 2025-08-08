from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy import create_engine
from app.config import settings


# Create SQLite DB in root folder
DATABASE_URL = settings.database_url

SYNC_DATABASE_URL = DATABASE_URL.replace("sqlite+aiosqlite://", "sqlite://")

# Async engine for the application
engine = create_async_engine(DATABASE_URL, echo=True)

#Sync engine for the alembic migrations
sync_engine=create_engine(SYNC_DATABASE_URL, echo=True)


# Async session maker
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


# Async DB dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Function to create tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

