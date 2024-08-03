from datetime import datetime
from functools import partial
from typing import Literal

from app.db.connection import get_connection
from app.db.query_getter import from_file
from app.schemas import Note, NoteToSend

file_getter = partial(from_file, "note")


async def create_note(user_id: int) -> int:
    async with get_connection() as conn:
        note = await conn.fetchrow(file_getter("create"), user_id)
    return note["id"]


async def update_note(
    note_id: int,
    field: Literal["text", "reminder_time", "notification_sent"],
    value: str | datetime,
) -> str:
    async with get_connection() as conn:
        result = await conn.execute(file_getter(f"update_{field}"), value, note_id)
        await conn.execute("commit")
        return result


async def list_notes(user_id: int) -> list[Note]:
    async with get_connection() as conn:
        notes = await conn.fetch(file_getter("list"), user_id)
    return [Note.model_validate(dict(note)) for note in notes]


async def list_upcoming(notes_till: datetime) -> list[NoteToSend]:
    async with get_connection() as conn:
        notes = await conn.fetch(file_getter("list_range"), notes_till)
    return [NoteToSend.model_validate(dict(note)) for note in notes]
