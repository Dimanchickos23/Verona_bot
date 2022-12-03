import logging

from aiogram import Dispatcher, Bot, types
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.utils.markdown import hlink

from tgbot.infrastructure.database.functions import get_user
from tgbot.infrastructure.database.users import User
from tgbot.keyboards.inline import channel_cb


async def confirm_offer(cb: CallbackQuery, callback_data: dict, session):
    who_posted_id = int(callback_data['id'])
    who_posted_fullname = callback_data['name']
    logging.info(f"{who_posted_id=}")
    bot = Bot.get_current()
    await cb.answer("Спасибо за отклик", cache_time=10)
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Спасибо за отклик!\n" + "Пожалуйста, пришлите все необходимые материалы, "
                                                         "если нужно что-то помимо ссылки на портфолио и параметров " +
                                hlink(
                                       f"{who_posted_fullname}",
                                       f"tg://user?id={who_posted_id}"
                                      ))
    user: User = await get_user(session, cb.from_user.id)
    anketa = user.anketa
    await bot.send_message(chat_id=who_posted_id, text="Модель " + hlink(
                               f"{cb.from_user.full_name}",
                               f"tg://user?id={cb.from_user.id}") + f" откликнулась на кастинг:\n"
                                                                    f"{cb.message.text}\n\n"
                                                                    f"Вот ее анкета:\n"
                                                                    f"{anketa}",
                           disable_web_page_preview=True)


async def decline_offer(cb: CallbackQuery, callback_data: dict):
    await cb.answer("Спасибо за отклик", cache_time=10)
    who_posted_id = int(callback_data['id'])
    logging.info(f"{who_posted_id=}")
    bot = Bot.get_current()
    a = await bot.send_message(chat_id=who_posted_id, text=hlink(f"{cb.from_user.full_name}",
                                                                 f"tg://user?id={cb.from_user.id}") + " отклонил кастинг.")
    logging.info(f"{a.message_id}")


async def not_sub(cb: CallbackQuery):
    await cb.answer("Вы не оплатили подписку на канал.", cache_time=10)


def register_channel(dp: Dispatcher):
    dp.register_callback_query_handler(confirm_offer, channel_cb.filter(action="confirm"), is_favorite=True)
    dp.register_callback_query_handler(confirm_offer, channel_cb.filter(action="confirm"), is_perspective=True)
    dp.register_callback_query_handler(decline_offer, channel_cb.filter(action="decline"), is_favorite=True)
    dp.register_callback_query_handler(decline_offer, channel_cb.filter(action="decline"), is_perspective=True)
    dp.register_callback_query_handler(not_sub)
