import pytest
from backend import create_app, clean_data
import json
import threading
import queue

register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567'}

default_payment_method = {'payment method': 'bogo'}

default_supply_method = "bogo"

default_address_checkout = { 'address': 'randomstreet 34th', 
                            'city': 'arkham', 
                            'state': 'gotham',
                            'country': 'Wakanda', 
                            'zip_code': '12345'}


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
    data = {"register_credentials": manager_credentials}
    response = client1.post('auth/register', headers=headers, json=data)

    data = { "username": "store_owner", "password": "test" }
    response = client1.post('auth/login', json=data, headers=headers)
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def user_token(client2, token2):
    headers = { 'Authorization': 'Bearer ' + token2 }
    data = {"register_credentials": register_credentials}
    response = client2.post('auth/register', headers=headers, json=data)
    data = { "username": "test", "password": "test" }
    response = client2.post('auth/login', json=data, headers=headers)
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

def test_user_checkout_success(client2, user_token, init_store, clean):
    data = {"store_id": 0, "product_id": 0, "quantity": 1}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"payment_details": default_payment_method, 
            "supply_method": default_supply_method, 
            "address": default_address_checkout}
    response = client2.post('market/checkout', headers=headers, json=data)
    print(response.data)
    assert response.status_code == 200

def test_guest_checkout_success(client3, guest_token, init_store, clean):
    data = {"store_id": 0, "product_id": 0, "quantity": 1}
    headers = {'Authorization': 'Bearer ' + guest_token}
    response = client3.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200

    data = {"payment_details": default_payment_method,
            "supply_method": default_supply_method,
            "address": default_address_checkout}
    response = client3.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 200

def test_checkout_fail_store_closed(client1, client2, owner_token, user_token, init_store, clean):
    data = {"store_id": 0, "product_id": 0, "quantity": 1}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)
    
    owner_headers = {'Authorization': 'Bearer ' + owner_token}
    data = {"store_id": 0}
    response = client1.post('store/closing_store', headers=owner_headers, json=data)

    data = {"payment_details": default_payment_method,
            "supply_method": default_supply_method,
            "address": default_address_checkout}
    response = client2.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 400

def test_checkout_fail_product_unavailable(client2, client3, user_token, guest_token, init_store, clean):
    guest_headers = {'Authorization': 'Bearer ' + guest_token}
    data = {"store_id": 0, "product_id": 0, "quantity": 7}
    response = client3.post('user/add_to_basket', headers=guest_headers, json=data)

    user_headers = {'Authorization': 'Bearer ' + user_token}
    data = {"store_id": 0, "product_id": 0, "quantity": 5}
    response = client2.post('user/add_to_basket', headers=user_headers, json=data)

    data = {"payment_details": default_payment_method,
            "supply_method": default_supply_method,
            "address": default_address_checkout}
    
    response = client2.post('market/checkout', headers=user_headers, json=data)
    assert response.status_code == 200

    response = client3.post('market/checkout', headers=guest_headers, json=data)
    assert response.status_code == 400


def test_checkout_failed_policy_not_met(client1, client2, user_token, owner_token, init_store, clean):

    data = {"store_id": 0, "product_id": 0, "quantity": 1}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_name": "name", "category_id": None, "product_id": 0}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_id": 0, 'predicate_builder': ("amount_product", 2,0,0)}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/assign_predicate_to_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"payment_details": default_payment_method,
            "supply_method": default_supply_method,
            "address": default_address_checkout}
    response = client2.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 400

def test_checkout_failed_payment_method_invalid(client2, user_token, init_store, clean):
    data = {"store_id": 0, "product_id": 0, "quantity": 1}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)
    
    data = {"payment_details": {'payment method': 'invalid'},
            "supply_method": default_supply_method,
            "address": default_address_checkout}
    response = client2.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 400

def test_checkout_failed_empty_cart(client2, user_token, clean):
    data = {"payment_details": default_payment_method,
            "supply_method": default_supply_method,
            "address": default_address_checkout}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 400

def test_checkout_failed_supply_method_invalid(client2, user_token, init_store, clean):
    data = {"store_id": 0, "product_id": 0, "quantity": 1}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)

    data = {"payment_details": default_payment_method,
            "supply_method": 'invalid',
            "address": default_address_checkout}
    response = client2.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 400

def test_checkout_failed_address_invalid(client2, user_token, init_store, clean):
    data = {"store_id": 0, "product_id": 0, "quantity": 1}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)

    data = {"payment_details": default_payment_method,
            "supply_method": default_supply_method,
            "address": {'address_id': 0}}
    response = client2.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 400

