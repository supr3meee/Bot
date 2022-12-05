import re

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from carsearch.carsearch import get_car_list
from keyboards import kb, ikb, ikb_cities
from config import TOKEN_API


COMMANDS = """
/start - начать работу с ботом
Команды - список команд
Описание - описание функционала бота
Настройки - Настройки
"""

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот запущен.')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text='Добро пожаловать в Перекуп Авто Бот!\nРаботает пока только с АВИТО и av.by!'
                              '\nСписок доступных команд: /help',
                         reply_markup=kb)
    await message.delete()


@dp.message_handler(Text(equals='Команды'))
async def help_command(message: types.Message):
    await message.reply(text=COMMANDS,
                        reply_markup=kb)
    await message.delete()


@dp.message_handler(Text(equals='Настройки'))
async def settings_command(message: types.Message):
    await message.answer(text='Настройки',
                         reply_markup=ikb)
    await message.delete()


@dp.message_handler(Text(equals='Описание'))
async def description_command(message: types.Message):
    await message.answer(text='<b>Этот бот создан для помощи продавцам автомобилей. Как им пользоваться: </b>'
                              '\n\n\t1. Вы находите заинтересовавший вас автомобиль.'
                              '\n\t2. Отправляете ссылку на него в бот.'
                              '\n\t3. Бот анализирует ваш местный рынок.'
                              '\n\t4. Присылает вам обратно максимально похожие автомобили.'
                              '\n\nВ расчет берется: год, пробег и базовые параметры автомобиля.'
                              '\n\n<em>Работает пока только с avito.ru и av.by!</em>',
                         parse_mode='HTML',
                         reply_markup=kb)
    await message.delete()


@dp.callback_query_handler()
async def set_location_settings(callback: types.CallbackQuery):
    if callback.data == 'location':
        await callback.message.edit_text(text='Выберете свой город',
                                         reply_markup=ikb_cities)
    elif callback.data == 'radius':
        await callback.answer('Изменение радиуса поиска')
    elif callback.data == 'krasnodar':
        print('Краснодар')
        await callback.answer()
    elif callback.data == 'moskva':
        print('Москва')
        await callback.answer()
    elif callback.data == 'close':
        await callback.message.delete()
    else:
        await callback.answer()


@dp.message_handler()
async def show_cars(message: types.Message):
    car_link = re.findall(r'https://www.avito.ru[.\S]*\D\d{10}', message.text)
    car_link_av = re.findall(r'https://cars.av.by[.\S]*\D\d{9}', message.text)
    if car_link:
        print(car_link[0])
        await message.reply(text='Поиск занимает 2-5 мин. Ожидайте.')
        for car in get_car_list(car_link[0]):
            await message.reply(text=car)
        await message.reply(text='Если ничего не пришло, значит ничего не найдено или бот сломался',
                            reply_markup=kb)
    elif car_link_av:
        print(car_link_av[0])
        await message.reply(text='Поиск занимает 2-5 мин. Ожидайте.')
        cars_list, by_car_price = get_car_list(car_link_av[0])
        for car in cars_list:
            await message.reply(text=car)
        await message.reply(text=f'Цена без учета доставки и оформления ≈ {by_car_price} ₽')
        await message.reply(text='Если ничего не пришло, значит ничего не найдено или бот сломался',
                            reply_markup=kb)
    else:
        await message.reply(text='Пока я принимаю только ссылки с АВИТО и av.by',
                            reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
