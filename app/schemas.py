from datetime import datetime
from pydantic import BaseModel


class Note(BaseModel):
    text: str
    reminder_time: datetime | None


class NoteToSend(BaseModel):
    id: int
    text: str
    telegram_id: int
