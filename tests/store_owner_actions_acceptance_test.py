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
    print(response.get_json())
    print("help")
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

policy_data = {'store_id': 0, 'policy_name': 'no_alcohol_past_time'}

def test_add_purchase_policy_success():
    data = policy_data.copy()
    headers = owner_headers
    response = client.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200

def test_add_purchase_policy_invalid_store_id():
    data = policy_data.copy()
    data['store_id'] = 30
    headers = owner_headers
    response = client.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400

def test_add_purchase_policy_already_exists():
    data = policy_data.copy()
    headers = owner_headers
    response = client.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400

def test_add_purchase_policy_invalid_policy_name():
    data = policy_data.copy()
    data['policy_name'] = 'invalid_policy'
    headers = owner_headers
    response = client.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400

def test_remove_purchase_policy_success():
    data = policy_data.copy()
    headers = owner_headers
    response = client.post('store/remove_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200

def test_remove_purchase_policy_invalid_store_id():
    data = policy_data.copy()
    data['store_id'] = 30
    headers = owner_headers
    response = client.post('store/remove_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400

def test_remove_purchase_policy_policy_missing():
    data = policy_data.copy()
    headers = owner_headers
    response = client.post('store/remove_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400

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

# --------------------------------------------------------------------------------

register_credentials1= { 
        'username': 'testing',
        'email': 'testing@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1238567' }

default_payment_method = {'payment method': 'bogo'}

default_supply_method = "bogo"

default_address = {'address_id': 0, 
                            'address': 'randomstreet 34th', 
                            'city': 'arkham', 
                            'country': 'Wakanda', 
                            'state': 'Utopia', 
                            'postal_code': '12345'}



@pytest.fixture
def app1():
    app1 = create_app()
    return app1

@pytest.fixture
def client11(app1):
    return app1.test_client()

@pytest.fixture
def new_token(client11):
    response = client11.get('/auth/')
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def admin_token(client11, new_token):
    data = {
        'username': 'admin',
        'password': 'admin'
    }
    headers = { 'Authorization': 'Bearer ' + new_token }
    response = client11.post('auth/login', headers=headers, json=data)
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def clean11():
    yield
    clean_data()
    
@pytest.fixture
def client12(app1):
    return app1.test_client()

@pytest.fixture
def client22(app1):
    return app1.test_client()

@pytest.fixture
def client33(app1):
    return app1.test_client()

@pytest.fixture
def token11(client12):
    response = client12.get('/auth/')
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def token22(client22):
    response = client22.get('/auth/')
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def guest_token10(client33):
    response = client33.get('/auth/')
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def owner_token11(client12, token11):
    headers = { 'Authorization': 'Bearer ' + token11}
    manager_credentials = register_credentials1.copy()
    manager_credentials['username'] = 'store_owner_new'
    data = {"register_credentials": manager_credentials}
    response = client12.post('auth/register', headers=headers, json=data)

    data = { "username": "store_owner_new", "password": "test" }
    response = client12.post('auth/login', json=data, headers=headers)
    data = json.loads(response.data)
    return data['token']




@pytest.fixture
def user_token(client22, token22):
    headers = { 'Authorization': 'Bearer ' + token22 }
    data = {"register_credentials": register_credentials1}
    response = client22.post('auth/register', headers=headers, json=data)
    data = { "username": "testing", "password": "test" }
    response = client22.post('auth/login', json=data, headers=headers)
    data = json.loads(response.data)
    return data['token']




@pytest.fixture
def init_store(client12):
    data = {'store_name': 'test_store', 'location_id': 1}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client12.post('store/add_store', headers=headers, json=data)

    data = {"store_id": 1, 
            "product_name": "test_product", 
            "description": "test_description",
            "price": 10.0,
            "weight": 1.0,
            "tags": ["tag1", "tag2"],
            "amount": 10}
    
    response = client12.post('store/add_product', headers=headers, json=data)

    data = {"store_id": 1, "policy_name": "no_funny_name"}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)

    data = {"store_id": 1, 
        "product_name": "funny", 
        "description": "test_description",
        "price": 10.0,
        "weight": 1.0,
        "tags": ["tag1", "tag2"],
        "amount": 10}

    response = client12.post('store/add_product', headers=headers, json=data)
    
    

@pytest.fixture
def init_store2(client12):
    data = {'store_name': 'test_store', 'location_id': 1}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client12.post('store/add_store', headers=headers, json=data)

    data = {"store_id": 2, 
            "product_name": "test_product", 
            "description": "test_description",
            "price": 10.0,
            "weight": 1.0,
            "tags": ["tag1", "tag2"],
            "amount": 10}
    
    response = client12.post('store/add_product', headers=headers, json=data)

#test 2.6.4.a (in a store)
def test_getting_info_about_purchase_history_of_a_store(client12, client22, client33, user_token,guest_token10, init_store, clean11):
    #user made purchase
    data = {"store_id": 1, "product_id": 0, "quantity": 3}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client22.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200
        
    data = {"payment_details": default_payment_method, 
            "supply_method": default_supply_method, 
            "address": default_address}
    response = client22.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 200

    #getting the purchase history:
    data = {"store_id": 1}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client12.get('market/store_purchase_history', headers=headers, json=data)
    assert response.status_code == 200
    
    
    # WRONG CREDENTIALS:
    data = {"store_id": 1}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.get('market/store_purchase_history', headers=headers, json=data)
    assert response.status_code == 400


    

