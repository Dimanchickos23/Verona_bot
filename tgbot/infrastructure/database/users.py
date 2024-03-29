from sqlalchemy import Column, VARCHAR, BIGINT, TEXT, TIMESTAMP, func, DateTime
from sqlalchemy.sql import expression

from tgbot.infrastructure.database.base import Base


class User(Base):
    __tablename__ = 'users'
    telegram_id = Column(BIGINT, nullable=False, autoincrement=False, primary_key=True)
    full_name = Column(VARCHAR(256), nullable=False)
    username = Column(VARCHAR(256), server_default=expression.null(), nullable=True)
    subscription_type = Column(VARCHAR(50), nullable=True, server_default=expression.null()) # favorite | perspective | NULL
    subscription_date = Column(DateTime, server_default=expression.null())
    anketa = Column(TEXT, nullable=True, server_default=expression.null())
    created_at = Column(DateTime, server_default=func.now())
    chat_id= Column(VARCHAR(50), nullable=True, server_default=expression.null())


