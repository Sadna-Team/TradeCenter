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
def client3(app):
    return app.test_client()

@pytest.fixture
def client4(app):
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
def token4(client4):
    response = client4.get('/auth/')
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

    data = {"store_id": 0, "policy_name": "no_funny_name"}
    response = client1.post('store/add_purchase_policy', headers=headers, json=data)

    data = {"store_id": 0, 
        "product_name": "funny", 
        "description": "test_description",
        "price": 10.0,
        "weight": 1.0,
        "tags": ["tag1", "tag2"],
        "amount": 10}

    response = client1.post('store/add_product', headers=headers, json=data)

@pytest.fixture
def setup_2_owners(client1, client4, owner_token, init_store, token4):
    owner_credentials = register_credentials.copy()
    owner_credentials['username'] = 'store_owner2'
    data = {"register_credentials": owner_credentials}
    
    response = client4.post('auth/register', headers={'Authorization': 'Bearer ' + token4}, json=data)

    data = { "username": "store_owner2", "password": "test" }
    response = client4.post('auth/login', json=data, headers={'Authorization': 'Bearer ' + token4})
    logged_in_token= json.loads(response.data)['token']

    data = {"store_id": 0, "username": "store_owner2"}
    response = client1.post('store/add_store_owner', headers={'Authorization': 'Bearer ' + owner_token}, json=data)

    data = {"promotion_id": 0, "accept": True}
    response = client4.post('user/accept_promotion', headers={'Authorization': 'Bearer ' + logged_in_token}, json=data)
    return logged_in_token


# CONCURRENT TESTS
results = queue.Queue()

def thread_purchase(client, token):
    headers = {'Authorization': f'Bearer {token}'}
    data = {"payment_details": default_payment_method,
            "supply_method": default_supply_method,
            "address": default_address_checkout}
    response = client.post('market/checkout', headers=headers, json=data)
    results.put(response)

def thread_remove_product(client, token):
    headers = {'Authorization': f'Bearer {token}'}
    data = {"store_id": 0, "product_id": 0}
    response = client.post('store/remove_product', headers=headers, json=data)
    results.put(response)

def thread_close_store(client, token):
    headers = {'Authorization': f'Bearer {token}'}
    data = {"store_id": 0}
    response = client.post('store/closing_store', headers=headers, json=data)
    results.put(response)

def thread_accept_promotion(client, token, nomination_id):
    headers = {'Authorization': f'Bearer {token}'}
    data = {"promotion_id": nomination_id, "accept": True}
    response = client.post('user/accept_promotion', headers=headers, json=data)
    results.put(response.status_code)

def test_concurrent_checkout_competition(client2, client3, user_token, guest_token, init_store, clean):
    data = {"store_id": 0, "product_id": 0, "quantity": 6}
    user_headers = {'Authorization': 'Bearer ' + user_token}
    guest_headers = {'Authorization': 'Bearer ' + guest_token}
    response = client2.post('user/add_to_basket', headers=user_headers, json=data)
    response = client3.post('user/add_to_basket', headers=guest_headers, json=data)

    thread1 = threading.Thread(target=thread_purchase, args=(client2, user_token))
    thread2 = threading.Thread(target=thread_purchase, args=(client3, guest_token))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    assert len(results.queue) == 2
    result1 = results.get()
    result2 = results.get()
    assert (result1.status_code == 200 and result2.status_code == 400) or (result1.status_code == 400 and result2.status_code == 200)
    results.queue.clear()

def test_concurrent_checkout_remove(client1, client2, owner_token, user_token, init_store, clean):
    data = {"store_id": 0, "product_id": 0, "quantity": 10}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)

    thread1 = threading.Thread(target=thread_purchase, args=(client2, user_token))
    thread2 = threading.Thread(target=thread_remove_product, args=(client1, owner_token))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    assert len(results.queue) == 2
    result1 = results.get()
    result2 = results.get()
    assert ((result1.status_code == 200 and result2.status_code == 200) or
            (result1.status_code == 400 and result1.get_json()['message'] == 'Product not found' and result2.status_code == 200) or
            (result1.status_code == 200 and result2.status_code == 400 and result2.get_json()['message'] == 'Product not found'))
    results.queue.clear()

def test_concurrent_checkout_close_store(client1, client2, owner_token, user_token, init_store, clean):
    data = {"store_id": 0, "product_id": 0, "quantity": 10}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)

    thread1 = threading.Thread(target=thread_purchase, args=(client2, user_token))
    thread2 = threading.Thread(target=thread_close_store, args=(client1, owner_token))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    assert len(results.queue) == 2
    result1 = results.get()
    result2 = results.get()

    assert ((result1.status_code == 200 and result2.status_code == 200) or
            (result1.status_code == 400 and result1.get_json()['message'] == 'Store not found' and result2.status_code == 200) or
            (result1.status_code == 200 and result2.status_code == 400 and result2.get_json()['message'] == 'Store not found'))
    results.queue.clear()

def test_concurrent_accept_twice(client1, client2, client4, owner_token, user_token, setup_2_owners, clean):
    owner1_header = {'Authorization': f'Bearer {owner_token}'}
    owner2_header = {'Authorization': f'Bearer {setup_2_owners}'}

    data = {"store_id": 0, "username": "test"}
    response = client1.post('store/add_store_owner', headers=owner1_header, json=data)

    data = {"store_id": 0, "username": "test"}
    response = client4.post('store/add_store_owner', headers=owner2_header, json=data)

    thread1 = threading.Thread(target=thread_accept_promotion, args=(client1, user_token, 1))
    thread2 = threading.Thread(target=thread_accept_promotion, args=(client4, user_token, 2))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    assert len(results.queue) == 2
    result1 = results.get()
    result2 = results.get()
    assert (result1 == 400 and result2 == 200) or (result1 == 200 and result2 == 400)
