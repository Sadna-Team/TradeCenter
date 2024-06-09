import pytest
from backend import create_app, clean_data
import json

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def token(client):
    response = client.get('/auth/')
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def admin_token(client, token):
    data = {
        'username': 'admin',
        'password': 'admin'
    }
    headers = { 'Authorization': 'Bearer ' + token }
    response = client.post('auth/login', headers=headers, json=data)
    data = json.loads(response.data)
    return data['token']

@pytest.fixture
def clean():
    yield
    clean_data()

def test_add_payment_method_success(client, admin_token, clean):
    data = {"method_name": "Visa", "config": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    print(response.data)
    assert response.status_code == 200

def test_add_payment_method_failed_missing_data(client, admin_token, clean):
    data = {"method_name": "Visa"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    assert response.status_code == 400

def test_add_payment_method_failed_duplicate_method(client, admin_token, clean):
    data = {"method_name": "bogo", "config": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.post('third_party/payment/add', headers=headers, json=data)
    assert response.status_code == 400

def test_add_payment_method_failed_not_logged_in(client, token, clean):
    data = {"method_name": "Visa", "config": {"key": "value"}}
    headers = { ' Authorization': 'Bearer ' + token }
    response = client.post('third_party/payment/add', json=data)
    assert response.status_code == 401

def test_edit_payment_method_success(client, admin_token, clean):
    data = {"method_name": "bogo", "editing_data": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 200

def test_edit_payment_method_failed_missing_data(client, admin_token, clean):
    data = {"method_name": "bogo"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 400

def test_edit_payment_method_failed_not_logged_in(client, token, clean):
    data = {"method_name": "bogo", "editing_data": {"key": "value"}}
    headers = { ' Authorization': 'Bearer ' + token }
    response = client.put('third_party/payment/edit', json=data)
    assert response.status_code == 401

def test_edit_payment_method_failed_wrong_name(client, admin_token, clean):
    data = {"method_name": "nothing", "editing_data": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.put('third_party/payment/edit', headers=headers, json=data)
    assert response.status_code == 400

def test_delete_payment_method_success(client, admin_token, clean):
    data = {"method_name": "bogo"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 200

def test_delete_payment_method_failed_missing_data(client, admin_token, clean):
    data = {}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 400

def test_delete_payment_method_failed_not_logged_in(client, token, clean):
    data = {"method_name": "bogo"}
    headers = { ' Authorization': 'Bearer ' + token }
    response = client.delete('third_party/payment/delete', json=data)
    assert response.status_code == 401

def test_delete_payment_method_failed_wrong_name(client, admin_token, clean):
    data = {"method_name": "nothing"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.delete('third_party/payment/delete', headers=headers, json=data)
    assert response.status_code == 400

def test_add_supply_method_success(client, admin_token, clean):
    data = {"method_name": "Fedex", "config": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 200

def test_add_supply_method_failed_missing_data(client, admin_token, clean):
    data = {"method_name": "Fedex"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 400

def test_add_supply_method_failed_duplicate_method(client, admin_token, clean):
    data = {"method_name": "bogo", "config": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.post('third_party/delivery/add', headers=headers, json=data)
    assert response.status_code == 400

def test_add_supply_method_failed_not_logged_in(client, token, clean):
    data = {"method_name": "Fedex", "config": {"key": "value"}}
    headers = { ' Authorization': 'Bearer ' + token }
    response = client.post('third_party/delivery/add', json=data)
    assert response.status_code == 401

def test_edit_supply_method_success(client, admin_token, clean):
    data = {"method_name": "bogo", "editing_data": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 200

def test_edit_supply_method_failed_missing_data(client, admin_token, clean):
    data = {"method_name": "bogo"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 400

def test_edit_supply_method_failed_not_logged_in(client, token, clean):
    data = {"method_name": "bogo", "editing_data": {"key": "value"}}
    headers = { ' Authorization': 'Bearer ' + token }
    response = client.put('third_party/delivery/edit', json=data)
    assert response.status_code == 401

def test_edit_supply_method_failed_wrong_name(client, admin_token, clean):
    data = {"method_name": "nothing", "editing_data": {"key": "value"}}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.put('third_party/delivery/edit', headers=headers, json=data)
    assert response.status_code == 400

def test_delete_supply_method_success(client, admin_token, clean):
    data = {"method_name": "bogo"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 200

def test_delete_supply_method_failed_missing_data(client, admin_token, clean):
    data = {}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 400

def test_delete_supply_method_failed_not_logged_in(client, token, clean):
    data = {"method_name": "bogo"}
    headers = { ' Authorization': 'Bearer ' + token }
    response = client.delete('third_party/delivery/delete', json=data)
    assert response.status_code == 401

def test_delete_supply_method_failed_wrong_name(client, admin_token, clean):
    data = {"method_name": "nothing"}
    headers = { 'Authorization': 'Bearer ' + admin_token }
    response = client.delete('third_party/delivery/delete', headers=headers, json=data)
    assert response.status_code == 400

# NEEDS TO BE IMPLEMENTED?
def test_cancel_membership_success(app, clean):
    pass
