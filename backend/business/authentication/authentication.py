from datetime import timedelta
from .. import UserFacade
from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity
from backend.error_types import *
import logging
from backend.database import db
from flask import current_app

logger = logging.getLogger('myapp')


class AuthenticationModel(db.Model):
    __tablename__ = 'authentication'
    __table_args__ = (
        db.UniqueConstraint('blacklisted_token', name='uq_blacklisted_token'),
    )

    blacklisted_token = db.Column(db.String(100), primary_key=True)

    def __init__(self, blacklisted_token):
        self.blacklisted_token = blacklisted_token


class Authentication:
    # Singleton instance
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
            self.load_blacklist_from_db()  # Load the blacklist from the database

    def clean_data(self):
        """
        For testing purposes only
        """
        from backend.app import app
        with app.app_context():
            # with db.session.begin():
            #     db.session.query(Authentication).delete()
            db.session.query(AuthenticationModel).delete()
            db.session.commit()
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
            raise UserError("Some credentials are missing", UserErrorTypes.missing_credentials)
        hashed_password = self.hash_password(user_credentials['password'])
        email = user_credentials['email']
        username = user_credentials['username']
        year = user_credentials['year']
        month = user_credentials['month']
        day = user_credentials['day']
        phone = user_credentials['phone']
        self.user_facade.register_user(user_id, email, username, hashed_password, year, month, day, phone)

    def start_guest(self) -> str:
        new_user_id = self.user_facade.create_user()
        token = self.generate_token(new_user_id)
        self.guests.add(new_user_id)
        logger.info('guest entered the app successfully - user_id: ' + str(new_user_id))
        return token

    def login_user(self, username: str, password: str):
        user_id, hashed_password = self.user_facade.get_password(username)
        if not self.verify_password(password, hashed_password):
            raise UserError("Invalid credentials", UserErrorTypes.invalid_credentials)
        elif user_id in self.logged_in:
            raise UserError("User is already logged in", UserErrorTypes.user_logged_in)
        else:
            token = self.generate_token(user_id)
            notification = self.user_facade.get_notifications(user_id)
            self.logged_in.add(user_id)
            return token, notification, user_id

    def logout_user(self, jti, user_id):
        if user_id not in self.logged_in:
            raise UserError("User is not logged in", UserErrorTypes.user_not_logged_in)
        else:
            with db.session.begin():
                db.session.add(AuthenticationModel(blacklisted_token=jti))
            self.blacklist.add(jti)
            self.logged_in.remove(user_id)
            return self.start_guest()

    def logout_guest(self, jti, user_id):
        if user_id not in self.guests:
            raise UserError("User is not a guest", UserErrorTypes.user_is_not_guest)
        else:
            with db.session.begin():
                db.session.add(AuthenticationModel(blacklisted_token=jti))
            self.blacklist.add(jti)
            self.guests.remove(user_id)
            UserFacade.remove_user(user_id)

    def is_logged_in(self, user_id):
        set = self.logged_in
        ans = user_id in set

        logger.info(f'User {user_id} is logged in: {ans}')
        return ans

    def get_user_id(self, token):
        decoded = decode_token(token)
        return decoded['sub']
        

    def load_blacklist_from_db(self):
        """
        Load the blacklist from the database into the blacklist set
        """
        from backend.app import app
        with app.app_context():
            blacklisted_tokens = db.session.query(AuthenticationModel.blacklisted_token).all()
        self.blacklist = {token[0] for token in blacklisted_tokens}
