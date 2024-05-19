'''
module for testing the third party services
'''


import unittest
from services.third_party_services.controllers import ThirdPartyService

class TestThirdPartyService(unittest.TestCase):
    '''
    test service functions for third party services
    '''

    def setUp(self):
        '''
        Code to set up the tests class
        '''

        self.service = ThirdPartyService()

    def tearDown(self):
        '''
        Code to clean up after each test
        '''

        pass

    def test_add_third_party_service(self):
        # Replace with your test case
        self.assertFalse(self.service.add_third_party_service('token', 'data'))

    def test_edit_third_party_service(self):
        # Replace with your test case
        self.assertFalse(self.service.edit_third_party_service('token', 'service_id', 'data'))

    def test_delete_third_party_service(self):
        # Replace with your test case
        self.assertFalse(self.service.delete_third_party_service('token', 'service_id'))

    def test_access_payment_service(self):
        # Replace with your test case
        self.assertFalse(self.service.access_payment_service('token', 'payment_method', 'payment_details', 'price'))

    def test_access_supply_service(self):
        # Replace with your test case
        self.assertFalse(self.service.access_supply_service('token', 'package_details', 'user_id'))

if __name__ == '__main__':
    unittest.main()