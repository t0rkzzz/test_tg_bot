import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import telegram_config
from app.handlers import note_router, start_router
from app.reminder.worker import notify_users


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(start_router())
    dp.include_router(note_router())
    dp.startup.register(notify_users)
    bot = Bot(token=telegram_config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
