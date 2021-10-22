from aiogram import types


def get_main_kb():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Показать список")
    btn2 = types.KeyboardButton("Добавить продукты")
    btn3 = types.KeyboardButton("Удалить список")
    keyboard.add(btn1, btn2, btn3)
    return keyboard


def get_show_kb():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text='✏', callback_data='edit')
    btn2 = types.InlineKeyboardButton(text='🗑', callback_data='delete')
    keyboard.add(btn1, btn2)
    return keyboard


def get_del_all_kb():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text='✔', callback_data='delete_all_yes')
    btn2 = types.InlineKeyboardButton(text='✖', callback_data='delete_all_no')
    keyboard.add(btn1, btn2)
    return keyboard


def get_inline_del_kb(dict_lop):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btns = []
    for product_id, product in dict_lop.items():
        btn = types.InlineKeyboardButton(text=f'{product}', callback_data=f'delete_product {product_id}')
        btns.append(btn)
    btn1 = types.InlineKeyboardButton(text='⬅', callback_data='back')
    btn2 = types.InlineKeyboardButton(text='✏', callback_data='edit')
    keyboard.add(*btns)
    keyboard.add(btn1, btn2)
    return keyboard


def get_inline_edit_kb(dict_lop):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btns = []
    for product_id, product in dict_lop.items():
        btn = types.InlineKeyboardButton(text=f'{product}', callback_data=f'edit_product {product_id}')
        btns.append(btn)
    btn1 = types.InlineKeyboardButton(text='⬅', callback_data='back')
    btn2 = types.InlineKeyboardButton(text='🗑', callback_data='delete')
    keyboard.add(*btns)
    keyboard.add(btn1, btn2)
    return keyboard
