import pytest
from backend import create_app

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def guest(client):
    response = client.get('/auth/')
    data = response.get_json()
    token = data['token']
    return token



def test_home_page(client):
    response = client.get('/auth/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data


def test_register(client, guest):
    response = client.post('/auth/register', headers={
            'Authorization': f'Bearer {guest}'
        }, json={
            'register_credentials': {
                'username': 'test_user',
                'password': 'password'
            }
        })
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == 'User registered successfully - great success'
