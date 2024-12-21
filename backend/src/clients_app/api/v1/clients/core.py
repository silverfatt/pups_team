from asyncpg import Pool

# async def get_all_records(pool: Pool):
#     query = "SELECT * FROM default.NewTable"
#     return client.execute(query)

rating_map = {0: "Негативные", 1: "Нейтральные", 2: "Положительные"}


async def get_grade_distribution_of_records(pool: Pool) -> dict:
    query = "SELECT rating_value, COUNT(*) FROM clients GROUP BY rating_value ORDER BY rating_value"
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(query)
    return {rating_map[item[0]]: item[1] for item in res} if res else {}


async def get_date_distribution_of_records(pool: Pool) -> dict:
    query = "SELECT  EXTRACT(month FROM comment_date),COUNT(*) FROM clients GROUP BY EXTRACT(month FROM comment_date) ORDER BY EXTRACT(month FROM comment_date)"

    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(
                query,
            )
    return {f"2024-{str(item[0])}": item[1] for item in res} if res else {}


async def get_date_distribution_of_records_1(pool: Pool) -> dict:
    query = "SELECT  EXTRACT(month FROM comment_date),COUNT(*) FROM clients WHERE rating_value = 1 GROUP BY EXTRACT(month FROM comment_date) ORDER BY EXTRACT(month FROM comment_date)"

    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(
                query,
            )
    return {f"2024-{str(item[0])}": item[1] for item in res} if res else {}


async def get_date_distribution_of_records_0(pool: Pool) -> dict:
    query = "SELECT  EXTRACT(month FROM comment_date),COUNT(*) FROM clients WHERE rating_value = 0 GROUP BY EXTRACT(month FROM comment_date) ORDER BY EXTRACT(month FROM comment_date)"

    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(
                query,
            )
    return {f"2024-{str(item[0])}": item[1] for item in res} if res else {}


async def get_date_distribution_of_records_2(pool: Pool) -> dict:
    query = "SELECT  EXTRACT(month FROM comment_date),COUNT(*) FROM clients WHERE rating_value = 2 GROUP BY EXTRACT(month FROM comment_date) ORDER BY EXTRACT(month FROM comment_date)"

    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(
                query,
            )
    return {f"2024-{str(item[0])}": item[1] for item in res} if res else {}
