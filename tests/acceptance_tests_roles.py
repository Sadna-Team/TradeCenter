
from backend import create_app
from flask import json, jsonify

global token1, token2

app = create_app()
client = app.test_client()


def test_start():

    global token1, token2

    response = client.get('/auth/')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'token' in data

    token1 = data['token']

    register_credentials = {
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'test',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '054-1234567'
    }
    headers = {
        'Authorization': 'Bearer ' + token1
    }
    response = client.post('auth/register', headers=headers, json={'register_credentials': register_credentials})
    assert response.status_code == 201

    response = client.post('/auth/login', headers=headers, json={'username': 'test', 'password': 'test'})
    assert response.status_code == 200
    token1 = json.loads(response.data)['token']

    response = client.get('/auth/')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'token' in data
    token2 = data['token']

    register_credentials = {
        'username': 'test2',
        'email': 'test2@gmail.com',
        'password': 'test2',
        'location_id': 1,
        'year': 2003,
        'month': 1,
        'day': 1,
        'phone': '050-1234567'
    }
    headers = {
        'Authorization': 'Bearer ' + token2
    }
    response = client.post('auth/register', headers=headers, json={'register_credentials': register_credentials})
    assert response.status_code == 201

    response = client.post('/auth/login', headers=headers, json={'username': 'test2', 'password': 'test2'})
    assert response.status_code == 200
    token2 = json.loads(response.data)['token']

    # create store

    response = client.post('/store/add_store', headers={'Authorization': 'Bearer ' + token1},
                           json={'store_name': 'test_store', 'location_id': 1})
    assert response.status_code == 200

def test_nominate_manager():
    response = client.post('/store/add_store_owner', headers={'Authorization': 'Bearer ' + token1},
                           json={'store_id': 0, 'username': 'test2'})
    assert response.status_code == 200

    response = client.post('/user/accept_promotion', headers={'Authorization': 'Bearer ' + token2}, json={'promotion_id': 0, 'accept': True})
    assert response.status_code == 200








