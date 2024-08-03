from aiogram import Router, types
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from app.commands import ADD_NOTE, MY_NOTES
from app.db.user import create_user, get_user, update_user
from app.states import UserRegisterGroup

COMMANDS_INFO = (
    f"Для того, чтобы создать новую заметку, используй команду /{ADD_NOTE}\n"
    f"Для того, чтобы посмотреть все созданные заметки, напиши команду /{MY_NOTES}"
)


async def start(message: types.Message, state: FSMContext) -> None:
    if message.from_user is None:
        return
    telegram_id = message.from_user.id
    user = await get_user(telegram_id)
    if user is None:
        user = await create_user(telegram_id)
        response = f"Привет, {message.from_user.full_name}!\nДавай знакомиться.\nНапиши, как тебя зовут"
        await message.answer(response)
        await state.set_state(UserRegisterGroup.wait_name)
    else:
        if not user["name"]:
            await message.answer("Пожалуйста, напиши, как тебя зовут")
            await state.set_state(UserRegisterGroup.wait_name)
        elif not user["email"]:
            await message.answer("Пожалуйста, напиши свой email")
            await state.set_state(UserRegisterGroup.wait_email)
        else:
            await message.answer(f"Кажется, мы уже знакомы\n{COMMANDS_INFO}")
            await state.set_state(UserRegisterGroup.registered)


async def reg_name(message: types.Message, state: FSMContext) -> None:
    if message.from_user is None:
        return
    user_state = await state.get_state()
    if user_state == UserRegisterGroup.wait_name:
        await update_user(message.from_user.id, "name", message.text)
        await message.answer(f"Очень приятно, {message.text}!\nА какой у тебя email?")
        await state.set_state(UserRegisterGroup.wait_email)
    else:
        await update_user(message.from_user.id, "email", message.text)
        await message.answer(f"Отлично!\n{COMMANDS_INFO}")
        await state.set_state(UserRegisterGroup.registered)


def start_router() -> Router:
    router = Router()

    router.message.register(start, CommandStart())
    router.message.register(reg_name, StateFilter(UserRegisterGroup.wait_name, UserRegisterGroup.wait_email))

    return router
