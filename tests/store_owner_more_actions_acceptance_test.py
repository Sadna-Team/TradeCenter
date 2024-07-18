#write more acceptance tests for store owner actions
from datetime import datetime
import pytest
from backend import clean_data
from backend.app_factory import create_app_instance
import json

# --------------------------------------------------------------------------------

register_credentials1= { 
        'username': 'test',
        'email': 'testing@gmail.com',
        'password': 'test',
        'address': 'randomstreet 34th',
        'city': 'arkham',
        'state': 'Utopia',
        'country': 'Wakanda',
        'zip_code': '12345',
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1238567' }


default_payment_method = {'payment method': 'bogo'}

default_supply_method = "bogo"

default_address = {'address': 'randomstreet 34th', 
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
def client11(app):
    return app.test_client()

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
def clean11(app):
    yield
    with app.app_context():
        from backend.database import clear_database
        clear_database()
        clean_data()
    
@pytest.fixture
def client12(app):
    return app.test_client()

@pytest.fixture
def client22(app):
    return app.test_client()

@pytest.fixture
def client33(app):
    return app.test_client()

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
    manager_credentials['username'] = 'store_owner_from_new_jerzey'
    data = {"register_credentials": manager_credentials}
    response = client12.post('auth/register', headers=headers, json=data)

    data = { "username": "store_owner_from_new_jerzey", "password": "test" }
    response = client12.post('auth/login', json=data, headers=headers)
    data = json.loads(response.data)
    return data['token']




@pytest.fixture
def user_token(client22, token22):
    headers = { 'Authorization': 'Bearer ' + token22 }
    user_credentials = register_credentials1.copy()
    data = {"register_credentials": register_credentials1}
    
    response = client22.post('auth/register', headers=headers, json=data)
    data = { "username": "test", "password": "test" }
    response = client22.post('auth/login', json=data, headers=headers)
    data = json.loads(response.data)
    return data['token']




@pytest.fixture
def init_store(client12, owner_token11, client11, admin_token):
    data = {'store_name': 'test_store', 'address': 'randomstreet 34th', 'city': 'arkham', 'state': 'Utopia', 'country': 'Wakanda', 'zip_code': '12345'}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_store', headers=headers, json=data)

    store_id = json.loads(response.data)['storeId']

    data = {"store_id": store_id, 
            "product_name": "test_product", 
            "description": "test_description",
            "price": 10.0,
            "weight": 1.0,
            "tags": ["tag1", "tag2"],
            "amount": 10}
    
    response = client12.post('store/add_product', headers=headers, json=data)
    product_id1 = json.loads(response.data)['product_id']
    data = {"store_id": store_id, 
        "product_name": "funny", 
        "description": "test_description",
        "price": 10.0,
        "weight": 1.0,
        "tags": ["tag1", "tag2"],
        "amount": 10}

    response = client12.post('store/add_product', headers=headers, json=data)
    product_id2 = json.loads(response.data)['product_id']
    headers = {'Authorization': 'Bearer ' + admin_token}
    
    data = {"category_name": "test_category"}

    response = client11.post('store/add_category', headers=headers, json=data)
    category_id = json.loads(response.data)['category_id']

    data = {'store_id': store_id, 'product_id1': product_id1, 'product_id2': product_id2, 'category_id': category_id}
    return data
    
    

@pytest.fixture
def init_store2(client12, owner_token11):
    data = {'store_name': 'test_store', 'address': 'randomstreet 34th', 'city': 'arkham', 'state': 'Utopia', 'country': 'Wakanda', 'zip_code': '12345'}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_store', headers=headers, json=data)
    store_id = json.loads(response.data)['storeId']
    data = {"store_id": store_id, 
            "product_name": "test_product", 
            "description": "test_description",
            "price": 10.0,
            "weight": 1.0,
            "tags": ["tag1", "tag2"],
            "amount": 10}
    
    response = client12.post('store/add_product', headers=headers, json=data)
    product_id = json.loads(response.data)['product_id']
    return {'store_id': store_id, 'product_id': product_id}

#test 2.6.4.a (in a store)
def test_getting_info_about_purchase_history_of_a_store(app, clean11,client12, owner_token11, client22, client33, user_token,guest_token10, init_store):
    #user made purchase
    data = {"store_id": init_store['store_id'], "product_id": init_store['product_id1'], "quantity": 3}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client22.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200
        
    data = {"payment_details": default_payment_method, 
            "supply_method": default_supply_method, 
            "address": default_address}
    response = client22.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 200

    #getting the purchase history:
    data = {"store_id": init_store['store_id']}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.get('market/store_purchase_history', headers=headers, json=data)
    assert response.status_code == 200
    
    
    # WRONG CREDENTIALS:
    data = {"store_id": init_store['store_id']}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.get('market/store_purchase_history', headers=headers, json=data)
    assert response.status_code == 400

    
#test 2.____
def test_add_discount(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    
def test_add_discount_no_permission(app, clean11,client33, guest_token10, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 400
    
def test_add_discount_wrong_store(app, clean11, client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id']+1, "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 400
    
def test_add_discount_wrong_percentage(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 1.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 400
    
def test_add_discount_wrong_dates(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2020,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 400
    
def test_add_discount_wrong_dates2(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2023,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 400
    
    
def test_add_discount_invalid_store_id(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id']+ 69, "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 400
    
def test_add_discount_invalid_product_id(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": init_store['product_id1']+69, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 400
    
def test_add_product_discount(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": init_store['product_id1'], "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200

def test_add_category_discount(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": init_store['category_id'], "applied_to_sub": False}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    

def test_add_discount_invalid_category_id(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": init_store['category_id']+69, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 400
        
    
def test_add_discount_invalid_start_date(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2020,1,23).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 400
    
    

    
def test_remove_discount(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id = json.loads(response.data)['discount_id']
    data = {"discount_id": discount_id, "store_id": init_store['store_id']}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/remove_discount', headers=headers, json=data)
    assert response.status_code == 200
    
    

def test_remove_discount_invalid_store_id(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id = json.loads(response.data)['discount_id']

    data = {"discount_id": discount_id, "store_id": init_store['store_id']+69}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/remove_discount', headers=headers, json=data)
    assert response.status_code == 400
    
    
def test_remove_discount_no_permission(app, clean11,client12, client33, guest_token10, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id = json.loads(response.data)['discount_id']
    data = {"discount_id": discount_id, "store_id": init_store['store_id']}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/remove_discount', headers=headers, json=data)
    assert response.status_code == 400
    
def test_remove_discount_no_discount(app, clean11,client12, owner_token11, init_store):
    data = {"discount_id": 69, "store_id": init_store['store_id']}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/remove_discount', headers=headers, json=data)
    assert response.status_code == 400
    
    
def test_create_logical_composite_discount(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']
    data = {"description": 'hara2', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.2, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id2 = json.loads(response.data)['discount_id']
    
    data = {"description": "hi", "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "discount_id1": discount_id1, "discount_id2": discount_id2, "type_of_composite": 1, "store_id": init_store['store_id']}
    response = client12.post('store/create_logical_composite', headers=headers, json=data)
    assert response.status_code == 200
    
    

def test_create_logical_composite_discount_invalid_store_id(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store["store_id"], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']
    
    data = {"description": 'hara2', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.2, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id2 = json.loads(response.data)['discount_id']
    
    data = {"description": "hi", "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "discount_id1": discount_id1, "discount_id2": discount_id2, "type_of_composite": 1, "store_id": init_store['store_id']+67}
    response = client12.post('store/create_logical_composite', headers=headers, json=data)
    assert response.status_code == 400
    
def test_create_logical_composite_discount_no_permission(app, clean11,client12,owner_token11, client33, guest_token10, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']
    data = {"description": 'hara2', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.2, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id2 = json.loads(response.data)['discount_id']
    
    data = {"description": "hi", "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "discount_id1": discount_id1, "discount_id2": discount_id2, "type_of_composite": 1, "store_id": init_store['store_id']}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/create_logical_composite', headers=headers, json=data)
    assert response.status_code == 400
    
def test_create_logical_composite_discount_no_discounts(app, clean11,client12, owner_token11, init_store):
    data = {"description": "hi", "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "discount_id1": 69, "discount_id2": 420, "type_of_composite": 1, "store_id": init_store['store_id']}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/create_logical_composite', headers=headers, json=data)
    assert response.status_code == 400
    
    
def test_create_numerical_composite_discount(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']
    
    data = {"description": 'hara2', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.2, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id2 = json.loads(response.data)['discount_id']
    
    data = {"description": "hi", "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "discount_ids": [discount_id1,discount_id2], "type_of_composite": 1, "store_id": init_store['store_id']}
    response = client12.post('store/create_numerical_composite', headers=headers, json=data)
    assert response.status_code == 200
    

def test_create_numerical_composite_discount_invalid_store_id(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']
    
    data = {"description": 'hara2', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.2, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id2 = json.loads(response.data)['discount_id']
    
    
    data = {"description": "hi", "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "discount_ids": [discount_id1,discount_id2], "type_of_composite": 1, "store_id": 77466}
    response = client12.post('store/create_numerical_composite', headers=headers, json=data)
    assert response.status_code == 400
    
def test_create_numerical_composite_discount_no_permission(app, clean11,client33, guest_token10, client12 ,owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']

    
    
    data = {"description": 'hara2', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.2, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id2 = json.loads(response.data)['discount_id']

    
    data = {"description": "hi", "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "discount_ids": [discount_id1,discount_id2], "type_of_composite": 1, "store_id": init_store['store_id']}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/create_numerical_composite', headers=headers, json=data)
    assert response.status_code == 400
    
def test_create_discount_no_discounts(app, clean11,client12, owner_token11, init_store):
    data = {"description": "hi", "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "discount_ids": [99888,92776], "type_of_composite": 1, "store_id": init_store['store_id']}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/create_numerical_composite', headers=headers, json=data)
    assert response.status_code == 400
    
    
    
def test_assign_predicate_to_discount(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']

    
    data = {"discount_id": discount_id1, "store_id": init_store['store_id'], 'predicate_builder':("amount_product", 2,-1,init_store['product_id1'],init_store['store_id'])}
    response = client12.post('store/assign_predicate_to_discount', headers=headers, json=data)
    assert response.status_code == 200
    
def test_assign_predicate_to_discount_invalid_store_id(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']

    
    data = {"discount_id": discount_id1, "store_id": 44332, 'predicate_builder':("amount_product", 2,-1,init_store['product_id1'],init_store['store_id'])}
    response = client12.post('store/assign_predicate_to_discount', headers=headers, json=data)
    assert response.status_code == 400
    
def test_assign_predicate_to_discount_no_permission(app, clean11,client33, guest_token10,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']

    
    data = {"discount_id": discount_id1, "store_id": init_store['store_id'] ,'predicate_builder':("amount_product", 2,init_store['product_id1'],init_store['store_id'])}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/assign_predicate_to_discount', headers=headers, json=data)
    assert response.status_code == 400
    
def test_assign_predicate_to_discount_no_discount(app, clean11,client12, owner_token11, init_store):
    data = {"discount_id": 99988, "store_id": init_store['store_id'], 'predicate_builder':("amount_product", 2,init_store['product_id1'],init_store['store_id'])}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/assign_predicate_to_discount', headers=headers, json=data)
    assert response.status_code == 400
    
def test_assign_predicate_to_discount_wrong_predicate(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']

        
    data = {"discount_id": discount_id1, "store_id": init_store['store_id'], 'predicate_builder':("random_predicate", 2,0,0)}
    response = client12.post('store/assign_predicate_to_discount', headers=headers, json=data)
    assert response.status_code == 400
    

    
def test_change_discount_percentage(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']

    
    data = {"discount_id": discount_id1, "store_id": init_store['store_id'], "percentage": 0.5}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/change_discount_percentage', headers=headers, json=data)
    assert response.status_code == 200
    

def test_change_discount_percentage_invalid_store_id(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']

    data = {"discount_id": discount_id1, "store_id": 4433, "percentage": 0.5}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/change_discount_percentage', headers=headers, json=data)
    assert response.status_code == 400
    
def test_change_discount_percentage_no_discount(app, clean11,client12, owner_token11, init_store):
    data = {"discount_id": 33333333,"store_id": init_store['store_id'] ,"percentage": 0.5}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/change_discount_percentage', headers=headers, json=data)
    assert response.status_code == 400
    
def test_change_discount_invalid_percentage(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']

    
    data = {"discount_id": discount_id1,"store_id": init_store['store_id'], "percentage": 1.5}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/change_discount_percentage', headers=headers, json=data)
    assert response.status_code == 400
    
    
def test_change_discount_percentage_no_permission(app, clean11,client33, guest_token10, client12,owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']

    
    data = {"discount_id": discount_id1, "store_id": init_store['store_id'], "percentage": 0.5}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/change_discount_percentage', headers=headers, json=data)
    assert response.status_code == 400
    
def test_change_discount_description(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']

    
    data = {"discount_id": discount_id1, "store_id": init_store['store_id'], "description": "new_description"}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/change_discount_description', headers=headers, json=data)
    assert response.status_code == 200
    

def test_change_discount_description_invalid_store_id(app, clean11,client12, owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": 66554, "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200
    discount_id1 = json.loads(response.data)['discount_id']

    
    data = {"discount_id": discount_id1, "store_id": init_store['store_id'], "description": "new_description"}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/change_discount_description', headers=headers, json=data)
    assert response.status_code == 400    

def test_change_discount_description_no_discount(app, clean11,client12, owner_token11, init_store):
    data = {"discount_id": 22222222, "store_id": init_store['store_id'], "description": "new_description"}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/change_discount_description', headers=headers, json=data)
    assert response.status_code == 400

    
    
def test_change_discount_description_no_permission(app, clean11,client33, guest_token10,client12,owner_token11, init_store):
    data = {"description": 'hara', "start_date": datetime(2023,1,23).strftime('%Y-%m-%d'), "end_date": datetime(2040,1,1).strftime('%Y-%m-%d'), "percentage": 0.1, "store_id": init_store['store_id'], "product_id": None, "category_id": None, "applied_to_sub": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_discount', headers=headers, json=data)
    assert response.status_code == 200   
    discount_id1 = json.loads(response.data)['discount_id']

   
    data = {"discount_id": discount_id1, "store_id": init_store['store_id'],"description": "new_description"}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/change_discount_description', headers=headers, json=data)
    assert response.status_code == 400
 



def test_add_purchase_policy(app, clean11,client12, init_store, owner_token11):
    data = {"store_id": init_store['store_id'], "policy_name": 'name', "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
        

#invalid_store_id
def test_add_purchase_policy_invalid_store_id(app, clean11,client12, init_store, owner_token11):
    data = {"store_id": 88877766, "policy_name": 'name', "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    

#invalid_policy_name
def test_add_purchase_policy_policy_missing(app, clean11,client12, init_store, owner_token11):
    data = {"store_id": init_store['store_id'],"policy_name": '', "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
    
def test_add_purchase_policy_no_permission(app, clean11,client33, guest_token10, init_store):
    data = {"store_id": init_store['store_id'], "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
def test_remove_purchase_policy(app, clean11,client12, init_store, owner_token11):
    data = {"store_id": init_store['store_id'], "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    policy_id1 = json.loads(response.data)['policy_id']
    
    
    data = {"store_id": init_store['store_id'], "policy_id": policy_id1}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/remove_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200    
    
def test_remove_purchase_policy_invalid_store_id (app, clean11,client12, init_store, owner_token11):
    data = {"store_id": init_store['store_id'], "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    policy_id1 = json.loads(response.data)['policy_id']

    
    data = {"store_id": 9999999, "policy_id": policy_id1}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/remove_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    


def test_remove_purchase_policy_no_permission(app, clean11,client12, client33,guest_token10, owner_token11, init_store):
    data = {"store_id": init_store['store_id'], "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    policy_id1 = json.loads(response.data)['policy_id']

    
    
    data = {"store_id": init_store['store_id'], "policy_id": policy_id1}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/remove_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
def test_create_composite_purchase_policy(app, clean11,client12, init_store, owner_token11):
    data = {"store_id": init_store['store_id'], "policy_name": "leaf1", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    policy_id1 = json.loads(response.data)['policy_id']

    
    data = {"store_id": init_store['store_id'], "policy_name": "leaf2", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    policy_id2 = json.loads(response.data)['policy_id']

    
    data = {"store_id": init_store['store_id'], "policy_name": "name", "policy_id1": policy_id1 , "policy_id2": policy_id2, "type_of_composite": 1}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/create_composite_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
def test_create_composite_purchase_policy_no_permission(app, clean11,client12, client33,guest_token10, owner_token11, init_store):
    data = {"store_id": init_store['store_id'], "policy_name": "leaf1", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    policy_id1 = json.loads(response.data)['policy_id']

    
    data = {"store_id": init_store['store_id'], "policy_name": "leaf2", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    policy_id2 = json.loads(response.data)['policy_id']

    
    data = {"store_id": init_store['store_id'], "policy_name": "name", "policy_id1": policy_id1 , "policy_id2": policy_id2, "type_of_composite": 1}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/create_composite_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
def test_create_composite_purchase_policy_invalid_left_policy_id(app, clean11,client12, init_store, owner_token11):
    data = {"store_id": init_store['store_id'], "policy_name": "leaf1", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": init_store['store_id'], "policy_name": "leaf2", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    policy_id2 = json.loads(response.data)['policy_id']

    
    data = {"store_id": init_store['store_id'], "policy_name": "name", "policy_id1": 5667 , "policy_id2": policy_id2, "type_of_composite": 1}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/create_composite_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
def test_create_composite_purchase_policy_invalid_right_policy_id(app, clean11,client12, init_store, owner_token11):
    data = {"store_id": init_store['store_id'], "policy_name": "leaf1", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    policy_id1 = json.loads(response.data)['policy_id']

    
    data = {"store_id": init_store['store_id'], "policy_name": "leaf2", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    policy_id2 = json.loads(response.data)['policy_id']

    
    data = {"store_id": init_store['store_id'], "policy_name": "name", "policy_id1": policy_id1 , "policy_id2": 55666, "type_of_composite": 1}
    headers = {'Authorization': 'Bearer ' + owner_token11}  
    response = client12.post('store/create_composite_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
    
    
def test_assign_predicate_to_purchase_policy(app, clean11,client12, init_store, owner_token11):
    data = {"store_id": init_store['store_id'], "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    policy_id1 = json.loads(response.data)['policy_id']

    
    data = {"store_id": init_store['store_id'], "policy_id": policy_id1, 'predicate_builder': ("amount_product", 2, -1, init_store['product_id1'],init_store['store_id'])}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/assign_predicate_to_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
def test_assign_predicate_to_purchase_policy_no_permission(app, clean11,client12, client33,guest_token10, owner_token11, init_store):
    data = {"store_id": init_store['store_id'], "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    policy_id1 = json.loads(response.data)['policy_id']

    
    data = {"store_id": init_store['store_id'], "policy_id": policy_id1, 'predicate_builder': ("amount_product", 2,-1, init_store['product_id1'],init_store['store_id'])}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/assign_predicate_to_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
def test_assign_predicate_to_purchase_policy_invalid_policy_id(app, clean11,client12, init_store, owner_token11):
    data = {"store_id": init_store['store_id'], "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    policy_id1 = json.loads(response.data)['policy_id']

    
    data = {"store_id": init_store['store_id'], "policy_id": 555566, 'predicate_builder': ("amount_product", 2,-1,init_store['product_id1'],init_store['store_id'])}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/assign_predicate_to_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    

#bid tests:


'''
def test_user_bid_offer(client12, init_store, user_token, clean11):
    data = {"proposed_price": 5, "store_id": 0, "product_id": 0}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client12.post('market/user_bid_offer', headers=headers, json=data)
    assert response.status_code == 200


def test_store_worker_accept_bid(client12, init_store, owner_token11, user_token, clean11):
    #the user makes a bid offer
    data = {"proposed_price": 5, "store_id": 0, "product_id": 0}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client12.post('market/user_bid_offer', headers=headers, json=data)
    assert response.status_code == 200

    #the owner accepts the bid
    data = {"store_id": 0, "bid_id": 0}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('market/store_worker_accept_bid', headers=headers, json=data)
    assert response.status_code == 200


def test_store_worker_decline_bid(client12, init_store, owner_token11, user_token, clean11):
    #the user makes a bid offer
    data = {"proposed_price": 5, "store_id": 0, "product_id": 0}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client12.post('market/user_bid_offer', headers=headers, json=data)
    assert response.status_code == 200

    #the iwner declines the bid
    data = {"store_id": 0, "bid_id": 0}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('market/store_worker_decline_bid', headers=headers, json=data)
    assert response.status_code == 200


def test_store_worker_counter_bid(client12, init_store, owner_token11, user_token, clean11):
    #the user makes a bid offer
    data = {"proposed_price": 5, "store_id": 0, "product_id": 0}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client12.post('market/user_bid_offer', headers=headers, json=data)
    assert response.status_code == 200

    #the uwner makes a counter bid
    data = {"store_id": 0, "bid_id": 0, "proposed_price": 6}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('market/store_worker_counter_bid', headers=headers, json=data)
    assert response.status_code == 200


def test_user_counter_bid_accept(client12, init_store, owner_token11, user_token, clean11):
    #the user makes a bid offer
    data = {"proposed_price": 5, "store_id": 0, "product_id": 0}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client12.post('market/user_bid_offer', headers=headers, json=data)
    assert response.status_code == 200

    #the owner makes a counter bid
    data = {"store_id": 0, "bid_id": 0, "proposed_price": 6}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('market/store_worker_counter_bid', headers=headers, json=data)
    assert response.status_code == 200

    #the user accepts the counter bid
    data = {"bid_id": 0}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client12.post('market/user_counter_bid_accept', headers=headers, json=data)
    assert response.status_code == 200

def test_user_counter_bid_decline(client12, init_store, owner_token11, user_token, clean11):
    #the user makes a bid offer
    data = {"proposed_price": 5, "store_id": 0, "product_id": 0}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client12.post('market/user_bid_offer', headers=headers, json=data)
    assert response.status_code == 200
    bid_id = response.get_json().get('bid_id', 0)

    #the owner makes a counter bid
    data = {"store_id": 0, "bid_id": bid_id, "proposed_price": 6}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('market/store_worker_counter_bid', headers=headers, json=data)
    assert response.status_code == 200

    #the user declines the counter bid
    data = {"bid_id": bid_id}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client12.post('market/user_counter_bid_decline', headers=headers, json=data)
    assert response.status_code == 200


def test_user_counter_bid(client12, init_store, owner_token11, user_token, clean11):
    #user makes a bid offer
    data = {"proposed_price": 5, "store_id": 0, "product_id": 0}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client12.post('market/user_bid_offer', headers=headers, json=data)
    assert response.status_code == 200

    #owner makes a counter bid
    data = {"store_id": 0, "bid_id": 0, "proposed_price": 6}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('market/store_worker_counter_bid', headers=headers, json=data)
    assert response.status_code == 200

    #user makes another counter bid
    data = {"bid_id": 0, "proposed_price": 7}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client12.post('market/user_counter_bid', headers=headers, json=data)
    assert response.status_code == 200

def test_show_user_bids(client12, user_token, init_store, clean11):
    #the user makes a bid offer
    data = {"proposed_price": 5, "store_id": 0, "product_id": 0}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client12.post('market/user_bid_offer', headers=headers, json=data)
    assert response.status_code == 200

    #the user checks their bids
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client12.get('market/show_user_bids', headers=headers, json={"user_id": 0})
    assert response.status_code == 200



def test_show_store_bids(client12, owner_token11, user_token, init_store, clean11):
    data = {"proposed_price": 5, "store_id": 0, "product_id": 0}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client12.post('market/user_bid_offer', headers=headers, json=data)
    assert response.status_code == 200

    data = {"store_id": 0}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.get('market/show_store_bids', headers=headers, json=data)
    assert response.status_code == 200
'''


