from aiogram import types
from aiogram.types import BotCommandScopeAllChatAdministrators


async def set_default_commands(dp):
    await dp.bot.set_my_commands(commands=[
        types.BotCommand("create_post", "Создать публикацию на n часов в выбранном канале"),
        types.BotCommand("add_f", "Установить пользователю подписку на 90 дней. Команда вводится в сообщение с "
                                  "пересылаемым чеком пользователя"),
        types.BotCommand("add_p", "Установить вечную подписку пользователю. Команда вводится в forward message от "
                                  "пользователя"),
        types.BotCommand("del_sub", "Удалить статус подписки у пользователя. Команда вводится в forward message от"
                                    "пользователя")
    ], scope=BotCommandScopeAllChatAdministrators())
