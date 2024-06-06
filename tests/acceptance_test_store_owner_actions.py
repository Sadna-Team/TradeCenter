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
    
app = create_app()

client = app.test_client()
client2 = app.test_client()
client3 = app.test_client()
client4 = app.test_client()

owner_token = ""
owner2_token = ""
guest1_token = ""
guest2_token = ""
guest3_token = ""
guest4_token = ""

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
guest1_token = start_guest1()

# create a user(owner)
add_user(guest1_token)

# start guest2 for client2
guest2_token = start_guest2()

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
headers = {'Authorization': 'Bearer ' + owner_token}
response = client.post('store/add_store', headers=headers, json=data)

# login as owner2
data = {'username': 'owner2', 'password': 'test'}
headers = {'Authorization': 'Bearer ' + guest1_token}
response = client.post('auth/login', headers=headers, json=data)
owner2_token = response.get_json()['token']

# appoint owner2 to owner
data = {'username': 'owner2'}
headers = {'Authorization': 'Bearer ' + owner_token}
response = client.post('store/add_store_owner', headers=headers, json=data)

# accept promotion
data = {'promotion_id': 3, 'accept': True}
headers = {'Authorization': 'Bearer ' + owner2_token}
response = client.post('store/accept_promotion', headers=headers, json=data)

print("-------------")
print("-------------")
print("-------------")
print("-------------")
print("-------------")
print("-------------")
print("-------------")
print("-------------")
print("-------------")
print("-------------")
print("-------------")
print("-------------")
print("-------------")
print("-------------")
print("-------------")

def test_appoint_store_manager_success():
    # appoint managers
    data = {'store_id': 0, 'username': 'new_manager'}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.post('store/add_store_manager', headers=headers, json=data)
    print(response.get_json())
    assert response.status_code == 200
    # assert response.get_json()['message'] == 'store manager was added successfully'

    data = {'store_id': 0, 'username': 'new_manager2'}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.post('store/add_store_manager', headers=headers, json=data)

    assert response.status_code == 200
    # assert response.get_json()['message'] == 'store manager was added successfully'

def test_appoint_store_manager_invalid_member_credentials():
    data = {'store_id': 0, 'username': 'invalid_user'}
    headers = {'Authorization': 'Bearer ' + owner_token}
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
    data = {'promotion_id': 1, 'accept': True}
    headers = {'Authorization': 'Bearer ' + manager1_token}
    response = client2.post('user/accept_promotion', headers=headers, json=data)

    print(response.get_json())
    assert response.status_code == 200
    # assert response.get_json()['message'] == 'promotion accepted successfully'

def test_appoint_store_manager_already_has_role_in_store():
    data = {'store_id': 0, 'username': 'new_manager'}
    headers = {'Authorization': 'Bearer ' + owner_token}
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
    data = {'manager_id': 1, 'permissions': ['add_manager']}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.post('store/change_permissions', headers=headers, json=data)
    assert response.status_code == 200
    # assert response.get_json()['message'] == 'Permissions changed successfully'

def test_change_store_manager_permissions_invalid_manager_id():
    data = {'manager_id': 999, 'permissions': ['add_manager']}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.post('store/change_permissions', headers=headers, json=data)
    assert response.status_code == 400
    # assert response.get_json()['message'] == 'Manager not found'

def test_change_store_manager_permissions_not_supervisor():
    # try to change permissions
    data = {'manager_id': 2, 'permissions': ['add_manager']}
    headers = {'Authorization': 'Bearer ' + owner2_token}
    response = client2.post('store/change_permissions', headers=headers, json=data)
    assert response.status_code == 400
    # assert response.get_json()['message'] == 'Actor is not a owner/manager of the manager'

def test_view_employees_info_success():
    data = {'store_id': 0} 
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.get('store/view_employees', headers=headers, json=data)
    assert response.status_code == 200
    """
    data = response.get_json()
    assert 'employees' in data
    """

def test_view_employees_info_invalid_store_id():
    data = {'store_id': 30} 
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.get('store/view_employees', headers=headers, json=data)
    assert response.status_code == 400
    clean_data()