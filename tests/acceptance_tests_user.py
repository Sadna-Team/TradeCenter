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

    data = {"store_id": store_id,
        "product_name": "funny", 
        "description": "test_description",
        "price": 10.0,
        "weight": 1.0,
        "tags": ["tag1", "tag2"],
        "amount": 10}

    response = client1.post('store/add_product', headers=headers, json=data)
    assert response.status_code == 200

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
    response = client2.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': store_id,
        'product_id': 0,
        'quantity': 1
    })

    assert response.status_code == 200
    
    


def test_add_product_to_basket_failed_amount_exceeds(app,clean, client1, user_token):
    response = client1.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': 1,
        'product_id': 0,
        'quantity': 100
    })

    assert response.status_code == 400
    
    


def test_add_product_to_basket_store_not_exists(app, clean, client1, user_token):
    response = client1.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': 100,
        'product_id': 0,
        'quantity': 1
    })

    assert response.status_code == 400


def test_add_product_to_basket_product_not_exists(app, clean, client1, user_token):
    response = client1.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': 0,
        'product_id': 100,
        'quantity': 1
    })

    assert response.status_code == 400
    
    


def test_remove_product_from_basket(app, clean, client1, user_token):
    response = client1.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': 0,
        'product_id': 0,
        'quantity': 1
    })

    assert response.status_code == 200
    
    


def test_remove_product_from_basket_failed_not_logged_in(app, client1, token1):
    response = client1.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {token1}'
    }, json={
        'store_id': 0,
        'product_id': 0,
        'quantity': 1
    })

    assert response.status_code == 400
    
    


def test_remove_product_from_basket_failed_store_not_exists(app, clean, client1, user_token):
    response = client1.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': 100,
        'product_id': 0,
        'quantity': 1
    })

    assert response.status_code == 400
    
    


def test_remove_product_from_basket_failed_product_not_exists(app, clean, client1, user_token):
    response = client1.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': 0,
        'product_id': 100,
        'quantity': 1
    })

    assert response.status_code == 400
    
    


def test_remove_product_from_basket_failed_quantity_exceeds(app, clean, client1, user_token):
    response = client1.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {user_token}'
    }, json={
        'store_id': 0,
        'product_id': 0,
        'quantity': 100
    })

    assert response.status_code == 400
    
    


def test_show_cart(app, client1, user_token):
    response = client1.get('/user/cart', headers={
        'Authorization': f'Bearer {user_token}'
    })

    assert response.status_code == 200
    
    


def test_search_by_category(app, client1, user_token):
    data = {"store_id": 0, "category_id": 0}
    response = client1.post('/market/search_products_by_category', headers={
        'Authorization': f'Bearer {user_token}'
    }, json=data)
    assert response.status_code == 200
    
    


def test_search_by_category_failed_store_not_exists(app, client1, user_token):
    data = {"store_id": 100, "category_id": 0}
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
    
    
