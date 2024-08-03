from functools import partial
from typing import Literal

from asyncpg import Record

from app.db.connection import get_connection
from app.db.query_getter import from_file

file_getter = partial(from_file, "user")


async def get_user(telegram_id: int) -> Record | None:
    async with get_connection() as conn:
        return await conn.fetchrow(file_getter("get"), telegram_id)


async def create_user(telegram_id: int) -> int:
    async with get_connection() as conn:
        return await conn.fetchrow(file_getter("create"), telegram_id)


async def update_user(telegram_id: int, field: Literal["name", "email"], value: str) -> str:
    async with get_connection() as conn:
        return await conn.execute(file_getter(f"update_{field}"), value, telegram_id)
