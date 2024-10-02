"""create doctors

Revision ID: 00c9a8cd22f0
Revises: 21903ed58564
Create Date: 2024-10-02 23:29:30.803386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00c9a8cd22f0'
down_revision: Union[str, None] = '21903ed58564'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('doctors',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('lastName', sa.String(), nullable=False),
    sa.Column('firstName', sa.String(), nullable=False),
    sa.Column('specialty', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('doctors')
    # ### end Alembic commands ###
