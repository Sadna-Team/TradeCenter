# import pytest
# from backend import create_app
#
#
# @pytest.fixture
# def app():
#     app = create_app()
#     return app
#
#
# @pytest.fixture
# def client(app):
#     return app.test_client()
#
#
# @pytest.fixture
# def runner(app):
#     return app.test_cli_runner()
#
#
# @pytest.fixture
# def start(client):
#     response = client.get('/auth/')
#     assert response.status_code == 200
#     token = response.json['token']
#     register_credentials = {
#         'username': 'test',
#         'email': 'test@mail.com',
#         'password': 'test',
#         'year': 2003,
#         'month': 1,
#         'day': 1,
#         'phone': '054-1234567'
#     }
#     response = client.post('/auth/register',
#                            json={'register_credentials': register_credentials},
#                            headers={'Authorization': 'Bearer ' + token})
#     assert response.status_code == 201
#     header = {'Authorization': 'Bearer ' + response.json['token']}
#     response = client.post('/auth/login',
#                            json={'username': 'test', 'password': 'test'},
#                            headers=header)
#     assert response.status_code == 200
#
#     data = {'location_id': 1, 'store_name': 'test_store'}
#     response = client.post('/store/add_store', json=data, headers=header)
#     assert response.status_code == 200
#
#
# @pytest.mark.usefixtures('client')
# class TestStoreEndpoints2:
#
#     @pytest.fixture
#     def test_nominated_store_owner(self, client, start):
#         new_user_token = client.get('/auth/').json['token']
#         register_credentials = {
#             'username': 'test2',
#             'email': 'test2@mail.com',
#             'password': 'test2',
#             'year': 2003,
#             'month': 1,
#             'day': 1,
#             'phone': '054-1234567'
#         }
#         response = client.post('/auth/register',
#                                json={'register_credentials': register_credentials},
#                                headers={'Authorization': 'Bearer ' + new_user_token})
#         assert response.status_code == 201
#
#         response = client.post('/auth/login',
#                                json={'username': 'test2', 'password': 'test2'},
#                                headers={'Authorization': 'Bearer ' + new_user_token})
#         assert response.status_code == 200
#         new_user_token = response.json['token']
#
#         data = {'location_id': 1, 'new_user_id': 2}
#
#         response = client.post('/store/add_store_owner', json=data,
#                                headers={'Authorization': 'Bearer ' + new_user_token})
#         assert response.status_code == 200
#         return new_user_token