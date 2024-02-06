from fastapi import FastAPI, Depends

from sqlalchemy import select, text
from sqlalchemy.orm import Session
from src.models.db_models import ContasPagarReceber
from src.router import contas_pagar_receber
from src.domain.conection import get_db_connection


# Base_ContasPagarReceber.metadata.drop_all(bind=DB_Engine)
# Base_ContasPagarReceber.metadata.create_all(bind=DB_Engine)

app = FastAPI()

# @app.get("/")
# def root():
#     return "Hello Word!!"

## Essa linha de código está funcionando e foi usada para testar a conexão com o BD e criação da tabale 'user'
# @app.get("/")
# async def root(db_connection: Session = Depends(get_db_connection)):
#      db_connection.execute(text("create table users (FirstName varchar(255), LastName varchar(255))"))
#      db_connection.commit()

@app.get("/")
async def root(db_connection: Session = Depends(get_db_connection)):
     select_query = select(ContasPagarReceber)

     db_connection.execute(select_query)
     db_connection.commit()
     
app.include_router(contas_pagar_receber.router)