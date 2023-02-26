import datetime
from typing import Callable, AsyncContextManager

from sqlalchemy import select, update, delete, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tgbot.config import DbConfig
from tgbot.infrastructure.database.users import User


def create_session_pool(db: DbConfig, echo=False) -> Callable[[], AsyncContextManager[AsyncSession]]:
    engine = create_async_engine(
        db.construct_sqlalchemy_url(),
        query_cache_size=1200,
        pool_size=20,
        max_overflow=200,
        future=True,
        echo=echo,
    )

    session_pool = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    return session_pool


async def get_user(session, telegram_id: int):
    stmt = select(
        User
    ).where(User.telegram_id == telegram_id)

    result = await session.scalars(stmt)
    return result.first()


async def delete_user(session, telegram_id: int):
    stmt = delete(
        User
    ).where(User.telegram_id == telegram_id)

    await session.scalars(stmt)


async def create_user(session, telegram_id,
                      full_name,
                      username):
    await session.execute(
        insert(
            User
        ).values(
            telegram_id=telegram_id,
            full_name=full_name,
            username=username
        )
    )
    await session.commit()


async def update_user(session, telegram_id, subscription_type, subscription_date=None):
    statement = update(
        User
    ).where(User.telegram_id == telegram_id).values(
        subscription_type=subscription_type,
        subscription_date=subscription_date
    )
    await session.execute(statement)
    await session.commit()


async def update_anketa(session, telegram_id, anketa):
    statement = update(
        User
    ).where(User.telegram_id == telegram_id).values(
        anketa=anketa
    )
    await session.execute(statement)
    await session.commit()


async def update_chat_id(session, telegram_id, chat_id):
    statement = update(
        User
    ).where(User.telegram_id == telegram_id).values(
        chat_id=chat_id
    )
    await session.execute(statement)
    await session.commit()


async def subs_90_list(session):
    statement = select(
        User.telegram_id.label('id'),
        User.full_name.label('name'),
        User.subscription_type.label('sub')
    ).where(
        and_(datetime.datetime.now() - User.created_at <= datetime.timedelta(days=91),
             datetime.datetime.now() - User.created_at >= datetime.timedelta(days=89))
    )
    result = await session.execute(statement)
    return result.all()


async def get_channel_users(session, chat_id):
    statement = select(
        User.full_name.label('name'),
        User.subscription_type.label('sub'),
        User.subscription_date.label('sub_date')
    ).where(
        User.chat_id == chat_id
    )
    result = await session.execute(statement)
    return result.all()