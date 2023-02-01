import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Config


class SuperAdminFilter(BoundFilter):
    key = 'is_super_admin'

    def __init__(self, is_super_admin: typing.Optional[bool] = None):
        self.is_super_admin = is_super_admin

    async def check(self, obj):
        if self.is_super_admin is None:
            return False
        config: Config = obj.bot.get('config')
        return (obj.from_user.id in config.tg_bot.super_ids) == self.is_super_admin