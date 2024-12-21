import json

from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from pydantic import BaseModel

# from ....external.clickhouse.connection import get_client
from ....external.postgres.connection import get_connection_pool
from ....settings import settings
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


class GigachatQuery(BaseModel):
    query: str


@clients_router.post("/query_gigachat")
async def query_gigachat(query: GigachatQuery):

    import requests

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload = {"scope": "GIGACHAT_API_PERS"}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": "6f0f9a3f-4794-4d8b-a809-3b7bc0b598b5",
        "Authorization": f"Basic {settings.gigachat_token}",
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, verify=False
    )
    token = response.json()["access_token"]

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    prompt = f"""Присвой какую-либо группу тексту: {query.query}\n
Группировка осуществляется по трем категориям:
1.     Претензия
2.     Предложение
3.     Благодарность
А также проанализируй причину:
- Ошибка сотрудника (в тексте есть ФИО / наименование офиса / слова «сотрудник/работник/человек/оператор/кассир/операционист и др.»)
- Несогласие клиента с тарифами, условиями обслуживания (в тексте есть слова «Тариф/Правила/Договор/заключение/расторжение и др.»
- Технический сбой (в тексте есть слова «Сбой/Авария/Замедление/Проблема/Завис/Погас и др.)
- Скорость обслуживания (в тексте есть слова «Медленно/Быстро/Оперативно/Скорость/Производительность и др.).
Отвечай строго двумя пунктами - категория и причина. Категория - та, что подходит больше всего по смыслу. Причину нужно найти внутри текста по всем пунктам, которые есть.
Отвечай в слудующем виде: 'Категория: *категория*, Причина: *причина*'
    """
    payload = json.dumps(
        {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": prompt}],
            "n": 1,
            "stream": False,
            "max_tokens": 512,
            "repetition_penalty": 1,
            "update_interval": 0,
        }
    )
    headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}

    response = requests.request(
        "POST", url, headers=headers, data=payload, verify=False
    )

    return response.json()["choices"][0]["message"]["content"]
