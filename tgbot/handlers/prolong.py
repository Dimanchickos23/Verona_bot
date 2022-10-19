import datetime
import logging

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import Config
from tgbot.filters.filters_data import favorite, perspective
from tgbot.infrastructure.database.functions import update_user
from tgbot.keyboards.inline import prolong_keyboard
from tgbot.misc.states import Prolong


async def remove_favorite(user_id: int):
    favorite.remove(user_id)
    bot = Bot.get_current()
    m = await bot.send_message(user_id, f"У вас кончилась подписка") #тут надо как то отправить сообщение админу, что у пользователя кончилась подписка
    config: Config = bot.get('config')
    admin = config.tg_bot.admin_ids[0]
    await bot.send_message(admin, "У " + hlink(f"{m.chat.full_name}",
                                        f"tg://user?id={m.chat.id}") + " закончилась подписка.")


async def prolong_handler(user_id: int):
    bot = Bot.get_current()
    await bot.send_message(user_id,
                         "Добрый день!\n"
                         "У нас скоро заканчивается контракт с Вами, скажите, пожалуйста, Вам было бы интересно "
                         "продление?\n"
                         "Чтобы больше замотивировать наших моделей на работу, доступ в чат теперь будет платным, "
                         "5000 рублей за 3 месяца.\n"
                         "Мы же со своей стороны постараемся Вас развивать и активно показывать клиентам, если Вам "
                         "интересно реализоваться в этой сфере.", reply_markup=prolong_keyboard)
    await bot.send_message(user_id, "По всем вопросам можете писать @lkrioni")


async def add_favorite(m: types.Message, scheduler: AsyncIOScheduler, state: FSMContext, session):
    user_id = m.forward_from.id
    logging.info(f"{user_id}")
    await update_user(session, m.from_user.id, subscription_type='favorite')

    scheduler.add_job(prolong_handler, 'date', run_date=datetime.datetime.now() + datetime.timedelta(days=89), kwargs=dict(user_id=user_id))
    scheduler.add_job(remove_favorite, 'date', run_date=datetime.datetime.now() + datetime.timedelta(days=90), kwargs=dict(user_id=user_id))
    # scheduler.add_job(update_user, 'date', run_date=datetime.datetime.now() + datetime.timedelta(days=90), kwargs=dict(session=session, telegram_id=m.from_user.id, subscription_type='NULL'))
    await m.answer(f"Для пользователя " + hlink(f"{m.forward_from.full_name}",
                                                           f"tg://user?id={user_id}") + " оформлена подписка на 90 дней.")
    await state.finish()


async def add_perspective(m: types.Message, state: FSMContext, session):
    user_id = m.forward_from.id
    perspective.append(user_id)
    await update_user(session, m.from_user.id, subscription_type='perspective')
    await m.answer(f"Для пользователя " + hlink(f"{m.forward_from.full_name}",
                                                f"tg://user?id={user_id}") + " оформлена вечная подписка.")
    await state.finish()


async def end_contract(cb: CallbackQuery):
    await cb.message.answer("Спасибо за сотрудничество!", reply_markup=None)
    user = cb.from_user.id
    bot = Bot.get_current()
    config: Config = bot.get('config')
    admin = config.tg_bot.admin_ids[0]
    await bot.send_message(admin, hlink(f"{cb.from_user.full_name}",
                                                           f"tg://user?id={user}") + " решил завершить сотрудничество.")


async def add_f(m: types.Message):
    await Prolong.F.set()


async def add_p(m: types.Message):
    await Prolong.P.set()


async def delete_sub(m: types.Message, session):
    user_id = m.forward_from.id
    await update_user(session, user_id, subscription_type='NULL')


def register_prolong(dp: Dispatcher):
    dp.register_message_handler(add_f, Command("add_f"), is_admin=True)
    dp.register_message_handler(add_p, Command("add_p"), is_admin=True)
    dp.register_message_handler(delete_sub, Command("del_sub"), is_admin=True)
    dp.register_callback_query_handler(end_contract, lambda callback_query: callback_query.data == "contract_end")
    dp.register_message_handler(add_favorite, content_types=types.ContentType.PHOTO, state=Prolong.F)
    dp.register_message_handler(add_perspective, content_types=types.ContentType.ANY, state=Prolong.P)



