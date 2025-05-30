from util.loader import ReplyKeyboardBuilder, ReplyKeyboardRemove, KeyboardButton


def reply_btn_builder(texts: list, size: list = None):
    btn = ReplyKeyboardBuilder()
    btn.add(*[KeyboardButton(text=text) for text in texts])
    if size:
        if True in size:
            size.remove(True)
            btn.adjust(*size, repeat=True)
        else:
            btn.adjust(*size)
    return btn.as_markup(resize_keyboard=True)


def get_phone_number():
    btn = ReplyKeyboardBuilder()
    btn.add(KeyboardButton(text="Telefon raqam qoldirish", request_contact=True))
    return btn.as_markup(resize_keyboard=True)


def set_user_data_btn():
    btn = ReplyKeyboardBuilder()
    btn.add(
        KeyboardButton(text="Ism"),
        KeyboardButton(text="Telefon raqam", request_contact=True),
        KeyboardButton(text="Orqaga"),
    )
    btn.adjust(1, 1, 1)
    return btn.as_markup(resize_keyboard=True)


def remove():
    btn = ReplyKeyboardRemove()
    return btn