import asyncio

from aiogram import types, Dispatcher
from aiogram.utils.markdown import hlink


async def super_msg(m: types.Message):
    await m.answer(f"Наверное вы ошиблись или что то делайте не так.\n"
                   f"Попробуйте воспользоваться командой\n/reset и начать заново.")

async def user_msg(m: types.Message):
    await m.answer_sticker("CAACAgIAAxkBAAEBcu1jcQSpGQABhH8I8Vx148-usjz0X0cAAgEBAAJWnb0KIr6fDrjC5jQrBA")
    await asyncio.sleep(2)
    await m.answer(f"Привет, {m.from_user.full_name}! Я бот модельного"
                   f" агенства Верона. Я размещаю для вас кастинги, оформляю подписку"
                   f" на канал и напоминаю об ее окончании. К сожалению, я подчиняюсь"
                   f" только админам каналов и вы не можете мною управлять.\n"
                   f"Если есть какие-то вопросы, обращайтесь к" + hlink(" Елизавете", "https://t.me/lkrioni"),
                   disable_web_page_preview=True)


def register_service(dp: Dispatcher):
    dp.register_message_handler(super_msg, state="*", content_types=types.ContentTypes.ANY, is_super_admin=True)
    dp.register_message_handler(super_msg, state="*", content_types=types.ContentTypes.ANY, is_admin=True)
    dp.register_message_handler(user_msg, state="*", content_types=types.ContentTypes.ANY)