# import pytest
# from backend import create_app, clean_data
# from ..backend.app import socketio
# from ..backend.socketio import send_real_time_notification

# register_credentials = { 
#         'username': 'test',
#         'email': 'test@gmail.com',
#         'password': 'test',
#         'location_id': 1,
#         'year': 2003,
#         'month': 1,
#         'day': 1,
#         'phone': '054-1234567' 
#         }

# @pytest.fixture
# def app():
#     app, socketio = create_app()
#     return app

# @pytest.fixture
# def client(app):
#     return app.test_client()

# @pytest.fixture
# def clean(app):
#     yield
#     clean_data()

# @pytest.fixture
# def token(client):
#     response = client.get('/auth/')
#     return response.get_json()['token']

# @pytest.fixture
# def owner_token(client, token):
#     headers = { 'Authorization': 'Bearer ' + token }
#     owner_register = register_credentials.copy()
#     owner_register['username'] = 'owner'
#     data = { 'register_credentials': owner_register }
#     client.post('auth/register', headers=headers, json=data)
    
#     headers = { 'Authorization': 'Bearer ' + token }
#     data = { "username": "test", "password": "test" }
#     response = client.post('auth/login', headers=headers, json=data)
#     return response.get_json()['token']

# @pytest.fixture
# def user_token(client, token):
#     headers = { 'Authorization': 'Bearer ' + token }
#     data = { 'register_credentials': register_credentials }
#     client.post('auth/register', headers=headers, json=data)

#     data = { "username": "test", "password": "test" }
#     response = client.post('auth/login', json=data)
#     return response.get_json()['token']

# def init_store(client, owner_token):
#     data = {'store_name': 'test_store', 'location_id': 1}
#     headers = { 'Authorization': 'Bearer ' + owner_token }
#     client.post('store/add_store', headers=headers, json=data)

#     # add item to store
#     data = {"store_id": 0, 
#         "product_name": "funny", 
#         "description": "test_description",
#         "price": 10.0,
#         "weight": 1.0,
#         "tags": ["tag1", "tag2"],
#         "amount": 10
#         }
#     client.post('store/add_product', headers=headers, json=data)

# def test_promote_manager_notification(client, user_token, owner_token):
#     init_store(client, owner_token)

#     socket_client = socketio.test_client()
#     socket_client.emit('join', { 'room': 'test' })
    
#     # add manager
#     headers = { 'Authorization': 'Bearer ' + owner_token }
#     data = { 'store_id': 0, 'username': 'test' }
#     client.post('store/add_store_manager', headers=headers, json=data)
    
#     # check if notification was sent
#     received = socket_client.get_received()
#     assert len(received) == 1
    
