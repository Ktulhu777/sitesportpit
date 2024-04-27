from django.conf import settings
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from asgiref.sync import sync_to_async
from cart.models import Order
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup


TOKEN = settings.TOKENBOT
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

description = types.bot_description.BotDescription(
    description="""Я бот разработанный для навигации по сайту ProjectPit.ru. Чем я могу Вам помочь?""")

dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='URL сайта', url='project-pit.ru/'),
         InlineKeyboardButton(text='Мои заказы')]])
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Здравствуйте {message.from_user.username}!\n{description}',
                           reply_markup=inline_markup)


@dp.message(Command('location'))
async def send_point(message: types.Message):
    await bot.send_location(chat_id=message.chat.id, latitude=50.554404, longitude=9.646871)


@dp.message(Command('order'))
async def get_order_user(message: types.Message):
    order_list = await sync_to_async(Order.objects.filter, thread_sensitive=False)(
        user__telegram_id=message.from_user.id)
    await message.delete()
    if order_list:
        counter = 0
        await message.answer(text="Вот ваш список заказов")
        for i in order_list:
            if counter == 10:
                await message.answer(
                    text=f"Список получится очень большим, остальное можете посмотреть на сайте. \n"
                         f"Более подробно тут project-pit.ru/api/v1/order/",
                    reply_markup=ReplyKeyboardRemove()
                )
                break
            await message.answer(
                text=f"Товар: {i.product}; \nЦена: {i.price}; \n"
                     f"Количество продуктов: {i.quantity_product}; \n"
                     f"Время заказа: {i.time_create_order} \n"
                     f"Статус заказа: {{{'Активен' if i.is_active else 'Неактивен'}}}"
            )
            counter += 1
    else:
        await message.answer(text="Список заказов пуст либо профиль не привязан", reply_markup=profile_markup())


@dp.message(Command('webprofile'))
async def open_profile_user(message):
    """Команда для перехода пользователя на свой профиль сайта"""
    await bot.send_message(message.chat.id,
                           text='project-pit.ru/api/users/me/')


def profile_markup():
    have_profile = KeyboardButton(text="У меня есть профиль на сайте")
    have_not_profile = KeyboardButton(text='Нет профиля на сайте')
    return ReplyKeyboardMarkup(resize_keyboard=True,
                               one_time_keyboard=True,
                               keyboard=[
                                   [have_not_profile, have_profile]
                               ])


@dp.message(lambda message: message.text == "У меня есть профиль на сайте")
async def get_profile(message: types.Message) -> None:
    await message.answer(text=f'Ваш ID: {message.from_user.id}. Введите свой ID в поле telegram_id. \n'
                              'project-pit.ru/api/users/me/',
                         reply_markup=ReplyKeyboardRemove())


@dp.message(lambda message: message.text == "Нет профиля на сайте")
async def get_register(message):
    await message.answer(text='Вы можете зарегистроваться по ссылке \nproject-pit.ru/api/users/me/')


async def main() -> None:
    dp.message.register(bot)
    await dp.start_polling(bot, skip_updates=True)
