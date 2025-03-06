from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+asyncpg://")

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session maker
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

# Define the base class for models
Base = declarative_base()

# ✅ Async function to create tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ✅ Run table creation when the app starts
async def init_db():
    await create_tables()

# Dependency to get a new async database session
async def get_db():
    async with async_session_maker() as session:
        yield session
