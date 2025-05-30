from util.loader import *
from util.texts import button_texts
from util.state import SettingsState
from buttons.reply_btn import reply_btn_builder, remove, set_user_data_btn
from buttons.inline_btn import user_data_btn
from database.postgres_conn import get_user, update_user, delete_user_pg

bs = button_texts['settings']


@dp.message(SettingsState.user_data, F.text == "Orqaga")
@dp.message(F.text == button_texts['main_menu']['settings'])
async def settings(message: Message, state: FSMContext):
    texts = [bs['set_lang'], bs['user_data'], "Orqaga"]
    btn = reply_btn_builder(texts, [1, True])
    await message.answer("Sozlamalar:", reply_markup=btn)
    await state.set_state(SettingsState.settings)


@dp.message(SettingsState.settings, F.text == bs['set_lang'])
async def set_language(message: Message, state: FSMContext):
    texts = ["English", "Русский", "O'zbek"]
    btn = reply_btn_builder(texts, [1, True])
    await message.answer("Ok, choose the language:", reply_markup=btn)
    await state.set_state(SettingsState.language)


@dp.message(SettingsState.language)
async def language_set(message: Message, state: FSMContext):
    lang = message.text
    if lang == "English":
        await message.answer("Language set to English!")
    elif lang == "Русский":
        await message.answer("Язык изменен на Русский!")
    elif lang == "O'zbek":
        await message.answer("Til o'zbek tiliga o'zgartirildi!")
    else:
        await message.answer("There is wrong language!")
    await settings(message, state)


@dp.message(SettingsState.set_user, F.text == "Orqaga")
@dp.message(SettingsState.settings, F.text == bs['user_data'])
async def settings_user_data(message: Message, state: FSMContext):
    texts = ["Mening malumotlarim", "O'zgartirish", "O'chirib tashlash", "Orqaga"]
    btn = reply_btn_builder(texts, [1, True])
    await message.answer("Bo'limni tanlang:", reply_markup=btn)
    await state.set_state(SettingsState.user_data)


@dp.message(SettingsState.user_data, F.text == "Mening malumotlarim")
async def show_user(message: Message):
    user = await get_user(message.from_user.id)
    is_employee = "Ha" if user[4] else "Yo'q"
    context = f"<b>Ism:</b> {user[1]}\n<b>Username:</b> {user[2]}\n<b>Telefon raqam:</b> {user[3]}\n<b>Servisning ishchisimi:</b> {is_employee}"
    await message.answer(context, parse_mode='html')


@dp.message(SettingsState.user_data, F.text == "O'zgartirish")
async def set_user_data(message: Message, state: FSMContext):
    btn = set_user_data_btn()
    await message.answer("Bo'limni tanlang:", reply_markup=btn)
    await state.set_state(SettingsState.set_user)


@dp.message(SettingsState.set_user)
async def set_user_data_value(message: Message, state: FSMContext):
    if message.text == "Ism":
        await message.answer("Yahshi, yangi ism kiriting:", reply_markup=remove())
        await state.set_state(SettingsState.set_user_fullname)
    elif message.contact:
        await state.update_data({'phone': message.contact.phone_number})
        btn = user_data_btn()
        await message.answer(f"Yangi telefon raqamingiz: <b>{message.contact.phone_number}</b>\n\nBuni tasdiqlaysizmi?", reply_markup=btn, parse_mode='html')


@dp.message(SettingsState.set_user_fullname)
async def get_user_full_name(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    btn = user_data_btn()
    await message.answer(f"Yangi ismingiz: <b>{message.text}</b>\n\nBuni tasdiqlaysizmi?", reply_markup=btn, parse_mode='html')



@dp.callback_query(F.data.startswith("data"))
async def set_user_btn(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if callback.data.endswith("done"):
        await update_user(**(await state.get_data()))
        await callback.message.answer("Malumotlaringiz o'zgartirildi!")
    await settings_user_data(callback.message, state)


@dp.message(SettingsState.user_data, F.text == "O'chirib tashlash")
async def delete_user_data(message: Message, state: FSMContext):
    await message.answer("Hisobingizni o'chirish uchun \"Tasdiqlayman, hisob ochirilsin\" deb kiriting, bekor qilish uchun istalgan matni kiriting:", reply_markup=remove())
    await state.set_state(SettingsState.delete_user)


@dp.message(SettingsState.delete_user)
async def delete_user(message: Message, state: FSMContext):
    if message.text == "Tasdiqlayman, hisob ochirilsin":
        await delete_user_pg(message.from_user.id)
        await message.answer("<b>Malumotlaringiz o'chirildi!</b>\n\nBotni qayta ishga tushirish uchun <b>/start</b> buyrug'ini yuboring!", reply_markup=remove(), parse_mode='html')
        await state.clear()
    else:
        await message.answer("Hisobni o'chirish bekor qilindi")
        await settings_user_data(message, state)





