from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import DeclarativeBase
class Base_FornecedorCliente(DeclarativeBase):
    pass

class FornecedorCliente(Base_FornecedorCliente):
    __tablename__ = 'fornecedor_cliente'


    id = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String(255))


