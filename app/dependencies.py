from sqlalchemy.ext.asyncio import async_sessionmaker

from app.database import engine

async_session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
