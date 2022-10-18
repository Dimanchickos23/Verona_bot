import logging
import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from tgbot.infrastructure.database.functions import get_user
from tgbot.infrastructure.database.users import User


class FavoriteFilter(BoundFilter):
    key = 'is_favorite'

    def __init__(self, is_favorite: typing.Optional[bool] = None):
        self.is_favorite = is_favorite

    async def check(self, obj):

        if self.is_favorite is None:
            return False

        user_id = obj.from_user.id
        data = ctx_data.get()
        session = data.get('session')
        user: User = await get_user(session, user_id)
        logging.info(f'User {user.full_name}, has subscription_type = {user.subscription_type}')
        return (user.subscription_type == 'favorite') == self.is_favorite
