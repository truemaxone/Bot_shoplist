import keyboards
from aiogram import types
from bot import db
from dispatcher import bot, dp


@dp.callback_query_handler(lambda callback_query: True)
async def callback_inline(call: types.CallbackQuery):
    list_of_products = db.db_recourse_call(call)
    dict_lop = {str(product_id): product for product_id, product in
                enumerate(list_of_products, 1)}  # lop - list_of_products

    if call.message and list_of_products and '' not in list_of_products:
        if call.data == 'delete':
            keyboard = keyboards.get_inline_del_kb(dict_lop)
            await bot.edit_message_text('What do you want to remove from the list?', call.message.chat.id,
                                        call.message.message_id, reply_markup=keyboard)
        elif call.data == 'edit':
            keyboard = keyboards.get_inline_edit_kb(dict_lop)
            await bot.edit_message_text('What do you want to mark?', call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
        elif call.data == 'back':
            if list_of_products:
                keyboard = keyboards.get_show_kb()
                await bot.edit_message_text(line_print(list_of_products), call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
            else:
                await call.message.answer("The list is empty")

        elif 'delete_product' in call.data:
            if list_of_products:
                product_id = call.data.replace('delete_product ', '')
                list_of_products.remove(dict_lop[product_id])
                db.db_update_call(call, list_of_products)
                # show alert
                await bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                text=f'{dict_lop[product_id]} removed')
                dict_lop = {str(product_id): product for product_id, product in
                            enumerate(list_of_products, 1)}
            else:
                await call.message.answer("The list is empty")

            keyboard = keyboards.get_inline_del_kb(dict_lop)
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
        elif 'edit_product' in call.data:
            product_id = call.data.replace('edit_product ', '')
            if '✖ ' in dict_lop[product_id]:
                for i in range(len(list_of_products)):
                    if list_of_products[i] == dict_lop[product_id]:
                        list_of_products[i] = dict_lop[product_id].replace('✖ ', '')
                dict_lop = {str(product_id): product for product_id, product in
                            enumerate(list_of_products, 1)}
                db.db_update_call(call, list_of_products)
                # show alert
                clear_product = dict_lop[product_id].replace('✖ ', '')
                await bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                text=f'{clear_product} unticked')
            else:
                cross_product = '✖ ' + dict_lop[product_id]
                for i in range(len(list_of_products)):
                    if list_of_products[i] == dict_lop[product_id]:
                        list_of_products[i] = cross_product
                dict_lop = {str(product_id): product for product_id, product in
                            enumerate(list_of_products, 1)}
                db.db_update_call(call, list_of_products)

                # show alert
                await bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                text=f'{dict_lop[product_id]} ticked')

            keyboard = keyboards.get_inline_edit_kb(dict_lop)
            await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)

        elif call.data == 'delete_all_yes':
            await bot.edit_message_text(chat_id=call.message.chat.id, text='Everything has been removed',
                                        message_id=call.message.message_id,
                                        reply_markup=None)
            list_of_products.clear()
            db.db_update_call(call, list_of_products)
        elif call.data == 'delete_all_no':
            await bot.edit_message_text(chat_id=call.message.chat.id, text='Oh, ok...',
                                        message_id=call.message.message_id,
                                        reply_markup=None)
    else:
        await bot.edit_message_text('The list is empty', call.message.chat.id, call.message.message_id)


#  Вывод пронумированных продуктов в столбик
def line_print(grocery_list):
    new_line = ''
    for i, item in enumerate(grocery_list):
        if '✖ ' in item:
            new_line += '\u0336'.join(str(i + 1) + ') ' + item.replace('✖ ', '') + '\n')
        else:
            new_line += (str(i + 1) + ') ' + item + '\n')
    return new_line
