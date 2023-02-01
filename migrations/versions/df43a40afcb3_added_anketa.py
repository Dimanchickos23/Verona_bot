"""added_anketa

Revision ID: df43a40afcb3
Revises: 7b23040498dc
Create Date: 2022-11-09 17:43:07.290752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df43a40afcb3'
down_revision = '7b23040498dc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('anketa', sa.TEXT(), server_default=sa.text('NULL'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'anketa')
    # ### end Alembic commands ###