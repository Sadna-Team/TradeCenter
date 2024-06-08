from backend import create_app
from flask import json, jsonify

app = create_app()
client = app.test_client()
global token
global guest_token


register_credentials = {
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567'}


def test_start():
    global token
    response = client.get('/auth/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    token = data['token']
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
    assert response.status_code == 400

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
    assert response.status_code == 400

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
    assert response.status_code == 400

def test_logout():
    global token

    response = client.post('/auth/logout', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    token = response.json['token']

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
    test_start()
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
        'store_id': 1,
        'product_id': 1,
        'quantity': 1
    })
    assert response.status_code == 200

def test_remove_product_from_basket():
    global token
    init_guest_token()
    response = client.post('/user/remove_from_basket', headers={
        'Authorization': f'Bearer {token}'
    }, json={
        'store_id': 1,
        'product_id': 1,
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

def test_show_cart():
    global token

    test_add_product_to_basket()

    response = client.get('/user/show_cart', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert response.json['shopping_cart'] == {'1': {'1': 1}}

