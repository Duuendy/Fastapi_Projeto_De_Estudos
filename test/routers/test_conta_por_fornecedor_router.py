from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from main import app
from src.domain.conection import get_db_connection
from src.models.contas_pg_models import FornecedorCliente

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

client = TestClient(app)


def test_listar_contas_do_fornecedor_cliente_by_id():
    FornecedorCliente.metadata.drop_all(bind=engine)
    FornecedorCliente.metadata.create_all(bind=engine)

    client.post("/fornecedor-cliente", json={"nome": "Alura"})
    client.post("/fornecedor-cliente", json={"nome": "Escola de Picobol"})

    client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Curso de Python",
        "valor": 1500,
        "tipo": "PAGAR",
        "fornecedor_id": 1
    })

    client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Aula de Saque",
        "valor": 150,
        "tipo": "PAGAR",
        "fornecedor_id": 2
    })

    client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Aula de Recepcao",
        "valor": 100,
        "tipo": "PAGAR",
        "fornecedor_id": 2
    })

    response_fornecedor1 = client.get("/fornecedor-cliente/1/contas-a-pagar-e-receber")
    assert response_fornecedor1.status_code == 200
    assert len(response_fornecedor1.json()) == 1

    response_fornecedor2 = client.get("/fornecedor-cliente/2/contas-a-pagar-e-receber")
    assert response_fornecedor2.status_code == 200
    assert len(response_fornecedor2.json()) == 2

def test_retornar_lista_vazia_de_contas_do_fornecedor_cliente_by_id():
    FornecedorCliente.metadata.drop_all(bind=engine)
    FornecedorCliente.metadata.create_all(bind=engine)

    client.post("/fornecedor-cliente", json={"nome": "Alura"})

    response_fornecedor = client.get("/fornecedor-cliente/1/contas-a-pagar-e-receber")
    assert response_fornecedor.status_code == 200
    assert len(response_fornecedor.json()) == 0

