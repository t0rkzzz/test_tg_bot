from datetime import time
from typing import Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


class WatchCallback(CallbackData, prefix="watch"):
    act: Literal["hour", "minute"]
    hour: int | None = None
    minute: int | None = None


def inline_markup(func):
    def inner(*args, **kwargs):
        return InlineKeyboardMarkup(row_width=6, inline_keyboard=func(*args, **kwargs))

    return inner


class DialogWatch:
    @inline_markup
    def get_hour_kb(self):
        return [
            [
                InlineKeyboardButton(text=str(hour), callback_data=WatchCallback(act="hour", hour=hour).pack())
                for hour in range(row * 6 + 1, row * 6 + 7)
            ]
            for row in range(4)
        ]

    @inline_markup
    def get_minute_kb(self, hour: int):
        return [
            [
                InlineKeyboardButton(
                    text=str(minute), callback_data=WatchCallback(act="minute", hour=hour, minute=minute).pack()
                )
                for minute in range(0, 60, 10)
            ]
        ]

    async def process_selection(self, query: CallbackQuery, time_cb: WatchCallback) -> tuple[time, bool]:
        return_data = (False, None)
        if time_cb.act == "hour":
            await query.message.edit_reply_markup(text="Теперь минуты:", reply_markup=self.get_minute_kb(time_cb.hour))
        if time_cb.act == "minute":
            return_data = (True, time(time_cb.hour, time_cb.minute))
        return return_data

    def start_watch(self):
        return self.get_hour_kb()
