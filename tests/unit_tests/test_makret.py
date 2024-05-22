import unittest
from flask import Flask
from backend.business.market import MarketFacade
from backend.business.user import UserFacade
from backend.business.authentication.authentication import Authentication
from backend.business.store.store import StoreFacade
from backend.business.roles import RolesFacade
from backend.business.DTOs import NotificationDTO
from unittest.mock import MagicMock, patch
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import datetime


class TestMarket(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test_secret_key'  # Set a test secret key
        self.jwt = JWTManager(self.app)
        self.bcrypt = Bcrypt(self.app)
        self.auth = Authentication()
        self.auth.set_jwt(self.jwt, self.bcrypt)

        self.market = MarketFacade()

        self.roles = RolesFacade()
        self.user = UserFacade()
        self.store = StoreFacade()

        self.app_context = self.app.app_context()
        self.app_context.push()

        # noinspection SpellCheckingInspection
        noti1 = NotificationDTO(1, "hello", "today")
        # noinspection SpellCheckingInspection
        noti2 = NotificationDTO(2, "there", "today")
        self.user.get_notifications = MagicMock(return_value=[noti1, noti2])

    def setUpBasic(self):
        # Create a user
        self.user_id = self.user.create_user()
        self.user.register_user(self.user_id, "mail@mail.com", "username", "password", 2000, 1, 1, "123456789")
        self.store.addStore(0,"store",self.user_id)
        self.store.addProductSpecification("product", 1, "test product",["test"],"test manufacture",[])
        #datetime of 1 year from now
        date = datetime.datetime.now() + datetime.timedelta(days=365)
        self.store.addProductToStore(0,0,date,1,10)



    def test_singleton(self):
        market2 = MarketFacade()
        self.assertEqual(self.market, market2)

    def test_admin_is_created(self):
        self.assertTrue(self.user.is_member(0))
        self.assertTrue(self.roles.check_if_user_is_admin(0))

    def test_show_notifications(self):
        noti = self.market.show_notifications(0)
        self.assertEqual(noti[0].get_notification_id(), 1)
        self.assertEqual(noti[0].get_message(), "hello")
        self.assertEqual(noti[0].get_date(), "today")
        self.assertEqual(noti[1].get_notification_id(), 2)
        self.assertEqual(noti[1].get_message(), "there")
        self.assertEqual(noti[1].get_date(), "today")

    def test_add_product_to_basket(self):
        self.market.add_product_to_basket(0, 0, 0)
        basket = self.user.get_shopping_cart(0)
        self.assertEqual(basket, {0: [0]})

    def test_checkout(self):
        self.setUpBasic()
        self.market.checkout(1, {"payment method": "bogo"}, {"address" : "israel"})

        # PURCHASE IS ADDED TO HISTORY
        # TODO : @LINA, TAMIR
        # BASKET IS EMPTY
        self.assertEqual(self.user.get_shopping_cart(1), {})
        # USER IS CHARGED
        # TODO : HOW ?
        # DELIVERY IS SCHEDULED
        # TODO : HOW ?
        # NOTIFICATION IS SENT
        self.market.notifier.send_notification.assert_called_once()



if __name__ == '__main__':
    unittest.main()
