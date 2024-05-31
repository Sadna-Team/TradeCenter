import unittest
from flask import Flask, appcontext_pushed, appcontext_popped

from backend.business.authentication.authentication import Authentication
from unittest.mock import MagicMock
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager



class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test_secret_key'  # Set a test secret key
        self.jwt = JWTManager(self.app)
        self.bcrypt = Bcrypt(self.app)
        self.auth = Authentication()
        self.auth.set_jwt(self.jwt, self.bcrypt)
        self.auth.user_facade = MagicMock()

        # Push application context for testing
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Pop application context after testing
        self.app_context.pop()

    def test_generate_token(self):
        token = self.auth.generate_token('test_user_id')
        self.assertIsInstance(token, str)

    def test_hash_password(self):
        password = 'test_password'
        hashed_password = self.auth.hash_password(password)
        self.assertIsInstance(hashed_password, str)
        self.assertNotEqual(password, hashed_password)

    def test_verify_password(self):
        password = 'test_password'
        hashed_password = self.auth.hash_password(password)
        self.assertTrue(self.auth.verify_password(password, hashed_password))
        self.assertFalse(self.auth.verify_password('wrong_password', hashed_password))

    def test_start_guest(self):
        self.auth.user_facade.create_user.return_value = 'guest_user_id'
        token = self.auth.start_guest()
        self.auth.user_facade.create_user.assert_called_once()
        self.assertIsInstance(token, str)

    def test_login_user(self):
        self.auth.user_facade.get_password.return_value = ('test_user_id', self.auth.hash_password('test_password'))
        token = self.auth.login_user('test_user', 'test_password')
        self.auth.user_facade.get_password.assert_called_once_with('test_user')
        self.assertIsInstance(token, str)
        with self.assertRaises(ValueError):
            self.auth.login_user('test_user', 'wrong_password')

    def test_logout_user(self):
        jti = 'test_jti'
        self.auth.logout_user(jti)
        self.assertIn(jti, self.auth.blacklist)


if __name__ == '__main__':
    unittest.main()
