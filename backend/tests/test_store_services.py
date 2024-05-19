'''
module for testing the store services
'''

import unittest
from services.store_services.controllers import StoreService

class TestStoreService(unittest.TestCase):
    '''
    test service functions for Store service
    '''

    def setUp(self):
        '''
        Code to set up the tests class
        '''

        self.service = StoreService()

    def tearDown(self):
        '''
        Code to clean up after each test
        '''

        pass

    def test_show_store_info(self):
        # Replace with your test case
        self.assertFalse(self.service.show_store_info('token'))

    def test_show_store_products(self):
        # Replace with your test case
        self.assertFalse(self.service.show_store_products('token', 'store_id'))

    def test_add_new_store(self):
        # Replace with your test case
        self.assertFalse(self.service.add_new_store('token', 'store_data'))

    def test_add_product_to_store(self):
        # Replace with your test case
        self.assertFalse(self.service.add_product_to_store('token', 'store_id', 'product_data'))

    def test_change_store_purchace_policy(self):
        # Replace with your test case
        self.assertFalse(self.service.change_store_purchace_policy('token', 'store_id', 'policy_data'))

    def test_change_store_purchace_types(self):
        # Replace with your test case
        self.assertFalse(self.service.change_store_purchace_types('token', 'store_id', 'types_data'))

    def test_change_store_discount_types(self):
        # Replace with your test case
        self.assertFalse(self.service.change_store_discount_types('token', 'store_id', 'types_data'))

    def test_change_store_discount_policy(self):
        # Replace with your test case
        self.assertFalse(self.service.change_store_discount_policy('token', 'store_id', 'policy_data'))

    def test_add_store_owner(self):
        # Replace with your test case
        self.assertFalse(self.service.add_store_owner('token', 'store_id', 'owner_id'))

    def test_add_store_manager(self):
        # Replace with your test case
        self.assertFalse(self.service.add_store_manager('token', 'store_id', 'manager_id', 'permissions'))

    def test_edit_manager_permissions(self):
        # Replace with your test case
        self.assertFalse(self.service.edit_manager_permissions('token', 'store_id', 'manager_id', 'permissions'))

    def test_closing_store(self):
        # Replace with your test case
        self.assertFalse(self.service.closing_store('token', 'store_id'))

    def test_view_employees_info(self):
        # Replace with your test case
        self.assertFalse(self.service.view_employees_info('token', 'store_id'))

if __name__ == '__main__':
    unittest.main()