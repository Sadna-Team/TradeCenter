import unittest
from unittest.mock import MagicMock
from backend.business.ThirdPartyHandlers import PaymentHandler, SupplyHandler

class TestPaymentHandler(unittest.TestCase):
    def test_process_payment_with_valid_method(self):
        payment_handler = PaymentHandler()
        payment_handler._resolve_payment_strategy = MagicMock(return_value=MagicMock(pay=MagicMock(return_value=True)))
        result = payment_handler.process_payment(100, {"payment method": "bogo"})
        self.assertTrue(result)

    def test_process_payment_with_invalid_method(self):
        payment_handler = PaymentHandler()
        with self.assertRaises(ValueError):
            payment_handler.process_payment(100, {"payment method": "invalid_method"})

class TestSupplyHandler(unittest.TestCase):
    def test_process_supply_with_valid_method(self):
        supply_handler = SupplyHandler()
        supply_handler._resolve_supply_strategy = MagicMock(return_value=MagicMock(order=MagicMock(return_value=True)))
        result = supply_handler.process_supply({"supply method": "bogo"}, 123)
        self.assertTrue(result)

    def test_process_supply_with_invalid_method(self):
        supply_handler = SupplyHandler()
        with self.assertRaises(ValueError):
            supply_handler.process_supply({"supply method": "invalid_method"}, 123)

if __name__ == '__main__':
    unittest.main()
