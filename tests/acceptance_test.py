import pytest
from backend import create_app, clean_data

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def clean():
    yield
    clean_data()

@pytest.fixture
def reset_app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def guest(client):
    response = client.get('/auth/')
    data = response.get_json()
    token = data['token']
    return token

@pytest.fixture
def register_user(client, guest):
    register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567' }
    data = {
        'register_credentials': register_credentials
    }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/register', headers=headers, json=data)
    return guest

@pytest.fixture
def login_user(client, register_user):
    data = {
            'username': 'test',
            'password': 'test'
        }
    headers = {
        'Authorization': 'Bearer ' + register_user
    }
    response = client.post('auth/login', headers=headers, json=data)
    data = response.get_json()
    token = data['token']
    return token

@pytest.fixture
def login_system_manager(client, guest):
    data = {
            'username': 'admin',
            'password': 'admin'
    }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/login', headers=headers, json=data)
    data = response.get_json()
    token = data['token']
    return token


def test_home_page(client, clean):
    response = client.get('/auth/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data


def test_register(client, guest, clean):
    register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567' }
    data = {
        'register_credentials': register_credentials
    }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/register', headers=headers, json=data)
    assert response.status_code == 201
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'User registered successfully - great success'

def test_register_fail_duplicate_user(client, register_user, clean):
    
    register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567' }
    data = {
        'register_credentials': register_credentials
    }
    headers = {
        'Authorization': 'Bearer ' + register_user
    }

    response = client.post('auth/register', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Username already exists'

def test_register_fail_missing_data(client, guest, clean):
    register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,}
    data = {
        'register_credentials': register_credentials
    }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/register', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Some credentials are missing'

def test_register_fail_missing_token(client, clean):
    register_credentials = { 
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567' }
    data = {
        'register_credentials': register_credentials
    }
    response = client.post('auth/register', json=data)
    assert response.status_code == 401


def test_login(client, register_user, clean):
    data = {
            'username': 'test',
            'password': 'test'
        }
    headers = {
        'Authorization': 'Bearer ' + register_user
        }
    response = client.post('auth/login', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert 'message' in data
    assert data['message'] == 'OK'

def test_login_fail_invalid_credentials(client, register_user, clean):
    data = {
            'username': 'test',
            'password': 'wrong_password'
        }
    headers = {
        'Authorization': 'Bearer ' + register_user
    }
    response = client.post('auth/login', headers=headers, json=data)
    assert response.status_code == 400

def test_login_fail_already_logged_in(client, guest, login_user, clean):
    response = client.get('/auth/')
    data = response.get_json()
    guest = data['token']
    
    data = {
            'username': 'test',
            'password': 'test'
        }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/login', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is already logged in'


def test_login_fail_missing_data(client, guest, clean):
    data = {
            'username': 'test',
        }
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/login', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'Missing username or password'

def test_login_fail_missing_token(client, clean):
    data = {
            'username': 'test',
            'password': 'test'
        }
    response = client.post('auth/login', json=data)
    assert response.status_code == 401

def test_logout(client, login_user, clean):
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('auth/logout', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'User logged out successfully'

def test_logout_fail_missing_token(client, clean):
    response = client.post('auth/logout')
    assert response.status_code == 401

def test_logout_fail_not_logged_in(app, client, guest, clean):
    headers = {
        'Authorization': 'Bearer ' + guest
    }
    response = client.post('auth/logout', headers=headers)
    assert response.status_code == 400

def test_add_payment_service(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
        'config': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Third party payment service added successfully'

def test_add_payment_service_fail_duplicate_key(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
        'config': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'payment method already supported'

def test_add_payment_service_fail_missing_data(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    assert response.status_code == 400

def test_add_payment_service_fail_missing_token(client, clean):
    data = {
        'method_name': 'test',
        'config': {'test': 'test'}
    }
    response = client.post('third_party/payment/add', json=data)
    assert response.status_code == 401

def test_add_payment_service_fail_not_system_manager(client, login_user, clean):
    data = {
        'method_name': 'test',
        'config': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is not a system manager'

def test_edit_payment_service(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
        'editing_data': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Third party payment service edited successfully'

def test_edit_payment_service_fail_missing_data(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 400

def test_edit_payment_service_fail_no_such_key(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
        'editing_data': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'payment method not supported'

def test_edit_payment_service_fail_missing_token(client, clean):
    data = {
        'method_name': 'bogo',
        'editing_data': {'test': 'test'}
    }
    response = client.put('third_party/payment/edit', json=data)
    assert response.status_code == 401

def test_edit_payment_service_fail_not_system_manager(client, login_user, clean):
    data = {
        'method_name': 'bogo',
        'editing_data': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is not a system manager'

def test_delete_payment_service(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Third party payment service deleted successfully'

def test_delete_payment_service_fail_missing_data(client, login_system_manager, clean):
    data = {}
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 400

def test_delete_payment_service_fail_no_such_key(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'payment method not supported'

def test_delete_payment_service_fail_missing_token(client, clean):
    data = {
        'method_name': 'bogo',
    }
    response = client.delete('third_party/payment/delete', json=data)
    assert response.status_code == 401

def test_delete_payment_service_fail_not_system_manager(client, login_user, clean):
    data = {
        'method_name': 'bogo',
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is not a system manager'

def test_add_supply_service(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
        'config': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Third party delivery service added successfully'

def test_add_supply_service_fail_duplicate_key(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
        'config': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'supply method already supported'

def test_add_supply_service_fail_missing_data(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 400

def test_add_supply_service_fail_missing_token(client, clean):
    data = {
        'method_name': 'test',
        'config': {'test': 'test'}
    }
    response = client.post('third_party/delivery/add', json=data)
    assert response.status_code == 401

def test_add_supply_service_fail_not_system_manager(client, login_user, clean):
    data = {
        'method_name': 'test',
        'config': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is not a system manager'

def test_edit_supply_service(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
        'editing_data': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Third party delivery service edited successfully'

def test_edit_supply_service_fail_missing_data(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 400

def test_edit_supply_service_fail_no_such_key(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
        'editing_data': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'supply method not supported'

def test_edit_supply_service_fail_missing_token(client, clean):
    data = {
        'method_name': 'bogo',
        'editing_data': {'test': 'test'}
    }
    response = client.put('third_party/delivery/edit', json=data)
    assert response.status_code == 401

def test_edit_supply_service_fail_not_system_manager(client, login_user, clean):
    data = {
        'method_name': 'bogo',
        'editing_data': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is not a system manager'

def test_delete_supply_service(client, login_system_manager, clean):
    data = {
        'method_name': 'bogo',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'Third party delivery service deleted successfully'

def test_delete_supply_service_fail_missing_data(client, login_system_manager, clean):
    data = {}
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 400

def test_delete_supply_service_fail_no_such_key(client, login_system_manager, clean):
    data = {
        'method_name': 'test',
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager
    }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'supply method not supported'

def test_delete_supply_service_fail_missing_token(client, clean):
    data = {
        'method_name': 'bogo',
    }
    response = client.delete('third_party/delivery/delete', json=data)
    assert response.status_code == 401

def test_delete_supply_service_fail_not_system_manager(client, login_user, clean):
    data = {
        'method_name': 'bogo',
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User is not a system manager'
    
    
  #-------------------------------------------------  
    
    # dont touch this 
    
    
"""
          #check
def test_checkout_accessing_payment_external_service (client, login_user, clean):    
    '''
    2.2.5.a: A member attempts to make a purchase for their shopping cart.
    Expected: Confirmation that the purchase was successful.
    '''  
    data = {
        'payment_details': {'test': 'test'},
        'address': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'successfully checked out'
    
    
    
              #check
def test_fail_checkout_accessing_payment_external_service_no_store (client, login_user, clean):  
    '''
    2.2.5.b: One of the stores is closed or does not exist in the system.
    Expected: message that the store is closed or doesnt exist
    '''  
    data = {
        'payment_details': {'test': 'test'},
        'address': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 400
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'store not found'
    
    
    
              #check
def test_fail_checkout_accessing_payment_external_service_insufficient_amount_of_products (client, login_user, clean):
    '''
    2.2.5.c: Insufficient amount of products.
    Expected: a message that there is insufficient amount of products
    '''  
    data = {
        'payment_details': {'test': 'test'},
        'address': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 400
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'insufficient amount of products'
    
    
    
              #check
def test_fail_checkout_accessing_payment_external_service_store_purchase_policy_not_met (client, login_user, clean):   
    '''
    2.2.5.d: Store purchase policy is not met.
    Expected: message that store purchase policy is not met
    '''  
    data = {
        'payment_details': {'test': 'test'},
        'address': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 400
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'purchase policy not met'

    
    
              #check
def test_fail_checkout_accessing_payment_external_service_external_service_fail (client, login_user, clean):   
    '''
    2.2.5.e: External payment service fail.
    Expected: message that external service failed
    '''  
    data = {
        'payment_details': {'test': 'test'},
        'address': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('market/checkout', headers=headers, json=data)
    assert response.status_code == 400
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'external service failed'
    
  
  #-------------------------------------------------  
  
         #check
def test_searching_for_products (client, login_user, clean):
    '''
    2.2.2.1.a: User Searches for a products Using Search parameters and Filters.
    Expected: successfully getting info about products
    '''   
    data = {
        'filters': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('market/search_products', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'searched products'
    
    
    
    
          #check
def test_searching_for_products_no_products (client, login_user, clean): 
    '''
    2.2.2.1.b: No products that pass the filters.
    Expected: getting an empty list.
    '''      
    data = {
        'filters': {'test': 'test'}
    }
    headers = {
        'Authorization': 'Bearer ' + login_user
    }
    response = client.post('market/search_products', headers=headers, json=data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'searched products'
    

  #-------------------------------------------------
   
           #check
def test_searching_for_products_in_a_specific_store (client, login_user, clean):
    '''
    2.2.2.2.a: User is searching for products in a specific store using filters
    Expected: geting the products with the requested filters
    '''    
    data = {
        'store_id': 1, # store's id
        'filters': {'test': 'test'} # filters
    }
    headers = {
        'Authorization': 'Bearer ' + login_user # member's token
    }   
    response = client.post('market/search_store_products', headers=headers, json=data) # search for products
    assert response.status_code == 200 # success
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'searched products' # check if the message is correct
    
   
   
   
   
           #check
def test_fail_searching_for_products_no_products_in_store (client, login_user, clean):
    '''
    2.2.2.2.b: store identifier doesnt exist
    Expected: prompt the user that the store identifier is invalid
    '''   
    data = {
        'store_id': 100, # corrupted store's id
        'filters': {'test': 'test'} # filters
    }
    headers = {
        'Authorization': 'Bearer ' + login_user # member's token
    }
    response = client.post('market/search_store_products', headers=headers, json=data) # search for products
    assert response.status_code == 400 # fail
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'store not found' # check if the message is correct
     
   
   
   
   
           #check
def test_searching_for_products_no_products_in_store_no_products_pass_filters (client, login_user, clean):
    '''
    2.2.2.2.c: no products pass the filters
    Expected: successfully getting an empty list
    '''    
    data = {
        'store_id': 1, # store's id
        'filters': {'test': 'test'} # filters
    }
    headers = {
        'Authorization': 'Bearer ' + login_user # member's token
    }
    response = client.post('market/search_store_products', headers=headers, json=data) # search for products
    assert response.status_code == 200 # success
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'searched products' # check if the message is correct
    
   
   #-------------------------------------------------
   
        #check
def test_opening_a_store (client, login_user, clean):
    '''
    2.3.2.a: A logged in member is attempting to open a store with legal details (proper location, proper name).
    Expected: Successfully opened a store
    '''
    data = {
        'store_name': 'test', # store's name
        'location_id': 1 # store's location
    }
    headers = {
        'Authorization': 'Bearer ' + login_user # member's token
    }
    response = client.post('market/open_store', headers=headers, json=data) # open the store
    assert response.status_code == 200 # success
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'store opened successfully' # check if the message is correct
    



        #check
def test_fail_opening_a_store (client, login_user, clean):
    
    '''
    2.3.2.b: store credentials are not valid)
    Expected: message that store credentials are not valid
    '''
    data = {
        'store_name': 'test', # store's name
        'location_id': 'test' # corrupted store's location
    }
    headers = {
        'Authorization': 'Bearer ' + login_user # member's token
    }
    response = client.post('market/open_store', headers=headers, json=data) # open the store
    assert response.status_code == 400 # fail
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'store not opened' # check if the message is correct
    
#-------------------------------------------------
    
        #check
def test_storage_management_add_product (client, login_system_manager, clean):
    '''
    2.4.1.a: A store owner or manager requests to add a product to their store.
    Expected: the store now supports the sales of the new product, and the product is added to the store.
    '''
    data = {
        'store_id': 1, # store's id
        'product_name': 'test', # product's name
        'product_description': 'test', # product's description
        'product_price': 100, # product's price
        'product_amount': 10 # product's amount
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.post('market/add_product', headers=headers, json=data) # add the product
    assert response.status_code == 200 # success
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'product added successfully' # check if the message is correct
    
    
    
    
        #check
def test_fail_storage_management_add_product_corrupted_data (client, login_system_manager, clean):
    '''
    2.4.1.b: product credentials are not valid.
    Expected: message that product credentials are not valid
    '''
    data = {
        'store_id': 1, # store's id
        'product_name': 'test', # product's name
        'product_description': 'test', # product's description
        'product_price': 'test', # corrupted product's price
        'product_amount': 10 # product's amount
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.post('market/add_product', headers=headers, json=data) # add the product
    assert response.status_code == 400 # fail
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'product not added' # check if the message is correct
    
    
    

    
        #check
def test_fail_storage_management_add_product_invalid_amount (client, login_system_manager, clean):
    '''
    2.4.1.c: amount of product is invalid.
    Expected: message that amount of products is invalid.
    '''
    data = {
        'store_id': 1, # store's id
        'product_name': 'test', # product's name
        'product_description': 'test', # product's description
        'product_price': 100, # product's price
        'product_amount': 'test' # corrupted product's amount
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.post('market/add_product', headers=headers, json=data) # add the product
    assert response.status_code == 400 # fail
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'product not added' # check if the message is correct
    
    
#-------------------------------------------------
    
      #check
def test_owner_changing_store_purchase_policy (client, login_system_manager, clean):
    '''
    2.4.2.1-a: A store owner changes the purchase policy to reject all purchases above 10000$
    Expected: The purchase policy of the store is successfully changed, and rejects all purchases above 10000$
    '''
    data = {
        'store_id': 1, # store's id
        'purchase_policy': {'max_purchase': 10000} # purchase policy
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.post('market/change_purchase_policy', headers=headers, json=data) # change the purchase policy
    assert response.status_code == 200 # success
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'purchase policy changed successfully' # check if the message is correct
    
    
        
    
    
    
    
      #check
def test_fail_owner_changing_store_purchase_policy_corrupted_data (client, login_system_manager, clean):
    '''
    2.4.2.1-b: A store owner changes the purchase policy with corrupted purchase policy information
    Expected: The purchase policy of the store is not changed, and an error is raised.
    '''
    data = {
        'store_id': 1, # store's id
        'purchase_policy': {'max_purchase': 'test'} # corrupted purchase policy
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.post('market/change_purchase_policy', headers=headers, json=data) # change the purchase policy
    assert response.status_code == 400 # fail
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'purchase policy not changed' # check if the message is correct
    
    
    
    
      #check
def test_manager_changing_store_purchase_policy (client, login_system_manager, clean):
    '''
    2.4.2.1-c: A store manager changes the purchase policy to reject all purchases above 10000$
    Expected: The purchase policy of the store is successfully changed, and rejects all purchases above 10000$
    '''
    data = {
        'store_id': 1, # store's id
        'purchase_policy': {'max_purchase': 10000} # purchase policy
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.post('market/change_purchase_policy', headers=headers, json=data) # change the purchase policy
    assert response.status_code == 200 # success
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'purchase policy changed successfully' # check if the message is correct
    
    
    
    
      #check
def test_fail_manager_changing_store_purchase_policy_corrupted_data (client, login_system_manager, clean):
    '''
    2.4.2.1-d: A store manager changes the purchase policy with corrupted purchase policy information
    Expected: The purchase policy of the store is not changed, and an error is raised.
    '''
    data = {
        'store_id': 1, # store's id
        'purchase_policy': {'max_purchase': 'test'} # corrupted purchase policy
    } 
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.post('market/change_purchase_policy', headers=headers, json=data) # change the purchase policy
    assert response.status_code == 400 # fail
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'purchase policy not changed' # check if the message is correct
    
   
   #------------------------------------------------- 
    
      #check
def test_owner_changing_store_purchase_policy_types (client, login_system_manager, clean):
    '''
    2.4.2.2-a: A store owner is attempting to change the store purchase type of their store.
    Expected: Successfully changed the store purchase type.
    '''
    data = {
        'store_id': 1, # store's id
        'purchase_type': 'auction' # purchase type
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.post('market/change_purchase_type', headers=headers, json=data) # change the store purchase type
    assert response.status_code == 200 # success
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'purchase type changed successfully' # check if the message is correct

    
    
    
      #check
def test_fail_manager_changing_store_purchase_policy_types_no_privileges (client, login_system_manager, clean):
    '''
    2.4.2.2-b: A store manager with no privileges is attempting to change the store purchase type.
    Expected: Didnt change the store purchase type as the store manager does not have the necessary permissions
    '''
    data = {
        'store_id': 1, # store's id
        'purchase_type': 'auction' # purchase type
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.post('market/change_purchase_type', headers=headers, json=data) # change the store purchase type
    assert response.status_code == 400 # fail
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'You do not have permissions to change the purchase type' # check if the message is correct
    
    
    
      #check
def test_fail_owner_changing_store_purchase_policy_types_closed_store (client, login_system_manager, clean):
    '''
    2.4.2.2-c: A store owner is attempting to change the store purchase types of an already closed store. 
    Expected: didnt change the store purchase type of an already closed store
    '''
    data = {
        'store_id': 2, # store's id
        'purchase_type': 'auction' # purchase type
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.post('market/change_purchase_type', headers=headers, json=data) # change the store purchase type
    assert response.status_code == 400 # fail
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'store is closed' # check if the message is correct
    
#-------------------------------------------------

    #check
def test_close_a_store (client, login_system_manager, clean):
    '''
    2.4.9.a: A store owner is attempting to close their store.
    Expected: Success: The owner successfully closed his store
    '''
    data = {
        'store_id': 1 # store's id
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.post('market/close_store', headers=headers, json=data) # close the store
    assert response.status_code == 200 # success
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'store closed successfully' # check if the message is correct
    
    
#-------------------------------------------------
    
    #check
def test_get_info_of_purchase_history_of_member_in_store (client, login_user, clean):
    '''
    2.4.13.a: A member is trying to view his purchase history in a store.
    Expected: The member successfully viewed his purchase history
    '''
    data = {
        'store_id': 1 # store's id
    }
    headers = {
        'Authorization': 'Bearer ' + login_user # member's token
    }
    response = client.get('market/store_purchase_history', headers=headers, json=data) # get the purchase history of the store
    assert response.status_code == 200 # success
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'purchase history sent' # check if the message is correct
    
 #-------------------------------------------------   

    
def test_get_info_of_purchase_history_of_member_in_system(client, login_system_manager, clean):
    '''
    2.6.4.a: A logged in system manager requests information regarding the purchase history of a member in the system.
    Expected: System manager successfully retrieved the requested information.
    '''
    data = {
        'username': 'bogo' # member's username
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.get('market/member_purchase_history', headers=headers, json=data) # get the purchase history of the member
    assert response.status_code == 200 # success
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'purchase history sent' # check if the message is correct
    
    
    

def test_fail_get_info_of_purchase_history_of_member_in_system(client, login_system_manager, clean):
    '''
    2.6.4.b: A logged in system manager requests information regarding the purchase history of a member in the system with wrong member credentials
    Expected: message that User credentials invalid or user doesn’t exist.
    '''
    data = {
        'username': 'test' # member's username
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.get('market/member_purchase_history', headers=headers, json=data) # get the purchase history of the member
    assert response.status_code == 400 # fail
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'User id is invalid' # check if the message is correct
    
    
    
    #check
def test_fail_get_info_of_purchase_history_in_a_store(client, login_system_manager, clean):
    '''
    2.6.4.a: A logged in system manager requests information regarding the purchase history of a store.
    Expected: the system renders to the member a message stating that he doesn’t have permissions to view information regarding the system. 
    '''
    data = {
        'username': 'test', # member's username
        'store_id': 1 # store's id
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.get('market/store_purchase_history', headers=headers, json=data) # get the purchase history of the store
    assert response.status_code == 400 # fail
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'You do not have permissions to view this information' # check if the message is correct
    #### fix the error msg
   
 #check
def test_fail_get_info_of_purchase_history_in_a_store (client, login_system_manager, clean):
    '''
    2.6.4.b: A logged in system manager requests information regarding the purchase history of a store in the system with wrong store credentials
    Expected: message that Store credentials invalid or store doesn’t exist. 
    '''
    data = {
        'username': 'test', # member's username
        'store_id': 2 # store's id
    }
    headers = {
        'Authorization': 'Bearer ' + login_system_manager # system manager's token
    }
    response = client.get('market/store_purchase_history', headers=headers, json=data) # get the purchase history of the store
    assert response.status_code == 400 # fail
    data = response.get_json() # get the response
    assert 'message' in data # check if the response contains the message
    assert data['message'] == 'Store credentials invalid or store doesn’t exist.' # check if the message is correct
    ### fix the error msg
   



"""

if __name__ == '__main__':
    pytest.main(['-s', 'tests/test_acceptance.py'])
