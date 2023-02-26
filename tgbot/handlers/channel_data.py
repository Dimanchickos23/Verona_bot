from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.infrastructure.database.functions import get_channel_users
from tgbot.keyboards.inline import channels_keyboard
from tgbot.misc.states import ChannelData


async def choose_channel_cmd(message: Message, state: FSMContext):
    await ChannelData.ChooseChannel.set()
    await message.answer("Выберите канал, о котором хотите узнать информацию", reply_markup=channels_keyboard)


async def show_channel_data(cb: CallbackQuery,state: FSMContext, session):
    await cb.answer()
    await state.finish()
    chat_id = cb.data
    print(chat_id)
    users = await get_channel_users(session,chat_id)
    text = ""
    for row in users:
        text += f"{row.name} {row.sub} {row.sub_date.date()}\n"
    await cb.message.edit_text(text)


def register_channel_data(dp: Dispatcher):
    dp.register_message_handler(choose_channel_cmd, commands=['data'])
    dp.register_callback_query_handler(show_channel_data, state=ChannelData.ChooseChannel)
