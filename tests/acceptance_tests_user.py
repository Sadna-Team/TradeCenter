import pytest
from backend import create_app

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()


import pytest
from flask import json


@pytest.mark.usefixtures('client')
class TestAuthEndpoints:
    def test_start(self, client):
        response = client.get('/auth/')
        assert response.status_code == 200
        data1 = json.loads(response.data)
        assert 'token' in data1
        return data1['token']

    def test_register(self, client):

        token = self.test_start(client)

        register_credentials = {
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'test',
            'location_id': 1,
            'year': 2003,
            'month': 1,
            'day': 1,
            'phone': '054-1234567'}
        data1 = {
            'register_credentials': register_credentials
        }
        headers = {
            'Authorization': 'Bearer ' + token
        }
        response = client.post('auth/register', headers=headers, json=data1)

        assert response.status_code == 201


    def test_login(self, client):

        token = self.test_start(client)

        response = client.post('/auth/login', headers={'Authorization': 'Bearer ' + token}, json={
            'username': 'test',
            'password': 'test'
        })

        data = json.loads(response.data)
        print(data)
        assert response.status_code == 200
        assert 'token' in data
        return data['token']

    def test_logout(self, client):
        token = self.test_login(client)
        login_response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        token = json.loads(login_response.data)['token']

        response = client.post('/auth/logout', headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 200

    def test_show_notifications(self, client):
        token = self.test_login(client)
        response = client.get('/user/notifications', headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 200
        assert json.loads(response.data)['notifications'] == []

    def test_add_product_to_basket(self, client):
        token = self.test_login(client)
        response = client.post('/user/add_to_basket', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            'store_id': 1,
            'product_id': 1,
            'quantity': 1
        })
        assert response.status_code == 200

    def test_remove_product_from_basket(self, client):
        token = self.test_login(client)
        response = client.post('/user/remove_from_basket', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            'store_id': 1,
            'product_id': 1,
            'quantity': 1
        })
        assert response.status_code == 200

    def test_show_cart(self, client):
        login_user = self.test_login(client)
        self.test_add_product_to_basket(client)

        response = client.get('/user/show_cart', headers={
            'Authorization': f'Bearer {login_user}'
        })
        assert response.status_code == 200
        assert json.loads(response.data)['cart'] == {1: {1: 1}}

