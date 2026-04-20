import pytest
from main import app
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200