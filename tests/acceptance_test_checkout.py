import pytest
from backend import create_app, clean_data
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

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client1(app):
    return app.test_client()

@pytest.fixture
def client2(app):
    return app.test_client()

@pytest.fixture
def client3(app):
    return app.test_client()

@pytest.fixture
def token1(client1):
    response = client1.get('/auth/')
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def token2(client2):
    response = client2.get('/auth/')
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def guest_token(client3):
    response = client3.get('/auth/')
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def owner_token(client1, token1):
    headers = { 'Authorization': 'Bearer ' + token1 }
    manager_credentials = register_credentials.copy()
    manager_credentials['username'] = 'store_owner'
    response = client1.post('auth/register', headers=headers, json=manager_credentials)

    data = { "username": "store_owner", "password": "test" }
    response = client1.post('auth/login', json=data)
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def user_token(client2, token2):
    headers = { 'Authorization': 'Bearer ' + token2 }
    response = client2.post('auth/register', headers=headers, json=register_credentials)
    data = { "username": "test", "password": "test" }
    response = client2.post('auth/login', json=data)
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def init_store(client1, owner_token):
    data = {'store_name': 'test_store', 'location_id': 1}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/add_store', headers=headers, json=data)

    data = {"store_id": 0, 
            "product_name": "test_product", 
            "description": "test_description",
            "price": 10.0,
            "weight": 1.0,
            "tags": ["tag1", "tag2"],
            "amount": 10}
    
    response = client1.post('store/add_product', headers=headers, json=data)

    data = {"store_id": 0, 
        "product_name": "funny", 
        "description": "test_description",
        "price": 10.0,
        "weight": 1.0,
        "tags": ["tag1", "tag2"],
        "amount": 10}

    response = client1.post('store/add_product', headers=headers, json=data)

