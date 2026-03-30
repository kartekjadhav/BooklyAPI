from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from src.schemas.setting import setting
from sqlmodel import SQLModel
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
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with asyncSessionmaker() as session:
        yield session