"""empty message

Revision ID: 21903ed58564
Revises: 
Create Date: 2024-10-01 23:04:55.961934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21903ed58564'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('lastName', sa.String(), nullable=False),
    sa.Column('firstName', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('refresh_token', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###