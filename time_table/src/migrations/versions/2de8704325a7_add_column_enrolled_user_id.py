"""add column 'enrolled_user_id'

Revision ID: 2de8704325a7
Revises: f9b9f1573f87
Create Date: 2024-10-16 12:03:15.691970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2de8704325a7'
down_revision: Union[str, None] = 'f9b9f1573f87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('time_table', sa.Column('enrolled_user_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('time_table', 'enrolled_user_id')
    # ### end Alembic commands ###
