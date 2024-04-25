import asyncio
import functools
from smtplib import SMTPRecipientsRefused
from django.conf import settings
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from asgiref.sync import sync_to_async
from cart.models import Order
from django.core.mail import send_mail
from .help_text import SuccessEmail
from .statebot import Form
from concurrent.futures import ThreadPoolExecutor
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove


TOKEN = settings.TOKENBOT
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Привет ты написал в группу')


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
                         f"Более подробно тут http://127.0.0.1:8000/api/v1/order/"
                )
                break
            await message.answer(
                text=f"Товар: {i.product}; \nЦена: {i.price}; \n"
                     f"Количество продуктов: {i.quantity_product}; \n"
                     f"Время заказа: {i.time_create_order}"
            )
            counter += 1
    else:
        await message.answer(text="Список заказов пуст либо профиль не привязан", reply_markup=profile_markup())


@dp.message(Command('webprofile'))
async def open_profile_user(message):
    """Команда для перехода пользователя на свой профиль сайта"""
    await bot.send_message(message.chat.id,
                           text='https://project-pit.ru/api/users/me/')


def profile_markup():
    have_profile = KeyboardButton(text="У меня есть профиль на сайте")
    have_not_profile = KeyboardButton(text='Нет профиля на сайте')
    return ReplyKeyboardMarkup(resize_keyboard=True,
                               one_time_keyboard=True,
                               keyboard=[
                                   [have_not_profile, have_profile]
                               ])


@dp.message(lambda message: message.text == "У меня есть профиль на сайте")
async def get_profile(message: types.Message, state: FSMContext) -> None:
    await message.answer(text='Напишите свой привязанный к профилю Email-адрес',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.email)


@dp.message(Form.email)
async def process_telegram_id(message: types.Message, state: FSMContext) -> None:
    await state.update_data(email=message.text)
    success = SuccessEmail(email=message.text,
                           nickname=message.from_user.username,
                           user_id=message.from_user.id)
    with ThreadPoolExecutor() as pool:
        loop = asyncio.get_running_loop()
        one_task = loop.run_in_executor(pool, functools.partial(send_email_user, success))
        try:
            await asyncio.gather(one_task)
            await message.answer(text=f'Мы отправили вам письмо на email {message.text}')
        except SMTPRecipientsRefused:
            await message.answer(text=f'Вы ввели неправильный Email')


@dp.message(lambda message: message.text == "Нет профиля на сайте")
async def get_register(message):
    await message.answer(text='Вы можете зарегистроваться по ссылке \nhttp://127.0.0.1:8000/api/users/')


def send_email_user(success: SuccessEmail):
    return send_mail('Привязка профиля к боту!', success.get_letter(), from_email=None,
                     recipient_list=[success.email], fail_silently=False)


async def main() -> None:
    dp.message.register(bot)
    await dp.start_polling(bot, skip_updates=True)
