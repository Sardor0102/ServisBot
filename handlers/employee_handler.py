from handlers.user_handler import main_menu
from util.loader import *
from util.state import EmployeeState
from buttons.reply_btn import reply_btn_builder, get_phone_number, remove
from buttons.inline_btn import get_services_to_employee, add_employee_done
from database.postgres_conn import get_all_services, get_service, add_employee, is_employee


# @dp.callback_query(F.data.startswith("order-to"))
# async def order_to_callback(callback: CallbackQuery):
#     pass


@dp.message(F.text == "Ishga joylashish")
async def add_employee(message: Message, state: FSMContext):
    if not await is_employee(message.from_user.id):
        btn = reply_btn_builder(["Registratsini boshlash", "Orqaga"], [1, True])
        await message.answer("Ishga joylashishingiz uchun registratsiyadan o'tishingiz kerak!", reply_markup=btn)
        await state.set_state(EmployeeState.start)
    else:
        await message.answer("Siz allaqachon servis hodimisiz\n\nAgar qandaydur savolaringiz bo'lsa <a href='https://t.me/zxwiper'>Admin</a>ga yozing!")


@dp.message(EmployeeState.start, F.text == "Registratsini boshlash")
async def start_employee(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data({'chat_id': message.from_user.id, 'username': f"{'@' + message.from_user.username if message.from_user.username else 'None'}"})
    await message.answer("Yahshi, registratsiyani boshlaymiz\n\nIsmingizni yozing:", reply_markup=remove())
    await state.set_state(EmployeeState.first_name)


@dp.message(EmployeeState.first_name)
async def first_name_employee(message: Message, state: FSMContext):
    await state.update_data({'firstname': message.text})
    await message.answer("Endi, familiyangizni kiriting:")
    await state.set_state(EmployeeState.last_name)


@dp.message(EmployeeState.last_name)
async def last_name_employee(message: Message, state: FSMContext):
    await state.update_data({'lastname': message.text})
    await message.answer("Telefon raqamingizni kiriting:", reply_markup=get_phone_number())
    await state.set_state(EmployeeState.phone_number)


@dp.message(EmployeeState.phone_number)
async def phone_number_employee(message: Message, state: FSMContext):
    if message.contact:
        await state.update_data({'phone_number': message.contact.phone_number})
        services = await get_all_services()
        btn = get_services_to_employee(services)
        await message.answer("Ishlaydigan servisingizni tanlang:", reply_markup=btn)
    else:
        await message.answer("Iltimos, telefon raqamingizni kiriting:", reply_markup=get_phone_number())


@dp.callback_query(F.data.startswith("e-service"))
async def service_employee(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data({'service_id': callback.data.split("_")[1]})
    data = await state.get_data()
    fullname = data.get('firstname') + data.get('lastname')
    username = data.get('username')
    phone = data.get('phone_number')
    service = (await get_service(int(data.get('service_id'))))[1]
    btn = await add_employee_done()
    context = f"""
<b>Ismi:</b> {fullname}
<b>Username:</b> {username}
<b>Telefon raqami:</b> {phone}
<b>Servis:</b> {service}
"""
    await callback.message.answer(context, parse_mode='html')


@dp.callback_query(F.data == "employee_done")
async def end_employee(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=await add_employee_done(True))
    data = await state.get_data()
    await add_employee(**data)
    await callback.message.answer("Tabriklaymiz, siz service hodimiga aylandingiz!")
    await main_menu(callback.message, state, True)








