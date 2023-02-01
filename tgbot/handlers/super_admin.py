from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hlink

from reset_commands import set_all_super_admins_commands
from tgbot.misc.states import SuperAdmin


async def super_admin_start(message: Message):
    await message.reply("Hello, super admin!")
    bot = Bot.get_current()
    await set_all_super_admins_commands(bot, message.chat.id)


async def add_admin1(message: types.Message):
    await SuperAdmin.AddAdmin.set()
    await message.answer("Перешлите любое сообщение пользователя, которого хотите сделать админом")


async def add_admin2(message: types.Message, state: FSMContext):
    bot = Bot.get_current()
    config = bot["config"]
    admins = config.tg_bot.admin_ids
    user = message.forward_from
    if user.id in admins:
        await message.answer(f"Пользователь " +
                             hlink(user.full_name, f"tg://user?id={user.id}") +
                             " уже является админом, его незачем еще раз добавлять")
    else:
        admins.append(int(user.id))
        await message.answer(f"Пользователь " +
                             hlink(user.full_name, f"tg://user?id={user.id}") +
                             " добавлен в админы")
        await bot.send_message(chat_id=user.id, text=f"{user.full_name},"
                                                     f" вас назначили админом бота, теперь"
                                                     f" я буду исполнять ваши команды")
    await state.finish()


async def delete_admin1(message: types.Message):
    await SuperAdmin.DeleteAdmin.set()
    await message.answer("Перешлите любое сообщение админа, которого хотите удалить")


async def delete_admin2(message: types.Message, state: FSMContext):
    bot = Bot.get_current()
    config = bot["config"]
    admins = config.tg_bot.admin_ids
    user = message.forward_from
    if user.id in admins:
        del admins[admins.index(user.id)]
        await message.answer(f"Пользователь " +
                             hlink(user.full_name, f"tg://user?id={user.id}") +
                             " удален из списка админов")
        await bot.send_message(chat_id=user.id, text=f"{user.full_name},"
                                                     f" вас удалили из админов бота, теперь"
                                                     f" я не буду исполнять ваши команды")
    else:
        await message.answer("Этот пользователь не является админом, наверное вы переслали сообщение не от того "
                             "человека")
    await state.finish()


def register_super_admin(dp: Dispatcher):
    dp.register_message_handler(super_admin_start, commands=["start"], state="*", is_super_admin=True)
    dp.register_message_handler(add_admin1, Command("add_admin"), is_super_admin=True)
    dp.register_message_handler(add_admin2, content_types=types.ContentType.ANY, state=SuperAdmin.AddAdmin,
                                is_super_admin=True)
    dp.register_message_handler(delete_admin1, Command("del_admin"), is_super_admin=True)
    dp.register_message_handler(delete_admin2, content_types=types.ContentType.ANY, state=SuperAdmin.DeleteAdmin,
                                is_super_admin=True)

