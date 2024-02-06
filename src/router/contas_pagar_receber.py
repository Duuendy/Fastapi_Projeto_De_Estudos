from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/contas-a-pagar-e-receber")

class contasPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str

class contasPagarReceberRequest(BaseModel):
    descricao: str
    valor: Decimal
    tipo: str


@router.get("", response_model=List[contasPagarReceberResponse])
def listar_contas():
    # metodo irá retornar uma lista de informações de operações bancárias
    return [
        contasPagarReceberResponse(
            id=1,
            descricao="Aluguel",
            valor=1000.50, 
            tipo="PAGAR"
        ),
        contasPagarReceberResponse(
            id=2,
            descricao="Salario",
            valor=5555.55, 
            tipo="RECEBER"
        ),       
    ]    

@router.post("/", response_model=contasPagarReceberResponse, status_code=201)
def criar_conta(conta: contasPagarReceberRequest):

    

    return contasPagarReceberResponse(
            id=3,
            descricao=conta.descricao,
            valor=conta.valor, 
            tipo=conta.tipo
    )