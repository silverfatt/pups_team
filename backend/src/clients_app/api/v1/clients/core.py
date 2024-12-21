from asyncpg import Pool

# async def get_all_records(pool: Pool):
#     query = "SELECT * FROM default.NewTable"
#     return client.execute(query)


async def get_grade_distribution_of_records(pool: Pool) -> dict:
    query = "SELECT rating_value, COUNT(*) FROM clients GROUP BY rating_value ORDER BY rating_value"
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(query)
    return {str(item[0]): item[1] for item in res} if res else {}  # type: ignore


async def get_date_distribution_of_records(pool: Pool) -> dict:
    query = "SELECT comment_date, COUNT(*) FROM clients GROUP BY comment_date ORDER BY comment_date"
    async with pool.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(
                query,
            )
    return {str(item[0]): item[1] for item in res} if res else {}  # type: ignore
