from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://pulseflow:pulseflow_dev@localhost:5432/pulseflow"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Note the +asyncpg part
DATABASE_URL = "postgresql+asyncpg://pulseflow:pulseflow_dev@localhost:5432/pulseflow"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()