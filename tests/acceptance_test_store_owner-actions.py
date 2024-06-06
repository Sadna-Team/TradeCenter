#write acceptance tests for store owner actions

import unittest
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
def client(app):
    return app.test_client()

def test_appoint_store_manager_success(client, owner_token, clean):
    data = {'username': 'new_manager'}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.post('/store/appoint_manager', headers=headers, json=data)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Manager appointed successfully'

def test_appoint_store_manager_invalid_member_credentials(client, owner_token, clean):
    data = {'username': 'invalid_user'}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.post('/store/appoint_manager', headers=headers, json=data)
    assert response.status_code == 404
    assert response.get_json()['message'] == 'User not found'

def test_appoint_store_manager_already_has_role_in_store(client, owner_token, clean):
    data = {'username': 'existing_manager'}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.post('/store/appoint_manager', headers=headers, json=data)
    assert response.status_code == 400
    assert response.get_json()['message'] == 'User already has a role in the store'

def test_appoint_store_manager_invalid_permissions_provided(client, owner_token, clean):
    data = {'username': 'user_with_invalid_permissions'}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.post('/store/appoint_manager', headers=headers, json=data)
    assert response.status_code == 403
    assert response.get_json()['message'] == 'Invalid permissions provided'

def accepting_manager_promotion_success(client, owner_token, clean):
    data = {'username': 'new_manager'}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.post('/store/accept_promotion', headers=headers, json=data)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Promotion accepted successfully'

def not_accepting_manager_promotion(client, owner_token, clean):
    data = {'username': 'new_manager'}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.post('/store/reject_promotion', headers=headers, json=data)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Promotion rejected successfully'

def test_change_store_manager_permissions_success(client, owner_token, clean):
    data = {'manager_id': 1, 'permissions': ['can_edit_products']}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.post('/store/change_permissions', headers=headers, json=data)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Permissions changed successfully'

def test_change_store_manager_permissions_invalid_manager_id(client, owner_token, clean):
    data = {'manager_id': 999, 'permissions': ['can_edit_products']}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.post('/store/change_permissions', headers=headers, json=data)
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Manager not found'

def test_change_store_manager_permissions_not_supervisor(client, owner_token, clean):
    data = {'manager_id': 2, 'permissions': ['can_edit_products']}
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.post('/store/change_permissions', headers=headers, json=data)
    assert response.status_code == 403
    assert response.get_json()['message'] == 'Not authorized to change permissions'

def test_view_employees_info_success(client, owner_token, clean):
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.get('/store/view_employees', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'employees' in data

def test_view_employees_info_invalid_store_id(client, owner_token, clean):
    headers = {'Authorization': 'Bearer ' + owner_token}
    response = client.get('/store/view_employees?store_id=9999', headers=headers)
    assert response.status_code == 404
    assert response.get_json()['message'] == 'Store not found'
