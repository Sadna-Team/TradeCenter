import os
from datetime import datetime, timedelta
from flask import current_app
from .. import UserFacade
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from backend import bcrypt, jwt


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

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(self, jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return jti in self.blacklist

    def generate_token(self, user_id):
        token = create_access_token(identity=user_id, expires_delta=timedelta(days=1))
        return token

    def hash_password(self, password):
        # get bcrypt from app context
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password, hashed_password):
        return bcrypt.check_password_hash(hashed_password, password)

    def register_user(self, user_id, user_credentials):
        hashed_password = self.hash_password(user_credentials['password'])
        location_id = user_credentials['location_id']
        email = user_credentials['email']
        username = user_credentials['username']
        year = user_credentials['year']
        month = user_credentials['month']
        day = user_credentials['day']
        phone = user_credentials['phone']
        self.user_facade.register_user(user_id, location_id, email, username, hashed_password, year, month, day, phone)
        # db.session.add(new_user)
        # db.session.commit()

    def start_guest(self) -> str:
        new_user_id = self.user_facade.create_user()
        token = self.generate_token(new_user_id)
        return token

    # @jwt_required()
    def login_user(self, user_id: int, username: str, password: str):
        user_id, hashed_password = self.user_facade.get_password(username)
        if self.verify_password(password, hashed_password):
            return self.generate_token(user_id)
        else:
            raise ValueError("Invalid credentials")

    def logout_user(self, jti):
        self.blacklist.add(jti)
