from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base_ContasPagarReceber(DeclarativeBase):
    pass

class ContasPagarReceber(Base_ContasPagarReceber):
    __tablename__ = 'contas_a_pagar_receber'

    id = mapped_column(Integer, primary_key=True, nulable=False)
    descricao = mapped_column(String(30))
    valor = mapped_column(Numeric)
    tipo = mapped_column(String(30)) 