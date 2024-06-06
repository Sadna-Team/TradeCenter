from datetime import timedelta
from .. import UserFacade
from flask_jwt_extended import create_access_token,decode_token


# from backend import bcrypt, jwt


class Authentication:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Authentication, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.user_facade = UserFacade()
            self.blacklist = set()
            self.logged_in = set()
            self.guests = set()
            self.jwt = None
            self.bcrypt = None

    def clean_data(self):
        """
        For testing purposes only
        """
        self.blacklist.clear()
        self.logged_in.clear()
        self.guests.clear()

    def set_jwt(self, jwt, bcrypt):
        self.jwt = jwt
        self.bcrypt = bcrypt

    def check_if_token_in_blacklist(self, jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return jti in self.blacklist

    def generate_token(self, user_id):
        while True:
            token = create_access_token(identity=user_id, expires_delta=timedelta(days=1))
            if decode_token(token)['jti'] not in self.blacklist:
                break
        return token

    def hash_password(self, password):
        # get bcrypt from app context
        return self.bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password, hashed_password):
        return self.bcrypt.check_password_hash(hashed_password, password)

    def register_user(self, user_id, user_credentials):
        if ('password' not in user_credentials
                or 'email' not in user_credentials
                or 'username' not in user_credentials
                or 'year' not in user_credentials
                or 'month' not in user_credentials
                or 'day' not in user_credentials
                or 'phone' not in user_credentials):
            raise ValueError("Some credentials are missing")
        hashed_password = self.hash_password(user_credentials['password'])
        email = user_credentials['email']
        username = user_credentials['username']
        year = user_credentials['year']
        month = user_credentials['month']
        day = user_credentials['day']
        phone = user_credentials['phone']
        self.user_facade.register_user(user_id, email, username, hashed_password, year, month, day, phone)
        # db.session.add(new_user)
        # db.session.commit()

    def start_guest(self) -> str:
        new_user_id = self.user_facade.create_user()
        token = self.generate_token(new_user_id)
        self.guests.add(new_user_id)
        return token

    # @jwt_required()
    def login_user(self, username: str, password: str):
        user_id, hashed_password = self.user_facade.get_password(username)
        if not self.verify_password(password, hashed_password):
            raise ValueError("Invalid credentials")
        elif user_id in self.logged_in:
            raise ValueError("User is already logged in")
        else:
            token = self.generate_token(user_id)
            notification = self.user_facade.get_notifications(user_id)
            self.logged_in.add(user_id)
            return token, notification

    def logout_user(self, jti, user_id):
        if user_id not in self.logged_in:
            raise ValueError("User is not logged in")
        else:
            self.blacklist.add(jti)
            self.logged_in.remove(user_id)
            return self.start_guest()

    def logout_guest(self, jti, user_id):
        if user_id not in self.guests:
            raise ValueError("User is not a guest")
        else:
            self.blacklist.add(jti)
            self.guests.remove(user_id)

    def is_logged_in(self, user_id):
        return user_id in self.logged_in
