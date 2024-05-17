'''
module for testing the ecommerce services
'''

import unittest
from services.ecommerce_services.controllers import SearchService, PurchaceService

class TestPurchaceService(unittest.TestCase):
    '''
    test service functions for purchase service
    '''
    
    def setUp(self):
        '''
        Code to set up the tests class
        '''

        self.service = PurchaceService()

    def tearDown(self):
        '''
        Code to clean up after each test
        '''

        pass

    def test_checkout(self):
        """result = self.service.checkout('token', 'payment_method', 'payment_details')
        self.assertIsNone(result)"""

    def test_show_purchace_history_in_store(self):
        """result = self.service.show_purchace_history_in_store('token', 'user_id')
        self.assertIsNone(result)"""

    def test_show_purchace_history_of_member(self):
        """result = self.service.show_purchace_history_of_member('token', 'user_id')
        self.assertIsNone(result)"""

class TestSearchService(unittest.TestCase):
    '''
    test service functions for purchase service
    '''
    
    def setUp(self):
        '''
        Code to set up the tests class
        '''
        self.service = SearchService()

    def tearDown(self):
        '''
        Code to clean up after each test
        '''
        pass

    def test_search_products(self):
        """result = self.service.search_products('token', 'filters')
        self.assertIsNone(result)"""

    def test_search_store_products(self):
        """result = self.service.search_store_products('token', 'user_id', 'filters')
        self.assertIsNone(result)"""

if __name__ == '__main__':
    unittest.main()