import logging

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.infrastructure.database.functions import get_user, create_user
from tgbot.infrastructure.database.users import User


class EnvironmentMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]
    
    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs
    
    async def pre_process(self, obj, data, *args):
        session_pool = self.kwargs.get('session_pool')
        session = session_pool()
        user = await get_user(session, obj.from_user.id)
        if not user:
            logging.info(f'{session=}')
            await create_user(session,
                                  telegram_id=obj.from_user.id,
                                  full_name=obj.from_user.full_name,
                                  username=obj.from_user.username
                              )
        data.update(session=session, **self.kwargs)

    async def post_process(self, obj, data, *args):
        session = data.get('session')
        await session.close()
