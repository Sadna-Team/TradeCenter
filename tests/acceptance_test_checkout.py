import pytest
from backend import create_app, clean_data
import json
import threading
import queue
register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'address': 'regular adddress',
        'city': 'regular city',
        'state': 'regular state',
        'country': 'regular country',
        'zip_code': '12345',
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567'}

default_payment_method = {'payment method': 'bogo'}

default_payment_additional_details = {"currency": "USD",
                                    "card_number": "1111222233334444",
                                    "month": "12",
                                    "year": "2025",
                                    "holder": "michael adar", 
                                    "cvv": "123",
                                    "id": "1234567890", 
                                    "currency": "USD"}

default_supply_method = "bogo"

default_supply_additional_details = {"name": "michael adar",
                                    "address": "Rager 130 13",
                                    "city": "Beer Sheva",
                                    "zip": "123456",
                                    "country": "Israel"}

default_address_checkout = { 'address': 'randomstreet 34th', 
                            'city': 'arkham', 
                            'state': 'gotham',
                            'country': 'Wakanda', 
                            'zip_code': '12345'}


@pytest.fixture(scope='session', autouse=True)
def app():
    # Setup: Create the Flask app
    """app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_secret_key'  # Set a test secret key
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
    auth = Authentication()
    auth.clean_data()
    auth.set_jwt(jwt, bcrypt)"""
    global app

    from backend.app_factory import create_app_instance
    app = create_app_instance(mode='testing')

    # Push application context for testing
    app_context = app.app_context()
    app_context.push()

    # Make the app context available in tests
    yield app

    clean_data()

    app_context.pop()

@pytest.fixture
def clean(app):
    yield
    with app.app_context():
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
    data = {'store_name': 'test_store', 'address': 'test_address', 'city': 'test_city', 'state': 'test_state', 'country': 'test_country', 'zip_code': '12345'}
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

def test_user_checkout_extended_payment_success(client2, user_token, init_store, clean):
    data = {"store_id": 0, "product_id": 0, "quantity": 1}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"payment_details": default_payment_method, 
            "payment_additional_details": default_payment_additional_details,
            "supply_method": default_supply_method, 
            "address": default_address_checkout}
    response = client2.post('market/checkout', headers=headers, json=data)
    print(response.data)
    assert response.status_code == 200

def test_user_checkout_extended_supply_success(client2, user_token, init_store, clean):
    data = {"store_id": 0, "product_id": 0, "quantity": 1}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"payment_details": default_payment_method, 
            "supply_method": default_supply_method, 
            "supply_additional_details": default_supply_additional_details,
            "address": default_address_checkout}
    response = client2.post('market/checkout', headers=headers, json=data)
    print(response.data)
    assert response.status_code == 200

def test_user_checkout_extended_all_success(client2, user_token, init_store, clean):
    data = {"store_id": 0, "product_id": 0, "quantity": 1}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"payment_details": default_payment_method, 
            "payment_additional_details": default_payment_additional_details,
            "supply_method": default_supply_method, 
            "supply_additional_details": default_supply_additional_details,
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
    
    data = {"store_id": 0, "policy_id": 0, 'predicate_builder': ("amount_product", 2,-1, 0,0)}
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
            "address": {'address': "missing_address"}}
    response = client2.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 400

