from fastapi import FastAPI, Depends

from sqlalchemy import text
from sqlalchemy.orm import Session
from src.api.router import contas_pagar_receber
from src.domain.conection import get_db_connection


app = FastAPI()


@app.get("/")
def root():
    
    return


app.include_router(contas_pagar_receber.router)

# async def root(db_connection: Session = Depends(get_db_connection)):
#      db_connection.execute(text("create table users (FirstName varchar(255), LastName varchar(255))"))
#      db_connection.commit()
