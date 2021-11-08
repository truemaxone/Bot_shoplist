import keyboards
from fsm import AdditionalStep
from aiogram import types
from aiogram.dispatcher import FSMContext
from dispatcher import bot, dp
from bot import db


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    sti = open('static/welcome.webp', 'rb')
    await message.answer_sticker(sti)

    keyboard = keyboards.get_main_kb()

    bot_name = await bot.get_me()
    await message.answer(f"Добро пожаловать, {message.from_user.first_name}!\nЯ - *{bot_name.first_name}*, "
                         f"бот созданный чтобы помогать со списком покупок.\nДля подробной информации по командам, "
                         f"введите /help", parse_mode='Markdown', reply_markup=keyboard)

    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # Проверка на наличие в базе
    db.check_existence(user_id, user_name)


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await message.answer("/add (название продукта) - добавить продукт в список, если продуктов  несколько,"
                         "то перечислите их через запятую или через Enter"
                         "\n/show - показать список покупок"
                         "\n/delete (название продукта) - удалить продукт из списка"
                         "\n/deleteall - удалить все продукты из списка"
                         "\n/help - справочная информация")


@dp.message_handler(commands=['add'])
async def add_product(message: types.Message):
    list_of_products = db.db_recourse(message)
    if '' in list_of_products:
        list_of_products.remove('')

    if '/add ' in message.text:
        if '\n' in message.text:
            products = message.text.replace('/add', '').replace(',', '\n').split('\n')
            products = [product for product in products if product != '']
            bag = []  # для вывода нескольких добавленных в список продуктов в сообщении
            for product in products:
                if product.strip().capitalize() in list_of_products:
                    await message.answer(f"{product} is already in the list")
                else:
                    list_of_products.append(product.strip().capitalize())
                    db.db_update(message, list_of_products)
                    bag.append(product.strip())
            if bag:
                await message.answer(f"{', '.join(bag)} added to the list")
        elif ',' in message.text:
            products = message.text.replace('/add', '').split(',')
            products = [product for product in products if product != '']
            bag = []  # для вывода нескольких добавленных в список продуктов в сообщении
            for product in products:
                if product.strip().capitalize() in list_of_products:
                    await message.answer(f"{product} is already in the list")
                else:
                    list_of_products.append(product.strip().capitalize())
                    db.db_update(message, list_of_products)
                    bag.append(product)
            if bag:
                await message.answer(f"{', '.join(bag)} added to the list")
        else:
            if message.text.replace('/add ', '').strip().capitalize() in list_of_products:
                await message.answer(f"{message.text.replace('/add ', '').strip()} is already in the list")
            else:
                list_of_products.append(message.text.replace('/add ', '').strip().capitalize())
                db.db_update(message, list_of_products)
                await message.answer(f"{message.text.replace('/add ', '').strip()} added to the list")
    else:
        await AdditionalStep.add_next_message.set()
        await message.answer("What do you want to add?")


@dp.message_handler(commands=['show'])
async def show_products(message: types.Message):
    list_of_products = db.db_recourse(message)

    if list_of_products and '' not in list_of_products:
        keyboard = keyboards.get_show_kb()
        await message.answer(('Shopping list:\n' + line_print(list_of_products)), reply_markup=keyboard)
    else:
        await message.answer("The list is empty")


@dp.message_handler(commands=['delete'])
async def delete_product(message: types.Message):
    list_of_products = db.db_recourse(message)
    if '/delete ' in message.text:
        try:
            list_of_products.remove(message.text.replace('/delete ', '').capitalize())
            db.db_update(message, list_of_products)
            await message.answer(f"{message.text.replace('/delete ', '').capitalize()} removed from the list")
        except ValueError:
            await message.answer("There is no product like this")
    else:
        await AdditionalStep.delete_next_message.set()
        await message.answer("What do you want to delete?")


@dp.message_handler(commands=['deleteall'])
async def delete_all_product(message: types.Message):
    keyboard = keyboards.get_del_all_kb()
    await message.answer("Are sure you want to remove everything?", reply_markup=keyboard)


@dp.message_handler(content_types=['text'])
async def bot_answer(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Показать список':
            await show_products(message)
        elif message.text == 'Добавить продукты':
            await add_product(message)
        elif message.text == 'Удалить список':
            await delete_all_product(message)


@dp.message_handler(state=AdditionalStep.add_next_message)
async def additional_product(message: types.Message, state: FSMContext):
    list_of_products = db.db_recourse(message)

    async with state.proxy() as data:
        data['add_next_message'] = message.text

        if '' in list_of_products:
            list_of_products.remove('')

        if '\n' in message.text:
            products = message.text.replace('/add', '').replace(',', '\n').split('\n')
            products = [product for product in products if product != '']
            bag = []  # для вывода нескольких добавленных в список продуктов в сообщении
            for product in products:
                if product.strip().capitalize() in list_of_products:
                    await message.answer(f"{product} is already in the list")
                else:
                    list_of_products.append(product.strip().capitalize())
                    db.db_update(message, list_of_products)
                    bag.append(product.strip())
            if bag:
                await message.answer(f"{', '.join(bag)} added to the list")
        elif ',' in message.text:
            products = message.text.replace('/add', '').split(',')
            products = [product for product in products if product != '']
            bag = []  # для вывода нескольких добавленных в список продуктов в сообщении
            for product in products:
                if product.strip().capitalize() in list_of_products:
                    await message.answer(f"{product} is already in the list")
                else:
                    list_of_products.append(product.strip().capitalize())
                    db.db_update(message, list_of_products)
                    bag.append(product)
            if bag:
                await message.answer(f"{', '.join(bag)} added to the list")
        else:
            if message.text.replace('/add ', '').strip().capitalize() in list_of_products:
                await message.answer(f"{message.text.replace('/add ', '').strip()} is already in the list")
            else:
                list_of_products.append(message.text.replace('/add ', '').strip().capitalize())
                db.db_update(message, list_of_products)
                await message.answer(f"{message.text.replace('/add ', '').strip()} added to the list")
    await state.finish()


@dp.message_handler(state=AdditionalStep.delete_next_message)
async def delete_additional_product(message: types.Message, state: FSMContext):
    list_of_products = db.db_recourse(message)

    async with state.proxy() as data:
        data['delete_next_message'] = message.text
        try:
            list_of_products.remove(message.text.capitalize())
            db.db_update(message, list_of_products)
            await message.answer(f"{message.text.capitalize()} removed from the list")
        except ValueError:
            await message.answer("There is no product like this")
    await state.finish()


#  Вывод пронумированных продуктов в столбик
def line_print(grocery_list):
    new_line = ''
    for i, item in enumerate(grocery_list):
        if '✖ ' in item:
            new_line += '\u0336'.join(str(i + 1) + ') ' + item.replace('✖ ', '') + '\n')
        else:
            new_line += (str(i + 1) + ') ' + item + '\n')
    return new_line
