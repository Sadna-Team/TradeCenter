import json
from flask_jwt_extended import get_jti, decode_token
from .ecommerce_services.controllers import PurchaseService
from .store_services.controllers import StoreService
from .user_services.controllers import UserService, AuthenticationService
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from backend.database import clear_database
from backend.business import market

class InitialState:

    def __init__(self, app, db, file='backend/services/initial_state.json'):
        self.purchase_service = PurchaseService()
        self.store_service = StoreService()
        self.user_service = UserService()
        self.authentication_service = AuthenticationService()

        self.app = app
        self.db = db
        self.file = file
        self.username_to_token = {}  # username -> token
        self.username_to_password = {}  # username -> password

        self.logged_in = set()
        self.guests = set()

        self.store_name_to_id = {}
        self.counter = 0

    def create_user(self, username, password, email, phone, year, month, day):
        with self.app.app_context():
            register_credentials = {
                'password': password,
                'email': email,
                'username': username,
                'year': year,
                'month': month,
                'day': day,
                'phone': phone
            }

            response, status_code = self.authentication_service.start_guest()
            if status_code != 200:
                return False
            token = response.json['token']
            user_id = decode_token(token)['sub']

            response, status_code = self.authentication_service.register(user_id, register_credentials)
            if status_code != 201:
                return False

            self.username_to_password[username] = password
            self.username_to_token[username] = token
            self.guests.add(username)
            return True

    def login_user(self, username):
        with self.app.app_context():
            token = self.username_to_token.get(username)
            password = self.username_to_password.get(username)
            if token is not None and password is not None:
                response, status_code =  self.authentication_service.login(username, password)
                if status_code != 200:
                    return False
                token = response.json['token']
                self.username_to_token[username] = token
                self.logged_in.add(username)
                self.guests.remove(username)
                return True
        return False

    def add_system_manager(self, username):
        with self.app.app_context():
            response, status_code =  self.user_service.add_system_manager(0, username)
            if status_code != 200:
                return False
            return True

    def add_store(self, username, store_name):
        with self.app.app_context():
            token = self.username_to_token.get(username, None)
            if token is None:
                return False

            response, status_code =  self.authentication_service.get_user_id(token)
            if status_code != 200:
                return False
            user_id = response.json['user_id']

            response, status_code =  self.store_service.add_new_store(user_id, 'address', 'city', 'state', 'country', '12345',
                                                        store_name)
            if status_code != 200:
                return False
            return True

    def add_product(self, username, store_name, product_name, price, quantity):
        with self.app.app_context():
            token = self.username_to_token.get(username, None)
            if token is None:
                return False

            response, status_code =  self.authentication_service.get_user_id(token)
            if status_code != 200:
                raise ValueError(f"Failed to get user id for {username}\n status code: {status_code}\n response: {response.json}")
            user_id = response.json['user_id']

            response, status_code =  self.store_service.get_store_id(store_name)
            if status_code != 200:
                raise ValueError(f"Failed to get store id for {store_name}\n status code: {status_code}\n response: {response.json}")
            store_id = response.json['message']
            response, status_code =  self.store_service.add_product_to_store(user_id, store_id, product_name, 'description', price, 1,
                                                               [], quantity)
            if status_code != 200:
                raise ValueError(f"Failed to add product {product_name} to store {store_name}\n status code: {status_code}\n response: {response.json}")
            return True

    def add_owner(self, username_actor, username, store_name):
        with self.app.app_context():
            token = self.username_to_token.get(username_actor, None)
            if token is None:
                return False

            response, status_code =  self.authentication_service.get_user_id(token)
            if status_code != 200:
                return False
            user_id = response.json['user_id']

            response, status_code =  self.store_service.get_store_id(store_name)
            if status_code != 200:
                return False
            store_id = response.json['message']

            response, status_code =  self.store_service.add_store_owner(user_id, store_id, username)
            if status_code != 200:
                return False

            token2 = self.username_to_token.get(username)
            if token2 is None:
                return False

            response, status_code =  self.authentication_service.get_user_id(token2)
            if status_code != 200:
                return False
            user_id2 = response.json['user_id']

            response, status_code =  self.user_service.accept_promotion(user_id2, self.counter, True)
            if status_code != 200:
                return False
            self.counter += 1
            return True

    def add_manager(self, username_actor, username, store_name, permissions):
        with self.app.app_context():
            token = self.username_to_token.get(username_actor, None)
            if token is None:
                return False

            response, status_code =  self.authentication_service.get_user_id(token)
            if status_code != 200:
                return False
            user_id = response.json['user_id']

            response, status_code =  self.store_service.get_store_id(store_name)
            if status_code != 200:
                return False
            store_id = response.json['message']

            response, status_code =  self.store_service.add_store_manager(user_id, store_id, username)
            if status_code != 200:
                return False

            token2 = self.username_to_token.get(username)
            if token2 is None:
                return False

            response, status_code =  self.authentication_service.get_user_id(token2)
            if status_code != 200:
                return False
            user_id2 = response.json['user_id']

            response, status_code =  self.user_service.accept_promotion(user_id2, self.counter, True)
            if status_code != 200:
                return False
            self.counter += 1

            response, status_code =  self.store_service.edit_manager_permissions(user_id, store_id, user_id2, permissions)
            if status_code != 200:
                return False
            return True

    def logout(self, username):
        with self.app.app_context():
            token = self.username_to_token.get(username)
            if token is not None:
                response, status_code =  self.authentication_service.get_user_id(token)
                if status_code != 200:
                    return False
                user_id = response.json['user_id']

                jti = get_jti(token)
                response, status_code =  self.authentication_service.logout(jti, user_id)
                if status_code != 200:
                    return False
                del self.username_to_token[username]
                self.logged_in.remove(username)
                return True
            return False

    def logout_guest(self, username):
        with self.app.app_context():
            token = self.username_to_token.get(username)
            if token is not None:
                user_id = decode_token(token)['sub']
                jti = get_jti(token)
                response, status_code = self.authentication_service.logout_guest(jti, user_id)
                if status_code != 200:
                    return False
                del self.username_to_token[username]
                self.guests.remove(username)
                return True
            return False

    def init_system_from_file(self):
        reset = input("Reset database? (y/n): ")
        if reset.lower() == 'n':
            return False
        print("Initializing system from file...")
        with self.app.app_context():
            session: Session = self.db.session  # Get the SQLAlchemy session
            try:
                clear_database()
                with session.begin():  # Start a transaction
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
                            raise ValueError(f"Action {action_name} failed for {action}")

                    logged_in = self.logged_in.copy()
                    guests = self.guests.copy()

                    for username in logged_in:
                        self.logout(username)
                    for username in guests:
                        self.logout_guest(username)

                return True

            except (SQLAlchemyError, ValueError) as e:
                print(f"Initialization failed: {e}")
                session.rollback()  # Roll back the transaction
                return False
