import asyncio
from datetime import datetime, timedelta

from telethon import TelegramClient

from app.config import telegram_config
from app.db.note import list_upcoming, update_note
from app.schemas import NoteToSend


async def notify_user(data: NoteToSend, bot: TelegramClient) -> None:
    await bot.send_message(data.telegram_id, f"Через 10 минут: {data.text}")
    await update_note(data.id, "notification_sent", True)


async def send_notifications(bot: TelegramClient):
    while True:
        tasks = []
        notes_till = datetime.now() + timedelta(minutes=10)
        for notification in await list_upcoming(notes_till):
            tasks.append(asyncio.create_task(notify_user(notification, bot)))
        await asyncio.sleep(5)
        if tasks:
            await asyncio.wait(tasks)


async def notify_users():
    bot = await TelegramClient(
        "bot",
        api_id=telegram_config.api_id,
        api_hash=telegram_config.api_hash,
    ).start(bot_token=telegram_config.token)
    asyncio.create_task(send_notifications(bot))
