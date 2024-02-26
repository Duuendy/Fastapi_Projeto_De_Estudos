"""Criando tabela com chave estrangeira de fornecedor

Revision ID: ffa7b9429c8c
Revises: c1f7461814c3
Create Date: 2024-02-26 18:47:14.535590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffa7b9429c8c'
down_revision: Union[str, None] = 'c1f7461814c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contas_a_pagar_receber', sa.Column('forncedor_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'contas_a_pagar_receber', 'fornecedor_cliente', ['forncedor_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contas_a_pagar_receber', type_='foreignkey')
    op.drop_column('contas_a_pagar_receber', 'forncedor_id')
    # ### end Alembic commands ###
