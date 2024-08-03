from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

from app.commands import ADD_NOTE, MY_NOTES
from app.db.note import create_note, list_notes, update_note
from app.db.user import get_user
from app.handlers.buttons import DialogWatch, WatchCallback
from app.states import NoteCreationGroup


async def add_note(message: types.Message, state: FSMContext) -> None:
    telegram_id = message.from_user.id
    user = await get_user(telegram_id)
    if not user:
        return
    note_id = await create_note(user["id"])
    await message.answer("О чем нужно напомнить?")
    await state.set_data({"note_id": note_id})
    await state.set_state(NoteCreationGroup.wait_text)


async def set_note_text(message: types.Message, state: FSMContext) -> None:
    note_id = (await state.get_data())["note_id"]
    await update_note(note_id, "text", message.text)
    await message.answer(
        "Когда напомнить?",
        reply_markup=await SimpleCalendar().start_calendar(),
    )
    await state.set_state(NoteCreationGroup.wait_date)


async def set_note_date(
    callback_query: CallbackQuery,
    callback_data: CallbackData,
    state: FSMContext,
) -> None:
    date: datetime
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        note_id = (await state.get_data())["note_id"]
        await state.set_data({"reminder_date": date.date(), "note_id": note_id})
        await state.set_state(NoteCreationGroup.wait_time)
        await callback_query.message.answer("А во сколько?", reply_markup=DialogWatch().start_watch())
        await callback_query.message.delete()


async def set_note_time(
    callback_query: CallbackQuery,
    callback_data: CallbackData,
    state: FSMContext,
) -> None:
    selected, selected_time = await DialogWatch().process_selection(callback_query, callback_data)
    state_data = await state.get_data()
    if selected:
        reminder_date = datetime.combine(state_data["reminder_date"], selected_time)
        await update_note(state_data["note_id"], "reminder_time", reminder_date)
        await callback_query.message.answer("Напоминание создано!")
        await callback_query.message.delete()
        await state.set_state(None)


async def my_notes(message: types.Message) -> None:
    user = await get_user(message.from_user.id)
    if not user:
        return
    notes = await list_notes(user["id"])
    if notes:
        await message.answer("\n".join([f"{note.reminder_time}: {note.text}" for note in notes]))
    else:
        await message.answer("У тебя пока нет заметок.")


def note_router() -> Router:
    router = Router()

    router.message.register(add_note, Command(ADD_NOTE))
    router.message.register(set_note_text, StateFilter(NoteCreationGroup.wait_text))
    router.callback_query.register(
        set_note_date,
        SimpleCalendarCallback.filter(),
        StateFilter(NoteCreationGroup.wait_date),
    )
    router.callback_query.register(set_note_time, WatchCallback.filter(), StateFilter(NoteCreationGroup.wait_time))
    router.message.register(my_notes, Command(MY_NOTES))

    return router
