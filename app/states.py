from aiogram.fsm.state import State, StatesGroup


class UserRegisterGroup(StatesGroup):
    new = State()
    wait_name = State()
    wait_email = State()
    registered = State()


class NoteCreationGroup(StatesGroup):
    wait_text = State()
    wait_date = State()
    wait_time = State()
