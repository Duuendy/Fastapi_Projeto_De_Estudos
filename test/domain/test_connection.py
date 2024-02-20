import pytest


from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.conection import get_db_connection
from src.models.contas_pg_models import ContasPagarReceber


# #FIXTURE - Definie a função setup_database como uma função que será automaticamente executada para todos os teste
# @pytest.fixture(scope="session", autouse=True)
# def setup_database()-> Engine:
#     #URL do banco de dados
#     SQLALCHEMY_DATABASE_URL = "sqlite:///.test.db"

#     #Mecanismo que irá conectar ao DataBase  através da URL informada
#     engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

#     #Variável responsável por criar sessões de banco de dados
#     TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#     def override_get_db():
#         #Instancia da sessão database
#         db = TestingSessionLocal
#         try:
#             yield db
#         finally:
#             db.close_all()

#     #Passo a funcao original como parametro para a funcao de teste
#     app.dependency_overrides[get_db_connection] = override_get_db

    # ContasPagarReceber.metadata.drop_all(bind=engine)
    # ContasPagarReceber.metadata.create_all(bind=engine)

    
#Para rodar o teste usando o pytest no terminal, não está funcionando, informa o erro de não encontrar a rota de alguns classes. Precisei usar o comando python -m pytest -v