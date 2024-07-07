#write more acceptance tests for store owner actions
from datetime import datetime
import pytest
from backend import create_app, clean_data
import json
from backend import socketio_manager

# --------------------------------------------------------------------------------

register_credentials1= { 
        'username': 'testing',
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



@pytest.fixture
def app1():
    app1 = create_app(mode='testing')
    return app1

@pytest.fixture
def client11(app1):
    return app1.test_client()

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
def clean11():
    yield
    clean_data()
    
@pytest.fixture
def client12(app1):
    return app1.test_client()

@pytest.fixture
def client22(app1):
    return app1.test_client()

@pytest.fixture
def client33(app1):
    return app1.test_client()

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
    manager_credentials['username'] = 'store_owner_new'
    data = {"register_credentials": manager_credentials}
    response = client12.post('auth/register', headers=headers, json=data)

    data = { "username": "store_owner_new", "password": "test" }
    response = client12.post('auth/login', json=data, headers=headers)
    data = json.loads(response.data)
    return data['token']




@pytest.fixture
def user_token(client22, token22):
    headers = { 'Authorization': 'Bearer ' + token22 }
    data = {"register_credentials": register_credentials1}
    response = client22.post('auth/register', headers=headers, json=data)
    data = { "username": "testing", "password": "test" }
    response = client22.post('auth/login', json=data, headers=headers)
    data = json.loads(response.data)
    return data['token']




@pytest.fixture
def init_store(client12, owner_token11):
    data = {'store_name': 'test_store', 'address': 'randomstreet 34th', 'city': 'arkham', 'state': 'Utopia', 'country': 'Wakanda', 'zip_code': '12345'}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_store', headers=headers, json=data)

    data = {"store_id": 0, 
            "product_name": "test_product", 
            "description": "test_description",
            "price": 10.0,
            "weight": 1.0,
            "tags": ["tag1", "tag2"],
            "amount": 10}
    
    response = client12.post('store/add_product', headers=headers, json=data)

    data = {"store_id": 0, 
        "product_name": "funny", 
        "description": "test_description",
        "price": 10.0,
        "weight": 1.0,
        "tags": ["tag1", "tag2"],
        "amount": 10}

    response = client12.post('store/add_product', headers=headers, json=data)
    
    

@pytest.fixture
def init_store2(client12, owner_token11):
    data = {'store_name': 'test_store', 'address': 'randomstreet 34th', 'city': 'arkham', 'state': 'Utopia', 'country': 'Wakanda', 'zip_code': '12345'}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_store', headers=headers, json=data)

    data = {"store_id": 1, 
            "product_name": "test_product", 
            "description": "test_description",
            "price": 10.0,
            "weight": 1.0,
            "tags": ["tag1", "tag2"],
            "amount": 10}
    
    response = client12.post('store/add_product', headers=headers, json=data)

#test 2.6.4.a (in a store)
def test_getting_info_about_purchase_history_of_a_store(client12, owner_token11, client22, client33, user_token,guest_token10, init_store, clean11):
    #user made purchase
    data = {"store_id": 0, "product_id": 0, "quantity": 3}
    headers = {'Authorization': 'Bearer ' + user_token}
    response = client22.post('user/add_to_basket', headers=headers, json=data)
    assert response.status_code == 200
        
    data = {"payment_details": default_payment_method, 
            "supply_method": default_supply_method, 
            "address": default_address}
    response = client22.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 200

    #getting the purchase history:
    data = {"store_id": 0}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.get('market/store_purchase_history', headers=headers, json=data)
    assert response.status_code == 200
    
    
    # WRONG CREDENTIALS:
    data = {"store_id": 0}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.get('market/store_purchase_history', headers=headers, json=data)
    assert response.status_code == 400




def test_add_purchase_policy(client12, init_store, owner_token11, clean11):
    data = {"store_id": 0, "policy_name": 'name', "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
        

#invalid_store_id
def test_add_purchase_policy_invalid_store_id(client12, init_store, owner_token11, clean11):
    data = {"store_id": 1, "policy_name": 'name', "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    

#invalid_policy_name
def test_add_purchase_policy_policy_missing(client12, init_store, owner_token11, clean11):
    data = {"store_id": 0,"policy_name": '', "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
    
def test_add_purchase_policy_no_permission(client33, guest_token10, init_store, clean11):
    data = {"store_id": 0, "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
def test_remove_purchase_policy(client12, init_store, owner_token11, clean11):
    data = {"store_id": 0, "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_id": 0}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/remove_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200    
    
def test_remove_purchase_policy_invalid_store_id (client12, init_store, owner_token11, clean11):
    data = {"store_id": 0, "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 100, "policy_id": 0}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/remove_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    


def test_remove_purchase_policy_no_permission(client12, client33,guest_token10, owner_token11, init_store, clean11):
    data = {"store_id": 0, "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    
    data = {"store_id": 0, "policy_id": 0}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/remove_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
def test_create_composite_purchase_policy(client12, init_store, owner_token11, clean11):
    data = {"store_id": 0, "policy_name": "leaf1", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_name": "leaf2", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_name": "name", "policy_id1": 0 , "policy_id2": 1, "type_of_composite": 1}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/create_composite_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
def test_create_composite_purchase_policy_no_permission(client12, client33,guest_token10, owner_token11, init_store, clean11):
    data = {"store_id": 0, "policy_name": "leaf1", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_name": "leaf2", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_name": "name", "policy_id1": 0 , "policy_id2": 1, "type_of_composite": 1}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/create_composite_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
def test_create_composite_purchase_policy_invalid_left_policy_id(client12, init_store, owner_token11, clean11):
    data = {"store_id": 0, "policy_name": "leaf1", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_name": "leaf2", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_name": "name", "policy_id1": 100 , "policy_id2": 1, "type_of_composite": 1}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/create_composite_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
def test_create_composite_purchase_policy_invalid_right_policy_id(client12, init_store, owner_token11, clean11):
    data = {"store_id": 0, "policy_name": "leaf1", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_name": "leaf2", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_name": "name", "policy_id1": 0 , "policy_id2": 100, "type_of_composite": 1}
    headers = {'Authorization': 'Bearer ' + owner_token11}  
    response = client12.post('store/create_composite_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
    
    
def test_assign_predicate_to_purchase_policy(client12, init_store, owner_token11, clean11):
    data = {"store_id": 0, "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_id": 0, 'predicate_builder': ("amount_product", 2, -1, 0,0)}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/assign_predicate_to_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
def test_assign_predicate_to_purchase_policy_no_permission(client12, client33,guest_token10, owner_token11, init_store, clean11):
    data = {"store_id": 0, "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_id": 0, 'predicate_builder': ("amount_product", 2,-1, 0,0)}
    headers = {'Authorization': 'Bearer ' + guest_token10}
    response = client33.post('store/assign_predicate_to_purchase_policy', headers=headers, json=data)
    assert response.status_code == 400
    
def test_assign_predicate_to_purchase_policy_invalid_policy_id(client12, init_store, owner_token11, clean11):
    data = {"store_id": 0, "policy_name": "name", "category_id": None, "product_id": None}
    headers = {'Authorization': 'Bearer ' + owner_token11}
    response = client12.post('store/add_purchase_policy', headers=headers, json=data)
    assert response.status_code == 200
    
    data = {"store_id": 0, "policy_id": 100, 'predicate_builder': ("amount_product", 2,-1,0,0)}
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


