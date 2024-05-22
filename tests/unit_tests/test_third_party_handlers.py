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


    def test_edit_payment_method_with_valid_method(self):
        payment_handler = PaymentHandler()
        payment_handler.edit_payment_method("bogo", {"test": "test"})
        self.assertEqual(PaymentHandler.payment_config["bogo"], {"test": "test"})

    def test_edit_payment_method_with_invalid_method(self):
        payment_handler = PaymentHandler()
        with self.assertRaises(ValueError):
            payment_handler.edit_payment_method("invalid_method", {"test": "test"})
        
    def test_add_payment_method_with_valid_method(self):
        payment_handler = PaymentHandler()
        payment_handler.add_payment_method("bogo1", {"test": "test"})
        self.assertEqual(PaymentHandler.payment_config["bogo1"], {"test": "test"})

    def test_add_payment_method_with_invalid_method(self):
        payment_handler = PaymentHandler()
        with self.assertRaises(ValueError):
            payment_handler.add_payment_method("bogo", {"test": "test"})

    def test_remove_payment_method_with_valid_method(self):
        payment_handler = PaymentHandler()
        payment_handler.remove_payment_method("bogo")
        self.assertNotIn("bogo", PaymentHandler.payment_config)

    
    def test_remove_payment_method_with_invalid_method(self):
        payment_handler = PaymentHandler()
        with self.assertRaises(ValueError):
            payment_handler.remove_payment_method("invalid_method")

    def test_remove_and_add_method(self):
        payment_handler = PaymentHandler()
        payment_handler.remove_payment_method("bogo")
        self.assertNotIn("bogo", PaymentHandler.payment_config)

        payment_handler.add_payment_method("bogo", {"test": "test"})
        self.assertEqual(PaymentHandler.payment_config["bogo"], {"test": "test"})
    

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

    
    def test_edit_supply_method_with_valid_method(self):
        supply_handler = SupplyHandler()
        supply_handler.edit_supply_method("bogo", {"test": "test"})
        self.assertEqual(SupplyHandler.supply_config["bogo"], {"test": "test"})

    def test_edit_supply_method_with_invalid_method(self):
        supply_handler = SupplyHandler()
        with self.assertRaises(ValueError):
            supply_handler.edit_supply_method("invalid_method", {"test": "test"})

    def test_add_supply_method_with_valid_method(self):
        supply_handler = SupplyHandler()
        supply_handler.add_supply_method("bogo1", {"test": "test"})
        self.assertEqual(SupplyHandler.supply_config["bogo1"], {"test": "test"}) 

    def test_add_supply_method_with_invalid_method(self):
        supply_handler = SupplyHandler()
        with self.assertRaises(ValueError):
            supply_handler.add_supply_method("bogo", {"test": "test"})

    def test_remove_supply_method_with_valid_method(self):
        supply_handler = SupplyHandler()
        supply_handler.remove_supply_method("bogo")
        self.assertNotIn("bogo", SupplyHandler.supply_config)   

    def test_remove_supply_method_with_invalid_method(self):
        supply_handler = SupplyHandler()
        with self.assertRaises(ValueError):
            supply_handler.remove_supply_method("invalid_method")

    def test_remove_and_add_method(self):
        supply_handler = SupplyHandler()
        supply_handler.remove_supply_method("bogo")
        self.assertNotIn("bogo", SupplyHandler.supply_config)

        supply_handler.add_supply_method("bogo", {"test": "test"})
        self.assertEqual(SupplyHandler.supply_config["bogo"], {"test": "test"})   

if __name__ == '__main__':
    unittest.main()
