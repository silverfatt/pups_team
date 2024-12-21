import csv
import re
import ssl
import sys
from asyncio import run
from datetime import date, datetime, timedelta
from time import sleep

import requests
import ujson
from asyncpg import create_pool
from asyncpg.pool import Pool
from bs4 import BeautifulSoup
from loguru import logger
from telegram import Bot


class DataBase:
    pool: Pool = None  # type: ignore
    results_pool: Pool = None  # type: ignore


db = DataBase()


async def connect_postgres():
    logger.info("msg='Initializing PostgreSQL connection.'")

    try:
        db.pool = await create_pool(  # type: ignore
            user="postgres",
            password="Kendol2002",
            host="localhost",
            port=5432,
            database="clients",
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


async def insert_rows(pool: Pool, data):
    query = """
    INSERT INTO clients (text, comment_date, rating_value)
    VALUES ($1, $2, $3)
    """
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.executemany(query, data)
            logger.debug(res)


TOKEN = "7551524394:AAFmCgtnnSuAWwLVtWAJwkdLYFsEiQYNENs"
CHAT_ID = 729118904

# Set headers for the requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

# URL template for the comments pages
URL_TEMPLATE = "https://www.banki.ru/services/responses/bank/promsvyazbank/?page={page_index}&is_countable=on"

HOURS_INTERVAL = 24


class TgBot:
    bot = None


tg_bot = TgBot()


async def connect_to_telegram():
    tg_bot.bot = Bot(TOKEN)


def get_bot():
    return tg_bot.bot


async def send_stats_to_telegram(result):
    bot = get_bot()
    stats = {
        "Положительные": 0,
        "Нейтральные": 0,
        "Негативные": 0,
    }
    for i in range(len(result)):
        if int(result[i][2]) >= 4:
            stats["Положительные"] += 1
        elif 3 <= int(result[i][2]) < 4:
            stats["Нейтральные"] += 1
        else:
            stats["Негативные"] += 1
    amount = len(result)
    # >=4 3<=x<=4  <3
    date_str = f"{str(date.today())} - {date.today() - timedelta(days=1)}"
    message = f"Статистика посчитана за {date_str}. Количество записей: {amount}, положительные отзывы: {stats['Положительные']}, негативные отзывы: {stats['Негативные']}, нейтральные отзывы: {stats['Нейтральные']}"
    await bot.send_message(chat_id=CHAT_ID, text=message)  # type: ignore


async def clean_comment_text(text: str) -> str:
    """
    Clean up the text of the comment by removing unwanted characters.
    """
    return re.sub(r"[^a-zA-Zа-яА-ЯёЁ0-9\s.,?!\-:;()]+", "", text)


async def get_comments(page_index: int):
    url = URL_TEMPLATE.format(page_index=page_index)

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_index}: {e}")
        return []

    # Parse the HTML page
    soup = BeautifulSoup(response.text, "html.parser")

    # Look for the JSON data embedded in a script tag
    script_tag = soup.find("script", {"type": "application/ld+json"})

    if script_tag:
        try:
            data = (
                script_tag.string.strip()
                .replace("&quot;", "")
                .replace("&lt;p&gt;", "")
                .replace("&lt;/p&gt;", "")
                .replace("\u00A0", "")
            )
            data = re.sub(r'\\[^"\\/bfnrtu]', "", data)
            data = ujson.loads(data)

            reviews = data.get("review", [])
            if not reviews:
                print(f"No reviews found on page {page_index}.")
                return []

            # Extract the required fields
            result = []
            for record in reviews:
                comment = await clean_comment_text(record.get("description", ""))
                date_published = record.get("datePublished", "N/A")
                best_rating = record.get("reviewRating", {}).get("ratingValue", "N/A")
                result.append((comment, date_published, best_rating))
            # print(result)
            # print(result)
            result = [
                item
                for item in result
                if datetime.strptime(item[1], "%Y-%m-%d %H:%M:%S")
                > datetime.now() - timedelta(hours=HOURS_INTERVAL)
            ]

            for i in range(len(result)):
                result[i] = (
                    result[i][0],
                    datetime.strptime(result[i][1], "%Y-%m-%d %H:%M:%S"),
                    int(result[i][2]),
                )
            print(result)
            return result

        except (ujson.JSONDecodeError, KeyError) as e:
            print(f"Error parsing JSON on page {page_index}: {e}")
            return []
    else:
        print(f"Script tag with JSON not found on page {page_index}.")
        return []


async def main():
    while True:
        await connect_to_telegram()
        await connect_postgres()
        page_index = 1

        comments = await get_comments(page_index)
        print(f"Page {page_index} comments: {len(comments)} found.")
        await insert_rows(get_connection_pool(), comments)
        await send_stats_to_telegram(comments)
        sleep(HOURS_INTERVAL * 60)


if __name__ == "__main__":
    run(main())
