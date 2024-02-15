from fastapi import FastAPI

from src.router import contas_pagar_receber


#Comando teste para verificar se os metodos de criação do BD estava funcionando - OK
#Importações para criação do banco de dados
# from src.domain.conection import DB_Engine
# from src.models.db_models import ContasPagarReceber

#Comando para derrubar e criar o BD assim que a aplicação fosse inicializada.
# ContasPagarReceber.metadata.drop_all(bind=DB_Engine)
# ContasPagarReceber.metadata.create_all(bind=DB_Engine)

app = FastAPI()
app.include_router(contas_pagar_receber.router)

@app.get("/")
def root():
    return "Hello Word!!"

## Essa linha de código está funcionando e foi usada para testar a conexão com o BD e criação da tabale 'user'
# @app.get("/")
# async def root(db_connection: Session = Depends(get_db_connection)):
#      db_connection.execute(text("create table users (FirstName varchar(255), LastName varchar(255))"))
#      db_connection.commit()

     
