from aiogram import types, Bot
from aiogram.types import BotCommandScopeAllChatAdministrators, BotCommandScopeDefault, BotCommandScopeAllPrivateChats, \
    BotCommandScopeAllGroupChats, BotCommandScopeChatMember, BotCommandScopeChat


async def set_all_admins_commands(bot: Bot, chat_id: int, user_id: int):
    return await bot.set_my_commands(commands=[
        types.BotCommand("create_post", "Создать публикацию на n часов в выбранном канале."),
        types.BotCommand("add_f", "Установить пользователю подписку на 90 дней."),
        types.BotCommand("add_p", "Установить вечную подписку пользователю."),
        types.BotCommand("del_sub", "Удалить статус подписки у пользователя.")
    ],
        scope=BotCommandScopeChat(chat_id)
    )


async def set_all_super_admins_commands(bot: Bot, chat_id: int, user_id: int):
    return await bot.set_my_commands(commands=[
        types.BotCommand("create_post", "Создать публикацию на n часов в выбранном канале."),
        types.BotCommand("add_f", "Установить пользователю подписку на 90 дней."),
        types.BotCommand("add_p", "Установить вечную подписку пользователю."),
        types.BotCommand("del_sub", "Удалить статус подписки у пользователя."),
        types.BotCommand("add_admin", "Добавить админа."),
        types.BotCommand("del_admin", "Удалить админа.")
    ],
        scope=BotCommandScopeChat(chat_id)
    )


async def force_reset_all_commands(bot: Bot):
    for language_code in ('ru', 'en', 'uk', 'uz'):
        for scope in (
                BotCommandScopeAllGroupChats(),
                BotCommandScopeAllPrivateChats(),
                BotCommandScopeAllChatAdministrators(),
                BotCommandScopeDefault(),
        ):
            await bot.delete_my_commands(scope, language_code)