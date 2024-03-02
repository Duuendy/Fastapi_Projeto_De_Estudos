from sqlalchemy import Integer, Numeric, String, Column, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from src.models import DB_Model


class ContasPagarReceber(DB_Model):
    __tablename__ = 'contas_a_pagar_receber'

    id = Column(Integer, primary_key=True, nullable=False)
    descricao = Column(String(30))
    valor = Column(Numeric)
    tipo = Column(String(30))
    data_baixa = Column(DateTime())
    valor_baixa = Column(Numeric)
    status = Column(Boolean, default=False)

    fornecedor_id = Column(Integer, ForeignKey("fornecedor_cliente.id"))
    fornecedor = relationship("FornecedorCliente")


class FornecedorCliente(DB_Model):
    __tablename__ = 'fornecedor_cliente'

    id = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String(255))
