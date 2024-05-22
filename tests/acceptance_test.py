import pytest
from backend import create_app, clean_data

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def clean():
    yield
    clean_data()

@pytest.fixture
def reset_app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def guest(app, client):
    response = client.get('/auth/')
    data = response.get_json()
    token = data['token']
    return token

@pytest.fixture
def register_user(app, client, guest):
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

@pytest.fixture
def login_user(app, client, guest, register_user):
    data = {
            'username': 'test',
            'password': 'test'
        }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/login', headers=headers, json=data)
    data = response.get_json()
    token = data['token']
    return token



def test_home_page(app, client, clean):
    response = client.get('/auth/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data


def test_register(app, client, guest, clean):
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

def test_register_fail_duplicate_user(app, client, guest, register_user, clean):
    
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
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Username already exists'

def test_register_fail_missing_data(app, client, guest, clean):
    register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,}
    data = {
        'register_credentials': register_credentials
    }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/register', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Some credentials are missing'

def test_register_fail_missing_token(app, client, clean):
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
    response = client.post('auth/register', json=data)
    assert response.status_code == 401


def test_login(app, client, guest, register_user, clean):
    data = {
            'username': 'test',
            'password': 'test'
        }
    headers = {
        'Authorization': 'Bearer ' + guest
        }
    response = client.post('auth/login', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert 'message' in data
    assert data['message'] == 'OK'

def test_login_fail_invalid_credentials(app, client, guest, register_user, clean):
    data = {
            'username': 'test',
            'password': 'wrong_password'
        }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/login', headers=headers, json=data)
    assert response.status_code == 400

def test_login_fail_already_logged_in(app, client, guest, register_user, login_user, clean):
    response = client.get('/auth/')
    data = response.get_json()
    guest = data['token']
    
    data = {
            'username': 'test',
            'password': 'test'
        }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/login', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is already logged in'


def test_login_fail_missing_data(app, client, guest, clean):
    data = {
            'username': 'test',
        }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/login', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Missing username or password'

def test_login_fail_missing_token(app, client, clean):
    data = {
            'username': 'test',
            'password': 'test'
        }
    response = client.post('auth/login', json=data)
    assert response.status_code == 401

def test_logout(app, client, register_user, login_user, clean):
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('auth/logout', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'User logged out successfully'

def test_logout_fail_missing_token(app, client, clean):
    response = client.post('auth/logout')
    assert response.status_code == 401

def test_logout_fail_not_logged_in(app, client, guest, clean):
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/logout', headers=headers)
    assert response.status_code == 400

if __name__ == '__main__':
    pytest.main(['-s', 'tests/test_acceptance.py'])
