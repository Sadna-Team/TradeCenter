#write acceptance tests for store owner actions

import pytest
from backend import create_app, clean_data

register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567' }
    
@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def clean():
    yield
    clean_data()

@pytest.fixture
def client(app):
    return app.test_client()

def client2(app):
    return app.test_client()

@pytest.fixture
def guest(client):
    response = client.get('/auth/')
    data = response.get_json()
    token = data['token']
    return token

@pytest.fixture
def get_token(client):
    response = client.get('/auth/')
    return response.get_json()['token']

@pytest.fixture
def add_user(client):
    data = {
        'register_credentials': register_credentials
    }
    headers = {'Authorization': 'Bearer ' + get_token(client)}
    response = client.post('/auth/register', headers=headers, json=data)
    return response.get_json()['token'] 

@pytest.fixture
def test_appoint_store_manager_success(client, clean):
    # create a user(owner)
    user_token = add_user(client)
    
    # create a user(manager1)
    manager_creds = register_credentials.copy()
    manager_creds['username'] = 'new_manager'
    data = {
        'register_credentials': manager_creds
    }
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.post('/auth/register', headers=headers, json=data)

    # create a user(manager2)
    manager_creds = register_credentials.copy()
    manager_creds['username'] = 'new_manager2'
    data = {
        'register_credentials': manager_creds
    }
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.post('/auth/register', headers=headers, json=data)

    # login as owner
    data = {'username': 'test', 'password': 'test'}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.post('/auth/login', headers=headers, json=data)
    user_token = response.get_json()['token']

    # create a store
    data = {'store_name': 'test_store', 'location_id': 1}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.post('/store/add_store', headers=headers, json=data)

    # appoint managers
    data = {'username': 'new_manager'}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.post('/store/appoint_manager', headers=headers, json=data)
    
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Manager appointed successfully'

    data = {'username': 'new_manager2'}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.post('/store/appoint_manager', headers=headers, json=data)

    assert response.status_code == 200
    assert response.get_json()['message'] == 'Manager appointed successfully'

@pytest.fixture
def test_appoint_store_manager_invalid_member_credentials(client, clean):
    user_token = get_token(client)

    data = {'username': 'invalid_user'}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.post('/store/appoint_manager', headers=headers, json=data)
    assert response.status_code == 404
    assert response.get_json()['message'] == 'User not found'

@pytest.fixture
def test_appoint_store_manager_already_has_role_in_store(client, clean):
    user_token = get_token(client)

    data = {'username': 'new_manager'}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.post('/store/appoint_manager', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User already has a role in the store'

@pytest.fixture
def accepting_manager_promotion_success(client2, clean):
    user_token = get_token(client2)

    # login as user(manager)
    data = {'username': 'new_manager', 'password': 'test'}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('/auth/login', headers=headers, json=data)
    user_token = response.get_json()['token']

    # accept promotion
    data = {'promotion_id': 1, 'accept': True}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.post('/store/accept_promotion', headers=headers, json=data)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'promotion accepted successfully'

    # logout
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('/auth/logout', headers=headers)

@pytest.fixture
def not_accepting_manager_promotion(client2, clean):   
    user_token = get_token(client2)

    # login as user(manager)
    data = {'username': 'new_manager2', 'password': 'test'}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('/auth/login', headers=headers, json=data)
    user_token = response.get_json()['token']

    data = {'promotion_id': 2, 'accept': False}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.post('/store/accept_promotion', headers=headers, json=data)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'promotion declined successfully'

    # logout
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('/auth/logout', headers=headers)

@pytest.fixture
def test_change_store_manager_permissions_success(client, clean):
    user_token = get_token(client)

    data = {'manager_id': 1, 'permissions': ['add_manager']}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.post('/store/change_permissions', headers=headers, json=data)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Permissions changed successfully'

@pytest.fixture
def test_change_store_manager_permissions_invalid_manager_id(client, clean):
    user_token = get_token(client)

    data = {'manager_id': 999, 'permissions': ['can_edit_products']}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.post('/store/change_permissions', headers=headers, json=data)
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Manager not found'

@pytest.fixture
def test_change_store_manager_permissions_not_supervisor(client, client2, clean):
    user2_token = get_token(client2)

    # appoint another owner
    owner2_creds = register_credentials.copy()
    owner2_creds['username'] = 'owner2'
    data = {
        'register_credentials': register_credentials
    }
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('/auth/register', headers=headers, json=data)
    user2_token = response.get_json()['token']

    # login as owner2
    data = {'username': 'owner2', 'password': 'test'}
    headers = {'Authorization': 'Bearer ' + user2_token}
    response = client2.post('/auth/login', headers=headers, json=data)
    user2_token = response.get_json()['token']

    # appoint user2 to owner
    user_token = get_token(client)
    data = {'username': 'owner2'}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.post('/store/appoint_owner', headers=headers, json=data)

    # accept promotion
    data = {'promotion_id': 3, 'accept': True}
    headers = {'Authorization': 'Bearer ' + user2_token}
    response = client2.post('/store/accept_promotion', headers=headers, json=data)

    # try to change permissions
    data = {'manager_id': 2, 'permissions': ['add_manager']}
    headers = {'Authorization': 'Bearer ' + user2_token}
    response = client2.post('/store/change_permissions', headers=headers, json=data)
    assert response.status_code == 401
    assert response.get_json()['message'] == 'Actor is not a owner/manager of the manager'

    # logout
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('/auth/logout', headers=headers)


@pytest.fixture
def test_view_employees_info_success(client, clean):
    user_token = get_token(client)

    data = {'store_id': 1} 
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.get('/store/view_employees', headers=headers, json=data)
    assert response.status_code == 200
    """
    data = response.get_json()
    assert 'employees' in data
    """

@pytest.fixture
def test_view_employees_info_invalid_store_id(client, clean):
    user_token = get_token(client)

    data = {'store_id': 30} 
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client.get('/store/view_employees', headers=headers, json=data)
    assert response.status_code == 400