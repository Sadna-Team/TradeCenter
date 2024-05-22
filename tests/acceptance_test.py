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
    response = client.post('auth/register', headers=headers, json=data)
    return guest

@pytest.fixture
def login_user(client, register_user):
    data = {
            'username': 'test',
            'password': 'test'
        }
    headers = {
        'Authorization': 'Bearer ' + register_user
    }
    response = client.post('auth/login', headers=headers, json=data)
    data = response.get_json()
    token = data['token']
    return token

@pytest.fixture
def login_system_manager(client, guest):
    data = {
            'username': 'admin',
            'password': 'admin'
    }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/login', headers=headers, json=data)
    data = response.get_json()
    token = data['token']
    return token


def test_home_page(client, clean):
    response = client.get('/auth/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data


def test_register(client, guest, clean):
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

def test_register_fail_duplicate_user(client, register_user, clean):
    
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
        'Authorization': 'Bearer ' + register_user
    }

    response = client.post('auth/register', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Username already exists'

def test_register_fail_missing_data(client, guest, clean):
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

def test_register_fail_missing_token(client, clean):
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


def test_login(client, register_user, clean):
    data = {
            'username': 'test',
            'password': 'test'
        }
    headers = {
        'Authorization': 'Bearer ' + register_user
        }
    response = client.post('auth/login', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert 'message' in data
    assert data['message'] == 'OK'

def test_login_fail_invalid_credentials(client, register_user, clean):
    data = {
            'username': 'test',
            'password': 'wrong_password'
        }
    headers = {
        'Authorization': 'Bearer ' + register_user
    }
    response = client.post('auth/login', headers=headers, json=data)
    assert response.status_code == 400

def test_login_fail_already_logged_in(client, guest, login_user, clean):
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


def test_login_fail_missing_data(client, guest, clean):
    data = {
            'username': 'test',
        }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/login', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Missing username or password'

def test_login_fail_missing_token(client, clean):
    data = {
            'username': 'test',
            'password': 'test'
        }
    response = client.post('auth/login', json=data)
    assert response.status_code == 401

def test_logout(client, login_user, clean):
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('auth/logout', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'User logged out successfully'

def test_logout_fail_missing_token(client, clean):
    response = client.post('auth/logout')
    assert response.status_code == 401

def test_logout_fail_not_logged_in(app, client, guest, clean):
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/logout', headers=headers)
    assert response.status_code == 400

def test_add_payment_service(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
        'config': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Third party payment service added successfully'

def test_add_payment_service_fail_duplicate_key(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
        'config': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'payment method already supported'

def test_add_payment_service_fail_missing_data(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    assert response.status_code == 400

def test_add_payment_service_fail_missing_token(client, clean):
    data = {
        'method_name': 'test',
        'config': {'test': 'test'}
    }
    response = client.post('third_party/payment/add', json=data)
    assert response.status_code == 401

def test_add_payment_service_fail_not_system_manager(client, login_user, clean):
    data = {
        'method_name': 'test',
        'config': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is not a system manager'

def test_edit_payment_service(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
        'editing_data': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Third party payment service edited successfully'

def test_edit_payment_service_fail_missing_data(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 400

def test_edit_payment_service_fail_no_such_key(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
        'editing_data': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'payment method not supported'

def test_edit_payment_service_fail_missing_token(client, clean):
    data = {
        'method_name': 'bogo',
        'editing_data': {'test': 'test'}
    }
    response = client.put('third_party/payment/edit', json=data)
    assert response.status_code == 401

def test_edit_payment_service_fail_not_system_manager(client, login_user, clean):
    data = {
        'method_name': 'bogo',
        'editing_data': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is not a system manager'

def test_delete_payment_service(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Third party payment service deleted successfully'

def test_delete_payment_service_fail_missing_data(client, login_system_manager, clean):
    data = {}
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 400

def test_delete_payment_service_fail_no_such_key(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'payment method not supported'

def test_delete_payment_service_fail_missing_token(client, clean):
    data = {
        'method_name': 'bogo',
    }
    response = client.delete('third_party/payment/delete', json=data)
    assert response.status_code == 401

def test_delete_payment_service_fail_not_system_manager(client, login_user, clean):
    data = {
        'method_name': 'bogo',
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is not a system manager'

def test_add_supply_service(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
        'config': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Third party delivery service added successfully'

def test_add_supply_service_fail_duplicate_key(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
        'config': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'supply method already supported'

def test_add_supply_service_fail_missing_data(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 400

def test_add_supply_service_fail_missing_token(client, clean):
    data = {
        'method_name': 'test',
        'config': {'test': 'test'}
    }
    response = client.post('third_party/delivery/add', json=data)
    assert response.status_code == 401

def test_add_supply_service_fail_not_system_manager(client, login_user, clean):
    data = {
        'method_name': 'test',
        'config': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is not a system manager'

def test_edit_supply_service(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
        'editing_data': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Third party delivery service edited successfully'

def test_edit_supply_service_fail_missing_data(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 400

def test_edit_supply_service_fail_no_such_key(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
        'editing_data': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'supply method not supported'

def test_edit_supply_service_fail_missing_token(client, clean):
    data = {
        'method_name': 'bogo',
        'editing_data': {'test': 'test'}
    }
    response = client.put('third_party/delivery/edit', json=data)
    assert response.status_code == 401

def test_edit_supply_service_fail_not_system_manager(client, login_user, clean):
    data = {
        'method_name': 'bogo',
        'editing_data': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is not a system manager'

def test_delete_supply_service(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Third party delivery service deleted successfully'

def test_delete_supply_service_fail_missing_data(client, login_system_manager, clean):
    data = {}
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 400

def test_delete_supply_service_fail_no_such_key(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'supply method not supported'

def test_delete_supply_service_fail_missing_token(client, clean):
    data = {
        'method_name': 'bogo',
    }
    response = client.delete('third_party/delivery/delete', json=data)
    assert response.status_code == 401

def test_delete_supply_service_fail_not_system_manager(client, login_user, clean):
    data = {
        'method_name': 'bogo',
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is not a system manager'


if __name__ == '__main__':
    pytest.main(['-s', 'tests/test_acceptance.py'])
