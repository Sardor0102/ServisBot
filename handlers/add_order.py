import time

from buttons.inline_btn import *
from database.postgres_conn import get_user, get_service
from handlers.user_handler import main_menu, start_order
from util.loader import *
from util.texts import months
from util.state import UserState


@dp.callback_query(F.data.startswith("service"))
async def start_service_callback(callback: CallbackQuery, state: FSMContext):
    ser, service_id = callback.data.split("_")
    if service_id == "back":
        await callback.message.delete()
        await main_menu(callback.message, state, True)
    else:
        await state.update_data({"service_id": service_id})
        await callback.message.delete()
        await set_date(callback.message)


async def set_date(message: Message):
    datas = {}
    for day in range(1, 8):
        date = time.localtime(time.time()+86400*day)
        key = f"📅 {date.tm_mday}-{months[date.tm_mon]}" # 23-fevral
        value = f"date_{date.tm_mday}.{date.tm_mon}"     # date_23.2
        datas.setdefault(key, value)
    btn = set_date_btn(datas)
    await message.answer("Sanani tanlang:", reply_markup=btn)


@dp.callback_query(F.data.startswith("date"))
async def set_date_callback(callback: CallbackQuery, state: FSMContext):
    d, date = callback.data.split("_")
    await callback.message.delete()
    if date == "back":
        await start_order(callback.message)
    else:
        await state.update_data({"date": date})
        await set_time(callback.message)


async def set_time(message: Message):
    btn = set_time_btn()
    await message.answer("Vaqtni tanlang:", reply_markup=btn)


@dp.callback_query(F.data.startswith("time"))
async def set_time_callback(callback: CallbackQuery, state: FSMContext):
    w, t = callback.data.split("_")
    await callback.message.delete()
    if t == "back":
        await set_date(callback.message)
    else:
        await state.update_data({"time": t})
        await callback.message.answer("Yahshi, endi kichikroq fikr qoldirip keting, masalan, sana yoki vaqti haqida yoki hizmatlari haqida:")
        await state.set_state(UserState.comment)


@dp.message(UserState.comment)
async def add_comment(message: Message, state: FSMContext):
    await state.update_data({"comment": message.text})
    await order_done(message, state)


async def order_done(message: Message, state: FSMContext):
    data = await state.get_data()
    user = await get_user(int(data.get('id')))

    service = await get_service(data.get('service_id'))

    date = data.get("date").split(".")
    month = months.get(int(date[1]))

    at_time = times.get(data.get('time'))

    comment = data.get('comment')

    context = f"""
<b>Buyurtma qiluvchi:</b> {user[2]}
<b>Telefon raqam:</b> {user[3]}
<b>Servis turi:</b> {service[1]}
<b>Kuni:</b> {date[0]}-{month}
<b>Vaqti:</b> {at_time}
<b>Qisqacha fikri:</b> {comment}
"""
    employee_context = f"user id:{user[0]}" + context
    await state.update_data({"order_message": employee_context})
    btn = order_done_btn()
    await message.answer(context, reply_markup=btn, parse_mode='html')


@dp.callback_query(F.data.startswith("order"))
async def order_done_callback(callback: CallbackQuery, state: FSMContext):
    call, ans = callback.data.split("_")
    user_id = (await state.get_data()).get('id')
    if ans == "done":
        order_data = (await state.get_data()).get('order_message')
        await callback.message.edit_reply_markup(reply_markup=done_cancel_btn('done'))
        btn = upload_order(user_id)
        await callback.message.bot.send_message(chat_id=-1002255126804, text=f"{order_data}", parse_mode='html', reply_markup=btn)
        await callback.message.answer("Malumotlar yuborildi va kerakli servis hodimi sizga javob yuboradi!\n\n(Malumotlari bu yerda: https://t.me/+-fG9yB2M2c8yNzcy)", disable_web_page_preview=True)
    else:
        await callback.message.edit_reply_markup(reply_markup=done_cancel_btn('cancel'))
    await state.clear()
    await state.update_data({'id': user_id})
    await main_menu(callback.message, state, True)

