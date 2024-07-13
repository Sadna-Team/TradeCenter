import json

from .ecommerce_services.controllers import PurchaseService
from .store_services.controllers import StoreService
from .user_services.controllers import UserService, AuthenticationService
from flask_jwt_extended import get_jti


class initial_state:
    def __init__(self, file = 'initial_state.json'):
        self.purchase_service = PurchaseService()
        self.store_service = StoreService()
        self.user_service = UserService()
        self.authentication_service = AuthenticationService()

        self.file = file
        self.username_to_token = {}
        self.username_to_password = {}
        self.store_name_to_id = {}

    def create_user(self, username, password, email, phone, year, month, day):
        register_credentials = {
            'password': password,
            'email': email,
            'username': username,
            'year': year,
            'month': month,
            'day': day,
            'phone': phone
        }

        response = self.authentication_service.start_guest()
        if response.status_code != 200:
            return False
        token = response.json()['token']

        response = self.authentication_service.register(token, register_credentials)
        if response.status_code != 201:
            return False

        self.username_to_password[username] = password
        return True

    def login_user(self, username):
        token = self.username_to_token.get(username)
        password = self.username_to_password.get(username)
        if token is not None and password is not None:
            response = self.authentication_service.login(username, password)
            if response.status_code != 200:
                return False
            token = response.json()['token']
            self.username_to_token[username] = token

    def add_system_manager(self, username):
        response = self.user_service.add_system_manager(0, username)
        if response.status_code != 200:
            return False
        return True

    def add_store(self, username, store_name):
        token = self.username_to_token.get(username, None)
        if token is None:
            return False

        response = self.authentication_service.get_user_id(token)
        if response.status_code != 200:
            return False
        user_id = response.json()['user_id']

        response = self.store_service.add_new_store(user_id, 'address', 'city', 'state', 'country', '12345', store_name)
        if response.status_code != 200:
            return False
        return True

    def add_product(self, username, store_name, product_name, price, quantity):
        token = self.username_to_token.get(username, None)
        if token is None:
            return False

        response = self.authentication_service.get_user_id(token)
        if response.status_code != 200:
            return False
        user_id = response.json()['user_id']

        response = self.store_service.get_store_id(store_name)
        if response.status_code != 200:
            return False
        store_id = response.json()['store_id']

        # def add_product_to_store(self, user_id: int, store_id: int, product_name: str, description: str, price: float,
        response = self.store_service.add_product_to_store(user_id, store_id, product_name, 'description', price, 1, [],
                                                           quantity)
        if response.status_code != 200:
            return False
        return True

    def add_owner(self, username_actor, username, store_name):
        token = self.username_to_token.get(username_actor, None)
        if token is None:
            return False

        response = self.authentication_service.get_user_id(token)
        if response.status_code != 200:
            return False
        user_id = response.json()['user_id']

        response = self.store_service.get_store_id(store_name)
        if response.status_code != 200:
            return False
        store_id = response.json()['store_id']

        response = self.store_service.add_store_owner(user_id, store_id, username)
        if response.status_code != 200:
            return False

        token2 = self.username_to_token.get(username)
        if token2 is None:
            return False

        response = self.authentication_service.get_user_id(token2)
        if response.status_code != 200:
            return False
        user_id2 = response.json()['user_id']

        response = self.user_service.accept_promotion(user_id2, store_id, True)
        if response.status_code != 200:
            return False
        return True

    def add_manager(self, username_actor, username, store_name, permissions):
        token = self.username_to_token.get(username_actor, None)
        if token is None:
            return False

        response = self.authentication_service.get_user_id(token)
        if response.status_code != 200:
            return False
        user_id = response.json()['user_id']

        response = self.store_service.get_store_id(store_name)
        if response.status_code != 200:
            return False
        store_id = response.json()['store_id']

        response = self.store_service.add_store_manager(user_id, store_id, username)
        if response.status_code != 200:
            return False

        token2 = self.username_to_token.get(username)
        if token2 is None:
            return False

        response = self.authentication_service.get_user_id(token2)
        if response.status_code != 200:
            return False
        user_id2 = response.json()['user_id']

        response = self.user_service.accept_promotion(user_id2, store_id, True)
        if response.status_code != 200:
            return False

        response = self.store_service.edit_manager_permissions(user_id, store_id, user_id2, permissions)
        if response.status_code != 200:
            return False
        return True

    def logout(self, username):
        token = self.username_to_token.get(username)
        if token is not None:
            response = self.authentication_service.get_user_id(token)
            if response.status_code != 200:
                return False
            user_id = response.json()['user_id']

            jti = get_jti(token)
            response = self.authentication_service.logout(jti, user_id)
            if response.status_code != 200:
                return False
            del self.username_to_token[username]
            return True
        return False

    def init_system_from_file(self):
        with open(self.file, 'r') as file:
            initial_state = json.load(file)

        for action in initial_state['actions']:
            action_name = action['action']
            if action_name == 'create_user':
                success = self.create_user(
                    username=action['username'],
                    password=action['password'],
                    email=action['email'],
                    phone=action['phone'],
                    year=action['year'],
                    month=action['month'],
                    day=action['day']
                )
            elif action_name == 'set_admin':
                success = self.add_system_manager(action['username'])
            elif action_name == 'login':
                success = self.login_user(action['username'])
            elif action_name == 'create_store':
                success = self.add_store(action['username'], action['store_name'])
            elif action_name == 'add_product':
                success = self.add_product(
                    username=action['username'],
                    store_name=action['store_name'],
                    product_name=action['product_name'],
                    price=action['price'],
                    quantity=action['quantity']
                )
            elif action_name == 'assign_owner':
                success = self.add_owner(
                    username_actor=action['username'],
                    username=action['target_username'],
                    store_name=action['store_name']
                )
            elif action_name == 'assign_manager':
                success = self.add_manager(
                    username_actor=action['username'],
                    username=action['target_username'],
                    store_name=action['store_name'],
                    permissions=action['permissions']
                )
            elif action_name == 'logout':
                success = self.logout(action['username'])
            else:
                print(f"Unknown action: {action_name}")
                success = False

            if not success:
                print(f"Action {action_name} failed for {action}")
                return False
        return True


