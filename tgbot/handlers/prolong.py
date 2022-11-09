import datetime
import logging

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import Config
from tgbot.infrastructure.database.functions import update_user
from tgbot.keyboards.inline import prolong_keyboard
from tgbot.misc.states import Prolong


async def remove_favorite(user_id: int):
    dp = Dispatcher.get_current()
    session_pool = dp.middleware.applications[0].kwargs.get('session_pool')
    async with session_pool() as session:
        await update_user(session, telegram_id=user_id, subscription_type=None)
    bot = Bot.get_current()
    m = await bot.send_message(user_id,
                               f"У вас кончилась подписка")  # тут надо как то отправить сообщение админу, что у пользователя кончилась подписка
    config: Config = bot.get('config')
    admin = config.tg_bot.admin_ids[0]
    await bot.send_message(admin, "У " + hlink(f"{m.chat.full_name}",
                                               f"tg://user?id={m.chat.id}") + " закончилась подписка.")


async def prolong_handler(user_id: int):
    bot = Bot.get_current()
    await bot.send_message(user_id,
                           "Добрый день!\n"
                           "У нас завтра заканчивается контракт с Вами, скажите, пожалуйста, Вам было бы интересно "
                           "продление?\n"
                           "Чтобы больше замотивировать наших моделей на работу, доступ в чат теперь будет платным, "
                           "5000 рублей за 3 месяца.\n"
                           "Продлить доступ можно по ссылке ниже. Выберите продукт «Доступ в чаты трудоустройства».\n"
                           "Мы же со своей стороны постараемся Вас развивать и активно показывать клиентам, если Вам "
                           "интересно реализоваться в этой сфере.\n"
                           "После оплаты отправьте чек @nzsz13"
                           , reply_markup=prolong_keyboard)
    await bot.send_message(user_id, "По всем вопросам можете писать @lkrioni")



async def add_perspective(m: types.Message, state: FSMContext, session):
    user_id = m.forward_from.id
    await update_user(session, telegram_id=user_id, subscription_type='perspective')
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
    await Prolong.F1.set()
    await m.answer("На сколько дней вы хотите оформить подписку?\nВведите число")


async def how_long(m: types.Message, state: FSMContext):
    await state.update_data(days=int(m.text))
    await Prolong.F2.set()
    await m.answer(f"Перешлите только фото чека пользователя. После этого будет оформлена подписка на {m.text} дней.")


async def add_favorite(m: types.Message, scheduler: AsyncIOScheduler, state: FSMContext, session):
    user_id = m.forward_from.id
    logging.info(f"{user_id}")
    data = await state.get_data()
    days = data.get("days")
    await update_user(session, telegram_id=user_id, subscription_type='favorite')
    scheduler.add_job(prolong_handler, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=days-1),
                      kwargs=dict(user_id=user_id))
    scheduler.add_job(remove_favorite, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=days),
                      kwargs=dict(user_id=user_id))
    await m.answer(f"Для пользователя " + hlink(f"{m.forward_from.full_name}",
                                                f"tg://user?id={user_id}") + f" оформлена подписка на {days} дней.")
    await state.finish()


async def add_p(m: types.Message):
    await Prolong.P.set()
    await m.answer("Перешлите любое сообщение от пользователя. После этого будет оформлена вечна подписка.")


async def delete_sub(m: types.Message, session, state: FSMContext):
    user_id = m.forward_from.id
    await m.answer(f"Для пользователя " + hlink(f"{m.forward_from.full_name}",
                                                f"tg://user?id={user_id}") + " удален статус подписки.")
    await update_user(session, user_id, subscription_type='NULL')
    await state.finish()


async def del_sub(m: types.Message):
    await Prolong.D.set()
    await m.answer("Перешлите любое сообщение от пользователя. Его подписка будет отменена.")


def register_prolong(dp: Dispatcher):
    dp.register_message_handler(add_f, Command("add_f"), is_admin=True)
    dp.register_message_handler(add_p, Command("add_p"), is_admin=True)
    dp.register_message_handler(del_sub, Command("del_sub"), is_admin=True)
    dp.register_callback_query_handler(end_contract, lambda callback_query: callback_query.data == "contract_end")
    dp.register_message_handler(how_long, state=Prolong.F1)
    dp.register_message_handler(add_favorite, content_types=types.ContentType.PHOTO, state=Prolong.F2)
    dp.register_message_handler(add_perspective, content_types=types.ContentType.ANY, state=Prolong.P)
    dp.register_message_handler(delete_sub, content_types=types.ContentType.ANY, state=Prolong.D)

