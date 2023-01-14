import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator

from reset_commands import force_reset_all_commands
from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.filters.super_admin import SuperAdminFilter
from tgbot.handlers.anketa_errors import register_survey_error
from tgbot.handlers.make_post import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.service_msgs import register_service
from tgbot.handlers.super_admin import register_super_admin
from tgbot.handlers.user import register_user
from tgbot.filters.favorite import FavoriteFilter
from tgbot.filters.perspective import PerspectiveFilter
from tgbot.handlers.anketa import register_test
from tgbot.infrastructure.database.functions import create_session_pool
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.handlers.channel import register_channel
from tgbot.handlers.prolong import register_prolong
from tgbot.middlewares.scheduler import SchedulerMiddleware

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config, scheduler, session_pool):
    dp.setup_middleware(EnvironmentMiddleware(config=config, session_pool=session_pool))
    dp.setup_middleware(SchedulerMiddleware(scheduler))


def register_all_filters(dp):
    dp.filters_factory.bind(SuperAdminFilter)
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(FavoriteFilter)
    dp.filters_factory.bind(PerspectiveFilter)


def register_all_handlers(dp):
    register_user(dp)
    register_channel(dp)
    register_prolong(dp)
    register_super_admin(dp)
    register_admin(dp)
    register_test(dp)
    register_survey_error(dp)
    register_service(dp)
    register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    # Чтобы работал Redis brew services start/stop/restart redis

    storage = RedisStorage2(host='redis_cache',
                            password=config.tg_bot.redis_password) if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    session_pool = create_session_pool(config.db, echo=True)

    job_stores = {
        "default": RedisJobStore(
            jobs_key="dispatched_trips_jobs", run_times_key="dispatched_trips_running",
            # параметры host и port необязательны, для примера показано как передавать параметры подключения
            host="localhost", port=6379
            # , password=config.tg_bot.redis_password
            # host="redis_cache", port=6379, password=config.tg_bot.redis_password
        )
    }

    # Оборачиваем AsyncIOScheduler специальным классом
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(jobstores=job_stores))
    bot['config'] = config

    register_all_middlewares(dp, config, scheduler, session_pool=session_pool)
    register_all_filters(dp)
    register_all_handlers(dp)

    await force_reset_all_commands(bot)

    # start
    try:
        scheduler.start()  # запускаем шедулер
        await dp.start_polling(allowed_updates=["message", "callback_query", "chat_member", "chat_join_request"])
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        # scheduler.remove_all_jobs()
        scheduler.shutdown()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
