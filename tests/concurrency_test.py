import pytest
from backend import create_app, clean_data

@pytest.fixture
def app():
    app = create_app()
    yield app
    clean_data()

@pytest.fixture
def client(app):
    return app.test_client()

def create_user(client, username, password):
    guest_token = client.get('auth/').get_json()['token']
    headers = {'Authorization': f'Bearer {guest_token}'}
    json = {'username': username, 'password': password}
    client.post('auth/register', headers=headers, json=json)

def login(client, username, password):
    guest_token = client.get('auth/').get_json()['token']
    headers = {'Authorization': f'Bearer {guest_token}'}
    json = {'username': username, 'password': password}
    return client.post('auth/login', headers=headers, json=json).get_json()['token']

@pytest.fixture
def admin_token(client):
    guest_token = client.get('auth/').get_json()['token']
    headers = {'Authorization': f'Bearer {guest_token}'}
    json = {'username': 'admin', 'password': 'admin'}
    return client.post('auth/login', headers=headers, json=json).get_json()['token']

def test_two_users_purchase_last_item_concurrently(client, admin_token):
    create_user(client, 'user1', 'password')
    create_user(client, 'user2', 'password')

    # User 1 logs in
    user1_token = login(client, 'user1', 'password')

    # User 2 logs in
    user2_token = login(client, 'user2', 'password')

    # admin adds a store
    headers = {'Authorization': f'Bearer {admin_token}'}
    json = {'name': 'store1', 'location_id': 1}
    client.post('store/add_store', headers=headers, json=json).get_json()

    # admin adds an item
    headers = {'Authorization': f'Bearer {admin_token}'}
    json = {'store_id': 0, 'product_name': 'item1', 'description': 'test product', 'price': 100, 'weight': 1, 'tags': ['test']}
    client.post('store/add_product', headers=headers, json=json).get_json()

    json = {'store_id': 0, 'product_id': 0, 'quantity': 1}
    client.post('store/restock_product', headers=headers, json=json)

    # user1 adds the item to cart
    headers = {'Authorization': f'Bearer {user1_token}'}
    json = {'store_id': 0, 'product_id': 0, 'quantity': 1}
    client.post('store/add_to_basket', headers=headers, json=json)

    # user2 adds the item to cart
    headers = {'Authorization': f'Bearer {user2_token}'}
    json = {'store_id': 0, 'product_id': 0, 'quantity': 1}
    client.post('store/add_to_basket', headers=headers, json=json)

    # user1 and user2 try to purchase the item at the same time (using threads)
    import threading
    import queue

    # create a queue to store the results
    results = queue.Queue()

    def purchase_item(token):
        headers = {'Authorization': f'Bearer {token}'}
        json = {"payment_details": {'payment method': 'bogo'},
            "supply_method": 'bogo',
            "address": {'address_id': 0, 
                            'address': 'randomstreet 34th', 
                            'city': 'arkham', 
                            'country': 'Wakanda', 
                            'state': 'Utopia', 
                            'postal_code': '12345'}
            }
        
        respones = client.post('market/checkout', headers=headers, json=json)
        results.put(respones.status_code)

    thread1 = threading.Thread(target=purchase_item, args=(user1_token,))
    thread2 = threading.Thread(target=purchase_item, args=(user2_token,))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    # check the results
    assert results.get() == 200
    assert results.get() == 400