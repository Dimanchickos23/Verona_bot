from aiogram import types
from aiogram.types import BotCommandScopeAllChatAdministrators


async def set_default_commands(dp):
    await dp.bot.set_my_commands(commands=[
        types.BotCommand("create_post", "Создать публикацию на n часов в выбранном канале."),
        types.BotCommand("add_f", "Установить пользователю подписку на 90 дней."),
        types.BotCommand("add_p", "Установить вечную подписку пользователю."),
        types.BotCommand("del_sub", "Удалить статус подписки у пользователя."),
        types.BotCommand("add_admin", "Добавить админа."),
        types.BotCommand("del_admin", "Удалить админа.")
    ])
