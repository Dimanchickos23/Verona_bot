import asyncio
import logging

from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hlink

from tgbot.config import Config
from tgbot.infrastructure.database.functions import delete_user
from tgbot.keyboards.inline import chat_cb
from tgbot.misc import Survey


async def user_join(join: types.ChatJoinRequest):
    # тут мы принимаем юзера в канал
    await join.approve()
    # Тут надо занести в БД

    bot = Bot.get_current()

    # а тут отправляем сообщение
    chat_id = join.chat.id
    chat_name = join.chat.full_name
    start_survey_button = InlineKeyboardButton(text="📝 Заполнить анкету",
                                               callback_data=chat_cb.new(chat_id=chat_id,
                                                                         chat_name=str(chat_name),
                                                                         action='start_survey')
                                               )

    survey_keyboard = InlineKeyboardMarkup(row_width=1)
    survey_keyboard.insert(start_survey_button)

    await bot.send_message(chat_id=join.from_user.id, reply_markup=survey_keyboard,
                           text="Привет! \n\n"
                                "Поздравляем с прохождением кастинг-просмотра, теперь Вы "
                                "часть команды модельного агентства VERONA! \n\n"
                                "Для того, чтобы участвовать "
                                "в кастингах необходимо "
                                "выслать свои данные менеджеру по развитию моделей.")


# не работает
async def user_left(m: types.ChatMember, session):
    logging.info(f"{m.user.id}")
    await delete_user(session, m.user.id)
    bot = Bot.get_current()
    config: Config = bot.get('config')
    admin = config.tg_bot.admin_ids[0]
    await bot.send_message(admin, hlink(f"{m.user.full_name}", f"tg://user?id={m.user.id}") +
                           f" вышел из канала")


async def start_survey(cb: CallbackQuery, state: FSMContext, callback_data: dict):
    await cb.answer()
    await cb.message.answer("Введите ваше ФИО:")
    await Survey.FIO.set()
    chat_id = callback_data['chat_id']
    chat_name = callback_data['chat_name']
    # await cb.message.answer(f"Айди чата -- {chat_id}\n"
    #                         f"Имя чата -- {chat_name}")
    await state.update_data(chat_id=str(chat_id), chat_name=str(chat_name))


def register_user(dp: Dispatcher):
    dp.register_chat_join_request_handler(user_join, state="*")
    dp.register_callback_query_handler(start_survey, chat_cb.filter(action='start_survey'))
    dp.chat_member_handler(user_left, state="*")
