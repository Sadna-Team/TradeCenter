import pytest
from backend.business.ThirdPartyHandlers.third_party_handlers import PaymentHandler, SupplyHandler, BogoSupply, BogoPayment
from datetime import datetime, timedelta
import time
from backend.error_types import *


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
    
    with pytest.raises(ThirdPartyHandlerError) as e:
        payment_handler.add_payment_method("test method", {"test": "test"})
        payment_handler.add_payment_method("test method", {"test": "test"})
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.payment_method_already_supported
     
    
    with pytest.raises(ThirdPartyHandlerError) as e:
        payment_handler.add_payment_method("bogo", {})
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.payment_method_already_supported

def test_remove_payment_method(payment_handler_extended):
    payment_handler_extended.remove_payment_method("test method")
    assert "test method" not in payment_handler_extended.payment_config

def test_remove_payment_method_not_found(payment_handler):
    with pytest.raises(ThirdPartyHandlerError) as e:
        payment_handler.remove_payment_method("test method")
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.payment_method_not_supported

    with pytest.raises(ThirdPartyHandlerError) as e:
        payment_handler.remove_payment_method("bogo")
        payment_handler.remove_payment_method("bogo")
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.payment_method_not_supported

def test_edit_payment_method(payment_handler_extended):
    payment_handler_extended.edit_payment_method("test method", {"test": "test2"})
    assert payment_handler_extended.payment_config["test method"] == {"test": "test2"}

def test_edit_payment_method_not_found(payment_handler):
    with pytest.raises(ThirdPartyHandlerError) as e:
        payment_handler.edit_payment_method("test method", {"test": "test2"})
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.payment_method_not_supported

def test_process_payment(payment_handler):
    assert payment_handler.process_payment(price, payment_details)

def test_process_payment_wrong_details(payment_handler):
    with pytest.raises(ThirdPartyHandlerError) as e:
        payment_handler.process_payment(price, wrong_payment_details)
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.payment_method_not_supported

def test_process_payment_no_details(payment_handler):
    with pytest.raises(ThirdPartyHandlerError) as e:
        payment_handler.process_payment(price, no_payment_details)
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.payment_method_not_supported

def test_bogosupply_order():
    bogo_supply = BogoSupply()
    package_details["arrival time"] = datetime.now() + timedelta(seconds=10)
    assert bogo_supply.order(package_details, user_id, supply_config, on_arrival) is None
    

def test_add_supply_method(supply_handler):
    supply_handler.add_supply_method("test method", {"test": "test"})
    assert supply_handler.supply_config["test method"] == {"test": "test"}

def test_add_supply_method_duplicate(supply_handler):
    with pytest.raises(ThirdPartyHandlerError) as e:
        supply_handler.add_supply_method("test method", {"test": "test"})
        supply_handler.add_supply_method("test method", {"test": "test"})
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.supply_method_already_supported

    with pytest.raises(ThirdPartyHandlerError) as e:
        supply_handler.add_supply_method("bogo", {})
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.supply_method_already_supported

def test_remove_supply_method(supply_handler_extended):
    supply_handler_extended.remove_supply_method("test method")
    assert "test method" not in supply_handler_extended.supply_config

def test_remove_supply_method_not_found(supply_handler):
    with pytest.raises(ThirdPartyHandlerError) as e:
        supply_handler.remove_supply_method("test method")
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.supply_method_not_supported

    with pytest.raises(ThirdPartyHandlerError) as e:
        supply_handler.remove_supply_method("bogo")
        supply_handler.remove_supply_method("bogo")
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.supply_method_not_supported

def test_edit_supply_method(supply_handler_extended):
    supply_handler_extended.edit_supply_method("test method", {"test": "test2"})
    assert supply_handler_extended.supply_config["test method"] == {"test": "test2"}

def test_edit_supply_method_not_found(supply_handler):
    with pytest.raises(ThirdPartyHandlerError) as e:
        supply_handler.edit_supply_method("test method", {"test": "test2"})
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.supply_method_not_supported

def test_process_supply(supply_handler):
    package_details["arrival time"] = datetime.now() + timedelta(seconds=10)
    assert supply_handler.process_supply(package_details, user_id, on_arrival) is None

def test_process_supply_wrong_details(supply_handler):
    with pytest.raises(ThirdPartyHandlerError) as e:
        supply_handler.process_supply(wrong_package_details, user_id, on_arrival)
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.missing_supply_method

def test_process_supply_no_details(supply_handler):
    with pytest.raises(ThirdPartyHandlerError) as e:
        supply_handler.process_supply({}, user_id, on_arrival)
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.missing_supply_method
        