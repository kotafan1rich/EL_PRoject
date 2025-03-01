"""chande auto

Revision ID: e0edb616b690
Revises: 40e10bfd393d
Create Date: 2024-12-08 22:04:45.617433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0edb616b690'
down_revision: Union[str, None] = '40e10bfd393d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'id_tg', existing_type=sa.Integer(), type_=sa.BigInteger())

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'id_tg')
    # ### end Alembic commands ###
