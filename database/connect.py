from contextlib import asynccontextmanager

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession


Base = declarative_base()


@asynccontextmanager
async def get_session() -> AsyncSession:
    engine = create_async_engine(
        url='sqlite+aiosqlite:///data/database.db',
        echo=False,
    )
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    async with async_session() as session:
        session: AsyncSession
        try:
            yield session
        except Exception:
            await session.rollback()
            raise Exception
        finally:
            await session.close()
