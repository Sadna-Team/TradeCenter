'''
module for testing the user services
'''

import unittest
from services.user_services.controllers import UserService, AuthenticationService

class TestUserService(unittest.TestCase):
    '''
    test service functions for user service
    '''

    def setUp(self):
        '''
        Code to set up the tests class
        '''

        self.service = UserService()

    def tearDown(self):
        '''
        Code to clean up after each test
        '''

        pass

    def test_show_notifications(self):
        # Replace with your test case
        self.assertFalse(self.service.show_notifications('token'))

    def test_add_product_to_basket(self):
        # Replace with your test case
        self.assertFalse(self.service.add_product_to_basket('token', 'product_id'))

    def test_show_shopping_cart(self):
        # Replace with your test case
        self.assertFalse(self.service.show_shopping_cart('token'))

    def test_remove_product_from_cart(self):
        # Replace with your test case
        self.assertFalse(self.service.remove_product_from_cart('token', 'product_id'))

    def test_checkout(self):
        # Replace with your test case
        self.assertFalse(self.service.checkout('token', 'payment_method', 'payment_details'))

    def test_accept_promotion_to_owner(self):
        # Replace with your test case
        self.assertFalse(self.service.accept_promotion_to_owner('token', 'store_id', 'owner_id'))

    def test_accept_promotion_to_manager(self):
        # Replace with your test case
        self.assertFalse(self.service.accept_promotion_to_manager('token', 'store_id', 'manager_id', 'permissions'))

class TestAuthenticationService(unittest.TestCase):
    '''
    test service functions for user service
    '''
    
    def setUp(self):
        '''
        Code to set up the tests class
        '''

        self.service = AuthenticationService()

    def tearDown(self):
        '''
        Code to clean up after each test
        '''

        pass

    def test_start_app(self):
        # Replace with your test case
        self.assertFalse(self.service.start_app())

    def test_login(self):
        # Replace with your test case
        self.assertFalse(self.service.login('token', 'user_credentials'))

    def test_logout(self):
        # Replace with your test case
        self.assertFalse(self.service.logout('token'))

    def test_register(self):
        # Replace with your test case
        self.assertFalse(self.service.register('token', 'register_credentials'))

if __name__ == '__main__':
    unittest.main()