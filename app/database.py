import os

from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(f"postgresql+asyncpg://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@postgres/{os.environ['POSTGRES_DB']}", echo=True if os.environ.get("DEBUG") else False)
