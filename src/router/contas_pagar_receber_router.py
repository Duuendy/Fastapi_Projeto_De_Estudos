from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.router.fornecedor_cliente_router import FornecedorClienteResponse
from src.models.contas_pg_models import ContasPagarReceber, FornecedorCliente
from src.domain.conection import get_db_connection
from src.domain.exceptions import NotFound

router = APIRouter(prefix="/contas-a-pagar-e-receber")


class ContasPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    tipo: str
    data_baixa: datetime | None = None
    valor_baixa: float | None = None
    status: bool | None = None
    fornecedor: FornecedorClienteResponse | None = None

    class ConfigDict:
        orm_mode = True


# OBS - O pytest não reconhece a entrada de dados configurado dessa forma, passando uma classe que recebece como
# propriedade str e Enum class ContasPagarReceberTipoEnum(str, Enum): PAGAR: 'PAGAR' # type: ignore RECEBER:
# 'RECEBER' # type: ignore

class ContasPagarReceberRequest(BaseModel):
    descricao: str
    valor: float
    tipo: str
    fornecedor_id: int | None = None


# OBS - O Fiel, no atual momento está sendo removido de versões do Pydantic, a solução foi usar o
# 'json_schema_extra', mas não obtive sucesso; Preciso olhar melhor esse novo metodo;


# descricao: str = Field(min_lenght=3, max_lenght=30)
# valor: Decimal = Field(gt=0)
# tipo: ContasPagarReceberTipoEnum

def buscar_por_id(id_conta_a_pagar_e_receber: int,
                  db_connection: Session) -> ContasPagarReceber:
    conta_a_pagar_e_receber = db_connection.get(ContasPagarReceber, id_conta_a_pagar_e_receber)

    if conta_a_pagar_e_receber is None:
        raise NotFound('Conta a Pagar e Receber')
    return conta_a_pagar_e_receber


# Verificando se o fornecedor existe - Verificando direto e caso não exista, tratar o erro
def valida_fornecedor(fornecedor_id, db_connection):
    if fornecedor_id is not None:
        conta_a_pagar_e_receber = db_connection.query(FornecedorCliente).get(fornecedor_id)
        if conta_a_pagar_e_receber is None:
            raise HTTPException(status_code=422, detail="Fornecedor não existe no BD")


@router.get("", response_model=List[ContasPagarReceberResponse])
def listar_contas(db_connection: Session = Depends(get_db_connection)) -> ContasPagarReceberResponse:
    return db_connection.query(ContasPagarReceber).all()


# def listar_contas():
#     # metodo irá retornar uma lista de informações de operações bancárias
#     return[ContasPagarReceberResponse(
#             id=1,
#             descricao="Aluguel",
#             valor=1000,50,
#             tipo="PAGAR"
#         )
#         ContasPagarReceberResponse(
#             id=2,
#             descricao="Salario",
#             valor=5555.55, 
#             tipo="RECEBER"
#         ),
#     ]    

@router.get("/{id_conta_a_pagar_e_receber}", response_model=ContasPagarReceberResponse)
def listar_contas_id(id_conta_a_pagar_e_receber: int,
                     db_connection: Session = Depends(get_db_connection)) -> ContasPagarReceberResponse:
    # Tratando erro caso a query solicitada não esteja correta(EX. Solicitar um id inexistente)
    # if conta_a_pagar_e_receber is None:
    #     raise HTTPException(status_code=404, detail="Item not found")

    return buscar_por_id(id_conta_a_pagar_e_receber, db_connection)


@router.post("", response_model=ContasPagarReceberResponse, status_code=201)
def criar_conta(conta_a_pagar_e_receber_request: ContasPagarReceberRequest,
                db_connection: Session = Depends(get_db_connection)) -> ContasPagarReceberResponse:
    # Função que irá validar se o fornecedor_id existe, caso não exista, a função criar_conta, não inicia
    valida_fornecedor(conta_a_pagar_e_receber_request.fornecedor_id, db_connection)

    # Para escrever no banco, crio uma variável que tem como modelo a Class do db_models, usando os parametros e
    # passando em uma lista;
    conta_a_pagar_e_receber = ContasPagarReceber(
        **conta_a_pagar_e_receber_request.model_dump()
    )

    db_connection.add(conta_a_pagar_e_receber)
    db_connection.commit()
    db_connection.refresh(conta_a_pagar_e_receber)

    return conta_a_pagar_e_receber


@router.put("/{id_conta_a_pagar_e_receber}", response_model=ContasPagarReceberResponse, status_code=200)
def atualizar_conta(id_conta_a_pagar_e_receber: int,
                    conta_a_pagar_e_receber_request: ContasPagarReceberRequest,
                    db_connection: Session = Depends(get_db_connection)) -> ContasPagarReceberResponse:
    valida_fornecedor(conta_a_pagar_e_receber_request.fornecedor_id, db_connection)
    # Busco no meu DB(db_connection.query) uma classe a partir do "id" conta_a_pagar_e_receber: ContasPagarReceber =
    # db_connection.query(ContasPagarReceber).get(id_conta_a_pagar_e_receber)

    # Metodo para buscar o item a partir de ID
    conta_a_pagar_e_receber = buscar_por_id(id_conta_a_pagar_e_receber, db_connection)
    # Os dados recebido e salvo na variavel, são atualziados nas variaveis através das respectivas variaveis
    conta_a_pagar_e_receber.tipo = conta_a_pagar_e_receber_request.tipo
    conta_a_pagar_e_receber.valor = conta_a_pagar_e_receber_request.valor
    conta_a_pagar_e_receber.descricao = conta_a_pagar_e_receber_request.descricao
    conta_a_pagar_e_receber.fornecedor_id = conta_a_pagar_e_receber_request.fornecedor_id

    db_connection.add(conta_a_pagar_e_receber)
    db_connection.commit()
    db_connection.refresh(conta_a_pagar_e_receber)

    return conta_a_pagar_e_receber


@router.delete("/{id_conta_a_pagar_e_receber}", status_code=204)
def remover_conta(id_conta_a_pagar_e_receber: int,
                  db_connection: Session = Depends(get_db_connection)) -> None:
    conta_a_pagar_e_receber = buscar_por_id(id_conta_a_pagar_e_receber, db_connection)
    db_connection.delete(conta_a_pagar_e_receber)
    db_connection.commit()

@router.post("/{id_conta_a_pagar_e_receber}/baixar", response_model=ContasPagarReceberResponse, status_code=200)
def baixar_conta(
        id_conta_a_pagar_e_receber: int,
        db_connection: Session = Depends(get_db_connection)) -> ContasPagarReceberResponse:

    # Metodo para buscar o item a partir de ID
    conta_a_pagar_e_receber = buscar_por_id(id_conta_a_pagar_e_receber, db_connection)

    if conta_a_pagar_e_receber.status and conta_a_pagar_e_receber.valor == conta_a_pagar_e_receber.valor_baixa:
        return conta_a_pagar_e_receber

    conta_a_pagar_e_receber.data_baixa = datetime.now()
    conta_a_pagar_e_receber.status = True
    conta_a_pagar_e_receber.valor_baixa = conta_a_pagar_e_receber.valor

    db_connection.add(conta_a_pagar_e_receber)
    db_connection.commit()
    db_connection.refresh(conta_a_pagar_e_receber)

    return conta_a_pagar_e_receber
