from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    full_name = State()
    phone_number = State()
    comment = State()


class SettingsState(StatesGroup):
    language = State()
    settings = State()
    user_data = State()
    set_user = State()
    set_user_fullname = State()
    set_phone_fullname = State()
    delete_user = State()


class EmployeeState(StatesGroup):
    start = State()
    first_name = State()
    last_name = State()
    phone_number = State()
    service = State()
    end = State()


