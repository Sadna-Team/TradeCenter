import unittest
from backend.business.user.user import *
from backend.business.DTOs import NotificationDTO
import datetime
from unittest.mock import patch, MagicMock
from backend.error_types import *
import pytest
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from backend import create_app
from backend.business.user.user import UserFacade, User, ShoppingCart, ShoppingBasket, Notification
from backend.error_types import UserError, UserErrorTypes, StoreError, StoreErrorTypes

class TestShoppingBasket(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global app
        app = create_app(mode='testing')
        app_context = app.app_context()
        app_context.push()

    @classmethod
    def tearDownClass(cls):
        from backend.database import clear_database
        clear_database()
        UserFacade().clean_data()
        app_context = app.app_context()
        # app_context.pop()

    def setUp(self):
        self.facade = UserFacade()
        self.connection = db.engine.connect()
        self.transaction = self.connection.begin()

    def test_add_product(self):
        basket = ShoppingBasket(store_id=1, user_id=1)
        basket.add_product(100, 1)
        self.assertEqual(basket.get_dto(), {100: 1})

    def test_add_product_duplicate(self):
        basket = ShoppingBasket(store_id=1, user_id=1)
        basket.add_product(100, 1)
        basket.add_product(100, 1)
        self.assertEqual(basket.get_dto(), {100: 2})

    def test_remove_product(self):
        basket = ShoppingBasket(store_id=1, user_id=1)
        basket.add_product(100, 1)
        basket.remove_product(100, 1)
        self.assertNotIn(100, basket.get_dto())
        self.assertEqual(basket.get_dto(), {})

    def test_remove_product_not_found(self):
        basket = ShoppingBasket(store_id=1, user_id=1)
        with self.assertRaises(StoreError) as e:
            basket.remove_product(100, 1)
        assert e.exception.store_error_type == StoreErrorTypes.product_not_found

# class TestShoppingCart(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         global app
#         app = create_app(mode='testing')
#         app_context = app.app_context()
#         app_context.push()

#     @classmethod
#     def tearDownClass(cls):
#         UserFacade.clean_data()
#         app_context = app.app_context()
#         app_context.pop()

#     def test_add_product_to_basket(self):
#         cart = ShoppingCart(user_id=0)
#         cart.add_product_to_basket(store_id=1, product_id=100, quantity=1)
#         self.assertEqual(cart.get_dto(), {1: {100: 1}})

#     def test_remove_product_from_basket(self):
#         cart = ShoppingCart(user_id=1)
#         cart.add_product_to_basket(store_id=1, product_id=100, quantity=1)
#         cart.remove_product_from_basket(store_id=1, product_id=100, quantity=1)
#         self.assertEqual(cart.get_dto(), {1: {}})

#     def test_remove_product_from_basket_store_not_found(self):
#         cart = ShoppingCart(user_id=1)
#         with self.assertRaises(StoreError) as e:
#             cart.remove_product_from_basket(store_id=1, product_id=100, quantity=1)
#         assert e.exception.store_error_type == StoreErrorTypes.store_not_found

class TestNotification(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global app
        app = create_app(mode='testing')
        app_context = app.app_context()
        app_context.push()

    @classmethod
    def tearDownClass(cls):
        UserFacade().clean_data()
        app_context = app.app_context()
        # app_context.pop()

    def setUp(self):
        self.facade = UserFacade()
        self.connection = db.engine.connect()
        self.transaction = self.connection.begin()

    def test_get_notification_dto(self):
        date = datetime.datetime.now()
        notification = Notification(message="Test Message", date=date)

        dto = notification.get_notification_dto()
        # self.assertEqual(dto.get_notification_id(), 1)
        self.assertEqual(dto.get_message(), "Test Message")
        self.assertEqual(dto.get_date(), date)

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global app
        app = create_app(mode='testing')
        app_context = app.app_context()
        app_context.push()

    @classmethod
    def tearDownClass(cls):
        from backend.database import clear_database
        clear_database()
        UserFacade().clean_data()
        app_context = app.app_context()
        # app_context.pop()

    def setUp(self):
        self.facade = UserFacade()
        self.connection = db.engine.connect()
        self.transaction = self.connection.begin()

    @patch('backend.business.user.user.c.currencies', ['USD', 'EUR'])
    def test_init_user_currency_supported(self):
        user = User(user_id=1, currency='USD')
        self.assertEqual(user.get_shopping_cart(), {})

    @patch('backend.business.user.user.c.currencies', ['USD', 'EUR'])
    def test_init_user_currency_not_supported(self):
        with self.assertRaises(UserError) as e:
            User(user_id=2, currency='GBP')
        assert e.exception.user_error_type == UserErrorTypes.currency_not_supported

    @patch.object(ShoppingBasket, 'add_product')
    def test_add_product_to_basket(self, mock_add_product):
        user = User(user_id=3, currency='USD')
        user.add_product_to_basket(store_id=1, product_id=100, quantity=1)
        mock_add_product.assert_called_with(100, 1)

    @patch.object(ShoppingBasket, 'remove_product')
    def test_remove_product_from_basket(self, mock_remove_product):
        user = User(user_id=4, currency='USD')
        user.add_product_to_basket(store_id=1, product_id=100, quantity=1)
        user.remove_product_from_basket(store_id=1, product_id=100, quantity=1)
        mock_remove_product.assert_called_with(100, 1)

    def test_subtract_product_from_cart(self):
        user = User(user_id=5, currency='USD')
        user.add_product_to_basket(store_id=1, product_id=100, quantity=2)
        user.remove_product_from_basket(store_id=1, product_id=100, quantity=1)
        self.assertEqual(user.get_shopping_cart(), {1: {100: 1}})

    def test_get_shopping_cart(self):
        user = User(user_id=6, currency='USD')
        user.add_product_to_basket(store_id=1, product_id=100, quantity=1)
        self.assertEqual(user.get_shopping_cart(), {1: {100: 1}})

    def test_register(self):
        user = User(user_id=7, currency='USD')
        user.register(email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        self.assertEqual(user.get_password(), "password")
        self.assertTrue(user.is_member())

    def test_register_already_registered(self):
        user = User(user_id=8, currency='USD')
        user.register(email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")

        with self.assertRaises(UserError) as e:
            user.register(email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        assert e.exception.user_error_type == UserErrorTypes.user_already_registered

    def test_get_notifications(self):
        user = User(user_id=9, currency='USD')
        user.register(email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        self.assertEqual(user.get_notifications(), [])
        user.add_notification(Notification("Test Message", datetime.datetime.now()))
        self.assertEqual(len(user.get_notifications()), 1)

    def test_get_password_member(self):
        user = User(user_id=10, currency='USD')
        user.register(email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        self.assertEqual(user.get_password(), "password")

    def test_get_password_guest(self):
        user = User(user_id=11, currency='USD')
        with self.assertRaises(UserError) as e:
            user.get_password()
        assert e.exception.user_error_type == UserErrorTypes.user_not_registered

    def test_clear_basket(self):
        user = User(user_id=12, currency='USD')
        user.add_product_to_basket(store_id=1, product_id=100, quantity=1)
        user.clear_basket()
        self.assertEqual(user.get_shopping_cart(), {})

    def test_suspend_user(self):
        user = User(user_id=13, currency='USD')
        user.register(email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        assert not user.is_suspended()

class TestUserFacade(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global app
        app = create_app(mode='testing')
        app_context = app.app_context()
        app_context.push()

    @classmethod
    def tearDownClass(cls):
        global app
        from backend.database import clear_database
        with app.app_context():
            clear_database()
        UserFacade().clean_data()
        app_context = app.app_context()
        # app_context.pop()

    def clear(self):
        with app.app_context():
            from backend.database import clear_database
            clear_database()
            UserFacade().clean_data()

    def setUp(self):
        self.facade = UserFacade().new_instance()
        self.connection = db.engine.connect()
        self.transaction = self.connection.begin()

    def tearDown(self):
        self.facade.clean_data()

    def test_get_instance(self):
        instance = UserFacade()
        self.assertIsInstance(instance, UserFacade)

    def test_get_users_dto_empty(self):
        self.assertEqual(self.facade.get_users_dto({}), {})

    # @patch.object(UserFacade, 'get_users_dto')
    # def test_get_users_dto(self, mock_get_users_dto):
    #     mock_get_users_dto.return_value = {'test': 'test'}
    #     result = self.facade.get_users_dto()
    #     self.assertEqual(result, {'test': 'test'})
    #     mock_get_users_dto.assert_called_once()
    #
    # @patch.object(UserFacade, 'get_user')

    def test_user_register(self):
        user = self.facade.create_user()
        self.facade.register_user(user, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        user = self.facade.get_user(user)
        self.assertIsInstance(user, User)
        self.assertEqual(user.get_username(), "testuser")

    def test_user_register_already_registered(self):
        user = self.facade.create_user()
        self.facade.register_user(user, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        with self.assertRaises(UserError) as e:
            self.facade.register_user(user, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        assert e.exception.user_error_type == UserErrorTypes.user_already_registered

    def test_suspend_user(self):
        user = self.facade.create_user()
        self.facade.register_user(user, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        self.facade.suspend_user_permanently(user_id=user)
        assert self.facade.get_user(user).is_suspended()

    def test_notify_user(self):
        self.clear()
        # delete magic mock - reset to original
        user = self.facade.create_user()
        self.facade.register_user(user, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        self.assertEqual(self.facade.get_notifications(user_id=user), [])
        # self.facade.notify_user(user_id=user, notification=NotificationDTO(0, "Test Message", datetime.datetime.now()))
        # self.assertEqual(len(self.facade.get_notifications(user_id=user)), 1)
