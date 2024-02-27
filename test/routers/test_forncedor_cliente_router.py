import httpx
from main import app

from fastapi.testclient import TestClient

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.domain.conection import get_db_connection
from src.models.contas_pg_models import FornecedorCliente
#URL do banco de dados
SQLALCHEMY_DATABASE_URL = "sqlite:///.test.db"

#Mecanismo que irá conectar ao DataBase  através da URL informada
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False}, echo=True)

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

def test_listar_fornecedor_cliente():

    FornecedorCliente.metadata.drop_all(bind=engine)
    FornecedorCliente.metadata.create_all(bind=engine)

    novo_fornecedor_cliente = {
        "nome": "Katsue Hernandes Haiabe"
    }

    novo_fornecedor_cliente_copy = novo_fornecedor_cliente.copy()
    novo_fornecedor_cliente_copy["id"] = 1

    response = client.post("/fornedor-cliente", json=novo_fornecedor_cliente)
    assert response.status_code == 201
    assert response.json() == novo_fornecedor_cliente_copy

    response = client.get('/fornedor-cliente')
    assert response.status_code == 200

    assert response.json() == [
        {'id': 1, 'nome': 'Katsue Hernandes Haiabe'}
    ]

def test_listar_fornecedor_cliente_by_id():

    FornecedorCliente.metadata.drop_all(bind=engine)
    FornecedorCliente.metadata.create_all(bind=engine)

    novo_fornecedor_cliente = {
        "nome": "Katsue Hernandes Haiabe"
    }

    novo_fornecedor_cliente_copy = novo_fornecedor_cliente.copy()
    novo_fornecedor_cliente_copy["id"] = 1

    response = client.post("/fornedor-cliente", json=novo_fornecedor_cliente)
    assert response.status_code == 201
    assert response.json() == novo_fornecedor_cliente_copy

    id_fornecedor_cliente = response.json()["id"]
    
    response_delete = client.get(f"/fornedor-cliente/{id_fornecedor_cliente}")

    assert response_delete.status_code == 200

    return

def test_criar_fornecedor_cliente():

    FornecedorCliente.metadata.drop_all(bind=engine)
    FornecedorCliente.metadata.create_all(bind=engine)

    novo_fornecedor_cliente = {
        "nome": "Katsue Hernandes Haiabe"
    }

    novo_fornecedor_cliente_copy = novo_fornecedor_cliente.copy()
    novo_fornecedor_cliente_copy["id"] = 1

    response = client.post("/fornedor-cliente", json=novo_fornecedor_cliente)
    assert response.status_code == 201
    assert response.json() == novo_fornecedor_cliente_copy

def test_atualizar_fornecedor_cliente():

    FornecedorCliente.metadata.drop_all(bind=engine)
    FornecedorCliente.metadata.create_all(bind=engine)

    response = client.post("/fornedor-cliente", json={
            "nome": "Katsue Haiabe"
        })
    
    id_fornecedor_cliente = response.json()["id"]
    
    response_put = client.put(f"/fornedor-cliente/{id_fornecedor_cliente}", json={
            "nome": "Katsue Hernandes Haiabe"
        })

    assert response_put.status_code == 200
    #assert response_put.json()['valor'] == 3000

def test_remover_fornecedor_cliente():

    FornecedorCliente.metadata.drop_all(bind=engine)
    FornecedorCliente.metadata.create_all(bind=engine)

    response = client.post("/fornedor-cliente", json={
            "nome": "Katsue Haiabe"
        })
    
    id_fornecedor_cliente = response.json()["id"]
    
    response_delete = client.delete(f"/fornedor-cliente/{id_fornecedor_cliente}")

    assert response_delete.status_code == 204
    
def test_retornar_erro_nao_econtrado():
    
    FornecedorCliente.metadata.drop_all(bind=engine)
    FornecedorCliente.metadata.create_all(bind=engine)
    
    response_get = client.get(f"/fornedor-cliente/100")

    assert response_get.status_code == 404
