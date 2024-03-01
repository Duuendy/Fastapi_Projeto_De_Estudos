from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.domain.conection import get_db_connection
from src.domain.exceptions import NotFound
from src.models.contas_pg_models import FornecedorCliente

router = APIRouter(prefix="/fornecedor-cliente")


class FornecedorClienteResponse(BaseModel):
    id: int
    nome: str

    class ConfigDict:
        orm_mode = True


class FornecedorClienteRequest(BaseModel):
    nome: str


def buscar_usuario_por_id(id_fornecedor_cliente: int, db_connection: Session) -> FornecedorCliente:
    fornecedor_cliente = db_connection.get(FornecedorCliente, id_fornecedor_cliente)

    if fornecedor_cliente is None:
        raise NotFound('Fornecedor e Cliente')
    return fornecedor_cliente


@router.get("", response_model=List[FornecedorClienteResponse])
def listar_fornecedor_cliente(db_connecion: Session = Depends(get_db_connection)) -> FornecedorClienteResponse:
    # def listar_fornecedor_cliente():
    #     return [
    #         FornecedorClienteResponse(
    #             id=1,
    #             nome="Endy"
    #         ),
    #         FornecedorClienteResponse(
    #             id=2,
    #             nome="Akira"
    #         )
    #     ]
    return db_connecion.query(FornecedorCliente).all()


@router.get("/{id_fornecedor_cliente}", response_model=FornecedorClienteResponse)
def listar_fornecedor_cliente_by_id(id_fornecedor_cliente: int,
                                    db_connection: Session = Depends(get_db_connection)) -> FornecedorClienteResponse:
    return buscar_usuario_por_id(id_fornecedor_cliente, db_connection)


@router.post("", response_model=FornecedorClienteResponse, status_code=201)
def cadastrar_fornecedor_cliente(fornecedor_cliente_request: FornecedorClienteRequest,
                                 db_connection: Session = Depends(get_db_connection)) -> FornecedorClienteResponse:
    fornecedor_cliente = FornecedorCliente(
        **fornecedor_cliente_request.model_dump()
    )

    db_connection.add(fornecedor_cliente)
    db_connection.commit()
    db_connection.refresh(fornecedor_cliente)

    return fornecedor_cliente


@router.put("/{id_fornecedor_cliente}", response_model=FornecedorClienteResponse, status_code=200)
def atualizar_fornecedor_cliente(id_fornecedor_cliente: int, forncedor_cliente_request: FornecedorClienteRequest,
                                 db_connection: Session = Depends(get_db_connection)) -> FornecedorClienteResponse:
    fornecedor_cliente = buscar_usuario_por_id(id_fornecedor_cliente, db_connection)

    fornecedor_cliente.nome = forncedor_cliente_request.nome

    db_connection.add(fornecedor_cliente)
    db_connection.commit()
    db_connection.refresh(fornecedor_cliente)

    return fornecedor_cliente


@router.delete("/{id_fornecedor_cliente}", status_code=204)
def remover_fornecedor_cliente(id_fornecedor_cliente: int, db_connection: Session = Depends(get_db_connection)) -> None:
    fornecedor_cliente = buscar_usuario_por_id(id_fornecedor_cliente, db_connection)
    db_connection.delete(fornecedor_cliente)
    db_connection.commit()
    return


