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

@pytest.fixture
def register_user(client, guest):
    register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567' }
    data = {
        'register_credentials': register_credentials
    }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    client.post('auth/register', headers=headers, json=data)

@pytest.fixture
def login_user(client, guest, register_user):
    data = {
            'username': 'test',
            'password': 'test'
        }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('user/login', headers=headers, json=data)
    data = response.get_json()
    token = data['token']
    return token



def test_home_page(client):
    response = client.get('/auth/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data


def test_register(client, guest):
    register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567' }
    data = {
        'register_credentials': register_credentials
    }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/register', headers=headers, json=data)
    assert response.status_code == 201
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'User registered successfully - great success'

def test_duplicate_register(client, guest):
    register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567' }
    data = {
        'register_credentials': register_credentials
    }
    headers = {
        'Authorization': 'Bearer ' + guest
    }

    response = client.post('auth/register', headers=headers, json=data)
    assert response.status_code == 201
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'User registered successfully - great success'

    response = client.post('auth/register', headers=headers, json=data)
    assert response.status_code == 400

def test_login(client, guest, register_user):
    data = {
            'username': 'test',
            'password': 'test'
        }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('user/login', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert 'message' in data
    assert data['message'] == 'OK'

def test_login_fail(client, guest):
    data = {
            'username': 'test',
            'password': 'test'
        }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('user/login', headers=headers, json=data)
    assert response.status_code == 400