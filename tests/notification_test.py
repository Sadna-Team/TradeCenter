import pytest
from backend import create_app, clean_data
from backend import socketio_manager
import json

register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567' }

default_payment_method = {'payment method': 'bogo'}

default_supply_method = "bogo"

default_address_checkout = {'address_id': 0, 
                            'address': 'randomstreet 34th', 
                            'city': 'arkham', 
                            'country': 'Wakanda', 
                            'state': 'Utopia', 
                            'postal_code': '12345'}


@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def clean(app):
    yield
    clean_data()

@pytest.fixture
def client1(app):
    return app.test_client()

@pytest.fixture
def client2(app):
    return app.test_client()

@pytest.fixture
def owner(client1):
    # register owner
    response = client1.get('auth/')
    data = json.loads(response.data)
    token = data['token']

    headers = {'Authorization': 'Bearer ' + token}
    owner_credentials = register_credentials.copy()
    owner_credentials['username'] = 'owner'
    data = {'register_credentials': owner_credentials}
    response = client1.post('auth/register', headers=headers, json=data)

    # login owner
    response = client1.post('auth/login', headers=headers, json={'username': 'owner', 'password': 'test'})
    data = json.loads(response.data)
    print(data)
    owner_token = data['token']
    return owner_token

@pytest.fixture
def user(client2):
    # register user
    response = client2.get('auth/')
    data = json.loads(response.data)
    token = data['token']

    headers = {'Authorization': 'Bearer ' + token}
    user_credentials = register_credentials.copy()
    user_credentials['username'] = 'user'
    data = {'register_credentials': user_credentials}
    client2.post('auth/register', headers=headers, json=data)
    
    # login user
    response = client2.post('auth/login', headers=headers, json={'username': 'user', 'password': 'test'})
    data = json.loads(response.data)
    user_token = data['token']
    return user_token

@pytest.fixture
def store(client1, owner):
    # create store
    headers = {'Authorization': 'Bearer ' + owner}
    data = {'store_name': 'store', 'location_id': 1}
    client1.post('store/add_store', headers=headers, json=data)

    # add product
    data = {"store_id": 0, 
            "product_name": "test_product", 
            "description": "test_description",
            "price": 10.0,
            "weight": 1.0,
            "tags": ["tag1", "tag2"],
            "amount": 10}
    client1.post('store/add_product', headers=headers, json=data)

@pytest.fixture
def owner_socket(app, client1, owner):
    owner_socket = socketio_manager.test_client(app, flask_test_client=client1, headers={'Authorization': 'Bearer ' + owner})
    owner_socket.emit('join')
    return owner_socket

@pytest.fixture
def user_socket(app, client2, user):
    user_socket = socketio_manager.test_client(app, flask_test_client=client2, headers={'Authorization': 'Bearer ' + user})
    user_socket.emit('join')
    return user_socket

def test_owner_nomination_notification_real_time(client1, owner, store, user_socket, clean):
    # nominate owner
    headers = {'Authorization': 'Bearer ' + owner}
    data = {'store_id': 0, 'username': 'user'}
    client1.post('store/add_store_owner', headers=headers, json=data)

    # check notification
    response = user_socket.get_received()

    assert len(response) == 1
    
    notification = response[0]['args']['message']
    assert notification == 'You have been nominated to be the owner of store 0. nomination id: 0 '

def test_owner_nomination_notification_delay(app, client1, owner, store, client2, user, user_socket, clean):
    # log out user
    user_socket.emit('leave')
    headers = {'Authorization': 'Bearer ' + user}
    client2.post('auth/logout', headers=headers, json={})

    # nominate owner
    headers = {'Authorization': 'Bearer ' + owner}
    data = {'store_id': 0, 'username': 'user'}
    client1.post('store/add_store_owner', headers=headers, json=data)

    # log in user
    guest_token = client2.get('auth/').get_json()['token']
    headers = {'Authorization': 'Bearer ' + guest_token}
    response = client2.post('auth/login', headers=headers, json={'username': 'user', 'password': 'test'})
    new_user_token = response.get_json()['token']
    new_user_socket = socketio_manager.test_client(app, flask_test_client=client2, headers={'Authorization': 'Bearer ' + new_user_token})
    new_user_socket.emit('join')

    # check notification
    notifications = response.get_json()['notification']
    
    assert len(notifications) == 1
    
    notification = notifications[0]['message']
    assert notification == 'You have been nominated to be the owner of store 0. nomination id: 0 '

def test_manager_nomination_notification_real_time(client1, owner, store, user_socket, clean):
    # nominate owner
    headers = {'Authorization': 'Bearer ' + owner}
    data = {'store_id': 0, 'username': 'user'}
    client1.post('store/add_store_owner', headers=headers, json=data)

    # nominate manager
    headers = {'Authorization': 'Bearer ' + owner}
    data = {'store_id': 0, 'username': 'user', 'permissions': 'manager'}
    client1.post('store/add_store_manager', headers=headers, json=data)

    # check notification
    response = user_socket.get_received()

    assert len(response) == 2
    
    notification = response[1]['args']['message']
    assert notification == 'You have been nominated to be the manager of store 0. nomination id: 1 '

def test_manager_nomination_notification_delay(app, client1, owner, store, client2, user, user_socket, clean):
    # log out user
    user_socket.emit('leave')
    headers = {'Authorization': 'Bearer ' + user}
    client2.post('auth/logout', headers=headers, json={})

    # nominate manager
    headers = {'Authorization': 'Bearer ' + owner}
    data = {'store_id': 0, 'username': 'user', 'permissions': 'manager'}
    client1.post('store/add_store_manager', headers=headers, json=data)

    # log in user
    guest_token = client2.get('auth/').get_json()['token']
    headers = {'Authorization': 'Bearer ' + guest_token}
    response = client2.post('auth/login', headers=headers, json={'username': 'user', 'password': 'test'})
    new_user_token = response.get_json()['token']
    new_user_socket = socketio_manager.test_client(app, flask_test_client=client2, headers={'Authorization': 'Bearer ' + new_user_token})
    new_user_socket.emit('join')

    # check notification
    notifications = response.get_json()['notification']
    
    assert len(notifications) == 1

    notification = notifications[0]['message']
    assert notification == 'You have been nominated to be the manager of store 0. nomination id: 0 '

def test_purchase_notification_real_time(owner_socket, client2, user, store, clean):
    # purchase product
    headers = {'Authorization': 'Bearer ' + user}
    data = {"store_id": 0, "product_id": 0, "quantity": 1}
    client2.post('user/add_to_basket', headers=headers, json=data)
    data = {"payment_details": default_payment_method, 
            "supply_method": default_supply_method, 
            "address": default_address_checkout}
    client2.post('market/checkout', headers=headers, json=data)

    # check notification
    response = owner_socket.get_received()

    assert len(response) == 1

    notification = response[0]['args']['message']
    assert notification == 'New purchase in store: 0\n purchase ID: 0'

def test_purchase_notification_delay(app, client1, owner, owner_socket, store, client2, user, clean):
    # log out owner
    owner_socket.emit('leave')
    headers = {'Authorization': 'Bearer ' + owner}
    client1.post('auth/logout', headers=headers, json={})

    # purchase product
    headers = {'Authorization': 'Bearer ' + user}
    data = {"store_id": 0, "product_id": 0, "quantity": 1}
    client2.post('user/add_to_basket', headers=headers, json=data)
    data = {"payment_details": default_payment_method, 
            "supply_method": default_supply_method, 
            "address": default_address_checkout}
    client2.post('market/checkout', headers=headers, json=data)

    # log in owner
    guest_token = client1.get('auth/').get_json()['token']
    headers = {'Authorization': 'Bearer ' + guest_token}
    response = client1.post('auth/login', headers=headers, json={'username': 'owner', 'password': 'test'})
    new_owner_token = response.get_json()['token']
    new_owner_socket = socketio_manager.test_client(app, flask_test_client=client1, headers={'Authorization': 'Bearer ' + new_owner_token})
    new_owner_socket.emit('join')

    # check notification
    notifications = response.get_json()['notification']

    assert len(notifications) == 1
    
    notification = notifications[0]['message']
    assert notification == 'New purchase in store: 0\n purchase ID: 0'

def test_purchase_notification_real_time_multiple_owners(client1, owner, owner_socket, store, client2, user, user_socket, clean):
    # nominate owner
    headers = {'Authorization': 'Bearer ' + owner}
    data = {'store_id': 0, 'username': 'user'}
    client1.post('store/add_store_owner', headers=headers, json=data)

    # user reads notification
    assert len(user_socket.get_received()) == 1

    # accept nomination
    headers = {'Authorization': 'Bearer ' + user}
    data = {'promotion_id': 0, 'accept': True}
    client2.post('user/accept_promotion', headers=headers, json=data)

    # purchase product
    headers = {'Authorization': 'Bearer ' + user}
    data = {"store_id": 0, "product_id": 0, "quantity": 1}
    client2.post('user/add_to_basket', headers=headers, json=data)
    data = {"payment_details": default_payment_method, 
            "supply_method": default_supply_method, 
            "address": default_address_checkout}
    client2.post('market/checkout', headers=headers, json=data)

    # check notification - owner
    response = owner_socket.get_received()

    assert len(response) == 1

    notification = response[0]['args']['message']
    assert notification == 'New purchase in store: 0\n purchase ID: 0'

    # check notification - user
    response = user_socket.get_received()

    assert len(response) == 1

    notification = response[0]['args']['message']
    assert notification == 'New purchase in store: 0\n purchase ID: 0'

def test_closing_opening_store_notification_real_time(client1, owner, store, client2, user, user_socket, clean):
    # nominate manager
    headers = {'Authorization': 'Bearer ' + owner}
    data = {'store_id': 0, 'username': 'user'}
    client1.post('store/add_store_manager', headers=headers, json=data)

    # user reads notification
    assert len(user_socket.get_received()) == 1

    # accept promotion
    headers = {'Authorization': 'Bearer ' + user}
    data = {'promotion_id': 0, 'accept': True}
    client2.post('user/accept_promotion', headers=headers, json=data)

    # close store
    headers = {'Authorization': 'Bearer ' + owner}
    data = {'store_id': 0}
    client1.post('store/closing_store', headers=headers, json=data)

    # check notification
    response = user_socket.get_received()

    assert len(response) == 1

    notification = response[0]['args']['message']
    assert notification == 'Store status updated for: 0\n Store is now: closed.\nadditional details: '

    # open store
    headers = {'Authorization': 'Bearer ' + owner}
    data = {'store_id': 0}
    client1.post('store/opening_store', headers=headers, json=data)

    # check notification
    response = user_socket.get_received()

    assert len(response) == 1

    notification = response[0]['args']['message']
    assert notification == 'Store status updated for: 0\n Store is now: opened.\nadditional details: '

def test_closing_store_notification_delay(app, client1, owner, store, client2, user, user_socket, clean):

    # nominate manager
    headers = {'Authorization': 'Bearer ' + owner}
    data = {'store_id': 0, 'username': 'user'}
    client1.post('store/add_store_manager', headers=headers, json=data)

    # user reads notification
    assert len(user_socket.get_received()) == 1

    # accept promotion
    headers = {'Authorization': 'Bearer ' + user}
    data = {'promotion_id': 0, 'accept': True}
    client2.post('user/accept_promotion', headers=headers, json=data)

    # log out user
    user_socket.emit('leave')
    headers = {'Authorization': 'Bearer ' + user}
    client2.post('auth/logout', headers=headers, json={})

    # close store
    headers = {'Authorization': 'Bearer ' + owner}
    data = {'store_id': 0}
    client1.post('store/closing_store', headers=headers, json=data)

    # open store
    headers = {'Authorization': 'Bearer ' + owner}
    data = {'store_id': 0}
    client1.post('store/opening_store', headers=headers, json=data)

    # log in user
    guest_token = client2.get('auth/').get_json()['token']
    headers = {'Authorization': 'Bearer ' + guest_token}
    response = client2.post('auth/login', headers=headers, json={'username': 'user', 'password': 'test'})
    new_user_token = response.get_json()['token']
    new_user_socket = socketio_manager.test_client(app, flask_test_client=client2, headers={'Authorization': 'Bearer ' + new_user_token})
    new_user_socket.emit('join')

    # check notification
    notifications = response.get_json()['notification']

    assert len(notifications) == 2

    notification = notifications[0]['message']
    assert notification == 'Store status updated for: 0\n Store is now: closed.\nadditional details: '

    notification = notifications[1]['message']
    assert notification == 'Store status updated for: 0\n Store is now: opened.\nadditional details: '