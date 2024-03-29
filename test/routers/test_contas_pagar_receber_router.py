from main import app

# from unittest.mock import Mock
# from faker import Faker

from starlette.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.domain.conection import get_db_connection
from src.models.contas_pg_models import ContasPagarReceber

# @pytest.fixture
# def mock_contas_pagar_receber() -> ContasPagarReceber:

#     mocked_constas_pg = Mock(spec_set=ContasPagarReceber)
#     mocked_constas_pg.id.return_value = fake.random_int(min=1, max=30)
#     mocked_constas_pg.descricao.return_value = fake.descricao()
#     mocked_constas_pg.valor.return_value = fake.random_numeric()
#     mocked_constas_pg.tipo.return_value = fake.tipo()

#     return mocked_constas_pg


# URL do banco de dados
SQLALCHEMY_DATABASE_URL = "sqlite:///.test.db"

# Mecanismo que irá conectar ao DataBase  através da URL informada
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

# Variável responsável por criar sessões de banco de dados
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Session:  # type: ignore
    # Instancia da sessão database
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Passo a funcao original como parametro para a funcao de teste
app.dependency_overrides[get_db_connection] = override_get_db

# fake = Faker()
client = TestClient(app)


def test_listar_contas_pagar_receber():
    ContasPagarReceber.metadata.drop_all(bind=engine)
    ContasPagarReceber.metadata.create_all(bind=engine)

    client.post("/contas-a-pagar-e-receber", json={
        'descricao': 'Aluguel',
        'valor': 1000.5,
        'tipo': 'PAGAR',
        'data_baixa': None,
        'valor_baixa': None,
        'status': False,
        'fornecedor': None
    })

    response = client.get('/contas-a-pagar-e-receber')
    assert response.status_code == 200
    assert response.json() == [{
        'id': 1,
        'descricao': 'Aluguel',
        'valor': 1000.5,
        'tipo': 'PAGAR',
        'data_baixa': None,
        'valor_baixa': None,
        'status': False,
        'fornecedor': None
    }]


def test_listar_contas_pagar_receber_by_id():
    response = client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Investimento",
        "valor": 1500,
        "tipo": "RECEBER",
        "fornecedor": None
    })
    id_conta_a_pagar_e_receber = response.json()["id"]

    response_get = client.get(f"/contas-a-pagar-e-receber/{id_conta_a_pagar_e_receber}")

    assert response_get.status_code == 200
    assert response_get.json()['descricao'] == "Investimento"
    assert response_get.json()['valor'] == 1500
    assert response_get.json()['tipo'] == "RECEBER"
    assert response_get.json()['fornecedor'] is None


def test_criar_conta_pagar_receber():
    ContasPagarReceber.metadata.drop_all(bind=engine)
    ContasPagarReceber.metadata.create_all(bind=engine)

    nova_conta = {
        'descricao': 'Aluguel',
        'valor': 1000.5,
        'tipo': 'PAGAR',
        'data_baixa': None,
        'valor_baixa': None,
        'status': False,
        'fornecedor': None
    }

    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 1
    # nova_conta_copy["valor"] = str(nova_conta_copy['valor'])

    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
    assert response.status_code == 201
    assert response.json() == nova_conta_copy


def test_atualizar_conta_pagar_receber():
    ContasPagarReceber.metadata.drop_all(bind=engine)
    ContasPagarReceber.metadata.create_all(bind=engine)

    response = client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Investimento",
        "valor": 1500,
        "tipo": "RECEBER"
    })

    id_conta_a_pagar_e_receber = response.json()["id"]

    response_put = client.put(f"/contas-a-pagar-e-receber/{id_conta_a_pagar_e_receber}", json={
        "descricao": "Investimento",
        "valor": 3000,
        "tipo": "RECEBER"
    })

    assert response_put.status_code == 200
    assert response_put.json()['valor'] == 3000


def test_remover_conta_pagar_receber():
    ContasPagarReceber.metadata.drop_all(bind=engine)
    ContasPagarReceber.metadata.create_all(bind=engine)

    response = client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Investimento",
        "valor": 1500,
        "tipo": "RECEBER"
    })

    id_conta_a_pagar_e_receber = response.json()["id"]

    response_delete = client.delete(f"/contas-a-pagar-e-receber/{id_conta_a_pagar_e_receber}")

    assert response_delete.status_code == 204


def test_retornar_erro_nao_encontrado():
    ContasPagarReceber.metadata.drop_all(bind=engine)
    ContasPagarReceber.metadata.create_all(bind=engine)

    response_get = client.get(f"/contas-a-pagar-e-receber/100")

    assert response_get.status_code == 404


# def test_criar_conta_pagar_receber_com_fornecedor():

#     ContasPagarReceber.metadata.drop_all(bind=engine)
#     ContasPagarReceber.metadata.create_all(bind=engine)

#     novo_fornecedor_cliente = {
#         "nome": "CENTAURO"
#     }

#     client.post("/fornedor-cliente", json=novo_fornecedor_cliente)

#     nova_conta = {
#         "descricao": "Camisa do SP",
#         "valor": 349.99,
#         "tipo": "PAGAR",
#         "fornecedor_id": 1
#     }

#     nova_conta_copy = nova_conta.copy()
#     nova_conta_copy["id"] = 1

#     #nova_conta_copy["valor"] = str(nova_conta_copy['valor'])

#     response = client.post("/contas-a-pagar-e-receber", json=nova_conta)
#     assert response.status_code == 201
#     assert response.json() == nova_conta_copy

def test_baixar_conta_pagar_receber():
    ContasPagarReceber.metadata.drop_all(bind=engine)
    ContasPagarReceber.metadata.create_all(bind=engine)

    client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Aluguel",
        "valor": 1000.5,
        "tipo": "PAGAR",
    })

    response = client.post(f"/contas-a-pagar-e-receber/1/baixar")

    assert response.status_code == 200
    assert response.json()["status"] is True
    assert response.json()["valor_baixa"] == 1000.5

def test_baixar_conta_pagar_receber_modificada():
    ContasPagarReceber.metadata.drop_all(bind=engine)
    ContasPagarReceber.metadata.create_all(bind=engine)

    client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Aluguel",
        "valor": 1000.5,
        "tipo": "PAGAR",
    })

    client.post(f"/contas-a-pagar-e-receber/1/baixar")

    client.put(f"/contas-a-pagar-e-receber/1", json={
        "descricao": "Aluguel",
        "valor": 999,
        "tipo": "PAGAR",
    })

    response = client.post(f"/contas-a-pagar-e-receber/1/baixar")

    assert response.status_code == 200
    assert response.json()["status"] is True
    assert response.json()["valor"] == 999
    assert response.json()["valor_baixa"] == 999

