from fastapi import APIRouter, Depends

from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.contas_pg_models import ContasPagarReceber
from src.domain.conection import get_db_connection
from src.domain.exceptions import NotFound

router = APIRouter(prefix="/fornedor-cliente")

class FornecedorClienteResponse(BaseModel):
    id: int
    nome: str

    class ConfigDict():
        orm_mode = True

class FornecedorClienteRequest(BaseModel):
    id: int
    nome: str

def listar_fornecedor_cliente():
    return

def listar_fornecedor_cliente_by_id():
    return

def cadastrar_fornecedor_cliente():
    return

def atualizar_fornecedor_cliente():
    return

def remover_fornecedor_cliente():
    return
    