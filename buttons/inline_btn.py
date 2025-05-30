from util.loader import InlineKeyboardBuilder, InlineKeyboardButton
from util.texts import times


def get_services_btn(services):
    btn = InlineKeyboardBuilder()
    btn.row(InlineKeyboardButton(text="⬅️ Ortga qaytish", callback_data="service_back"))
    btn.add(*[InlineKeyboardButton(text=service[1], callback_data=f"service_{service[0]}") for service in services])
    btn.adjust(1, repeat=True)
    return btn.as_markup()


def set_date_btn(datas: dict):
    btn = InlineKeyboardBuilder()
    btn.row(*[InlineKeyboardButton(text=text, callback_data=data) for text, data in datas.items()], width=3)
    btn.button(text="⬅️ Ortga qaytish", callback_data="date_back")
    return btn.as_markup()


def set_time_btn():
    btn = InlineKeyboardBuilder()
    btn.row(*[InlineKeyboardButton(text=text, callback_data=f"time_{time}") for time, text in times.items()], width=3)
    btn.button(text="⬅️ Ortga qaytish", callback_data="time_back")
    return btn.as_markup()


def order_done_btn():
    btn = InlineKeyboardBuilder()
    btn.button(text="❌ Bekor qilish", callback_data="order_cancel")
    btn.button(text="✅ Tasdiqlash", callback_data="order_done")
    btn.adjust(1, 1)
    return btn.as_markup()


def done_cancel_btn(value):
    btn = InlineKeyboardBuilder()
    if value == "done":
        btn.button(text="✅ Yuborildi", callback_data="d")
    else:
        btn.button(text="❌ Bekor qilindi", callback_data="c")
    btn.adjust(1,)
    return btn.as_markup()


def user_data_btn():
    btn = InlineKeyboardBuilder()
    btn.button(text="✅ Tasdiqlash", callback_data="data_done")
    btn.button(text="❌ Bekor qilish", callback_data="data_cancel")
    btn.adjust(1, 1)
    return btn.as_markup()


def upload_order(user_id):
    btn = InlineKeyboardBuilder()
    btn.button(text="✅ Buyurtmani qabul qilishi", callback_data="add_order")
    return btn.as_markup()


def get_services_to_employee(services):
    btn = InlineKeyboardBuilder()
    btn.add(*[InlineKeyboardButton(text=service[1], callback_data=f"e-service_{service[0]}") for service in services])
    btn.adjust(1, repeat=True)
    return btn.as_markup()


def add_employee_done(done = False):
    btn = InlineKeyboardBuilder()
    if done:
        btn.button(text="✅ Tasdiqlash", callback_data="employee_done")
    else:
        btn.button(text="✅ Tasdiqlandi", callback_data="EAnhb328*YGUbd32iubd")
    btn.adjust(1,)
    return btn.as_markup()

