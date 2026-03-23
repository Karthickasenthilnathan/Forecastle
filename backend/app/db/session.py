from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings

DATABASE_URL = settings.DATABASE_URL

# Create engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Dependency
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session