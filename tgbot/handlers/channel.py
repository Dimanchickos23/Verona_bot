import logging

from aiogram import Dispatcher, Bot, types
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.utils.markdown import hlink


async def confirm_offer(cb: CallbackQuery):
    who_posted_id = cb.data
    await cb.answer(url=f"tg://user?id={who_posted_id}")


async def decline_offer(cb: CallbackQuery):
    await cb.answer(cache_time=1)
    who_posted_id = cb.data
    logging.info(f"{who_posted_id=}")
    bot = Bot.get_current()
    a = await bot.send_message(chat_id=cb.data, text=hlink(f"{cb.from_user.full_name}",
                                                           f"tg://user?id={cb.from_user.id}") + " отклонил кастинг.")
    logging.info(f"{a.message_id}")


async def not_sub(cb: CallbackQuery):
    await cb.answer("Вы не оплатили подписку на канал.")


def register_channel(dp: Dispatcher):
    dp.register_callback_query_handler(confirm_offer, is_favorite=True)
    dp.register_callback_query_handler(confirm_offer, is_perspective=True)
    dp.register_callback_query_handler(decline_offer, is_favorite=True)
    dp.register_callback_query_handler(decline_offer, is_perspective=True)
    dp.register_callback_query_handler(not_sub)
