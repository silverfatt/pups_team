import json
import logging
import os
import sys

from fastapi import Request
from fastapi.applications import FastAPI
from loguru import logger
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import _StreamingResponse
from starlette.middleware.cors import CORSMiddleware

from .api.v1.clients.views import clients_router
from .external.clickhouse.connection import connect_clickhouse
from .external.postgres.connection import connect_postgres, disconnect_postgres

# from .external.postgres.connection import connect_postgres, disconnect_postgres
# from .settings import settings


app = FastAPI(
    title="Analytics Backend",
    docs_url="/api/docs",
    version=os.getenv("APP_VERSION", default="DEV"),
)


logger_config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<level>{level}: {message}</level>",  # noqa
        }
    ]
}


def create_app():
    logger.remove()
    app.include_router(clients_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_event_handler("startup", connect_clickhouse)
    app.add_event_handler("startup", connect_postgres)
    app.add_event_handler("shutdown", disconnect_postgres)
    # app.add_event_handler("shutdown", disconnect_postgres)
    return app
