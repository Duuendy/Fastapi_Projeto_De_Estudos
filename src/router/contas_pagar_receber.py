from decimal import Decimal
from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.models.db_models import ContasPagarReceber

from src.domain.conection import get_db_connection

router = APIRouter(prefix="/contas-a-pagar-e-receber")

class contasPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str

    class Config():
        orm_mode = True

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
def criar_conta(conta_a_pagar_e_receber_request: contasPagarReceberRequest, db_connection: Session = Depends(get_db_connection)) -> contasPagarReceberResponse:
 
    conta_a_pagar_e_receber = ContasPagarReceber(
        **conta_a_pagar_e_receber_request.model_dump()
    )

    db_connection.add(conta_a_pagar_e_receber)
    db_connection.commit()
    db_connection.refresh(conta_a_pagar_e_receber)

    return conta_a_pagar_e_receber