import logging
import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from tgbot.filters.filters_data import perspective
from tgbot.infrastructure.database.functions import get_user
from tgbot.infrastructure.database.users import User


class PerspectiveFilter(BoundFilter):
    key = 'is_perspective'

    def __init__(self, is_perspective: typing.Optional[bool] = None):
        self.is_perspective = is_perspective

    async def check(self, obj):
        if self.is_perspective is None:
            return False

        user_id = obj.from_user.id
        data = ctx_data.get()
        session = data.get('session')
        user: User = await get_user(session, user_id)
        logging.info(f'User {user.full_name}, has subscription_type = {user.subscription_type}')
        return (user.subscription_type == 'perspective') == self.is_perspective
