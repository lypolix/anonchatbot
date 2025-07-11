from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text='Выбрать функцию')], 
                                       [KeyboardButton(text='/start')]],
                            resize_keyboard = True, 
                            input_field_placeholder = 'Выберите пункт меню...')

send = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить сообщение', callback_data = 'input')], 
    [InlineKeyboardButton(text='Прочитать сообщение', callback_data = 'read')]])

another = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Показать ещё сообщения', callback_data = 'newmessanges')], 
    [InlineKeyboardButton(text='Не показывать больше', callback_data = 'sleep')]])
