from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

# from ....external.clickhouse.connection import get_client
from ....external.postgres.connection import get_connection_pool
from .core import (
    get_date_distribution_of_records,
    get_date_distribution_of_records_0,
    get_date_distribution_of_records_1,
    get_date_distribution_of_records_2,
    get_grade_distribution_of_records,
)

clients_router = APIRouter(prefix="/api/v1/clients", tags=["clients"])


@clients_router.get("/grades_distribution")
async def grades_distribution(pool=Depends(get_connection_pool)) -> dict:
    return await get_grade_distribution_of_records(pool)


@clients_router.get("/date_distribution")
async def date_distribution(pool=Depends(get_connection_pool)) -> dict:
    return await get_date_distribution_of_records(pool)


@clients_router.get("/date_distribution_1")
async def date_distribution_1(pool=Depends(get_connection_pool)) -> dict:
    return await get_date_distribution_of_records_1(pool)


@clients_router.get("/date_distribution_0")
async def date_distribution_0(pool=Depends(get_connection_pool)) -> dict:
    return await get_date_distribution_of_records_0(pool)


@clients_router.get("/date_distribution_2")
async def date_distribution_2(pool=Depends(get_connection_pool)) -> dict:
    return await get_date_distribution_of_records_2(pool)
