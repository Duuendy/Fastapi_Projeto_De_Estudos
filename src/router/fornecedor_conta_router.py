from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.models.contas_pg_models import ContasPagarReceber
from src.router.contas_pagar_receber_router import ContasPagarReceberResponse
from src.domain.conection import get_db_connection

router = APIRouter(prefix="/fornecedor-cliente")


@router.get("/{id_fornecedor_cliente}/contas-a-pagar-e-receber", response_model=List[ContasPagarReceberResponse])
def listar_contas_pagar_receber_de_fornecedor_cliente_by_id(
        id_fornecedor_cliente: int,
        db_connection: Session = Depends(get_db_connection)) -> List[ContasPagarReceberResponse]:
    return db_connection.query(ContasPagarReceber).filter_by(fornecedor_id=id_fornecedor_cliente).all()
