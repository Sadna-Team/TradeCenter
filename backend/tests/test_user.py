# Unit tests for user module

# tests/test_module.py
import unittest
from unittest.mock import patch, Mock
from business.user import *

from business.user import ShoppingBasket


class TestUserFunctions(unittest.TestCase):

    def setUp(self, mock_obj) -> None:
        pass
        
    # Shopping Basket
    def test_add_product(self):
        # Test that the product was added to the basket
        id = 1
        profuct_id = 2
        basket = ShoppingBasket(id)
        basket.add_product(profuct_id, id)

        self.assertEqual(); #TODO: assert what galko wold do his changes


if __name__ == '__main__':
    unittest.main()
