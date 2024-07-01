from backend import create_app
from flask import json

app = create_app(mode='testing')
client = app.test_client()


def create_and_login_user(username, password, email, phone, year, month, day):
    response = client.get('/auth/')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'token' in data

    token1 = data['token']

    register_credentials2 = {
        'username': username,
        'email': email,
        'password': password,
        'address': 'address2',
        'city': 'city2',
        'state': 'state2',
        'country': 'country2',
        'zip_code': '12345',
        'year': year,
        'month': month,
        'day': day,
        'phone': phone
    }

    headers = {
        'Authorization': 'Bearer ' + token1
    }
    response = client.post('auth/register', headers=headers, json={'register_credentials': register_credentials2})
    assert response.status_code == 201

    response = client.post('/auth/login', headers=headers, json={'username': username, 'password': password})
    assert response.status_code == 200
    token1 = json.loads(response.data)['token']

    return token1


global token
global guest_token


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


def test_start(first=True):
    global token
    response = client.get('/auth/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    token = data['token']


    if first:
        user2 = create_and_login_user('test2', 'test2', 'test2@gmail.com', '054-7654321', 2003, 1, 1)

        response = client.post('/store/add_store', headers={'Authorization': 'Bearer ' + user2},
                               json={'store_name': 'test_store','address': 'address', 'city': 'city', 'state': 'state', 'country': 'country', 'zip_code': '12346'})
        assert response.status_code == 200

        response = client.post('/store/add_product', headers={'Authorization': 'Bearer ' + user2},
                               json={'store_id': 0,
                                     'product_name': 'test_product',
                                     'description': 'test_description',
                                     'price': 10,
                                     'weight': 1,
                                     'tags': ['test_tag'],
                                     'amount': 10
                                     })
        assert response.status_code == 200

        response = client.post('/store/add_product', headers={'Authorization': 'Bearer ' + user2},
                               json={'store_id': 0,
                                     'product_name': 'test_product2',
                                     'description': 'test_description',
                                     'price': 10,
                                     'weight': 1,
                                     'tags': ['test_tag2'],
                                     'amount': 10
                                     })

        guest_token = client.get('/auth/').json['token']
        admin_token = client.post('/auth/login', 
                                  headers={'Authorization': 'Bearer ' + guest_token}, 
                                  json={'username': 'admin', 'password': 'admin'}).json['token']

        response = client.post('/store/add_category', headers={'Authorization': 'Bearer ' + admin_token},
                               json={'store_id': 0, 'category_name': 'test_category'})
        
        assert response.status_code == 200

        response = client.post('store/assign_product_to_category', headers={'Authorization': 'Bearer ' + user2},
                               json={'store_id': 0, 'product_id': 0, 'category_id': 0})
        
        assert response.status_code == 200

        response = client.post('/store/restock_product', headers={'Authorization': 'Bearer ' + user2},
                               json={'store_id': 0,
                                     'product_id': 0,
                                     'quantity': 1
                                     })
        assert response.status_code == 200

    return data['token']


def init_guest_token():
    global guest_token
    response = client.get('/auth/')
    data = json.loads(response.data)
    guest_token = data['token']


def test_register():
    global token

    data1 = {
        'register_credentials': register_credentials
    }
    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = client.post('auth/register', headers=headers, json=data1)

    assert response.status_code == 201


def test_register_failed_duplicate_username():
    global token
    data1 = {
        'register_credentials': register_credentials
    }
    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = client.post('auth/register', headers=headers, json=data1)

    assert response.status_code == 400


def test_register_failed_missing_data():
    global token
    temp = register_credentials.copy()
    temp.pop('username')
    data1 = {
        'register_credentials': temp
    }
    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = client.post('auth/register', headers=headers, json=data1)

    assert response.status_code == 400


def test_login():
    global token
    data = {
        'username': 'test',
        'password': 'test'
    }
    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = client.post('/auth/login', headers=headers, json=data)
    assert response.status_code == 200
    token = json.loads(response.data)['token']


def test_login_failed_user_doesnt_exist():
    global token
    data = {
        'username': 'test2',
        'password': 'test'
    }
    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = client.post('/auth/login', headers=headers, json=data)
    assert response.status_code == 401


def test_login_failed_wrong_password():
    global token
    data = {
        'username': 'test',
        'password': 'test2'
    }
    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = client.post('/auth/login', headers=headers, json=data)
    assert response.status_code == 401


def test_login_failed_already_logged_in():
    global token
    data = {
        'username': 'test',
        'password': 'test'
    }
    headers = {
        'Authorization': 'Bearer ' + token
    }

    response = client.post('/auth/login', headers=headers, json=data)
    assert response.status_code == 401


def test_logout():
    global token

    response = client.post('/auth/logout', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    token = response.json['token']

def test_login_then_logout():
    global token
    test_login()
    test_logout()

def test_logout_failed_not_logged_in():
    global token

    response = client.post('/auth/logout', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 400


def test_logout_guest():
    global token
    response = client.post('/auth/logout_guest', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200


def test_show_notifications():
    global token
    test_start(False)
    test_login()
    response = client.get('/user/notifications', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert json.loads(response.data)['notifications'] == []


def test_show_notifications_failed_not_logged_in():
    global guest_token
    init_guest_token()
    response = client.get('/user/notifications', headers={
        'Authorization': f'Bearer {guest_token}'
    })
    assert response.status_code == 400


def test_add_product_to_basket():
    global token
    response = client.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'store_id': 0,
        'product_id': 0,
        'quantity': 1
    })
    assert response.status_code == 200


def test_add_product_to_basket_failed_amount_exceeds():
    global token
    response = client.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'store_id': 0,
        'product_id': 0,
        'quantity': 100
    })

    assert response.status_code == 400


def test_add_product_to_basket_store_not_exists():
    global token
    response = client.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'store_id': 100,
        'product_id': 1,
        'quantity': 1
    })

    assert response.status_code == 400


def test_add_product_to_basket_product_not_exists():
    global token
    response = client.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'store_id': 0,
        'product_id': 100,
        'quantity': 1
    })

    assert response.status_code == 400


def test_remove_product_from_basket():
    global token
    init_guest_token()
    response = client.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'store_id': 0,
        'product_id': 0,
        'quantity': 1
    })
    assert response.status_code == 200


def test_remove_product_from_basket_failed_not_logged_in():
    global guest_token
    init_guest_token()
    response = client.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {guest_token}'
    }, json={
        'store_id': 1,
        'product_id': 1,
        'quantity': 1
    })
    assert response.status_code == 400


def test_remove_product_from_basket_failed_store_not_exists():
    global token
    response = client.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'store_id': 100,
        'product_id': 0,
        'quantity': 1
    })
    assert response.status_code == 400


def test_remove_product_from_basket_failed_product_not_exists():
    global token
    response = client.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'store_id': 0,
        'product_id': 100,
        'quantity': 1
    })
    assert response.status_code == 400


def test_remove_product_from_basket_failed_quantity_exceeds():
    global token
    response = client.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'store_id': 0,
        'product_id': 0,
        'quantity': 100
    })
    assert response.status_code == 400


def test_show_cart():
    global token

    test_add_product_to_basket()

    response = client.get('/user/show_cart', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.json['shopping_cart'] == {'0': {'0': 1}}


def test_search_by_category():
    global token
    data = {"store_id": 0, "category_id": 0}
    response = client.post('/market/search_products_by_category', headers={
        'Authorization': f'Bearer {token}'
    }, json=data)
    assert response.status_code == 200

def test_search_by_category_failed_store_not_exists():
    global token
    data = {"store_id": 100, "category_id": 0}
    response = client.post('/market/search_products_by_category', headers={
        'Authorization': f'Bearer {token}'
    }, json=data)
    assert response.status_code == 400

def test_search_by_category_failed_category_not_exists():
    global token
    data = {"store_id": 0, "category_id": 100}
    response = client.post('/market/search_products_by_category', headers={
        'Authorization': f'Bearer {token}'} , json=data)
    assert response.status_code == 400

def test_search_by_tags():
    global token
    data = {"store_id": 0, "tags": ["test_tag"]}
    response = client.post('/market/search_products_by_tags', headers={
        'Authorization': f'Bearer {token}'
    }, json=data)
    assert response.status_code == 200

def test_search_by_tags_failed_store_not_exists():
    global token
    data = {"store_id": 100, "tags": ["test_tag"]}
    response = client.post('/market/search_products_by_tags', headers={
        'Authorization': f'Bearer {token}'
    }, json=data)
    assert response.status_code == 400

def test_search_by_name():
    global token
    data = {"store_id": 0, "name": "test_product"}
    response = client.post('/market/search_products_by_name', headers={
        'Authorization': f'Bearer {token}'
    }, json=data)
    assert response.status_code == 200

def test_search_by_name_failed_store_not_exists():
    global token
    data = {"store_id": 100, "name": "test_product"}
    response = client.post('/market/search_products_by_name', headers={
        'Authorization': f'Bearer {token}'
    }, json=data)
    assert response.status_code == 400

def test_information_about_stores():
    global token

    test_add_product_to_basket()

    response = client.get('/store/store_info', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'store_id': 0
    })
    assert response.status_code == 200


def test_information_about_stores_failed_store_not_exists():
    global guest_token

    init_guest_token()
    response = client.post('/store/store_info', headers={
        'Authorization': f'Bearer {guest_token}'
    }, json={
        'store_id': 100
    })
    assert response.status_code == 400


def test_add_store():
    global token
    create_and_login_user('tests4', 'tests4', 'tests4@gmail.com', '054-1111111', 2003, 1, 1)
    response = client.post('/store/add_store', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'store_name': 'test_store',
        'address': 'address',
        'city': 'city',
        'state': 'state',
        'country': 'country',
        'zip_code': '12345'
    })
    assert response.status_code == 200

def test_add_store_failed_user_not_a_member():
    global guest_token
    init_guest_token()
    response = client.post('/store/add_store', headers={
        'Authorization': f'Bearer {guest_token}'
    }, json={
        'store_name': 'test_store',
        'address': 'address',
        'city': 'city',
        'state': 'state',
        'country': 'country',
        'zip_code': '12345'
    })
    assert response.status_code == 400


default_payment_method = {'payment method': 'bogo'}

default_supply_method = "bogo"

default_address_checkout = {'address': 'randomstreet 34th', 
                            'city': 'arkham',
                            'state': 'gotham', 
                            'country': 'Wakanda', 
                            'zip_code': '12345'}

def test_show_purchase_history_of_user():
    global token 
    test_add_product_to_basket()

    create_and_login_user('tests5', 'tests5', 'tests5@gmail.com', '055-1111111', 2003, 1, 1)
    #purchase the product
    response = client.post('market/checkout', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'payment_details': default_payment_method,
        'supply_method': default_supply_method,
        'address': default_address_checkout})
    assert response.status_code == 200

    #show purchase history
    response = client.get('market/user_purchase_history', headers={
        'Authorization': f'Bearer {token}'
    }, json={"user_id": 1})
    assert response.status_code == 200


def test_show_purchase_history_of_user_failed_is_not_logged_in():
    global guest_token
    init_guest_token()

    #adding a product to the basket
    response = client.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {guest_token}'
    }, json={
        'store_id': 0,
        'product_id': 0,
        'quantity': 1
    })
    assert response.status_code == 200

    #purchase the product
    response = client.post('market/checkout', headers={
        'Authorization': f'Bearer {guest_token}'
    }, json={
        'payment_details': default_payment_method,
        'supply_method': default_supply_method,
        'address': default_address_checkout})
    assert response.status_code == 200

    #show purchase history
    response = client.get('market/user_purchase_history', headers={
        'Authorization': f'Bearer {guest_token}'
    }, json={"user_id": 1})
    assert response.status_code == 400

def test_show_purchase_history_of_user_in_store():
    global token 
    test_add_product_to_basket()

    create_and_login_user('tests6', 'tests6', 'tests6@gmail.com', '056-1111111', 2003, 1, 1)
    #purchase the product
    response = client.post('market/checkout', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'payment_details': default_payment_method,
        'supply_method': default_supply_method,
        'address': default_address_checkout})
    assert response.status_code == 200

    #show purchase history
    response = client.get('market/user_purchase_history', headers={
        'Authorization': f'Bearer {token}'
    }, json={"user_id": 1, "store_id": 0})
    assert response.status_code == 200


def test_show_purchase_history_of_user_in_store_failed_is_not_logged_in():
    global guest_token
    init_guest_token()

    #adding a product to the basket
    response = client.post('/user/add_to_basket', headers={
        'Authorization': f'Bearer {guest_token}'
    }, json={
        'store_id': 0,
        'product_id': 0,
        'quantity': 1
    })
    assert response.status_code == 200

    #purchase the product
    response = client.post('market/checkout', headers={
        'Authorization': f'Bearer {guest_token}'
    }, json={
        'payment_details': default_payment_method,
        'supply_method': default_supply_method,
        'address': default_address_checkout})
    assert response.status_code == 200

    #show purchase history
    response = client.get('market/user_purchase_history', headers={
        'Authorization': f'Bearer {guest_token}'
    }, json={"user_id": 1, "store_id": 0})
    assert response.status_code == 400

