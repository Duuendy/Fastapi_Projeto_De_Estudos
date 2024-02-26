"""Criando tabela fornecedor

Revision ID: c1f7461814c3
Revises: 1309e3ec5551
Create Date: 2024-02-26 17:39:24.189931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1f7461814c3'
down_revision: Union[str, None] = '1309e3ec5551'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fornecedor_cliente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fornecedor_cliente')
    pass
    # ### end Alembic commands ###
