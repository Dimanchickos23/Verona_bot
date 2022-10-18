from aiogram import Dispatcher, Bot, types
from aiogram.types import CallbackQuery

from tgbot.keyboards.inline import survey_keyboard
from tgbot.misc import Survey


async def user_join(join: types.ChatJoinRequest):
    # тут мы принимаем юзера в канал
    await join.approve()
    # Тут надо занести в БД

    bot = Bot.get_current()
    # а тут отправляем сообщение
    await bot.send_message(chat_id=join.from_user.id, reply_markup=survey_keyboard, text="Привет! \n\n"
                                                                                         "Поздравляем с прохождением кастинг-просмотра, теперь Вы "
                                                                                         "часть команды модельного агентства VERONA! \n\n"
                                                                                         "Для того, чтобы участвовать в кастингах необходимо "
                                                                                         "выслать свои данные менеджеру по развитию моделей.")


async def user_left(left: types.ChatMemberLeft):
    # тут удаляем из БД
    pass


async def start_survey(cb: CallbackQuery):
    await cb.message.answer("Введите ваше ФИО:")
    await Survey.FIO.set()


def register_user(dp: Dispatcher):
    dp.register_chat_join_request_handler(user_join, state="*")
    dp.register_callback_query_handler(start_survey, lambda callback_query: callback_query.data == "survey_start", state="*")
    dp.register_chat_member_handler(user_left, state="*")

