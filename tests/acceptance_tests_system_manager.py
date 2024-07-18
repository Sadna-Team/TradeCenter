from datetime import datetime, time
import pytest
from backend import clean_data
from backend.app_factory import create_app_instance
import json


register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'address': 'address',
        'city': 'city',
        'state': 'state',
        'country': 'country',
        'zip_code': '12345',
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567' }

default_payment_method = {'payment method': 'bogo'}

default_supply_method = "bogo"

default_address = { 'address': 'randomstreet 34th', 
                    'city': 'arkham',
                    'state': 'Utopia', 
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
    app = create_app_instance('testing')

    # Push application context for testing
    app_context = app.app_context()
    app_context.push()

    # Make the app context available in tests
    yield app

    clean_data()
    from backend.database import clear_database
    clear_database()

    app_context.pop()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def token(client):
    response = client.get('/auth/')
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def admin_token(client, token):
    data = {
        'username': 'admin',
        'password': 'admin'
    }
    headers = { 'Authorization': 'Bearer ' + token }
    response = client.post('auth/login', headers=headers, json=data)
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def clean(app):
    yield
    with app.app_context():
        from backend.database import clear_database
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
    data = {'store_name': 'test_store', 'address': 'address', 'city': 'city', 'state': 'state', 'country': 'country', 'zip_code': '12345'}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/add_store', headers=headers, json=data)
    
    store_id = json.loads(response.data)['storeId']

    data = {"store_id": store_id, 
            "product_name": "test_product", 
            "description": "test_description",
            "price": 10.0,
            "weight": 1.0,
            "tags": ["tag1", "tag2"],
            "amount": 10}
    
    response = client1.post('store/add_product', headers=headers, json=data)

 
    data = {"store_id": store_id, "policy_name": "no_funny_name", "category_id": None, "product_id": None}
    response = client1.post('store/add_purchase_policy', headers=headers, json=data)

    data = {"store_id": store_id, 
        "product_name": "funny", 
        "description": "test_description",
        "price": 10.0,
        "weight": 1.0,
        "tags": ["tag1", "tag2"],
        "amount": 10}

    response = client1.post('store/add_product', headers=headers, json=data)
    
    return store_id

#test 2.6.4.a
def test_getting_info_about_purchase_history_of_a_member(client, admin_token, client2, user_token, client1, owner_token, init_store, clean):
    # add discounts:
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store, "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    
    #assign_discount_predicate
    data = {"discount_id": 0, "store_id": init_store, 'predicate_builder':("amount_product", 2,-1,0,0)}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/assign_predicate_to_discount', headers=headers, json=data)
    assert response.status_code == 200
    
    #user made purchase
    data = {"store_id": init_store, "product_id": 0, "quantity": 3}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200
  
    data = {"payment_details": default_payment_method, 
            "supply_method": default_supply_method, 
            "address": default_address}
    response = client2.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 200

    #getting the purchase history:
    data = {"user_id": 2}
    headers = {'Authorization': 'Bearer ' + admin_token}
    response = client.get('market/user_purchase_history', headers=headers, json=data)
    assert response.status_code == 200

    
#test 2.6.4.b wrong member credentials:
def test_getting_info_about_purchase_history_of_a_member_wrong_credentials(client2,client3, owner_token, init_store, user_token, guest_token, client1, clean):
    # add discounts:
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store, "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    
    #assign_discount_predicate
    data = {"discount_id": 0, "store_id": init_store ,'predicate_builder':("amount_product", 2,-1,0,0)}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/assign_predicate_to_discount', headers=headers, json=data)
    assert response.status_code == 200
    
    #adding to basket:
    data = {"store_id": init_store, "product_id": 0, "quantity": 3}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)
    
    #checkout:
    data = {"payment_details": default_payment_method,
            "supply_method": default_supply_method,
            "address": default_address}
    response = client2.post('market/checkout', headers=headers, json=data)
    
    #getting the purchase history, wrong credentials:
    data = {"user_id": 69}
    headers = {'Authorization': 'Bearer ' + guest_token}
    response = client3.get('market/user_purchase_history', headers=headers, json=data)
    assert response.status_code == 400

#test 2.6.4.a (in a store)
def test_getting_info_about_purchase_history_of_a_store(client, admin_token, client2, user_token, guest_token, client3, client1, owner_token, init_store, clean):
    # add discounts:
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store, "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    
    #assign_discount_predicate
    data = {"discount_id": 0, "store_id": init_store, 'predicate_builder':("amount_product", 2,-1,0,0)}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/assign_predicate_to_discount', headers=headers, json=data)
    assert response.status_code == 200
    
    #user made purchase
    data = {"store_id": init_store, "product_id": 0, "quantity": 3}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200
        
    data = {"payment_details": default_payment_method, 
            "supply_method": default_supply_method, 
            "address": default_address}
    response = client2.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 200

    #guest made purchase
    data = {"store_id": init_store, "product_id": 0, "quantity": 4}
    headers = {'Authorization': 'Bearer ' + guest_token}
    response = client3.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200

    data = {"payment_details": default_payment_method,
            "supply_method": default_supply_method,
            "address": default_address}
    response = client3.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 200
    
    #getting the purchase history:
    data = {"store_id": init_store}
    headers = {'Authorization': 'Bearer ' + admin_token}
    response = client.get('market/store_purchase_history', headers=headers, json=data)
    assert response.status_code == 200


#test 2.6.4.b (in a store- wrong store credentials) 
def test_getting_info_about_purchase_history_of_a_store_wrong_store_credentials(client, admin_token, client2, user_token, client1, owner_token, init_store, clean):
    # add discounts:
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store, "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    
    #assign_discount_predicate
    data = {"discount_id": 0, "store_id": init_store,'predicate_builder':("amount_product", 2,-1,0,0)}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/assign_predicate_to_discount', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": init_store, "product_id": 0, "quantity": 3}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200

        
    data = {"payment_details": default_payment_method, 
            "supply_method": default_supply_method, 
            "address": default_address}
    response = client2.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 200
    
    #getting the purchase history:
    headers = {'Authorization': 'Bearer ' + admin_token}
    data = {"store_id": 69}
    response = client.get('market/store_purchase_history', headers=headers, json=data)
    assert response.status_code == 400


#test 2.4.13.a: A member is trying to view his purchase history
def test_getting_info_about_purchase_history_of_a_user_in_store(client, admin_token, client2, user_token, init_store, owner_token, client1, clean):
    # add discounts:    
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store, "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    
    #assign_discount_predicate
    data = {"discount_id": 0, "store_id": init_store, 'predicate_builder':("amount_product", 2,-1,0,0)}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/assign_predicate_to_discount', headers=headers, json=data)
    assert response.status_code == 200
    
    #user made purchase
    data = {"store_id": init_store, "product_id": 0, "quantity": 3}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200
  
    data = {"payment_details": default_payment_method, 
            "supply_method": default_supply_method, 
            "address": default_address}
    response = client2.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 200

    #getting the purchase history:
    data = {"user_id":2, "store_id": init_store}
    headers = {'Authorization': 'Bearer ' + admin_token}
    response = client.get('market/user_purchase_history', headers=headers, json=data)
    assert response.status_code == 200
    
#test 2.4.13.b: A member is trying to view his purchase history with wrong credentials
def test_getting_info_about_purchase_history_of_a_user_in_store_wrong_credentials(client, admin_token, client2, user_token, guest_token, client1, owner_token, init_store, clean):
    # add discounts:
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store, "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    
    #assign_discount_predicate
    data = {"discount_id": 0, "store_id":0,'predicate_builder':("amount_product", 2,-1,0,0)}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client1.post('store/assign_predicate_to_discount', headers=headers, json=data)
    assert response.status_code == 200
    
    #adding to basket:
    data = {"store_id": init_store, "product_id": 0, "quantity": 3}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client2.post('user/add_to_basket', headers=headers, json=data)
    
    #checkout:
    data = {"payment_details": default_payment_method,
            "supply_method": default_supply_method,
            "address": default_address}
    response = client2.post('market/checkout', headers=headers, json=data)
    
    #getting the purchase history, wrong credentials:
    data = {"user_id":2, "store_id": init_store}
    headers = {'Authorization': 'Bearer ' + guest_token}
    response = client.get('market/user_purchase_history', headers=headers, json=data)
    assert response.status_code == 400
    

def test_add_payment_method_success(client, admin_token, clean):
    data = {"method_name": "Visa", "config": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    print(response.data)
    assert response.status_code == 200

def test_add_payment_method_failed_missing_data(client, admin_token, clean):
    data = {"method_name": "Visa"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    assert response.status_code == 400

def test_add_payment_method_failed_duplicate_method(client, admin_token, clean):
    data = {"method_name": "bogo", "config": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    assert response.status_code == 400

def test_add_payment_method_failed_not_logged_in(client, token, clean):
    data = {"method_name": "Visa", "config": {"key": "value"}}
    headers = { ' Authorization': 'Bearer ' + token }
    response = client.post('third_party/payment/add', json=data)
    assert response.status_code == 401

def test_edit_payment_method_success(client, admin_token, clean):
    data = {"method_name": "bogo", "editing_data": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 200

def test_edit_payment_method_failed_missing_data(client, admin_token, clean):
    data = {"method_name": "bogo"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 400

def test_edit_payment_method_failed_not_logged_in(client, token, clean):
    data = {"method_name": "bogo", "editing_data": {"key": "value"}}
    headers = { ' Authorization': 'Bearer ' + token }
    response = client.put('third_party/payment/edit', json=data)
    assert response.status_code == 401

def test_edit_payment_method_failed_wrong_name(client, admin_token, clean):
    data = {"method_name": "nothing", "editing_data": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 400

def test_delete_payment_method_success(client, admin_token, clean):
    data = {"method_name": "bogo"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 200

def test_delete_payment_method_failed_missing_data(client, admin_token, clean):
    data = {}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 400

def test_delete_payment_method_failed_not_logged_in(client, token, clean):
    data = {"method_name": "bogo"}
    headers = { ' Authorization': 'Bearer ' + token }
    response = client.delete('third_party/payment/delete', json=data)
    assert response.status_code == 401

def test_delete_payment_method_failed_wrong_name(client, admin_token, clean):
    data = {"method_name": "nothing"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 400

def test_add_supply_method_success(client, admin_token, clean):
    data = {"method_name": "Fedex", "config": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 200

def test_add_supply_method_failed_missing_data(client, admin_token, clean):
    data = {"method_name": "Fedex"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 400

def test_add_supply_method_failed_duplicate_method(client, admin_token, clean):
    data = {"method_name": "bogo", "config": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 400

def test_add_supply_method_failed_not_logged_in(client, token, clean):
    data = {"method_name": "Fedex", "config": {"key": "value"}}
    headers = { ' Authorization': 'Bearer ' + token }
    response = client.post('third_party/delivery/add', json=data)
    assert response.status_code == 401

def test_edit_supply_method_success(client, admin_token, clean):
    data = {"method_name": "bogo", "editing_data": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 200

def test_edit_supply_method_failed_missing_data(client, admin_token, clean):
    data = {"method_name": "bogo"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 400

def test_edit_supply_method_failed_not_logged_in(client, token, clean):
    data = {"method_name": "bogo", "editing_data": {"key": "value"}}
    headers = { ' Authorization': 'Bearer ' + token }
    response = client.put('third_party/delivery/edit', json=data)
    assert response.status_code == 401

def test_edit_supply_method_failed_wrong_name(client, admin_token, clean):
    data = {"method_name": "nothing", "editing_data": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 400

def test_delete_supply_method_success(client, admin_token, clean):
    data = {"method_name": "bogo"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 200

def test_delete_supply_method_failed_missing_data(client, admin_token, clean):
    data = {}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 400

def test_delete_supply_method_failed_not_logged_in(client, token, clean):
    data = {"method_name": "bogo"}
    headers = { ' Authorization': 'Bearer ' + token }
    response = client.delete('third_party/delivery/delete', json=data)
    assert response.status_code == 401

def test_delete_supply_method_failed_wrong_name(client, admin_token, clean):
    data = {"method_name": "nothing"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 400

# NEEDS TO BE IMPLEMENTED?
def test_cancel_membership_success(app, clean):
    pass


