import asyncio

from aiogram import types, Bot, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.misc import Survey


async def survey_error(m: types.Message, state: FSMContext):
    bot = Bot.get_current()
    message = await m.answer("Вы ошиблись, заполняя анкету. Пожалуйста, внимательно прочитайте вопрос"
                             " в предыдущем сообщении. Ваш неправильный ответ и это сообщение самоуничтожатся через"
                             " 8 секунд.")
    await asyncio.sleep(8)
    await bot.delete_message(m.chat.id, m.message_id)
    await bot.delete_message(m.chat.id, message.message_id)


def register_survey_error(dp: Dispatcher):
    dp.register_message_handler(survey_error, state=Survey.FIO)
    dp.register_message_handler(survey_error, state=Survey.Age)
    dp.register_message_handler(survey_error, state=Survey.Height)
    dp.register_message_handler(survey_error, state=Survey.Bust)
    dp.register_message_handler(survey_error, state=Survey.Waist)
    dp.register_message_handler(survey_error, state=Survey.Hips)
    dp.register_message_handler(survey_error, state=Survey.Size)
    dp.register_message_handler(survey_error, state=Survey.Leg_size)
    dp.register_message_handler(survey_error, state=Survey.Disk)
