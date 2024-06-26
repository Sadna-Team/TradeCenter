import unittest
from backend.business.user.user import *
from backend.business.DTOs import NotificationDTO
import datetime
from unittest.mock import patch, MagicMock
from backend.error_types import *

class TestShoppingBasket(unittest.TestCase):

    def test_add_product(self):
        basket = ShoppingBasket(store_id=1)
        basket.add_product(100, 1)
        self.assertEqual(basket.get_dto(), {100: 1})

    def test_add_product_duplicate(self):
        basket = ShoppingBasket(store_id=1)
        basket.add_product(100, 1)
        basket.add_product(100, 1)
        self.assertEqual(basket.get_dto(), {100: 2})

    def test_remove_product(self):
        basket = ShoppingBasket(store_id=1)
        basket.add_product(100, 1)
        basket.remove_product(100, 1)
        self.assertNotIn(100, basket.get_dto())
        self.assertEqual(basket.get_dto(), {})

    def test_remove_product_not_found(self):
        basket = ShoppingBasket(store_id=1)
        with self.assertRaises(StoreError) as e:
            basket.remove_product(100, 1)
        assert e.exception.store_error_type == StoreErrorTypes.product_not_found

class TestShoppingCart(unittest.TestCase):

    def test_add_product_to_basket(self):
        cart = ShoppingCart(user_id=1)
        cart.add_product_to_basket(store_id=1, product_id=100, quantity=1)
        self.assertEqual(cart.get_dto(), {1: {100: 1}})

    def test_remove_product_from_basket(self):
        cart = ShoppingCart(user_id=1)
        cart.add_product_to_basket(store_id=1, product_id=100, quantity=1)
        cart.remove_product_from_basket(store_id=1, product_id=100, quantity=1)
        self.assertEqual(cart.get_dto(), {1: {}})

    def test_remove_product_from_basket_store_not_found(self):
        cart = ShoppingCart(user_id=1)
        with self.assertRaises(StoreError) as e:
            cart.remove_product_from_basket(store_id=1, product_id=100, quantity=1)
        assert e.exception.store_error_type == StoreErrorTypes.store_not_found


class TestState(unittest.TestCase):

    def test_guest_get_password(self):
        guest = Guest()
        with self.assertRaises(UserError) as e:
            guest.get_password()
        assert e.exception.user_error_type == UserErrorTypes.user_not_registered

    def test_member_get_password(self):
        member = Member(email="test@example.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        self.assertEqual(member.get_password(), "password")


class TestNotification(unittest.TestCase):

    def test_get_notification_dto(self):
        date = datetime.datetime.now()
        notification = Notification(notification_id=1, message="Test Message", date=date)
        dto = notification.get_notification_dto()
        self.assertEqual(dto.get_notification_id(), 1)
        self.assertEqual(dto.get_message(), "Test Message")
        self.assertEqual(dto.get_date(), date)


class TestUser(unittest.TestCase):

    @patch('backend.business.user.user.c.currencies', ['USD', 'EUR'])
    def test_init_user_currency_supported(self):
        user = User(user_id=1, currency='USD')
        self.assertEqual(user.get_shopping_cart(), {})

    @patch('backend.business.user.user.c.currencies', ['USD', 'EUR'])
    def test_init_user_currency_not_supported(self):
        with self.assertRaises(UserError) as e:
            User(user_id=1, currency='GBP')
        assert e.exception.user_error_type == UserErrorTypes.currency_not_supported

    @patch.object(ShoppingCart, 'add_product_to_basket')
    def test_add_product_to_basket(self, mock_add_product_to_basket):
        user = User(user_id=1, currency='USD')
        user.add_product_to_basket(store_id=1, product_id=100, quantity=1)
        mock_add_product_to_basket.assert_called_once_with(1, 100, 1)

    @patch.object(ShoppingCart, 'remove_product_from_basket')
    def test_remove_product_from_basket(self, mock_remove_product_from_basket):
        user = User(user_id=1, currency='USD')
        user.add_product_to_basket(store_id=1, product_id=100, quantity=1)
        user.remove_product_from_basket(store_id=1, product_id=100, quantity=1)
        mock_remove_product_from_basket.assert_called_once_with(1, 100, 1)

    def test_subtract_product_from_cart(self):
        user = User(user_id=1, currency='USD')
        user.add_product_to_basket(store_id=1, product_id=100, quantity=2)
        user.remove_product_from_basket(store_id=1, product_id=100, quantity=1)
        self.assertEqual(user.get_shopping_cart(), {1: {100: 1}})

    def test_get_shopping_cart(self):
        user = User(user_id=1, currency='USD')
        user.add_product_to_basket(store_id=1, product_id=100, quantity=1)
        self.assertEqual(user.get_shopping_cart(), {1: {100: 1}})

    def test_register(self):
        user = User(user_id=1, currency='USD')
        user.register(email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        self.assertEqual(user.get_password(), "password")
        self.assertTrue(user.is_member())

    def test_register_already_registered(self):
        user = User(user_id=1, currency='USD')
        user.register(email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")

        with self.assertRaises(UserError) as e:
            user.register(email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1,
                          phone="1234567890")
        assert e.exception.user_error_type == UserErrorTypes.user_already_registered
            
    def test_get_notifications(self):
        user = User(user_id=1, currency='USD')
        user.register(email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1,
                      phone="1234567890")
        self.assertEqual(user.get_notifications(), [])
        user.add_notification(Notification(1, "Test Message", datetime.datetime.now()))
        self.assertEqual(len(user.get_notifications()), 1)

    def test_get_password_member(self):
        user = User(user_id=1, currency='USD')
        user.register(email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1,
                      phone="1234567890")
        self.assertEqual(user.get_password(), "password")

    def test_get_password_guest(self):
        user = User(user_id=1, currency='USD')
        with self.assertRaises(UserError) as e:
            user.get_password()
        assert e.exception.user_error_type == UserErrorTypes.user_not_registered
    
    def test_clear_basket(self):
        user = User(user_id=1, currency='USD')
        user.add_product_to_basket(store_id=1, product_id=100, quantity=1)
        user.clear_basket()
        self.assertEqual(user.get_shopping_cart(), {})

    def test_suspend_user(self):
        user = User(user_id=1, currency='USD')
        user.register(email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1,
                      phone="1234567890")
        assert not user.is_suspended()

class TestUserFacade(unittest.TestCase):

    def setUp(self):
        self.user_facade = UserFacade()
        self.user_facade.clean_data()

    @patch.object(User, '__init__', lambda x, y, z: None)  # Mocking User init method
    def test_create_user(self):

        facade = UserFacade()
        user_id = facade.create_user(currency='USD')
        self.assertIsInstance(user_id, int)
        self.assertEqual(user_id, 0)

    @patch.object(User, 'register')
    def test_register_user(self, mock_register):
        facade = UserFacade()
        user_id = facade.create_user(currency='USD')
        facade.register_user(user_id, email="test@example.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        self.assertIn(user_id, facade._UserFacade__users)

    # @patch.object(User, 'get_notifications')
    # def test_get_notifications(self, mock_get_notifications):
    #     facade = UserFacade()
    #     user_id = facade.create_user(currency='USD')
    #     facade.get_notifications(user_id)
    #     mock_get_notifications.assert_called_once_with()

    def test_clear_notifications(self):
        user_id = self.user_facade.create_user(currency='USD')
        self.user_facade.register_user(user_id, "test@gmail.com", "testuser", "password", 2000, 1, 1, "1234567890")
        self.user_facade.clear_notifications(user_id)
        self.assertEqual(self.user_facade.get_notifications(user_id), [])
        self.user_facade._UserFacade__get_user(user_id).add_notification(Notification(1, "Test Message", datetime.datetime.now()))
        self.user_facade.clear_notifications(user_id)
        self.assertEqual(self.user_facade.get_notifications(user_id), [])

    @patch.object(User, 'add_product_to_basket')
    def test_add_product_to_basket(self, mock_add_product_to_basket):
        user_id = self.user_facade.create_user(currency='USD')
        self.user_facade.add_product_to_basket(user_id, store_id=1, product_id=100, quantity=1)
        mock_add_product_to_basket.assert_called_once_with(1, 100, 1)
        #self.assertEqual(self.user_facade.get_shopping_cart(user_id), {1: {100: 1}})

    @patch.object(User, 'get_shopping_cart')
    def test_get_shopping_cart(self, mock_get_shopping_cart):
        facade = UserFacade()
        user_id = facade.create_user(currency='USD')
        facade.get_shopping_cart(user_id)
        mock_get_shopping_cart.assert_called_once_with()

    @patch.object(User, 'remove_product_from_basket')
    def test_remove_product_from_basket(self, mock_remove_product_from_basket):
        facade = UserFacade()
        user_id = facade.create_user(currency='USD')
        facade.add_product_to_basket(user_id, store_id=1, product_id=100, quantity=1)
        facade.remove_product_from_basket(user_id, store_id=1, product_id=100, quantity=1)
        mock_remove_product_from_basket.assert_called_once_with(1, 100, 1)

    @patch.object(User, 'remove_product_from_basket')
    def test_remove_product_from_basket(self, mock_remove_product_from_basket):
        facade = UserFacade()
        user_id = facade.create_user(currency='USD')
        facade.add_product_to_basket(user_id, store_id=1, product_id=100, quantity=2)
        facade.remove_product_from_basket(user_id, store_id=1, product_id=100, quantity=1)
        mock_remove_product_from_basket.assert_called_once_with(1, 100, 1)

    @patch.object(User, 'get_password')
    def test_get_password_guest(self, mock_get_password):
        self.user_facade.create_user(currency='USD')
        with self.assertRaises(UserError) as e:
            self.user_facade.get_password("testuser")
        assert e.exception.user_error_type == UserErrorTypes.user_not_found

    @patch.object(User, 'get_password')
    def test_get_password_member(self, mock_get_password):
        user_id = self.user_facade.create_user(currency='USD')
        self.user_facade.register_user(user_id, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        self.user_facade.get_password("testuser")

    def test_remove_user(self):
        user_id = self.user_facade.create_user(currency='USD')
        self.user_facade.remove_user(user_id)
        self.assertNotIn(user_id, self.user_facade._UserFacade__users)

    def test_remove_user_not_found(self):
        with self.assertRaises(UserError) as e:
            self.user_facade.remove_user(1)
        assert e.exception.user_error_type == UserErrorTypes.user_not_found

    def test_is_member(self):
        user_id = self.user_facade.create_user(currency='USD')
        self.user_facade.register_user(user_id, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        self.assertTrue(self.user_facade.is_member(0))
    
    def test_is_suspended_true(self):
        user_id = self.user_facade.create_user(currency='USD')
        self.user_facade.register_user(user_id, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        assert not self.user_facade.suspended(user_id)

    def test_permanently_suspend_user(self):
        user_id = self.user_facade.create_user(currency='USD')
        self.user_facade.register_user(user_id, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        self.user_facade.suspend_user_permanently(user_id)
        assert self.user_facade.suspended(user_id)

    def test_temporarily_suspend_user(self):
        user_id = self.user_facade.create_user(currency='USD')
        self.user_facade.register_user(user_id, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        details = {
            "year": 2026,
            "month": 1,
            "day": 1,
            "hour": 0,
            "minute": 0,
        }
        self.user_facade.suspend_user_temporarily(user_id, details)
        assert self.user_facade.suspended(user_id)

    def test_temporarily_suspend_user_and_the_time_passed(self):
        user_id = self.user_facade.create_user(currency='USD')
        self.user_facade.register_user(user_id, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")

        if datetime.datetime.now().minute == 0:
            minutes = 59
            hour = datetime.datetime.now().hour - 1
        else:
            minutes = datetime.datetime.now().minute - 1
            hour = datetime.datetime.now().hour
            
        details = {
            "year": datetime.datetime.now().year,
            "month": datetime.datetime.now().month,
            "day": datetime.datetime.now().day,
            "hour": hour,
            "minute": minutes
        }
        self.user_facade.suspend_user_temporarily(user_id, details)
        assert not self.user_facade.suspended(user_id)
    
    def test_suspend_user_not_found(self):
        with self.assertRaises(UserError) as e:
            self.user_facade.suspend_user_permanently(1)
        assert e.exception.user_error_type == UserErrorTypes.user_not_found

    def test_unsuspend_user(self):
        user_id = self.user_facade.create_user(currency='USD')
        self.user_facade.register_user(user_id, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        self.user_facade.suspend_user_permanently(user_id)
        self.user_facade.unsuspend_user(user_id)
        assert not self.user_facade.suspended(user_id)
    
    def test_get_empty_suspended_users(self):
        user_id = self.user_facade.create_user(currency='USD')
        self.user_facade.register_user(user_id, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        assert self.user_facade.get_suspended_users() == {}
    
    def test_get_suspended_users(self):
        user_id = self.user_facade.create_user(currency='USD')
        self.user_facade.register_user(user_id, email="test@mail.com", username="testuser", password="password", year=2000, month=1, day=1, phone="1234567890")
        self.user_facade.suspend_user_permanently(user_id)
        assert self.user_facade.get_suspended_users() == {user_id: None}

if __name__ == '__main__':
    unittest.main()
