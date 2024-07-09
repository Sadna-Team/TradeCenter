from abc import ABC, abstractmethod
from typing import Dict, Tuple, Callable, List
from datetime import datetime, timedelta
import time
import threading
from backend.error_types import *


import logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                     format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("third_party_handlers logger")

class PaymentAdapter(ABC):
    """
        * PaymentAdapter is an abstract class that defines the interface for payment strategies.
        * Concrete implementations of PaymentAdapter should implement the pay method.
        * Each pay method is an adapter for a specific external payment gateway.
    """

    @abstractmethod
    def pay(self, amount: float, payment_config: Dict) -> int:
        """
            * pay is an abstract method that should be implemented by concrete payment strategies.
            * pay should return True if the payment was successful, and False / raise exception otherwise.
        """
        pass

    @abstractmethod
    def cancel_payment(self, payment_id: int) -> int:
        """
            * cancel_payment is an abstract method that should be implemented by concrete payment strategies.
            * cancel_payment should return True if the payment was successfully canceled, and False / raise exception otherwise.
        """
        pass


class BogoPayment(PaymentAdapter):
    def pay(self, amount: float, payment_config: Dict) -> int:
        """
            * For testing purposes, BogoPayment pay always returns True.
        """
        return 1
    
    def cancel_payment(self, payment_id: int) -> int:
        """
            * For testing purposes, BogoPayment cancel_payment always returns True.
        """
        return 1

class PaymentHandler:
    __instance: bool = None
    EXISTING_PAYMENT_METHODS = ["bogo", "external payment"]  # NOTE: << should make the requested value a constant >>

    def __new__(cls):
        if PaymentHandler.__instance is None:
            PaymentHandler.__instance = object.__new__(cls)
        return PaymentHandler.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized: bool = True
            self.payment_config: Dict = {"bogo": {}, "external payment": {}}

    def reset(self) -> None:
        """
            * reset is a method that resets the PaymentHandler's payment_config attribute.
        """
        self.payment_config = {"bogo": {}, "external payment": {}}

    def _resolve_payment_strategy(self, payment_details: Dict) -> PaymentAdapter:
        """
            * _resolve_payment_strategy is a method that resolves a payment strategy based on the payment method.
            * _resolve_payment_strategy should return an instance of a PaymentAdapter subclass.
        """
        method = payment_details.get("payment method")  # NOTE: << should make the requested value a constant >>
        if method not in self.payment_config:
            raise ThirdPartyHandlerError("payment method not supported", ThirdPartyHandlerErrorTypes.payment_method_not_supported)
        elif method == "bogo":  # NOTE: << should make the requested value a constant >>
            return BogoPayment()
        else:
            raise ThirdPartyHandlerError("Invalid payment method", ThirdPartyHandlerErrorTypes.invalid_payment_method)

    def process_payment(self, amount: float, payment_details: Dict) -> int:
        """
            * process_payment is a method that processes a payment using the PaymentHandler's PaymentAdapter object.
            * process_payment should return True if the payment was successful, and False / raise exception otherwise.
        """
   
        logger.info(f"Processing payment of {amount} with details {payment_details}")
        return (self._resolve_payment_strategy(payment_details)
                .pay(amount, self.payment_config[payment_details.get("payment method")]))

    def process_payment_cancel(self, payment_details: Dict, payment_id: int) -> int:
        """
            * process_payment_cancel is a method that cancels a payment using the PaymentHandler's PaymentAdapter object.
            * process_payment_cancel should return True if the payment was successfully canceled, and False / raise exception otherwise.
        """
        return (self._resolve_payment_strategy(payment_details)
                .cancel_payment(payment_id))

    def edit_payment_method(self, method_name: str, editing_data: Dict) -> None:
        """
            * edit_payment_method is a method that edits the current methos configuration.
            * edit_payment_method should return True if the payment method was edited successfully, and False / raise
            exception otherwise.
        """

        if method_name not in self.payment_config:
            raise ThirdPartyHandlerError("payment method not supported", ThirdPartyHandlerErrorTypes.payment_method_not_supported)
        self.payment_config[method_name] = editing_data
        logger.info(f"Edited payment method {method_name}") 

    def add_payment_method(self, method_name: str, config: Dict) -> None:
        """
            * add_payment_method is a method that marks a user's payment method as fully supported in the system.
        """
        if method_name in self.payment_config:
            raise ThirdPartyHandlerError("payment method already supported", ThirdPartyHandlerErrorTypes.payment_method_already_supported)
        self.payment_config[method_name] = config
        logger.info(f"Added payment method {method_name}")

    def remove_payment_method(self, method_name: str) -> None:
        """
            * remove_payment_method is a method that marks a user's payment method as unsupported in the system.
        """
        
        if method_name not in self.payment_config:
            raise ThirdPartyHandlerError("payment method not supported", ThirdPartyHandlerErrorTypes.payment_method_not_supported)
        logger.info(f"Removing payment method {method_name}")
        del self.payment_config[method_name]
        logger.info(f"Removed payment method {method_name}")

    def get_payment_methods(self)-> List[str]:
        """
            * get_payment_methods is a method that returns the list of supported payment methods.
        """
        return self.EXISTING_PAYMENT_METHODS
    
    def get_active_payment_methods(self) -> List[str]:
        """
            * get_active_payment_methods is a method that returns the active payment methods.
        """
        return list(self.payment_config.keys())


class SupplyAdapter(ABC):
    """
        * SupplyAdapter is an abstract class that defines the interface for supply strategies.
        * Concrete implementations of SupplyAdapter should implement the pay method.
        * Each pay method is an adapter for a specific external payment gateway.
    """

    @abstractmethod
    def order(self, package_details: Dict, user_id: int, supply_config: Dict,
              on_arrival: Callable[[int], None]) -> int:
        """
            * order is an abstract method that should be implemented by concrete supply strategies.
            * order should wait for the supply to arrive and call the on_arrival callback.
        """
        pass

    @abstractmethod
    def cancel_order(self, package_details: Dict, order_id: int) -> int:
        """
            * cancel_order is an abstract method that should be implemented by concrete supply strategies.
            * cancel_order should cancel the supply order.
        """
        pass


def do_task(pur_id: int, sleep_time: int, on_arrival: Callable[[int], None]):
    time.sleep(sleep_time)
    on_arrival(pur_id)


class BogoSupply(SupplyAdapter):
    def order(self, package_details: Dict, user_id: int, supply_config: Dict,
              on_arrival: Callable[[int], None]) -> int:
        """
            * For testing purposes, BogoSupply always returns True.
        """
        arrival_time = package_details.get("arrival time")
        sleep_time = (arrival_time - datetime.now()).total_seconds()
        pur_id = package_details.get("purchase id")
        thread = threading.Thread(target=do_task, args=(pur_id, sleep_time, on_arrival))
        thread.start()
        return 1

    def cancel_order(self, package_details: Dict, order_id: int) -> int:
        """
            * For testing purposes, BogoSupply cancel_order always returns True.
        """
        return 1


# ----------------------------------------- Will be used for address validation using Google Maps API later on ----------------------------------------- #
class SupplyHandler:
    __instance = None
    EXISTING_SUPPLY_METHODS = ["bogo", "external supply"]

    def __new__(cls):
        if SupplyHandler.__instance is None:
            SupplyHandler.__instance = object.__new__(cls)
        return SupplyHandler.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized: bool = True
            self.supply_config: Dict = {"bogo": {}}
            self.active_shipments: Dict[int, Tuple[int, datetime]] = {}

    def reset(self) -> None:
        """
            * reset is a method that resets the SupplyHandler's supply_config attribute.
        """
        self.supply_config = {"bogo": {}}

    def _validate_supply_method(self, method_name: str, address: dict) -> bool:
        """
            * validate_supply_method is a method that validates a user's chosen supply method for his address.
            * validate_supply_method should return True if the supply method is valid for the address, and False otherwise.
        """
        logger.info(f"Validating supply method {method_name} for address {address}")

        if method_name not in self.supply_config:
            return False
        return True

    def get_delivery_time(self, package_details: Dict, address: Dict) -> datetime:
        """
            * get_delivery_time is a method that returns the estimated delivery time for a package.
        """
        if not self._validate_supply_method(package_details.get("supply method"), address):
            raise ThirdPartyHandlerError(f"supply method not supported for address: {address}", ThirdPartyHandlerErrorTypes.supply_method_not_supported)
        time = datetime.now() + timedelta(seconds=5)
        logger.info(f"Estimated delivery time: {time} - for package {package_details} to address {address}")
        return time

    def _resolve_supply_strategy(self, package_details: Dict) -> SupplyAdapter:
        """
            * _resolve_supply_strategy is a private method that resolves a supply strategy based on the package details.
            * _resolve_supply_strategy should return an instance of a SupplyAdapter subclass.
        """
        method = package_details.get("supply method")
        if method not in self.supply_config:
            raise ThirdPartyHandlerError("supply method not supported", ThirdPartyHandlerErrorTypes.supply_method_not_supported)
        if "arrival time" not in package_details:
            raise ThirdPartyHandlerError("Missing arrival time in package details", ThirdPartyHandlerErrorTypes.missing_arrival_time)
        date: datetime = package_details.get("arrival time")
        date_now = datetime.now()
        if date < date_now:
            raise ThirdPartyHandlerError("arrival time cannot be in the past", ThirdPartyHandlerErrorTypes.invalid_arrival_time)
        if method == "bogo":
            return BogoSupply()
        else:
            raise ThirdPartyHandlerError("Invalid supply method", ThirdPartyHandlerErrorTypes.invalid_supply_method)

    def process_supply(self, package_details: Dict, user_id: int, on_arrival: Callable[[int], None]) -> int:
        """
            * process_supply is a method that processes a supply using the SupplyHandler's SupplyAdapter object.
            * process_supply should return True if the supply was successful, and False / raise exception otherwise.
        """
        if "supply method" not in package_details:
            raise ThirdPartyHandlerError("Missing supply method in package details", ThirdPartyHandlerErrorTypes.missing_supply_method)
        if "address" not in package_details:
            raise ThirdPartyHandlerError("Missing address in package details", ThirdPartyHandlerErrorTypes.missing_address)
        if not self._validate_supply_method(package_details.get("supply method"), package_details.get("address")):
            raise ThirdPartyHandlerError("supply method not supported for address", ThirdPartyHandlerErrorTypes.supply_method_not_supported)
        if "arrival time" not in package_details:
            raise ThirdPartyHandlerError("Missing arrival time in package details", ThirdPartyHandlerErrorTypes.missing_arrival_time)
        if "purchase id" not in package_details:
            raise ThirdPartyHandlerError("Missing purchase id in package details" , ThirdPartyHandlerErrorTypes.missing_purchase_id)
        order_id = (self._resolve_supply_strategy(package_details)
         .order(package_details, user_id, self.supply_config[package_details.get("supply method")], on_arrival))
        logger.info(f"Processed supply for package {package_details} to user {user_id}")
        return order_id
    
    def process_supply_cancel(self, package_details: Dict, order_id: int) -> int:
        """
            * process_supply_cancel is a method that cancels a supply using the SupplyHandler's SupplyAdapter object.
            * process_supply_cancel should return True if the supply was successfully canceled, and False / raise exception otherwise.
        """
        if "supply method" not in package_details:
            raise ThirdPartyHandlerError("Missing supply method in package details", ThirdPartyHandlerErrorTypes.missing_supply_method)
        if "address" not in package_details:
            raise ThirdPartyHandlerError("Missing address in package details", ThirdPartyHandlerErrorTypes.missing_address)
        if not self._validate_supply_method(package_details.get("supply method"), package_details.get("address")):
            raise ThirdPartyHandlerError("supply method not supported for address", ThirdPartyHandlerErrorTypes.supply_method_not_supported)
        if "arrival time" not in package_details:
            raise ThirdPartyHandlerError("Missing arrival time in package details", ThirdPartyHandlerErrorTypes.missing_arrival_time)
        if "purchase id" not in package_details:
            raise ThirdPartyHandlerError("Missing purchase id in package details" , ThirdPartyHandlerErrorTypes.missing_purchase_id)
        return (self._resolve_supply_strategy(package_details)
                .cancel_order(package_details, order_id))

    def edit_supply_method(self, method_name: str, editing_data: Dict) -> None:
        """
            * edit_supply_method is a method that edits a supply method.
            * edit_supply_method should return True if the supply method was edited successfully, and False / raise
            exception otherwise.
        """
        if method_name not in self.supply_config:
            raise ThirdPartyHandlerError("supply method not supported", ThirdPartyHandlerErrorTypes.supply_method_not_supported)
        self.supply_config[method_name] = editing_data
        logger.info(f"Edited supply method {method_name}")

    def add_supply_method(self, method_name: str, config: Dict) -> None:
        """
            * add_supply_method is a method that marks a user's supply method as fully supported in the system.
        """
        if method_name in self.supply_config:
            raise ThirdPartyHandlerError("supply method already supported", ThirdPartyHandlerErrorTypes.supply_method_already_supported)
        self.supply_config[method_name] = config
        logger.info(f"Added supply method {method_name}")

    def remove_supply_method(self, method_name: str) -> None:
        """
            * remove_supply_method is a method that marks a user's supply method as unsupported in the system.
        """
        if method_name not in self.supply_config:
            raise ThirdPartyHandlerError("supply method not supported", ThirdPartyHandlerErrorTypes.supply_method_not_supported)
        del self.supply_config[method_name]
        logger.info(f"Removed supply method {method_name}")

    def get_supply_methods(self) -> List[str]:
        """
            * get_supply_methods is a method that returns the list of supported supply methods.
        """
        return self.EXISTING_SUPPLY_METHODS
    
    def get_active_supply_methods(self) -> List[str]:
        """
            * get_active_supply_methods is a method that returns the active supply methods.
        """
        return list(self.supply_config.keys())
