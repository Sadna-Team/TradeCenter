import pytest
from backend import create_app, clean_data
from backend.database import clear_database
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
    clear_database()

    app_context.pop()


@pytest.fixture
def clean(app):
    with app.app_context():
        clear_database()
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
def token1(app, client1):
    response = client1.get('/auth/')
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def token2(app, client2):
    response = client2.get('/auth/')
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def guest_token(app, client3):
    response = client3.get('/auth/')
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def owner_token(app, client1, token1):
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
def user_token(app, client2, token2):
    headers = { 'Authorization': 'Bearer ' + token2 }
    data = {"register_credentials": register_credentials}
    response = client2.post('auth/register', headers=headers, json=data)
    data = { "username": "test", "password": "test" }
    response = client2.post('auth/login', headers=headers, json=data)
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def init_store(app, client1, owner_token):
    data = {'store_name': 'test_store', 'address': 'test_address', 'city': 'test_city', 'state': 'test_state', 'country': 'test_country', 'zip_code': '12345'}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/add_store', headers=headers, json=data)
    print(response.data)
    assert response.status_code == 200

    store_id = response.json['storeId']

    data = {"store_id": store_id,
            "product_name": "test_product", 
            "description": "test_description",
            "price": 10.0,
            "weight": 1.0,
            "tags": ["tag1", "tag2"],
            "amount": 10}
    
    response = client1.post('store/add_product', headers=headers, json=data)
    assert response.status_code == 200
    product_id1 = response.json['product_id']

    data = {"store_id": store_id,
        "product_name": "funny", 
        "description": "test_description",
        "price": 10.0,
        "weight": 1.0,
        "tags": ["tag1", "tag2"],
        "amount": 10}

    response = client1.post('store/add_product', headers=headers, json=data)
    assert response.status_code == 200
    product_id2 = response.json['product_id']

    return {'store_id': store_id, 'product_id1': product_id1, 'product_id2': product_id2}
# def create_and_login_user(username, password, email, phone, year, month, day):
#     response = client.get('/auth/')
#     assert response.status_code == 200

#     data = json.loads(response.data)
#     assert 'token' in data

#     token1 = data['token']

#     register_credentials2 = {
#         'username': username,
#         'email': email,
#         'password': password,
#         'address': 'address2',
#         'city': 'city2',
#         'state': 'state2',
#         'country': 'country2',
#         'zip_code': '12345',
#         'year': year,
#         'month': month,
#         'day': day,
#         'phone': phone
#     }

#     headers = {
#         'Authorization': 'Bearer ' + token1
#     }
#     response = client.post('auth/register', headers=headers, json={'register_credentials': register_credentials2})
#     assert response.status_code == 201

#     response = client.post('/auth/login', headers=headers, json={'username': username, 'password': password})
#     assert response.status_code == 200
#     token1 = json.loads(response.data)['token']

#     return token1


# global token
# global guest_token


register_credentials = {
    'username': 'test',
    'email': 'test@gmail.com',
    'password': 'test',
    'address': 'address',
    'city': 'city',
    'state': 'state',
    'country': 'country',
    'zip_code': '12346',
    'year': 2003,
    'month': 1,
    'day': 1,
    'phone': '054-1234567'}


def test_start(app, client1):
    global token
    response = client1.get('/auth/')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'token' in data


def test_register(app, client1, token1):
    headers = {
        'Authorization': 'Bearer ' + token1
    }
    data1 = {
        'register_credentials': register_credentials
    }
    response = client1.post('auth/register', headers=headers, json=data1)

    assert response.status_code == 201

    


def test_register_failed_duplicate_username(app,clean, client1, token1, token2):
    headers = {
        'Authorization': 'Bearer ' + token1
    }
    data1 = {
        'register_credentials': register_credentials
    }
    response = client1.post('auth/register', headers=headers, json=data1)
    
    assert response.status_code == 201
    
    

    headers = {
        'Authorization': 'Bearer ' + token2
    }
    response = client1.post('auth/register', headers=headers, json=data1)

    assert response.status_code == 400


def test_register_failed_missing_data(app, client1, token1):
    headers = {
        'Authorization': 'Bearer ' + token1
    }
    data1 = {
        'register_credentials': {
            'username': 'test',
            'email': ' ',
            'password': 'test'
        }
    }
    response = client1.post('auth/register', headers=headers, json=data1)

    assert response.status_code == 400
    
    


def test_login(app, clean, client1, token1):
    # register user
    headers = {
        'Authorization': 'Bearer ' + token1
    }
    data = {
        'register_credentials': register_credentials
    }
    response = client1.post('auth/register', headers=headers, json=data)
    
    assert response.status_code == 201

    # login user
    data = {
        'username': 'test', 
        'password': 'test'
    }
    headers = {
        'Authorization': 'Bearer ' + token1
    }
    response = client1.post('/auth/login', headers=headers, json=data)
    
    


def test_login_failed_user_doesnt_exist(app, client1, token1):
    data = {
        'username': 'test2',
        'password': 'test'
    }
    headers = {
        'Authorization': 'Bearer ' + token1
    }

    response = client1.post('/auth/login', headers=headers, json=data)
    assert response.status_code == 401
    
    


def test_login_failed_wrong_password(app, client1, token1):
    data = {
        'username': 'test',
        'password': 'test2'
    }
    headers = {
        'Authorization': 'Bearer ' + token1
    }

    response = client1.post('/auth/login', headers=headers, json=data)
    assert response.status_code == 401
    
    


def test_login_failed_already_logged_in(app,clean, client1, token1, user_token):
    data = {
        'username': 'test',
        'password': 'test'
    }
    headers = {
        'Authorization': 'Bearer ' + token1
    }

    response = client1.post('/auth/login', headers=headers, json=data)
    assert response.status_code == 401
    
    
def test_logout(app,clean, client1, user_token):
    data = {
        'username': 'test',
        'password': 'test'
    }
    headers = {
        'Authorization': 'Bearer ' + user_token
    }

    response = client1.post('/auth/logout', headers=headers)
    assert response.status_code == 200
    

def test_logout_failed_not_logged_in(app, client1, token1):
    data = {
        'username': 'test',
        'password': 'test'
    }
    headers = {
        'Authorization': 'Bearer ' + token1
    }

    response = client1.post('/auth/logout', headers=headers)
    assert response.status_code == 400
    
    


def test_logout_guest(app, client1, token1):
    response = client1.post('/auth/logout_guest', headers={
        'Authorization': f'Bearer {token1}'
    })
    assert response.status_code == 200 


def test_show_notifications(app,clean, client1, user_token):
    response = client1.get('/user/notifications', headers={
        'Authorization': f'Bearer {user_token}'
    })
    assert response.status_code == 200

    notifications = response.json['notifications']
    assert len(notifications) == 0
    
    


def test_show_notifications_failed_not_logged_in(app, client1, token1):
    response = client1.get('/user/notifications', headers={
        'Authorization': f'Bearer {token1}'
    })

    assert response.status_code == 400
    
    


def test_add_product_to_basket(app,clean, client2, user_token, client1, owner_token):
    data = {'store_name': 'test_store', 'address': 'test_address', 'city': 'test_city', 'state': 'test_state', 'country': 'test_country', 'zip_code': '12345'}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/add_store', headers=headers, json=data)
    print(response.data)
    assert response.status_code == 200

    store_id = response.json['storeId']

    data = {"store_id": store_id,
            "product_name": "test_product", 
            "description": "test_description",
            "price": 10.0,
            "weight": 1.0,
            "tags": ["tag1", "tag2"],
            "amount": 10}
    
    response = client1.post('store/add_product', headers=headers, json=data)
    assert response.status_code == 200
    product_id = response.json['product_id']
    response = client2.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': store_id,
        'product_id': product_id,
        'quantity': 1
    })

    assert response.status_code == 200
    
    


def test_add_product_to_basket_failed_amount_exceeds(app,clean, client1, user_token, init_store):
    response = client1.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1'],
        'quantity': 100
    })

    assert response.status_code == 400
    
    


def test_add_product_to_basket_store_not_exists(app, clean, client1, user_token, init_store):
    response = client1.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': init_store['store_id']+100,
        'product_id': init_store['product_id1'],
        'quantity': 1
    })

    assert response.status_code == 400


def test_add_product_to_basket_product_not_exists(app, clean, client1, user_token, init_store):
    response = client1.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1']+100,
        'quantity': 1
    })

    assert response.status_code == 400
    
    


def test_remove_product_from_basket(app, clean, client1, user_token, init_store):
    response = client1.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1'],
        'quantity': 1
    })

    assert response.status_code == 200
    
    


def test_remove_product_from_basket_failed_not_logged_in(app, client1, token1, init_store):
    response = client1.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {token1}'
    }, json={
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1'],
        'quantity': 1
    })

    assert response.status_code == 400
    
    


def test_remove_product_from_basket_failed_store_not_exists(app, clean, client1, user_token, init_store):
    response = client1.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': init_store['store_id']+100,
        'product_id': init_store['product_id1'],
        'quantity': 1
    })

    assert response.status_code == 400
    
    


def test_remove_product_from_basket_failed_product_not_exists(app, clean, client1, user_token, init_store):
    response = client1.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1']+100,
        'quantity': 1
    })

    assert response.status_code == 400
    
    


def test_remove_product_from_basket_failed_quantity_exceeds(app, clean, client1, user_token, init_store):
    response = client1.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1'],
        'quantity': 100
    })

    assert response.status_code == 400
    
    


def test_show_cart(app, client1, user_token):
    response = client1.get('/user/cart', headers={
        'Authorization': f'Bearer {user_token}'
    })

    assert response.status_code == 200
    
    


def test_search_by_category(app, client1, user_token, init_store):
    data = {"store_id": init_store['store_id'], "category_id": 0}
    response = client1.post('/market/search_products_by_category', headers={
        'Authorization': f'Bearer {user_token}'
    }, json=data)
    assert response.status_code == 200
    
    


def test_search_by_category_failed_store_not_exists(app, client1, user_token):
    data = {"store_id": init_store['store_id']+100, "category_id": 0}
    response = client1.post('/market/search_products_by_category', headers={
        'Authorization': f'Bearer {user_token}'
    }, json=data)
    assert response.status_code == 400
    
    


def test_search_by_category_failed_category_not_exists(app, client1, user_token):
    data = {"store_id": 0, "category_id": 100}
    response = client1.post('/market/search_products_by_category', headers={
        'Authorization': f'Bearer {user_token}'
    }, json=data)
    assert response.status_code == 400
    
    


def test_search_by_tags(app, client1, user_token):
    data = {"store_id": 0, "tags": ["tag1"]}
    response = client1.post('/market/search_products_by_tags', headers={
        'Authorization': f'Bearer {user_token}'
    }, json=data)
    assert response.status_code == 200
    
    


def test_search_by_tags_failed_store_not_exists(app, client1, user_token):
    data = {"store_id": 100, "tags": ["tag1"]}
    response = client1.post('/market/search_products_by_tags', headers={
        'Authorization': f'Bearer {user_token}'
    }, json=data)
    assert response.status_code == 400
    
    


def test_search_by_name(app, client1, user_token):
    data = {"store_id": 0, "name": "test_product"}
    response = client1.post('/market/search_products_by_name', headers={
        'Authorization': f'Bearer {user_token}'
    }, json=data)
    assert response.status_code == 200
    
    


def test_search_by_name_failed_store_not_exists(app, client1, user_token):
    data = {"store_id": 100, "name": "test_product"}
    response = client1.post('/market/search_products_by_name', headers={
        'Authorization': f'Bearer {user_token}'
    }, json=data)
    assert response.status_code == 400
    
    


def test_information_about_stores(app, client1, user_token):
    response = client1.get('/store/store_info', headers={
        'Authorization': f'Bearer {user_token}'
    })
    assert response.status_code == 200
    
    



def test_information_about_stores_failed_store_not_exists(app, client1, user_token):
    response = client1.get('/store/store_info', headers={
        'Authorization': f'Bearer {user_token}'
    })
    assert response.status_code == 400
    
    



def test_add_store(app, client1, owner_token):
    data = {
        'store_name': 'test_store',
        'address': 'test_address',
        'city': 'test_city',
        'state': 'test_state',
        'country': 'test_country',
        'zip_code': '12345'
    }
    headers = {
        'Authorization': 'Bearer ' + owner_token
    }
    response = client1.post('store/add_store', headers=headers, json=data)

    assert response.status_code == 200
    
    


def test_add_store_failed_user_not_a_member(app, client1, token1):
    data = {
        'store_name': 'test_store',
        'address': 'test_address',
        'city': 'test_city',
        'state': 'test_state',
        'country': 'test_country',
        'zip_code': '12345'
    }
    headers = {
        'Authorization': 'Bearer ' + token1
    }
    response = client1.post('store/add_store', headers=headers, json=data)

    assert response.status_code == 400


default_payment_method = {'payment method': 'bogo'}

default_supply_method = "bogo"

default_address_checkout = {'address': 'randomstreet 34th', 
                            'city': 'arkham',
                            'state': 'gotham', 
                            'country': 'Wakanda', 
                            'zip_code': '12345'}

def test_show_purchase_history_of_user(app, client1, user_token):
    #adding a product to the basket
    response = client1.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': 0,
        'product_id': 0,
        'quantity': 1
    })
    assert response.status_code == 200

    #purchase the product
    response = client1.post('market/checkout', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'payment_details': default_payment_method,
        'supply_method': default_supply_method,
        'address': default_address_checkout})
    assert response.status_code == 200


    #show purchase history
    response = client1.get('market/user_purchase_history', headers={
        'Authorization': f'Bearer {token}'
    }, json={"user_id": 1})
    assert response.status_code == 200
    
    


def test_show_purchase_history_of_user_failed_is_not_logged_in(app, client1, guest_token):
    #adding a product to the basket
    response = client1.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {guest_token}'
    }, json={
        'store_id': 0,
        'product_id': 0,
        'quantity': 1
    })
    assert response.status_code == 200

    #purchase the product
    response = client1.post('market/checkout', headers={
        'Authorization': f'Bearer {guest_token}'
    }, json={
        'payment_details': default_payment_method,
        'supply_method': default_supply_method,
        'address': default_address_checkout})
    assert response.status_code == 200

    #show purchase history
    response = client1.get('market/user_purchase_history', headers={'Authorization': f'Bearer {guest_token}'}, json={"user_id": 1})
    assert response.status_code == 400
    
    


def test_show_purchase_history_of_user_in_store(app, client1, user_token):
    #adding a product to the basket
    response = client1.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': 0,
        'product_id': 0,
        'quantity': 1
    })
    assert response.status_code == 200

    #purchase the product
    response = client1.post('market/checkout', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'payment_details': default_payment_method,
        'supply_method': default_supply_method,
        'address': default_address_checkout})
    assert response.status_code == 200
    
    #show purchase history
    response = client1.get('market/user_purchase_history', headers
    ={'Authorization': f'Bearer {user_token}'}, json={"user_id": 1, "store_id": 0})
    assert response.status_code == 200
    
    


def test_show_purchase_history_of_user_in_store_failed_is_not_logged_in(app, client1, guest_token):
    #adding a product to the basket
    response = client1.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {guest_token}'
    }, json={
        'store_id': 0,
        'product_id': 0,
        'quantity': 1
    })
    assert response.status_code == 200
    
    

    #purchase the product
    response = client1.post('market/checkout', headers={
        'Authorization': f'Bearer {guest_token}'
    }, json={
        'payment_details': default_payment_method,
        'supply_method': default_supply_method,
        'address': default_address_checkout})
    assert response.status_code == 200

    #show purchase history
    response = client1.get('market/user_purchase_history', headers={'Authorization': f'Bearer {guest_token}'}, json={"user_id": 1, "store_id": 0})
    assert response.status_code == 400
   
   #bid tests:
   
   
   # Use-Case: user bid offer 2.2.5.2.1.a
def test_user_bid_offer_success(app, clean, client, user_token, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    data = {
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1'],
        'proposed_price': 20.0
    }
    response = client.post('market/user_bid_offer', headers=headers, json=data)
    assert response.status_code == 200
    response_data = response.json
    assert 'bid_id' in response_data
    assert response_data['status'] == 'ongoing'

# Use-Case: user bid offer 2.2.5.2.1.b
def test_user_bid_offer_failure_store_not_exist(app, clean, client, user_token, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    data = {
        'store_id': init_store['store_id']+999,
        'product_id': init_store['product_id1'],
        'proposed_price': 20.0
    }
    response = client.post('market/user_bid_offer', headers=headers, json=data)
    assert response.status_code == 400

# Use-Case: user bid offer 2.2.5.2.1.c
def test_user_bid_offer_failure_negative_price(app, clean, client, user_token, store_setup, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    data = {
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1'],
        'proposed_price': -10.0
    }
    response = client.post('market/user_bid_offer', headers=headers, json=data)
    assert response.status_code == 400

# Use-Case: user bid offer 2.2.5.2.1.d
'''
def test_user_bid_offer_failure_user_suspended(app, clean, client, user_token, store_setup):
    headers = { 'Authorization': 'Bearer ' + user_token }
    
    
    headers = { 'Authorization': 'Bearer ' + user_token }
    data = {
        'store_id': store_setup,
        'product_id': 0,
        'proposed_price': 20.0
    }
    response = client.post('user/offer_bid', headers=headers, json=data)
    assert response.status_code == 403
'''

# Use-Case: user counter bid accept 2.2.5.2.5.a
def test_user_counter_bid_accept_success(app, clean, client, user_token, client1, owner_token, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1'],
        'proposed_price': 20.0
    }
    client.post('market/user_bid_offer', headers=headers, json=bid_data)
    assert response.status_code == 200
    bid_id = response.json['message']
    headers = { 'Authorization': 'Bearer ' + owner_token }
    client1.post('market/store_worker_counter_bid', headers=headers, json={'bid_id': bid_id, 'store_id': init_store['store_id'] ,'proposed_price': 15.0})
    assert response.status_code == 200
    
    headers = { 'Authorization': 'Bearer ' + user_token }
    response = client.post('market/user_counter_accept', headers=headers, json={'bid_id': bid_id})
    assert response.status_code == 200

# Use-Case: user counter bid accept 2.2.5.2.5.b
def test_user_counter_bid_accept_failure_not_offer_to_user(app, clean, client, user_token, client1, owner_token, guest_token, client3, init_store):
    headers = { 'Authorization': 'Bearer ' + guest_token }
    bid_data = {
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1'],
        'proposed_price': 20.0
    }
    client3.post('market/user_bid_offer', headers=headers, json=bid_data)
    assert response.status_code == 200
    bid_id = response.json['message']
    headers = { 'Authorization': 'Bearer ' + owner_token }
    client1.post('market/store_worker_counter_bid', headers=headers, json={'bid_id': bid_id, 'store_id': init_store['store_id'] ,'proposed_price': 15.0})
    assert response.status_code == 200
    
    headers = { 'Authorization': 'Bearer ' + user_token }
    response = client.post('market/user_counter_accept', headers=headers, json={'bid_id': bid_id})
    assert response.status_code == 400
    
# Use-Case: user counter bid accept 2.2.5.2.5.c
def test_user_counter_bid_accept_failure_bid_not_ongoing(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1'],
        'proposed_price': 20.0
    }
    client.post('market/user_bid_offer', headers=headers, json=bid_data)
    assert response.status_code == 200
    bid_id = response.json['message']
    headers = { 'Authorization': 'Bearer ' + owner_token }
    client1.post('market/store_worker_decline_bid', headers=headers, json={'bid_id': bid_id, 'store_id': init_store['store_id']})
    assert response.status_code == 200
    
    headers = { 'Authorization': 'Bearer ' + user_token }
    response = client.post('market/user_counter_accept', headers=headers, json={'bid_id': bid_id})
    assert response.status_code == 400

# Use-Case: user counter bid accept 2.2.5.2.5.d
'''
def test_user_counter_bid_accept_failure_user_suspended(app, clean, client, user_token, store_setup):
    headers = { 'Authorization': 'Bearer ' + user_token }
    # Simulate user suspension
    app.config['TEST_USER_SUSPENDED'] = True
    
    # Accept counter bid
    response = client.post('user/accept_counter_bid', headers=headers, json={'bid_id': 0})
    assert response.status_code == 403
'''

# Use-Case: user counter bid accept 2.2.5.2.5.e
def test_user_counter_bid_accept_failure_bid_not_exist(app, clean, client, user_token):
    headers = { 'Authorization': 'Bearer ' + user_token }
    
    response = client.post('user/accept_counter_bid', headers=headers, json={'bid_id': 999})
    assert response.status_code == 400

# Use-Case: user counter bid decline 2.2.5.2.6.a
def test_user_counter_bid_decline_success(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1'],
        'proposed_price': 20.0
    }
    client.post('market/user_bid_offer', headers=headers, json=bid_data)
    assert response.status_code == 200
    bid_id = response.json['message']
    headers = { 'Authorization': 'Bearer ' + owner_token }
    client1.post('market/store_worker_counter_bid', headers=headers, json={'bid_id': bid_id, 'store_id': init_store['store_id'] ,'proposed_price': 15.0})
    assert response.status_code == 200
    
    headers = { 'Authorization': 'Bearer ' + user_token }
    response = client.post('market/user_counter_decline', headers=headers, json={'bid_id': bid_id})
    assert response.status_code == 200

# Use-Case: user counter bid decline 2.2.5.2.6.b
def test_user_counter_bid_decline_failure_not_offer_to_user(app, clean, client, user_token, owner_token, guest_token, client3 client1, init_store):
    headers = { 'Authorization': 'Bearer ' + guest_token }
    bid_data = {
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1'],
        'proposed_price': 20.0
    }
    client3.post('market/user_bid_offer', headers=headers, json=bid_data)
    assert response.status_code == 200
    bid_id = response.json['message']
    headers = { 'Authorization': 'Bearer ' + owner_token }
    client1.post('market/store_worker_counter_bid', headers=headers, json={'bid_id': bid_id, 'store_id': init_store['store_id'] ,'proposed_price': 15.0})
    assert response.status_code == 200
    
    headers = { 'Authorization': 'Bearer ' + user_token }
    response = client.post('market/user_counter_decline', headers=headers, json={'bid_id': bid_id})
    assert response.status_code == 200

# Use-Case: user counter bid decline 2.2.5.2.6.c
def test_user_counter_bid_decline_failure_bid_not_ongoing(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': init_store['store_id'],
        'product_id': init_store['product_id1'],
        'proposed_price': 20.0
    }
    client.post('market/user_bid_offer', headers=headers, json=bid_data)
    assert response.status_code == 200
    bid_id = response.json['message']
    headers = { 'Authorization': 'Bearer ' + owner_token }
    client1.post('market/store_worker_counter_bid', headers=headers, json={'bid_id': bid_id, 'store_id': init_store['store_id'] ,'proposed_price': 15.0})
    assert response.status_code == 200
    
    headers = { 'Authorization': 'Bearer ' + user_token }
    response = client.post('market/user_counter_decline', headers=headers, json={'bid_id': bid_id})
    assert response.status_code == 200

# Use-Case: user counter bid decline 2.2.5.2.6.d
'''
def test_user_counter_bid_decline_failure_user_suspended(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    # Simulate user suspension
    app.config['TEST_USER_SUSPENDED'] = True
    
    # Decline counter bid
    response = client.post('user/decline_counter_bid', headers=headers, json={'bid_id': 0})
    assert response.status_code == 403
'''

# Use-Case: user counter bid decline 2.2.5.2.6.e
def test_user_counter_bid_decline_failure_bid_not_exist(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    
    response = client.post('user/decline_counter_bid', headers=headers, json={'bid_id': 999})
    assert response.status_code == 404

# Use-Case: user bid cancel 2.2.5.2.8.a
def test_user_bid_cancel_success(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': store_setup,
        'product_id': 0,
        'proposed_price': 20.0
    }
    client.post('user/offer_bid', headers=headers, json=bid_data)
    
    response = client.post('user/cancel_bid', headers=headers, json={'bid_id': 0})
    assert response.status_code == 200

# Use-Case: user bid cancel 2.2.5.2.8.b
def test_user_bid_cancel_failure_bid_accepted(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': store_setup,
        'product_id': 0,
        'proposed_price': 20.0
    }
    client.post('user/offer_bid', headers=headers, json=bid_data)
    
    app.config['TEST_BID_ACCEPTED'] = True
    
    response = client.post('user/cancel_bid', headers=headers, json={'bid_id': 0})
    assert response.status_code == 400

# Use-Case: user bid cancel 2.2.5.2.8.c
def test_user_bid_cancel_failure_bid_declined(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': store_setup,
        'product_id': 0,
        'proposed_price': 20.0
    }
    client.post('user/offer_bid', headers=headers, json=bid_data)
    
    app.config['TEST_BID_DECLINED'] = True
    
    response = client.post('user/cancel_bid', headers=headers, json={'bid_id': 0})
    assert response.status_code == 400

# Use-Case: bid checkout 2.2.5.2.9.a
def test_bid_checkout_success(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': store_setup,
        'product_id': 0,
        'proposed_price': 20.0
    }
    client.post('user/offer_bid', headers=headers, json=bid_data)
    
    app.config['TEST_BID_APPROVED'] = True
    
    response = client.post('user/checkout_bid', headers=headers, json={
        'bid_id': 0,
        'payment_details': default_payment_method,
        'supply_method': default_supply_method
    })
    assert response.status_code == 200

# Use-Case: bid checkout 2.2.5.2.9.b
def test_bid_checkout_failure_bid_not_approved(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': store_setup,
        'product_id': 0,
        'proposed_price': 20.0
    }
    client.post('user/offer_bid', headers=headers, json=bid_data)
    
    response = client.post('user/checkout_bid', headers=headers, json={
        'bid_id': 0,
        'payment_details': default_payment_method,
        'supply_method': default_supply_method
    })
    assert response.status_code == 400

# Use-Case: Payment 2.2.5.2.9.c
def test_payment_failure_store_not_active(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': store_setup,
        'product_id': 0,
        'proposed_price': 20.0
    }
    client.post('user/offer_bid', headers=headers, json=bid_data)
    
    app.config['TEST_STORE_NOT_ACTIVE'] = True
    
    response = client.post('user/checkout_bid', headers=headers, json={
        'bid_id': 0,
        'payment_details': default_payment_method,
        'supply_method': default_supply_method
    })
    assert response.status_code == 400

# Use-Case: Payment 2.2.5.2.9.d
def test_payment_failure_insufficient_product(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': store_setup,
        'product_id': 0,
        'proposed_price': 20.0
    }
    client.post('user/offer_bid', headers=headers, json=bid_data)
    
    app.config['TEST_INSUFFICIENT_PRODUCT'] = True
    
    response = client.post('user/checkout_bid', headers=headers, json={
        'bid_id': 0,
        'payment_details': default_payment_method,
        'supply_method': default_supply_method
    })
    assert response.status_code == 400

# Use-Case: Payment 2.2.5.2.9.e
def test_payment_failure_purchase_policy_not_met(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': store_setup,
        'product_id': 0,
        'proposed_price': 20.0
    }
    client.post('user/offer_bid', headers=headers, json=bid_data)
    
    app.config['TEST_PURCHASE_POLICY_NOT_MET'] = True
    
    response = client.post('user/checkout_bid', headers=headers, json={
        'bid_id': 0,
        'payment_details': default_payment_method,
        'supply_method': default_supply_method
    })
    assert response.status_code == 400

# Use-Case: Payment 2.2.5.2.9.f
def test_payment_failure_unsupported_supply_method(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': store_setup,
        'product_id': 0,
        'proposed_price': 20.0
    }
    client.post('user/offer_bid', headers=headers, json=bid_data)
    
    app.config['TEST_UNSUPPORTED_SUPPLY_METHOD'] = True
    
    response = client.post('user/checkout_bid', headers=headers, json={
        'bid_id': 0,
        'payment_details': default_payment_method,
        'supply_method': default_supply_method
    })
    assert response.status_code == 400

# Use-Case: Payment 2.2.5.2.9.g
def test_payment_failure_external_payment_service(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': store_setup,
        'product_id': 0,
        'proposed_price': 20.0
    }
    client.post('user/offer_bid', headers=headers, json=bid_data)
    
    app.config['TEST_PAYMENT_SERVICE_FAIL'] = True
    
    response = client.post('user/checkout_bid', headers=headers, json={
        'bid_id': 0,
        'payment_details': default_payment_method,
        'supply_method': default_supply_method
    })
    assert response.status_code == 500

# Use-Case: view user bids 2.2.5.2.10.a
def test_view_user_bids_success(app, clean, client, user_token, owner_token, client1, init_store):
    headers = { 'Authorization': 'Bearer ' + user_token }
    bid_data = {
        'store_id': store_setup,
        'product_id': 0,
        'proposed_price': 20.0
    }
    client.post('user/offer_bid', headers=headers, json=bid_data)
    
    response = client.get('user/view_bids', headers=headers)
    assert response.status_code == 200

# Use-Case: view user bids 2.2.5.2.10.b
'''
def test_view_user_bids_failure_user_suspended(app, clean, client, user_token):
    headers = { 'Authorization': 'Bearer ' + user_token }
    # Simulate user suspension
    app.config['TEST_USER_SUSPENDED'] = True
    
    # View user bids
    response = client.get('user/view_bids', headers=headers)
    assert response.status_code == 403 
''' 
