from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.db_models import ContasPagarReceber
from src.domain.conection import get_db_connection

# from unittest.mock import Mock
# from faker import Faker
from main import app

# fake = Faker()

# @pytest.fixture
# def mock_contas_pagar_receber() -> ContasPagarReceber:

#     mocked_constas_pg = Mock(spec_set=ContasPagarReceber)
#     mocked_constas_pg.id.return_value = fake.random_int(min=1, max=30)
#     mocked_constas_pg.descricao.return_value = fake.descricao()
#     mocked_constas_pg.valor.return_value = fake.random_numeric()
#     mocked_constas_pg.tipo.return_value = fake.tipo()

#     return mocked_constas_pg



#Para rodar o teste, só chamar o pytest no terminal, não está funcionando, informa o erro de não encontrar a rota de alguns classes. Precisei usar o comando python -m pytest -v

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal
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

    response = client.get('/contas-a-pagar-e-receber')
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'descricao': 'Aluguel', 'valor': '1000.5', 'tipo': 'PAGAR'}, 
        {'id': 2, 'descricao': 'Salario', 'valor': '5555.55', 'tipo': 'RECEBER'}
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

    response = client.post('/contas-a-pagar-e-receber', json=nova_conta)
    
    assert response.status_code == 201
    assert response.json()  == nova_conta_copy

def teste_retornar_erro_descricao():
    response = client.post('/contas-a-pagar-e-receber', json={
        "descricao": "0123456789012345678901234567890",
        "valor": 150.00,
        "tipo": "PAGAR"
    })
    
    assert response.status_code == 422
    #SQLite não força o tamanho de um VARCHAR

    #nova_conta_copy = nova_conta.copy()
    #nova_conta_copy["id"] = 3
    #assert response.json() == nova_conta_copy

     
    #Esta ocorrendo um erro onde o pytest informa que a representação numerica dos valores entre response.json() e nova_conta_copy
    #Para a solução, testei força transformar os valores em string, porem sem sucesso 
    #assert str(response.json()["valor"]) == str(nova_conta_copy("valor"))
    
    #Para a solução, testei força formatar os valores, porem sem sucesso 
    #assert "{:.2f}".format(response.json()["valor"]) == "{:.2f}".format(nova_conta_copy["valor"])

def test_atualizar_conta_pagar_receber():

    ContasPagarReceber.metadata.drop_all(bind=engine)
    ContasPagarReceber.metadata.create_all(bind=engine)
    
    
    response = client.post('/contas-a-pagar-e-receber', json=nova_conta)
    nova_conta = {
        "descricao": "Faculdade",
        "valor": 150.00,
        "tipo": "PAGAR"
    }

    id_da_conta_pagar_receber = response.json()['id']

    response_put = client.put('/contas-a-pagar-e-receber/{id_da_conta_pagar_receber}', json={
        "descricao": "Faculdade",
        "valor": 150.00,
        "tipo": "PAGAR"
    })

    assert response_put.status_code == 200
    