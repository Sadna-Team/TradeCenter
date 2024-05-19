import unittest
from unittest.mock import patch, Mock

from backend.business.store.store import *

from backend.business.store.store import product


class TestProductFunctions(unittest.TestCase):

    def setUp(self, mock_obj) -> None:
        self.mock_product = Mock(spec = product)
        self.mock_product.product_id = 1
        self.mock_product.storeId = 1
        self.mock_product.specificationId = 1
        self.mock_product.exporationDate = '2024-12-31'
        self.mock_product.condition = 'New'
        self.mock_product.price = 10.00
        
    def test_get_productId(self):
        self.assertEqual(self.mock_product.get_productId(), 1)

    def test_set_productId(self):
        self.mock_product.set_productId(2)
        self.assertEqual(self.mock_product.get_productId(), 2)

    def test_get_storeId(self):
        self.assertEqual(self.mock_product.get_storeId(), 1)

    def test_set_storeId(self):
        self.mock_product.set_storeId(2)
        self.assertEqual(self.mock_product.get_storeId(), 2)
    
    def test_get_specificationId(self):
        self.assertEqual(self.mock_product.get_specificationId(), 1)

    def test_set_specificationId(self):
        self.mock_product.set_specificationId(2)
        self.assertEqual(self.mock_product.get_specificationId(), 2)
    
    def test_get_exporationDate(self):
        self.assertEqual(self.mock_product.get_exporationDate(), '2024-12-31')

    def test_set_exporationDate(self):
        self.mock_product.set_exporationDate('2025-12-31')
        self.assertEqual(self.mock_product.get_exporationDate(), '2025-12-31')
    
    def test_get_condition(self):
        self.assertEqual(self.mock_product.get_condition(), 'New')

    def test_set_condition(self):
        self.mock_product.set_condition('Used')
        self.assertEqual(self.mock_product.get_condition(), 'Used')
    
    def test_get_price(self):
        self.assertEqual(self.mock_product.get_price(), 10.00)
    
    def test_set_price(self):
        self.mock_product.set_price(20.00)
        self.assertEqual(self.mock_product.get_price(), 20.00)
    
    def test_isExpired(self):
        self.assertEqual(self.mock_product.isExpired(), False)
    
    def test_changePrice_success(self):
        self.assertEqual(self.mock_product.changePrice(5.00), True)
        self.assertEqual(self.mock_product.get_price(), 5.00)

    def test_changePrice_fail(self):
        self.assertEqual(self.mock_product.changePrice(-5.00), False)
        self.assertEqual(self.mock_product.get_price(), 10.00)

    

    
    



if __name__ == '__main__':
    unittest.main()
