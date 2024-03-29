"""Init database

Revision ID: 7b23040498dc
Revises: 
Create Date: 2022-10-18 16:14:29.894237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b23040498dc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('telegram_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('full_name', sa.VARCHAR(length=256), nullable=False),
    sa.Column('username', sa.VARCHAR(length=256), server_default=sa.text('NULL'), nullable=True),
    sa.Column('subscription_type', sa.VARCHAR(length=50), server_default=sa.text('NULL'), nullable=True),
    sa.PrimaryKeyConstraint('telegram_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
