from backend import create_app
from flask import json

global token1, token2, token3

app = create_app(mode='testing')
client = app.test_client()


def create_and_login_user(username, password, email, phone, year, month, day):
    response = client.get('/auth/')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'token' in data

    token = data['token']

    register_credentials = {
        'username': username,
        'email': email,
        'password': password,
        'address': 'address',
        'city': 'city',
        'state': 'state',
        'country': 'country',
        'zip_code': '12345',
        'year': year,
        'month': month,
        'day': day,
        'phone': phone
    }
    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = client.post('auth/register', headers=headers, json={'register_credentials': register_credentials})
    assert response.status_code == 201

    response = client.post('/auth/login', headers=headers, json={'username': username, 'password': password})
    assert response.status_code == 200
    token = json.loads(response.data)['token']

    return token


def test_start():
    global token1, token2, token3
    token1 = create_and_login_user('test1', 'test1', 'test1@gmail.com', '054-1234567', 2003, 1, 1)
    token2 = create_and_login_user('test2', 'test2', 'test2@gmail.com', '054-7654321', 2003, 1, 1)
    token3 = create_and_login_user('test3', 'test3', 'test3@gmail.com', '054-1234567', 2003, 1, 1)

    response = client.post('/store/add_store', headers={'Authorization': 'Bearer ' + token1},
                           json={'store_name': 'test_store', 'address': 'address', 'city': 'city', 'state': 'state', 'country': 'country', 'zip_code': '12345'})
    assert response.status_code == 200


def test_nominate_owner_acc():
    global token1, token2
    response = client.post('/store/add_store_owner', headers={'Authorization': 'Bearer ' + token1},
                           json={'store_id': 0, 'username': 'test2'})
    assert response.status_code == 200

    response = client.post('/user/accept_promotion', headers={'Authorization': 'Bearer ' + token2},
                           json={'promotion_id': 0, 'accept': True})
    assert response.status_code == 200


def test_nominate_owner_dec():
    global token1, token3
    response = client.post('/store/add_store_owner',
                           headers={'Authorization': 'Bearer ' + token1},
                           json={'store_id': 0, 'username': 'test3'})

    assert response.status_code == 200

    response = client.post('/user/accept_promotion',
                           headers={'Authorization': 'Bearer ' + token3},
                           json={'promotion_id': 1, 'accept': False})

    assert response.status_code == 200


def test_cancel_ownership():
    global token1, token2
    response = client.post('/store/remove_store_role',
                           headers={'Authorization': 'Bearer ' + token1},
                           json={'store_id': 0, 'username': 'test2'})

    assert response.status_code == 200


def test_give_up_ownership():
    global token1, token2
    response = client.post('/store/add_store_owner',
                           headers={'Authorization': 'Bearer ' + token1},
                           json={'store_id': 0, 'username': 'test2'})

    assert response.status_code == 200

    response = client.post('/user/accept_promotion',
                           headers={'Authorization': 'Bearer ' + token2},
                           json={'promotion_id': 2, 'accept': True})

    assert response.status_code == 200

    # nominate another owner
    response = client.post('/store/add_store_owner',
                            headers={'Authorization': 'Bearer ' + token2},
                            json={'store_id': 0, 'username': 'test3'})
    assert response.status_code == 200

    # accept the nomination
    response = client.post('/user/accept_promotion',
                            headers={'Authorization': 'Bearer ' + token3},
                            json={'promotion_id': 3, 'accept': True})
    assert response.status_code == 200

    response = client.post('/store/give_up_role',
                           headers={'Authorization': 'Bearer ' + token2},
                           json={'store_id': 0})

    assert response.status_code == 200

    # check if the user test3 is no longer an owner
    response = client.get('/user/is_store_owner',
                            headers={'Authorization': 'Bearer ' + token3},
                            json={'store_id': 0})

    assert response.status_code == 200
    # assert json.loads(response.data)['is_store_owner'] is False

    response = client.get('/user/is_store_owner',
                            headers={'Authorization': 'Bearer ' + token2},
                            json={'store_id': 0})

    assert response.status_code == 200
    # assert json.loads(response.data)['is_store_owner'] is False


def test_is_system_manager():
    global token1
    response = client.get('/user/is_system_manager',
                          headers={'Authorization': 'Bearer ' + token1})
    assert response.status_code == 200
    assert json.loads(response.data)['is_system_manager'] is False

    # login as admin
    response = client.get('/auth/')
    assert response.status_code == 200
    token = json.loads(response.data)['token']

    response = client.post('/auth/login', headers={'Authorization': 'Bearer ' + token},
                           json={'username': 'admin', 'password': 'admin'})
    assert response.status_code == 200
    token = json.loads(response.data)['token']

    # check if admin is system manager
    response = client.get('/user/is_system_manager',
                          headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    assert json.loads(response.data)['is_system_manager'] is True


def test_is_store_owner():
    global token1
    global token2
    response = client.get('/user/is_store_owner',
                          headers={'Authorization': 'Bearer ' + token1},
                          json={'store_id': 0})
    assert response.status_code == 200
    assert json.loads(response.data)['is_store_owner'] is True

    response = client.get('/user/is_store_owner', headers={'Authorization': 'Bearer ' + token2}, json={'store_id': 0})
    assert response.status_code == 200
    assert json.loads(response.data)['is_store_owner'] is False


def test_is_store_manager():
    global token1
    global token2
    response = client.get('/user/is_store_manager',
                          headers={'Authorization': 'Bearer ' + token1},
                          json={'store_id': 0})
    assert response.status_code == 200
    assert json.loads(response.data)['is_store_manager'] is False

    response = client.get('/user/is_store_manager', headers={'Authorization': 'Bearer ' + token2}, json={'store_id': 0})
    assert response.status_code == 200
    assert json.loads(response.data)['is_store_manager'] is False

    response = client.post('/store/add_store_manager', headers={'Authorization': 'Bearer ' + token1},
                           json={'store_id': 0, 'username': 'test2'})
    assert response.status_code == 200
