from sqlalchemy import Column, VARCHAR, BIGINT
from sqlalchemy.sql import expression

from tgbot.infrastructure.database.base import Base


class User(Base):
    __tablename__ = 'users'
    telegram_id = Column(BIGINT, nullable=False, autoincrement=False, primary_key=True)
    full_name = Column(VARCHAR(256), nullable=False)
    username = Column(VARCHAR(256), server_default=expression.null(), nullable=True)
    subscription_type = Column(VARCHAR(50), nullable=True, server_default=expression.null()) # favorite | perspective | NULL


