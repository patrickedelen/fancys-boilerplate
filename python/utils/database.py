import logging
from asyncio import current_task
from collections import defaultdict, deque
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncIterator, DefaultDict, Deque, Set

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.pool import NullPool


from utils.envs import envs

logger = logging.getLogger(__name__)


def get_base_db_url(
    postgres_user: str | None = None,
    postgres_password: str | None = None,
    postgres_db: str | None = None,
    postgres_host: str | None = None,
    postgres_port: str | None = None,
) -> str:
    if postgres_user is None:
        postgres_user = envs.POSTGRES_USER
    if postgres_password is None:
        postgres_password = envs.POSTGRES_PASSWORD
    if postgres_db is None:
        postgres_db = envs.POSTGRES_DB
    if postgres_host is None:
        postgres_host = envs.POSTGRES_HOST
    if postgres_port is None:
        postgres_port = envs.POSTGRES_PORT

    return f"{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"


def get_async_db_url() -> str:
    return f"postgresql+asyncpg://{get_base_db_url()}"


def get_sync_db_url() -> str:
    return f"db+postgresql://{get_base_db_url()}"


# create engine once on initial db access
# this saves resources instead of creating a new engine each time
_engine_async = None


async def get_shared_async_engine() -> AsyncEngine:
    global _engine_async
    if _engine_async is None:
        database_url = get_async_db_url()
        # https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine

        logger.warning("Starting async engine with pool")

        _engine_async = create_async_engine(
            database_url,
            isolation_level="READ COMMITTED",
            pool_size=100,
            pool_recycle=3600,
            connect_args={"timeout": 120},
        )

    return _engine_async


async def close_shared_async_engine() -> None:
    # close the engine and its connections on teardown
    global _engine_async
    if _engine_async:
        await _engine_async.dispose()


async def get_shared_async_session_factory() -> async_sessionmaker:
    # get the SQLAlchemy session factory for the database
    engine = await get_shared_async_engine()
    return async_sessionmaker(
        autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
    )


# use `with` keyword to automatically close db session when done accessing it
@asynccontextmanager
async def db_session() -> AsyncIterator[AsyncSession]:
    async_session_factory = await get_shared_async_session_factory()
    db_session = async_scoped_session(async_session_factory, scopefunc=current_task)
    session = db_session()
    assert isinstance(session, AsyncSession)
    try:
        yield session
    finally:
        await db_session.remove()
