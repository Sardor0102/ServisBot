from buttons.inline_btn import get_services_btn
from database.postgres_conn import get_all_services, get_user, update_username
from util.loader import *

from buttons.reply_btn import reply_btn_builder, remove
from util.texts import button_texts
from util.state import SettingsState, EmployeeState

MAIN_TEXTS = button_texts['main_menu']

@dp.message(SettingsState.settings, F.text == "Orqaga")
@dp.message(EmployeeState.start, F.text == "Orqaga")
async def main_menu(message: Message, state: FSMContext, back = False):
    if not back:
        await state.clear()
        await state.update_data({'id': message.from_user.id})
        user = await get_user(message.from_user.id)
        if user[2] != message.from_user.username:
            new_username = f"@{message.from_user.username}" if message.from_user.username else "None"
            await update_username(user[0], new_username)
        await state.update_data({'id': message.from_user.id})
    texts = [text for text in MAIN_TEXTS.values()]
    btn = reply_btn_builder(texts, [2, 1, 1])
    await message.answer("Asosiy menyu:", reply_markup=btn)


@dp.message(F.text == MAIN_TEXTS['add_order'])
async def start_order_remover(message: Message, state: FSMContext):
    await state.update_data({'id': message.from_user.id})
    await message.answer(text="Servis buyurtma qilish boshlandi:", reply_markup=remove())
    await start_order(message)


async def start_order(message: Message):
    service = await get_all_services()
    btn = get_services_btn(service)
    await message.answer("Kerakli servisni tanlang:", reply_markup=btn)


