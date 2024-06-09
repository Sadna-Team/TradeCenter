import pytest
from backend import create_app, clean_data

register_credentials = { 
    'username': '',
    'email': 'test@gmail.com',
    'password': 'test',
    'location_id': 1,
    'year': 2003,
    'month': 1,
    'day': 1,
    'phone': '054-1234567'
    }

checkout_dict = {"payment_details": {'payment method': 'bogo'},
                    "supply_method": 'bogo',
                    "address": {'address_id': 0, 
                        'address': 'randomstreet 34th', 
                        'city': 'arkham', 
                        'country': 'Wakanda', 
                        'state': 'Utopia', 
                        'postal_code': '12345'}
                }

@pytest.fixture
def app():
    app = create_app()
    yield app
    clean_data()

@pytest.fixture
def client(app):
    return app.test_client()

def create_user(client, username):
    guest_token = client.get('auth/').get_json()['token']
    headers = {'Authorization': f'Bearer {guest_token}'}
    data = register_credentials.copy()
    data['username'] = username
    json = {'register_credentials': data}
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

@pytest.fixture
def add_store(client, admin_token):
    headers = {'Authorization': f'Bearer {admin_token}'}
    json = {'store_name': 'store1', 'location_id': 1}
    client.post('store/add_store', headers=headers, json=json)

@pytest.fixture
def add_item(client, admin_token):
    headers = {'Authorization': f'Bearer {admin_token}'}
    json = {'store_id': 0, 'product_name': 'item1', 'description': 'test product', 'price': 100, 'weight': 1, 'tags': ['test']}
    client.post('store/add_product', headers=headers, json=json).get_json()
    json = {'store_id': 0, 'product_id': 0, 'quantity': 1}
    client.post('store/restock_product', headers=headers, json=json)

def test_two_users_purchase_last_item_concurrently(client, admin_token, add_store, add_item):
    create_user(client, 'user1')
    create_user(client, 'user2')

    # User 1 logs in
    user1_token = login(client, 'user1', 'test')

    # User 2 logs in
    user2_token = login(client, 'user2', 'test')

    # user1 adds the item to cart
    headers = {'Authorization': f'Bearer {user1_token}'}
    json = {'store_id': 0, 'product_id': 0, 'quantity': 1}
    client.post('user/add_to_basket', headers=headers, json=json)

    # user2 adds the item to cart
    headers = {'Authorization': f'Bearer {user2_token}'}
    json = {'store_id': 0, 'product_id': 0, 'quantity': 1}
    client.post('user/add_to_basket', headers=headers, json=json)

    # user1 and user2 try to purchase the item at the same time (using threads)
    import threading
    import queue

    # create a queue to store the results
    results = queue.Queue()

    def purchase_item(token):
        headers = {'Authorization': f'Bearer {token}'}
        json = checkout_dict
        respones = client.post('market/checkout', headers=headers, json=json)
        results.put(respones.status_code)

    thread1 = threading.Thread(target=purchase_item, args=(user1_token,))
    thread2 = threading.Thread(target=purchase_item, args=(user2_token,))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    res = [0, 0]
    # check the results
    for _ in range(2):
        if results.get() == 200:
            res[0] += 1
        else:
            res[1] += 1
    assert res == [1, 1]

    # concurrency issues
    # assert results.get() == 200
    # assert results.get() == 400

    clean_data()

def test_user_purchases_item_while_admin_removes_item_from_store(client, admin_token, add_store, add_item):
    create_user(client, 'user1')

    # User 1 logs in
    user1_token = login(client, 'user1', 'test')

    # user1 adds the item to cart
    headers = {'Authorization': f'Bearer {user1_token}'}
    json = {'store_id': 0, 'product_id': 0, 'quantity': 1}
    client.post('user/add_to_basket', headers=headers, json=json)

    # user1 checkout with item while admin removes the item from the store (using threads)
    import threading
    import queue

    # create a queue to store the results
    results = queue.Queue()

    def purchase_item(token):
        headers = {'Authorization': f'Bearer {token}'}
        json = checkout_dict 
        respones = client.post('market/checkout', headers=headers, json=json)
        results.put(respones)
    
    def remove_item():
        headers = {'Authorization': f'Bearer {admin_token}'}
        json = {'store_id': 0, 'product_id': 0}
        respones = client.post('store/remove_product', headers=headers, json=json)
        #results.put(respones.status_code)

    thread1 = threading.Thread(target=purchase_item, args=(user1_token,))
    thread2 = threading.Thread(target=remove_item)

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    # check the results
    ans = results.get()
    assert ans.status_code == 200 or (ans.status_code == 400 and ans.get_json()['message'] == 'Product is not found') # error message taken from new_store.py/remove_product_amount()


def test_two_owners_promoting_a_manager_at_the_same_time(client, admin_token, add_store):
    # create two owners
    create_user(client, 'owner1')
    owner1_token = login(client, 'owner1', 'test')
    
    create_user(client, 'owner2')
    owner2_token = login(client, 'owner2', 'test')

    # promote owner1 to owner
    headers = {'Authorization': f'Bearer {admin_token}'}
    json = {'store_id': 0, 'username': 'owner1'}
    client.post('store/add_store_owner', headers=headers, json=json)

    # promote owner2 to owner
    headers = {'Authorization': f'Bearer {admin_token}'}
    json = {'store_id': 0, 'username': 'owner2'}
    client.post('store/add_store_owner', headers=headers, json=json)

    # owner1 and owner2 accept the promotion
    headers = {'Authorization': f'Bearer {owner1_token}'}
    json = {'promotion_id': 0, 'accept': True}
    client.post('user/accept_promotion', headers=headers, json=json)

    headers = {'Authorization': f'Bearer {owner2_token}'}
    json = {'promotion_id': 1, 'accept': True}
    client.post('user/accept_promotion', headers=headers, json=json)

    # create user (manager)
    create_user(client, 'manager')
    
    # both owner1 and owner2 promote the manager to manager at the same time (using threads)
    import threading
    import queue

    # create a queue to store the results
    results = queue.Queue()

    def promote_manager(token):
        headers = {'Authorization': f'Bearer {token}'}
        json = {'store_id': 0, 'username': 'manager'}
        respones = client.post('store/add_store_manager', headers=headers, json=json)
        results.put(respones.status_code)
    
    thread1 = threading.Thread(target=promote_manager, args=(owner1_token,))
    thread2 = threading.Thread(target=promote_manager, args=(owner2_token,))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    res = [0, 0]
    # check the results
    for _ in range(2):
        if results.get() == 200:
            res[0] += 1
        else:
            res[1] += 1
    assert res == [1, 1]

    clean_data()