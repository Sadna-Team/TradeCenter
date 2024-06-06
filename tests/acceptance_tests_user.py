import pytest
from backend import create_app

@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def start(client):
    response = client.get('/auth/')
    assert response.status_code == 200
    return response.json['token']


import pytest
from flask import json


@pytest.mark.usefixtures('client')
class TestAuthEndpoints:

    @pytest.fixture
    def test_start(self, client):
        response = client.get('/auth/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
        return data['token']

    @pytest.fixture
    def test_register(self, client, test_start):

        register_credentials = {
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'test',
            'location_id': 1,
            'year': 2003,
            'month': 1,
            'day': 1,
            'phone': '054-1234567'}
        data = {
            'register_credentials': register_credentials
        }
        headers = {
            'Authorization': 'Bearer ' + test_start
        }
        response = client.post('auth/register', headers=headers, json=data)
        assert response.status_code == 201
        return test_start

    @pytest.fixture
    def test_login(self, client, test_register):
        response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        }, headers={
            'Authorization': f'Bearer {test_register}'
        })

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
        return data['token']

    @pytest.fixture
    def test_logout(self, client, test_login):
        login_response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        }, headers={
            'Authorization': f'Bearer {test_login}'
        })
        token = json.loads(login_response.data)['token']

        response = client.post('/auth/logout', headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 200


# @pytest.mark.usefixtures('client')
# class TestUserEndpoints:

    @pytest.fixture
    def test_show_notifications(self, client, login_user):
        response = client.get('/user/notifications', headers={
            'Authorization': f'Bearer {login_user}'
        })
        assert response.status_code == 200
        assert json.loads(response.data)['notifications'] == []

    @pytest.fixture
    def test_add_product_to_basket(self, client, login_user):

        response = client.post('/user/add_to_basket', headers={
            'Authorization': f'Bearer {login_user}'
        }, json={
            'store_id': 1,
            'product_id': 1,
            'quantity': 1
        })
        assert response.status_code == 200

    @pytest.fixture
    def test_remove_product_from_basket(self, client, login_user):

        response = client.post('/user/remove_from_basket', headers={
            'Authorization': f'Bearer {login_user}'
        }, json={
            'store_id': 1,
            'product_id': 1,
            'quantity': 1
        })
        assert response.status_code == 200

    @pytest.fixture
    def test_show_cart(self, client, login_user, add_product_to_basket):

        response = client.get('/user/show_cart', headers={
            'Authorization': f'Bearer {login_user}'
        })
        assert response.status_code == 200
        assert json.loads(response.data)['cart'] == {1: {1: 1}}

    def test_accept_promotion(self, client):
        login_response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        token = json.loads(login_response.data)['token']

        response = client.post('/user/accept_promotion', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            'promotion_id': 1,
            'accept': True
        })
        assert response.status_code == 200
