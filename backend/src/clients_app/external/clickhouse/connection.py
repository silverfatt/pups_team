import sys

from clickhouse_driver import Client
from loguru import logger

from ...settings import settings


class DataBase:
    client: Client = None  # type: ignore


db = DataBase()


async def connect_clickhouse():
    logger.info("Initializing Clickhouse connection.")

    try:
        db.client = Client(settings.clickhouse_host)  # type: ignore

    except Exception as exc:
        logger.error("Failed connect to Clickhouse.")
        logger.error(str(exc))
        sys.exit(1)

    logger.info("Successfully initialized Clickhouse connection.")


def get_client() -> Client:

    return db.client
