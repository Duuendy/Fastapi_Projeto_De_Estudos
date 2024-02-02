from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_contas_pagar_receber():
    response = client.get('/contas-a-pagar-e-receber')

    assert response.status_code == 200

    assert response.json() == [
        {'id': 1, 'descricao': 'Aluguel', 'valor': '1000.5', 'tipo': 'PAGAR'}, 
        {'id': 2, 'descricao': 'Salario', 'valor': '5555.55', 'tipo': 'RECEBER'}
    ]

def test_deve_criar_conta_pagar_receber():
    
    nova_conta = {
        "descricao": "Faculdade",
        "valor": 150.00,
        "tipo": "PAGAR"
    }

    response = client.post('/contas-a-pagar-e-receber', json=nova_conta)

    assert response.status_code == 201