import unittest
from flask import Flask, appcontext_pushed, appcontext_popped
from flask_jwt_extended import JWTManager, create_access_token, decode_token
from flask_bcrypt import Bcrypt
from backend.business.authentication.authentication import Authentication
from unittest.mock import MagicMock
from backend.error_types import *
from backend import create_app

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        # self.app = Flask(__name__)
        # self.app.config['SECRET_KEY'] = 'test_secret_key'  # Set a test secret key
        # from backend import app as app2
        # app2.app = self.app
        # self.jwt = JWTManager(self.app)
        # self.bcrypt = Bcrypt(self.app)
        # self.auth.set_jwt(self.jwt, self.bcrypt)
        self.app = create_app('testing')
        from backend import app as app2
        app2.app = self.app
        self.auth = Authentication()
        self.auth.clean_data()
        self.auth.user_facade = MagicMock()
        self.bcrypt = Bcrypt()


        # Push application context for testing
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Pop application context after testing
        self.app_context.pop()

    def test_singleton(self):
        auth = Authentication()
        self.assertEqual(self.auth, auth)

    def test_check_if_token_in_blacklist(self):
        token = create_access_token(identity='test_user_id')

        decoded = decode_token(token)
        jwt_header = {'alg': 'HS256', 'typ': 'JWT'}
        jti = decoded['jti']
        self.assertFalse(self.auth.check_if_token_in_blacklist(jwt_header, {'jti': jti}))
        self.auth.blacklist.add(jti)
        self.assertTrue(self.auth.check_if_token_in_blacklist(jwt_header, {'jti': jti}))

    def test_generate_token(self):
        token = self.auth.generate_token('test_user_id')
        decoded = decode_token(token)
        self.assertEqual(decoded['sub'], 'test_user_id')
        self.assertFalse(self.auth.check_if_token_in_blacklist({'alg': 'HS256', 'typ': 'JWT'}, {'jti': decoded['jti']}))
        self.assertIsInstance(token, str)

    def test_hash_password(self):
        password = 'test_password'
        hashed_password = self.auth.hash_password(password)
        self.assertIsInstance(hashed_password, str)
        self.assertNotEqual(password, hashed_password)
        self.assertTrue(self.auth.verify_password(password, hashed_password))

    def test_verify_password(self):
        password = 'test_password'
        hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')
        self.assertTrue(self.auth.verify_password(password, hashed_password))
        self.assertFalse(self.auth.verify_password('wrong_password', hashed_password))

    def test_start_guest(self):
        self.auth.user_facade.create_user.return_value = 1
        token = self.auth.start_guest()
        self.auth.user_facade.create_user.assert_called_once()
        self.assertIsInstance(token, str)
        self.assertIn(1, self.auth.guests)

    def test_login_user(self):
        self.auth.user_facade.get_password.return_value = (3, self.auth.hash_password('test_password'))
        token, _,_ = self.auth.login_user('test_user', 'test_password')
        self.auth.user_facade.get_password.assert_called_once_with('test_user')
        self.assertIsInstance(token, str)
        with self.assertRaises(UserError) as e:
            self.auth.login_user('test_user', 'test_password')
        assert e.exception.user_error_type == UserErrorTypes.user_logged_in
        with self.assertRaises(UserError) as e:
            self.auth.login_user('test_user', 'wrong_password')
        assert e.exception.user_error_type == UserErrorTypes.invalid_credentials

    def test_logout_user(self):
        jti = 'test_jti'
        self.auth.user_facade.create_user.return_value = 5
        self.auth.logged_in.add(3)
        self.auth.user_facade.create_user.return_value = 3
        self.auth.logout_user(jti, 3)
        self.assertIn(jti, self.auth.blacklist)
        self.assertNotIn(3, self.auth.logged_in)

    def test_logout_guest(self):
        jti = 'test_jti'
        self.auth.guests.add(3)
        self.auth.logout_guest(jti, 3)
        self.assertIn(jti, self.auth.blacklist)
        self.assertNotIn(3, self.auth.guests)

    def test_is_logged_in(self):
        self.auth.logged_in.add(3)
        self.assertTrue(self.auth.is_logged_in(3))
        self.assertFalse(self.auth.is_logged_in(4))

    def test_register_user(self):
        user_credentials = {
            'password': 'test_password',
            'email': 'test_email',
            'username': 'test_username',
            'year': 2000,
            'month': 1,
            'day': 1,
            'phone': 'test_phone'
        }
        self.auth.hash_password = MagicMock(return_value='hashed_password')
        self.auth.register_user(3, user_credentials)
        self.auth.user_facade.register_user.assert_called_once_with(3, 'test_email', 'test_username', 'hashed_password', 2000, 1, 1, 'test_phone')
        self.auth.hash_password.assert_called_once_with('test_password')


if __name__ == '__main__':
    unittest.main()
