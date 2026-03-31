from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from src.schemas.setting import setting
from sqlmodel import SQLModel, text
from src.models import Books, Users

engine = create_async_engine(
    url=setting.DATABASE_URL,
    echo=True
)

asyncSessionmaker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_= AsyncSession
)


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))

        print("✅ Postgres connection working fine")
    except Exception as e:
        print("❌ Postgres connection failed:", e)
        raise e  # crash app


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with asyncSessionmaker() as session:
        yield session