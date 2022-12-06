import asyncio
import logging

from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink

from tgbot.config import Config
from tgbot.infrastructure.database.functions import delete_user
from tgbot.keyboards.inline import survey_keyboard
from tgbot.misc import Survey


async def user_join(join: types.ChatJoinRequest, state: FSMContext):
    # тут мы принимаем юзера в канал
    await join.approve()
    # Тут надо занести в БД

    bot = Bot.get_current()
    # а тут отправляем сообщение
    chat_id = join.chat.id
    chat_name = join.chat.full_name
    await Survey.Start.set()
    await state.update_data(chat_id=chat_id, chat_name=chat_name)
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


async def start_survey(cb: CallbackQuery):
    await cb.message.answer("Введите ваше ФИО:")
    await Survey.FIO.set()


def register_user(dp: Dispatcher):
    dp.register_chat_join_request_handler(user_join, state="*")
    dp.register_callback_query_handler(start_survey, lambda callback_query: callback_query.data == "survey_start",
                                       state=Survey.Start)
    dp.chat_member_handler(user_left, state="*")

