import pytest
from main import app

# from unittest.mock import Mock
# from faker import Faker

from fastapi.testclient import TestClient

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.domain.conection import get_db_connection
from src.models.db_models import ContasPagarReceber



# fake = Faker()

# @pytest.fixture
# def mock_contas_pagar_receber() -> ContasPagarReceber:

#     mocked_constas_pg = Mock(spec_set=ContasPagarReceber)
#     mocked_constas_pg.id.return_value = fake.random_int(min=1, max=30)
#     mocked_constas_pg.descricao.return_value = fake.descricao()
#     mocked_constas_pg.valor.return_value = fake.random_numeric()
#     mocked_constas_pg.tipo.return_value = fake.tipo()

#     return mocked_constas_pg


#URL do banco de dados
SQLALCHEMY_DATABASE_URL = "sqlite:///.test.db"

#Mecanismo que irá conectar ao DataBase  através da URL informada
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

#Variável responsável por criar sessões de banco de dados
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Session: # type: ignore
    #Instancia da sessão database
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#Passo a funcao original como parametro para a funcao de teste
app.dependency_overrides[get_db_connection] = override_get_db

    
client = TestClient(app)
    

def test_listar_contas_pagar_receber():

    ContasPagarReceber.metadata.drop_all(bind=engine)
    ContasPagarReceber.metadata.create_all(bind=engine)
    
    # client.post("/contas-a-pagar-e-receber", json={'descricao': 'Aluguel', 'valor': 1000.5, 'tipo': 'PAGAR'})
    # client.post("/contas-a-pagar-e-receber", json={'descricao': 'Salario', 'valor': 5555.55, 'tipo': 'RECEBER'})

    nova_conta = {
        "descricao": "Aluguel",
        "valor": 1000.5,
        "tipo": "PAGAR"
    }

    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 1
    #nova_conta_copy["valor"] = str(nova_conta_copy['valor'])

    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    assert response.status_code == 201
    assert response.json() == nova_conta_copy


    response = client.get('/contas-a-pagar-e-receber')
    assert response.status_code == 200
    
    assert response.json() == [
        {'id': 1, 'descricao': 'Aluguel', 'valor': 1000.5, 'tipo': 'PAGAR'}, 
        #{'id': 2, 'descricao': 'Salario', 'valor': 5555.55, 'tipo': 'RECEBER'}
    ]

def test_criar_conta_pagar_receber():

    ContasPagarReceber.metadata.drop_all(bind=engine)
    ContasPagarReceber.metadata.create_all(bind=engine)

    nova_conta = {
        "descricao": "Faculdade",
        "valor": 150.00,
        "tipo": "PAGAR"
    }

    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 1
    #nova_conta_copy["valor"] = str(nova_conta_copy['valor'])

    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    assert response.status_code == 201
    assert response.json() == nova_conta_copy
    

# def test_atualizar_conta_pagar_receber():

#     response = client.post("/contas-a-pagar-e-receber", json={
#             "descricao": "Investimento",
#             "valor": 1500,
#             "tipo": "RECEBER"
#         })
    
#     id_conta_a_pagar_e_receber = response.json()["id"]
    
#     response_put = client.put("/contas-a-pagar-e-receber/{id_conta_a_pagar_e_receber}", json={
#             "descricao": "Investimento",
#             "valor": 3000,
#             "tipo": "RECEBER"
#         })

#     assert response_put.status_code == 200