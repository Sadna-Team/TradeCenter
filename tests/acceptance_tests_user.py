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
    Token = None

    def test_start(self, client):
        response = client.get('/auth/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
        self.Token = data['token']

    def test_register(self, client):
        register_credentials = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testemail',
            'year': 1990,
            'month': 1,
            'day': 1,
            'phone': '1234567890'
        }
        # Register new user
        response = client.post('/auth/register', json={
            'register_credentials': register_credentials
        }, headers={
            'Authorization': f'Bearer {self.Token}'
        })
        print(response.data)
        assert response.status_code == 200

    def test_login(self, client):
        response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data

    def test_logout(self, client):
        login_response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        token = json.loads(login_response.data)['token']

        response = client.post('/auth/logout', headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 200


@pytest.mark.usefixtures('client')
class TestUserEndpoints:

    def test_show_notifications(self, client):
        login_response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        token = json.loads(login_response.data)['token']

        response = client.get('/user/notifications', headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 200

    def test_add_product_to_basket(self, client):
        login_response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        token = json.loads(login_response.data)['token']

        response = client.post('/user/add_to_basket', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            'store_id': 1,
            'product_id': 1,
            'quantity': 1
        })
        assert response.status_code == 200

    def test_remove_product_from_basket(self, client):
        login_response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        token = json.loads(login_response.data)['token']

        response = client.post('/user/remove_from_basket', headers={
            'Authorization': f'Bearer {token}'
        }, json={
            'store_id': 1,
            'product_id': 1,
            'quantity': 1
        })
        assert response.status_code == 200

    def test_show_cart(self, client):
        login_response = client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        token = json.loads(login_response.data)['token']

        response = client.get('/user/show_cart', headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 200

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

