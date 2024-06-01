import pytest
from backend.business.ThirdPartyHandlers.third_party_handlers import PaymentHandler, SupplyHandler, BogoSupply, BogoPayment
from datetime import datetime, timedelta
import time


payment_config = {"immediate": True, "card": "visa", "currency": "USD"}
payment_details = {"payment method": "bogo", "card": "visa", "currency": "USD"}
wrong_payment_details = {"payment method": "card", "card": "mastercard", "currency": "USD"}
no_payment_details = {}
price = 100
package_details = { "supply method": "bogo",
                    "shopping cart": {},
                   "address": {
                       "street": "test", 
                       "city": "test", 
                       "zip": "test", 
                       "country": "test"}, 
                    "purchase id": 6,
                    "arrival time": datetime.now() + timedelta(seconds=10)}

wrong_package_details = { "method name": "no bogo sad",
                    "shopping cart": {},
                     "address": {
                          "street": "test",
                            "city": "test",
                            "zip": "test",
                            "country": "test"},
                    "purchase id": 6,
                    "arrival time": datetime.now() + timedelta(seconds=10)}


on_arrival = lambda x: None
supply_config = {"transport": "truck"}
user_id = 1


@pytest.fixture
def payment_handler():
    PaymentHandler().reset()
    return PaymentHandler()

@pytest.fixture
def payment_handler_extended(payment_handler):
    payment_handler.add_payment_method("test method", {"test": "test"})
    return payment_handler

@pytest.fixture
def supply_handler():
    SupplyHandler().reset()
    return SupplyHandler()

@pytest.fixture
def supply_handler_extended(supply_handler):
    supply_handler.add_supply_method("test method", {"test": "test"})
    return supply_handler

def test_bogopayment_pay():
    bogo_payment = BogoPayment()
    assert bogo_payment.pay(price, payment_config)
    
def test_add_payment_method(payment_handler):
    payment_handler.add_payment_method("test method", {"test": "test"})
    assert payment_handler.payment_config["test method"] == {"test": "test"}

def test_add_payment_method_duplicate(payment_handler):
    with pytest.raises(ValueError):
        payment_handler.add_payment_method("test method", {"test": "test"})
        payment_handler.add_payment_method("test method", {"test": "test"})

    with pytest.raises(ValueError):
        payment_handler.add_payment_method("bogo", {})

def test_remove_payment_method(payment_handler_extended):
    payment_handler_extended.remove_payment_method("test method")
    assert "test method" not in payment_handler_extended.payment_config

def test_remove_payment_method_not_found(payment_handler):
    with pytest.raises(ValueError):
        payment_handler.remove_payment_method("test method")

    with pytest.raises(ValueError):
        payment_handler.remove_payment_method("bogo")
        payment_handler.remove_payment_method("bogo")

def test_edit_payment_method(payment_handler_extended):
    payment_handler_extended.edit_payment_method("test method", {"test": "test2"})
    assert payment_handler_extended.payment_config["test method"] == {"test": "test2"}

def test_edit_payment_method_not_found(payment_handler):
    with pytest.raises(ValueError):
        payment_handler.edit_payment_method("test method", {"test": "test2"})

def test_process_payment(payment_handler):
    assert payment_handler.process_payment(price, payment_details)

def test_process_payment_wrong_details(payment_handler):
    with pytest.raises(ValueError):
        payment_handler.process_payment(price, wrong_payment_details)

def test_process_payment_no_details(payment_handler):
    with pytest.raises(ValueError):
        payment_handler.process_payment(price, no_payment_details)

def test_bogosupply_order():
    bogo_supply = BogoSupply()
    package_details["arrival time"] = datetime.now() + timedelta(seconds=10)
    start = time.time()
    bogo_supply.order(package_details, user_id, supply_config, on_arrival)
    end = time.time()
    assert (9.5 <= end - start) and (end - start <= 10.5)

def test_add_supply_method(supply_handler):
    supply_handler.add_supply_method("test method", {"test": "test"})
    assert supply_handler.supply_config["test method"] == {"test": "test"}

def test_add_supply_method_duplicate(supply_handler):
    with pytest.raises(ValueError):
        supply_handler.add_supply_method("test method", {"test": "test"})
        supply_handler.add_supply_method("test method", {"test": "test"})

    with pytest.raises(ValueError):
        supply_handler.add_supply_method("bogo", {})

def test_remove_supply_method(supply_handler_extended):
    supply_handler_extended.remove_supply_method("test method")
    assert "test method" not in supply_handler_extended.supply_config

def test_remove_supply_method_not_found(supply_handler):
    with pytest.raises(ValueError):
        supply_handler.remove_supply_method("test method")

    with pytest.raises(ValueError):
        supply_handler.remove_supply_method("bogo")
        supply_handler.remove_supply_method("bogo")

def test_edit_supply_method(supply_handler_extended):
    supply_handler_extended.edit_supply_method("test method", {"test": "test2"})
    assert supply_handler_extended.supply_config["test method"] == {"test": "test2"}

def test_edit_supply_method_not_found(supply_handler):
    with pytest.raises(ValueError):
        supply_handler.edit_supply_method("test method", {"test": "test2"})

def test_process_supply(supply_handler):
    package_details["arrival time"] = datetime.now() + timedelta(seconds=10)
    start = time.time()
    supply_handler.process_supply(package_details, user_id, on_arrival)
    end = time.time()
    assert (9.5 <= end - start) and (end - start <= 10.5)

def test_process_supply_wrong_details(supply_handler):
    with pytest.raises(ValueError):
        supply_handler.process_supply(wrong_package_details, user_id, on_arrival)

def test_process_supply_no_details(supply_handler):
    with pytest.raises(ValueError):
        supply_handler.process_supply({}, user_id, on_arrival)