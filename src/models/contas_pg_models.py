from sqlalchemy import ForeignKey, Integer, Numeric, String, Column
from sqlalchemy.orm import DeclarativeBase

class Base_ContasPagarReceber(DeclarativeBase):
    pass

class ContasPagarReceber(Base_ContasPagarReceber):
    __tablename__ = 'contas_a_pagar_receber'

    id = Column(Integer, primary_key=True, nullable=False)
    descricao = Column(String(30))
    valor = Column(Numeric)
    tipo = Column(String(30)) 

   