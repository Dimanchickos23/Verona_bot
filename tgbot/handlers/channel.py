import logging

from aiogram import Dispatcher, Bot, types
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.utils.markdown import hlink

from tgbot.keyboards.inline import channel_cb


async def confirm_offer(cb: CallbackQuery, callback_data: dict):
    who_posted_id = int(callback_data['id'])
    who_posted_fullname = callback_data['name']
    logging.info(f"{who_posted_id=}")
    bot = Bot.get_current()
    await cb.answer("Спасибо за отклик")
    await bot.send_message(chat_id=cb.from_user.id, text="Свяжитесь с " + hlink(f"{who_posted_fullname}",
                                                                                f"tg://user?id={who_posted_id}") + "чтобы узнать "
                                                                                                                   "подробнее про "
                                                                                                                   "кастинг.")


async def decline_offer(cb: CallbackQuery, callback_data: dict):
    await cb.answer("Спасибо за отклик")
    who_posted_id = int(callback_data['id'])
    logging.info(f"{who_posted_id=}")
    bot = Bot.get_current()
    a = await bot.send_message(chat_id=who_posted_id, text=hlink(f"{cb.from_user.full_name}",
                                                                 f"tg://user?id={cb.from_user.id}") + " отклонил кастинг.")
    logging.info(f"{a.message_id}")


async def not_sub(cb: CallbackQuery):
    await cb.answer("Вы не оплатили подписку на канал.")


def register_channel(dp: Dispatcher):
    dp.register_callback_query_handler(confirm_offer, channel_cb.filter(action="confirm"), is_favorite=True)
    dp.register_callback_query_handler(confirm_offer, channel_cb.filter(action="confirm"), is_perspective=True)
    dp.register_callback_query_handler(decline_offer, channel_cb.filter(action="decline"), is_favorite=True)
    dp.register_callback_query_handler(decline_offer, channel_cb.filter(action="decline"), is_perspective=True)
    dp.register_callback_query_handler(not_sub)
