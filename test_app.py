import pytest
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# 1. Testa se a rota inicial responde com sucesso
def test_home_status_code(client):
    response = client.get('/')
    assert response.status_code == 200


# 2. Testa se a rota inicial retorna JSON
def test_home_retorna_json(client):
    response = client.get('/')
    assert response.is_json


# 3. Testa se a mensagem existe na resposta da rota inicial
def test_home_contem_mensagem(client):
    response = client.get('/')
    data = response.get_json()
    assert "mensagem" in data


# 4. Testa se a rota /estudantes responde com sucesso
def test_estudantes_status_code(client):
    response = client.get('/estudantes')
    assert response.status_code == 200


# 5. Testa se uma rota inexistente retorna 404
def test_rota_invalida_retorna_404(client):
    response = client.get('/rota-invalida')
    assert response.status_code == 404