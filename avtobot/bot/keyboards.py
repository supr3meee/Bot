from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Main menu
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton('Команды')
button2 = KeyboardButton('Описание')
button3 = KeyboardButton('Настройки')
kb.add(button1, button2)
kb.add(button3)

# Settings ( in future it'll be possible to change search location )
ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='Выберете ваш город',
                           callback_data='location')
ib2 = InlineKeyboardButton(text='Выберете радиус поиска',
                           callback_data='radius')
ikb.add(ib1, ib2)

# City settings
ikb_cities = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Краснодар', callback_data='krasnodar'),
         InlineKeyboardButton(text='Москва', callback_data='moskva')],
        [InlineKeyboardButton(text='Закрыть', callback_data='close')]
    ]
)
