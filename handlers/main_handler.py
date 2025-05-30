from aiogram.filters import CommandStart

from database.postgres_conn import add_user, check_user
from buttons.reply_btn import *

from handlers.user_handler import *
from handlers.employee_handler import *
from handlers.add_order import *
from handlers.settings import *


@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    if await check_user(message.from_user.id):
        await state.update_data({'id': message.from_user.id})
        await message.answer("<b>Hisobga muvaffaqiyatli kirildi</b>", parse_mode='html')
        await main_menu(message, state)
    else:
        await message.answer(f"<b>Assalomu Alaykum!</b>\n\nIltimos, to'liq ismingizni yozing:", parse_mode='html')
        await state.set_state(UserState.full_name)  


@dp.message(UserState.full_name)
async def get_full_name(message: Message, state: FSMContext):
    btn = get_phone_number()
    await state.update_data({"fullname": message.text})
    await message.answer("Yahshi, endi telefon raqamingizni qoldirip keting", reply_markup=btn)
    await state.set_state(UserState.phone_number)


@dp.message(UserState.phone_number)
async def get_phone_number_name(message: Message, state: FSMContext):
    if not message.contact:
        await get_full_name(message, state)
        return
    user_data = {
        "chat_id": message.from_user.id,
        "fullname": (await state.get_data())['fullname'],
        "username": f"@{message.from_user.username}" if message.from_user.username else "None",
        "phone": message.contact.phone_number,
    }
    await add_user(**user_data)
    await state.clear()
    await message.answer("<b>Hisobga muvaffaqiyatli kirildi</b>", parse_mode='html', reply_markup=remove())
    await main_menu(message, state)




