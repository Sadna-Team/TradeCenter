#write acceptance tests for store owner actions
from datetime import datetime
import pytest
from backend import create_app, clean_data
import json
from backend import socketio_manager


register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567' }
    
app = create_app()

client = app.test_client()
client2 = app.test_client()
client3 = app.test_client()
client4 = app.test_client()
client5 = app.test_client()

owner_token = ""
global owner2_token
owner2_token = ""
guest1_token = ""
guest2_token = ""
guest3_token = ""
guest4_token = ""
guest5_token = ""

def clean():
    yield
    clean_data()

def start_guest1():
    response = client.get('auth/')
    data = response.get_json()
    token = data['token']
    return token

def start_guest2():
    response = client2.get('auth/')
    data = response.get_json()
    token = data['token']
    return token

def start_guest3():
    response = client3.get('auth/')
    data = response.get_json()
    token = data['token']
    return token

def add_user(token):
    data = {
        'register_credentials': register_credentials
    }
    headers = {'Authorization': 'Bearer ' + token}
    response = client.post('auth/register', headers=headers, json=data)

"""@pytest.fixture
def setup():
"""
# start guest1 for client
guest1_token = start_guest1() # id = 1

# create a user(owner)
add_user(guest1_token) # id = 1

# start guest2 for client2
guest2_token = start_guest2() # id = 3

# create a user(manager1)
manager_creds = register_credentials.copy()
manager_creds['username'] = 'new_manager'
data = {
'register_credentials': manager_creds
}
headers = {'Authorization': 'Bearer ' + guest2_token}
response = client2.post('auth/register', headers=headers, json=data)

# start guest3 for client3
guest3_token = start_guest3()

# create a user(manager2)
manager_creds = register_credentials.copy()
manager_creds['username'] = 'new_manager2'
data = {
'register_credentials': manager_creds
}
headers = {'Authorization': 'Bearer ' + guest3_token}
response = client3.post('auth/register', headers=headers, json=data)

# start guest4 for client4
guest4_token = start_guest1()

# create a user(owner2)
owner2_creds = register_credentials.copy()
owner2_creds['username'] = 'owner2'
data = {
'register_credentials': owner2_creds
}
headers = {'Authorization': 'Bearer ' + guest4_token}
response = client.post('auth/register', headers=headers, json=data)

# login as owner
data = {'username': 'test', 'password': 'test'}
headers = {'Authorization': 'Bearer ' + guest1_token}
response = client.post('auth/login', headers=headers, json=data)
owner_token = response.get_json()['token']

# create a store
data = {'store_name': 'test_store', 'location_id': 1}
owner_headers = {'Authorization': 'Bearer ' + owner_token}
response = client.post('store/add_store', headers=headers, json=data)

# login as owner2
data = {'username': 'owner2', 'password': 'test'}
headers = {'Authorization': 'Bearer ' + guest1_token}
response = client.post('auth/login', headers=headers, json=data)
owner2_token = response.get_json()['token']

# start guest5 for client
guest5_token = start_guest1()

# create a user(owner3)
owner3_creds = register_credentials.copy()
owner3_creds['username'] = 'owner3'
data = {
'register_credentials': owner3_creds
}
headers = {'Authorization': 'Bearer ' + guest5_token}
response = client.post('auth/register', headers=headers, json=data)

# login as owner3
data = {'username': 'owner3', 'password': 'test'}
headers = {'Authorization': 'Bearer ' + guest4_token}
response = client.post('auth/login', headers=headers, json=data)
owner3_token = response.get_json()['token']

# connect users to sockets
user1_socket = socketio_manager.test_client(app, flask_test_client=client, headers={'Authorization': 'Bearer ' + owner_token})
# send token to socket

user1_socket.emit('join')


def test_appoint_store_manager_success():
    # appoint managers
    data = {'store_id': 0, 'username': 'new_manager'}
    headers = owner_headers
    response = client.post('store/add_store_manager', headers=headers, json=data)
    assert response.status_code == 200
    # assert response.get_json()['message'] == 'store manager was added successfully'

    data = {'store_id': 0, 'username': 'new_manager2'}
    headers = owner_headers
    response = client.post('store/add_store_manager', headers=headers, json=data)

    assert response.status_code == 200
    # assert response.get_json()['message'] == 'store manager was added successfully'

def test_appoint_store_manager_invalid_member_credentials():
    data = {'store_id': 0, 'username': 'invalid_user'}
    headers = owner_headers
    response = client.post('store/add_store_manager', headers=headers, json=data)
    assert response.status_code == 400
    # assert response.get_json()['message'] == 'User not found'

def test_accepting_manager_promotion_success():
    # login as user(manager1)
    data = {'username': 'new_manager', 'password': 'test'}
    headers = {'Authorization': 'Bearer ' + guest2_token}
    response = client2.post('auth/login', headers=headers, json=data)
    manager1_token = response.get_json()['token']

    # accept promotion
    data = {'promotion_id': 0, 'accept': True}
    headers = {'Authorization': 'Bearer ' + manager1_token}
    response = client2.post('user/accept_promotion', headers=headers, json=data)
    assert response.status_code == 200
    # assert response.get_json()['message'] == 'promotion accepted successfully'

def test_appoint_store_manager_already_has_role_in_store():
    data = {'store_id': 0, 'username': 'new_manager'}
    headers = owner_headers
    response = client.post('store/add_store_manager', headers=headers, json=data)
    assert response.status_code == 400
    # assert response.get_json()['message'] == 'User already has a role in the store'

def test_not_accepting_manager_promotion():   
    # login as user(manager2)
    data = {'username': 'new_manager2', 'password': 'test'}
    headers = {'Authorization': 'Bearer ' + guest3_token}
    response = client3.post('auth/login', headers=headers, json=data)
    manager2_token = response.get_json()['token']

    data = {'promotion_id': 1, 'accept': False}
    headers = {'Authorization': 'Bearer ' + manager2_token}
    response = client.post('user/accept_promotion', headers=headers, json=data)
    assert response.status_code == 200
    # assert response.get_json()['message'] == 'promotion declined successfully'

def test_change_store_manager_permissions_success():
    data = {'store_id': 0, 'manager_id': 2, 'permissions': ['add_manager']}
    headers = owner_headers
    response = client.post('store/edit_manager_permissions', headers=headers, json=data)
    print(response.get_json())
    assert response.status_code == 200
    # assert response.get_json()['message'] == 'Permissions changed successfully'

def test_change_store_manager_permissions_invalid_manager_id():
    data = {'store_id': 0, 'manager_id': 999, 'permissions': ['add_manager']}
    headers = owner_headers
    response = client.post('store/edit_manager_permissions', headers=headers, json=data)
    assert response.status_code == 400
    # assert response.get_json()['message'] == 'Manager not found'

def test_change_store_manager_permissions_not_supervisor():
    # try to change permissions
    data = {'store_id': 0, 'manager_id': 2, 'permissions': ['add_manager']}
    headers = {'Authorization': 'Bearer ' + owner2_token}
    response = client2.post('store/edit_manager_permissions', headers=headers, json=data)
    assert response.status_code == 400
    # assert response.get_json()['message'] == 'Actor is not a owner/manager of the manager'

def test_view_employees_info_success():
    data = {'store_id': 0} 
    headers = owner_headers
    response = client.get('store/view_employees_info', headers=headers, json=data)
    assert response.status_code == 200
    """
    data = response.get_json()
    assert 'employees' in data
    """

def test_view_employees_info_invalid_store_id():
    data = {'store_id': 30} 
    headers = owner_headers
    response = client.get('store/view_employees_info', headers=headers, json=data)
    assert response.status_code == 400

def test_appoint_store_owner_success():
    global owner2_token
    # logout owner2
    headers = {'Authorization': 'Bearer ' + owner2_token}
    response = client.post('auth/logout', headers=headers)
    assert response.status_code == 200

    data = {'store_id': 0, 'username': 'owner2'}
    headers = owner_headers
    response = client.post('store/add_store_owner', headers=headers, json=data)
    print(response.get_json())
    assert response.status_code == 200

    # login as owner2
    data = {'username': 'owner2', 'password': 'test'}
    temp_token = client.get('auth/').get_json()['token']
    headers = {'Authorization': 'Bearer ' + temp_token}
    response = client.post('auth/login', headers=headers, json=data)
    owner2_token = response.get_json()['token']
    assert response.status_code == 200

def test_appoint_store_owner_invalid_member_credentials():
    data = {'store_id': 0, 'username': 'invalid_user'}
    headers = owner_headers
    response = client.post('store/add_store_owner', headers=headers, json=data)
    assert response.status_code == 400 

def test_accepting_owner_promotion_success():
    data = {'promotion_id': 2, 'accept': True}
    headers = {'Authorization': 'Bearer ' + owner2_token}
    response = client.post('user/accept_promotion', headers=headers, json=data)
    assert response.status_code == 200

def test_appoint_store_owner_already_a_store_owner():
    data = {'store_id': 0, 'username': 'owner2'}
    headers = owner_headers
    response = client.post('store/add_store_owner', headers=headers, json=data)
    assert response.status_code == 400

def test_not_accepting_owner_promotion():
    # appoint owner3 to owner
    data = {'store_id': 0, 'username': 'owner3'}
    headers = owner_headers
    response = client.post('store/add_store_owner', headers=headers, json=data)
    
    # reject promotion
    data = {'promotion_id': 3, 'accept': False}
    headers = {'Authorization': 'Bearer ' + owner3_token}
    response = client.post('user/accept_promotion', headers=headers, json=data)
    assert response.status_code == 200

store_close_open_data = {'store_id': 0}

def test_close_store_success():
    data = store_close_open_data.copy()
    headers = owner_headers
    response = client.post('store/closing_store', headers=headers, json=data)
    print(response.get_json())
    assert response.status_code == 200

def test_close_store_invalid_store_id():
    data = store_close_open_data.copy()
    data['store_id'] = 30
    headers = owner_headers
    response = client.post('store/closing_store', headers=headers, json=data)
    assert response.status_code == 400

def test_close_store_already_closed():
    data = store_close_open_data.copy()
    headers = owner_headers
    response = client.post('store/closing_store', headers=headers, json=data)
    assert response.status_code == 400

def test_open_store_success():
    data = store_close_open_data.copy()
    headers = owner_headers
    response = client.post('store/opening_store', headers=headers, json=data)
    assert response.status_code == 200

def test_open_store_invalid_store_id():
    data = store_close_open_data.copy()
    data['store_id'] = 30
    headers = owner_headers
    response = client.post('store/opening_store', headers=headers, json=data)
    assert response.status_code == 400

def test_open_store_already_open():
    data = store_close_open_data.copy()
    headers = owner_headers
    response = client.post('store/opening_store', headers=headers, json=data)
    assert response.status_code == 400

product_data = {"store_id": 0,
            "product_name": "test_product",
            "description": "test_description",
            "price": 100.0,
            "weight": 1.0,
            "tags": ["tag1", "tag2"],
            "amount": 10}

def test_add_product_success():
    data = product_data.copy()
    headers = owner_headers
    response = client.post('store/add_product', headers=headers, json=data)
    assert response.status_code == 200

def test_add_product_invalid_store_id():
    data = product_data.copy()
    data['store_id'] = 30
    headers = owner_headers
    response = client.post('store/add_product', headers=headers, json=data)
    assert response.status_code == 400

def test_add_product_invalid_price():
    data = product_data.copy()
    data['price'] = -100.0
    headers = owner_headers
    response = client.post('store/add_product', headers=headers, json=data)
    assert response.status_code == 400

def test_add_product_invalid_weight():
    data = product_data.copy()
    data['weight'] = -1.0
    headers = owner_headers
    response = client.post('store/add_product', headers=headers, json=data)
    assert response.status_code == 400

def test_add_product_invalid_amount():
    data = product_data.copy()
    data['amount'] = -10
    headers = owner_headers
    response = client.post('store/add_product', headers=headers, json=data)
    assert response.status_code == 400

def test_add_product_invalid_tags():
    data = product_data.copy()
    data['tags'] = "tag1"
    headers = owner_headers
    response = client.post('store/add_product', headers=headers, json=data)
    assert response.status_code == 500

remove_product_data = {"store_id": 0, "product_id": 0}

def test_remove_product_success():
    data = remove_product_data.copy()
    headers = owner_headers
    response = client.post('store/remove_product', headers=headers, json=data)
    assert response.status_code == 200

def test_remove_product_invalid_store_id():
    data = remove_product_data.copy()
    headers = owner_headers
    response = client.post('store/remove_product', headers=headers, json=data)
    assert response.status_code == 400

def test_remove_product_invalid_product_id():
    data = remove_product_data.copy()
    headers = owner_headers
    response = client.post('store/remove_product', headers=headers, json=data)
    assert response.status_code == 400