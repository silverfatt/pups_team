import ssl
import sys

from asyncpg import create_pool
from asyncpg.pool import Pool
from loguru import logger

from ...settings import settings


class DataBase:
    pool: Pool = None  # type: ignore
    results_pool: Pool = None  # type: ignore


db = DataBase()


async def connect_postgres():
    logger.info("msg='Initializing PostgreSQL connection.'")

    try:
        db.pool = await create_pool(  # type: ignore
            user=settings.postgres_user,
            password=settings.postgres_password,
            host=settings.postgres_host,
            port=settings.postgres_port,
            database=settings.postgres_database,
            min_size=0,
            max_size=15,
            max_inactive_connection_lifetime=60,
        )

    except Exception as exc:
        logger.error("msg='Failed connect to PostgreSQL.'")
        raise exc

    logger.info("msg='Successfully initialized PostgreSQL connection.'")


async def disconnect_postgres():
    logger.info("msg='Closing PostgreSQL connections.'")
    await db.pool.close()


def get_connection_pool() -> Pool:
    """
    https://magicstack.github.io/asyncpg/current/usage.html#connection-pools
    """

    return db.pool
