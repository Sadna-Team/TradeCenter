import unittest
from backend.business.user.user import *
from backend.business.DTOs import NotificationDTO
import datetime
from unittest.mock import patch, MagicMock
class TestShoppingBasket(unittest.TestCase):

    def test_add_product(self):
        basket = ShoppingBasket(store_id=1)
        basket.add_product(100)
        self.assertIn(100, basket.get_dto())
        self.assertEqual(basket.get_dto(), [100])

    def test_add_product_duplicate(self):
        basket = ShoppingBasket(store_id=1)
        basket.add_product(100)
        with self.assertRaises(ValueError):
            basket.add_product(100)

    def test_remove_product(self):
        basket = ShoppingBasket(store_id=1)
        basket.add_product(100)
        basket.remove_product(100)
        self.assertNotIn(100, basket.get_dto())
        self.assertEqual(basket.get_dto(), [])

    def test_remove_product_not_found(self):
        basket = ShoppingBasket(store_id=1)
        with self.assertRaises(ValueError):
            basket.remove_product(100)


class TestShoppingCart(unittest.TestCase):

    def test_add_product_to_basket(self):
        cart = SoppingCart(user_id=1)
        cart.add_product_to_basket(store_id=1, product_id=100)
        self.assertEqual(cart.get_dto(), {1: [100]})

    def test_remove_product_from_cart(self):
        cart = SoppingCart(user_id=1)
        cart.add_product_to_basket(store_id=1, product_id=100)
        cart.remove_product_from_cart(store_id=1, product_id=100)
        self.assertEqual(cart.get_dto(), {1: []})

    def test_remove_product_from_cart_store_not_found(self):
        cart = SoppingCart(user_id=1)
        with self.assertRaises(ValueError):
            cart.remove_product_from_cart(store_id=1, product_id=100)


class TestState(unittest.TestCase):

    def test_guest_get_password(self):
        guest = Guest()
        with self.assertRaises(ValueError):
            guest.get_password()

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
        with self.assertRaises(ValueError):
            User(user_id=1, currency='GBP')

    @patch.object(SoppingCart, 'add_product_to_basket')
    def test_add_product_to_basket(self, mock_add_product_to_basket):
        user = User(user_id=1, currency='USD')
        user.add_product_to_basket(store_id=1, product_id=100)
        mock_add_product_to_basket.assert_called_once_with(1, 100)

    @patch.object(SoppingCart, 'remove_product_from_cart')
    def test_remove_product_from_cart(self, mock_remove_product_from_cart):
        user = User(user_id=1, currency='USD')
        user.add_product_to_basket(store_id=1, product_id=100)
        user.remove_product_from_cart(store_id=1, product_id=100)
        mock_remove_product_from_cart.assert_called_once_with(1, 100)


class TestUserFacade(unittest.TestCase):

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
        mock_register.assert_called_once_with("test@example.com", "testuser", "password", 2000, 1, 1, "1234567890")

    @patch.object(User, 'add_product_to_basket')
    def test_add_product_to_basket(self, mock_add_product_to_basket):
        facade = UserFacade()
        user_id = facade.create_user(currency='USD')
        facade.add_product_to_basket(user_id, store_id=1, product_id=100)
        mock_add_product_to_basket.assert_called_once_with(1, 100)

    @patch.object(User, 'remove_product_from_cart')
    def test_remove_product_from_cart(self, mock_remove_product_from_cart):
        facade = UserFacade()
        user_id = facade.create_user(currency='USD')
        facade.add_product_to_basket(user_id, store_id=1, product_id=100)
        facade.remove_product_from_cart(user_id, store_id=1, product_id=100)
        mock_remove_product_from_cart.assert_called_once_with(1, 100)


if __name__ == '__main__':
    unittest.main()
