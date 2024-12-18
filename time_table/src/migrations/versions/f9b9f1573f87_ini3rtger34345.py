"""ini3rtger34345

Revision ID: f9b9f1573f87
Revises: 
Create Date: 2024-10-13 23:02:03.441255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9b9f1573f87'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('time_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hospitalId', sa.Integer(), nullable=False),
    sa.Column('doctorId', sa.Integer(), nullable=False),
    sa.Column('from_', sa.DateTime(), nullable=False),
    sa.Column('to', sa.DateTime(), nullable=False),
    sa.Column('room', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('time_table')
    # ### end Alembic commands ###
