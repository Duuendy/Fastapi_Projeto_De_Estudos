from decimal import Decimal
from enum import Enum
from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.models.db_models import ContasPagarReceber

from src.domain.conection import get_db_connection

router = APIRouter(prefix="/contas-a-pagar-e-receber")

class ContasPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str

    class Config():
        orm_mode = True

class ContasPagarReceberTipoEnum(str, Enum):
    PAGAR: 'PAGAR' # type: ignore
    RECEBER: 'RECEBER' # type: ignore

class ContasPagarReceberRequest(BaseModel):
    descricao: str = Field(min_lenght=3, max_lenght=30)
    valor: Decimal = Field(gt=0)
    tipo: ContasPagarReceberTipoEnum


@router.get("", response_model=List[ContasPagarReceberResponse])
#def listar_contas(db_connection: Session = Depends(get_db_connection)) -> ContasPagarReceberResponse:
def listar_contas():
    # metodo irá retornar uma lista de informações de operações bancárias
    return [
        ContasPagarReceberResponse(
            id=1,
            descricao="Aluguel",
            valor=1000.50, 
            tipo="PAGAR"
        ),
        ContasPagarReceberResponse(
            id=2,
            descricao="Salario",
            valor=5555.55, 
            tipo="RECEBER"
        ),       
    ]    
    # return db_connection.query(ContasPagarReceber).all()

@router.post("", response_model=ContasPagarReceberResponse, status_code=201)
def criar_conta(conta_a_pagar_e_receber_request: ContasPagarReceberRequest, db_connection: Session = Depends(get_db_connection)) -> ContasPagarReceberResponse:
    
    #Para escrever no banco, crio uma variável que tem como modelo a Class do db_models, usando os parametros e passando em uma lista;  
    conta_a_pagar_e_receber = ContasPagarReceber(
        **conta_a_pagar_e_receber_request.model_dump()
    )

    db_connection.add(conta_a_pagar_e_receber)
    db_connection.commit()
    db_connection.refresh(conta_a_pagar_e_receber)

    return conta_a_pagar_e_receber

@router.put("/{id_da_conta_pagar_receber}", response_model=ContasPagarReceberResponse, status_code=200)
def criar_conta(id_da_conta_pagar_receber: int,
                conta_a_pagar_e_receber_request: ContasPagarReceberRequest, 
                db_connection: Session = Depends(get_db_connection)) -> ContasPagarReceberResponse:
    
    conta_a_pagar_e_receber: ContasPagarReceber = db_connection.query(ContasPagarReceber).get(id_da_conta_pagar_receber)
    conta_a_pagar_e_receber.tipo = conta_a_pagar_e_receber_request.tipo
    conta_a_pagar_e_receber.valor = conta_a_pagar_e_receber_request.valor
    conta_a_pagar_e_receber.descricao = conta_a_pagar_e_receber_request.descricao

    db_connection.add(conta_a_pagar_e_receber)
    db_connection.commit()
    db_connection.refresh()

    return conta_a_pagar_e_receber