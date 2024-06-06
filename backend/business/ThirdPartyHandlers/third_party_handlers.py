from abc import ABC, abstractmethod
from typing import Dict, Tuple, Callable
from datetime import datetime, timedelta
import time

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
    def pay(self, amount: float, payment_config: Dict) -> bool:
        """
            * pay is an abstract method that should be implemented by concrete payment strategies.
            * pay should return True if the payment was successful, and False / raise exception otherwise.
        """
        pass


class BogoPayment(PaymentAdapter):
    def pay(self, amount: float, payment_config: Dict) -> bool:
        """
            * For testing purposes, BogoPayment pay always returns True.
        """
        return True


class PaymentHandler:
    __instance: bool = None

    def __new__(cls):
        if PaymentHandler.__instance is None:
            PaymentHandler.__instance = object.__new__(cls)
        return PaymentHandler.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized: bool = True
            self.payment_config: Dict = {"bogo": {}}

    def reset(self) -> None:
        """
            * reset is a method that resets the PaymentHandler's payment_config attribute.
        """
        self.payment_config = {"bogo": {}}

    def _resolve_payment_strategy(self, payment_details: Dict) -> PaymentAdapter:
        """
            * _resolve_payment_strategy is a method that resolves a payment strategy based on the payment method.
            * _resolve_payment_strategy should return an instance of a PaymentAdapter subclass.
        """
        method = payment_details.get("payment method")  # NOTE: << should make the requested value a constant >>
        if method not in self.payment_config:
            raise ValueError("payment method not supported")
        elif method == "bogo":  # NOTE: << should make the requested value a constant >>
            return BogoPayment()
        else:
            raise ValueError("Invalid payment method")

    def process_payment(self, amount: float, payment_details: Dict) -> bool:
        """
            * process_payment is a method that processes a payment using the PaymentHandler's PaymentAdapter object.
            * process_payment should return True if the payment was successful, and False / raise exception otherwise.
        """
   
        logger.info(f"Processing payment of {amount} with details {payment_details}")
        return (self._resolve_payment_strategy(payment_details)
                .pay(amount, self.payment_config[payment_details.get("payment method")]))

    def edit_payment_method(self, method_name: str, editing_data: Dict) -> None:
        """
            * edit_payment_method is a method that edits the current methos configuration.
            * edit_payment_method should return True if the payment method was edited successfully, and False / raise
            exception otherwise.
        """

        if method_name not in self.payment_config:
            raise ValueError("payment method not supported")
        self.payment_config[method_name] = editing_data
        logger.info(f"Edited payment method {method_name}") 

    def add_payment_method(self, method_name: str, config: Dict) -> None:
        """
            * add_payment_method is a method that marks a user's payment method as fully supported in the system.
        """
        if method_name in self.payment_config:
            raise ValueError("payment method already supported")
        self.payment_config[method_name] = config
        logger.info(f"Added payment method {method_name}")

    def remove_payment_method(self, method_name: str) -> None:
        """
            * remove_payment_method is a method that marks a user's payment method as unsupported in the system.
        """
        
        if method_name not in self.payment_config:
            raise ValueError("payment method not supported")
        del self.payment_config[method_name]
        logger.info(f"Removed payment method {method_name}")


class SupplyAdapter(ABC):
    """
        * SupplyAdapter is an abstract class that defines the interface for supply strategies.
        * Concrete implementations of SupplyAdapter should implement the pay method.
        * Each pay method is an adapter for a specific external payment gateway.
    """

    @abstractmethod
    def order(self, package_details: Dict, user_id: int, supply_config: Dict, on_arrival: Callable[[int], None]) -> None:
        """
            * order is an abstract method that should be implemented by concrete supply strategies.
            * order should wait for the supply to arrive and call the on_arrival callback.
        """
        pass


class BogoSupply(SupplyAdapter):
    def order(self, package_details: Dict, user_id: int, supply_config: Dict, on_arrival: Callable[[int], None]) -> None:
        """
            * For testing purposes, BogoSupply always returns True.
        """
        arrival_time = package_details.get("arrival time")
        sleep_time = (arrival_time - datetime.now()).total_seconds()
        pur_id = package_details.get("purchase id")
        time.sleep(sleep_time)
        on_arrival(pur_id)


class SupplyHandler:
    __instance = None

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
            raise ValueError(f"supply method not supported for address: {address}")
        
        time = datetime.now() + timedelta(minutes=1)
        logger.info(f"Estimated delivery time: {time} - for package {package_details} to address {address}")
        return time

    def _resolve_supply_strategy(self, package_details: Dict) -> SupplyAdapter:
        """
            * _resolve_supply_strategy is a private method that resolves a supply strategy based on the package details.
            * _resolve_supply_strategy should return an instance of a SupplyAdapter subclass.
        """
        method = package_details.get("supply method")
        if method not in self.supply_config:
            raise ValueError("supply method not supported")
        if "arrival time" not in package_details:
            raise ValueError("Missing arrival time in package details")
        date = package_details.get("arrival time")
        if date < datetime.now():
            raise ValueError("arrival time cannot be in the past")
        if method == "bogo":
            return BogoSupply()
        else:
            raise ValueError("Invalid supply method")

    def process_supply(self, package_details: Dict, user_id: int, on_arrival: Callable[[int], None]) -> None:
        """
            * process_supply is a method that processes a supply using the SupplyHandler's SupplyAdapter object.
            * process_supply should return True if the supply was successful, and False / raise exception otherwise.
        """
        if "supply method" not in package_details:
            raise ValueError("Missing supply method in package details")
        if "address" not in package_details:
            raise ValueError("Missing address in package details")
        if not self._validate_supply_method(package_details.get("supply method"), package_details.get("address")):
            raise ValueError("supply method not supported for address")
        if "arrival time" not in package_details:
            raise ValueError("Missing arrival time in package details")
        if "purchase id" not in package_details:
            raise ValueError("Missing purchase id in package details")
        (self._resolve_supply_strategy(package_details)
         .order(package_details, user_id, self.supply_config[package_details.get("supply method")], on_arrival))
        logger.info(f"Processed supply for package {package_details} to user {user_id}")

    def edit_supply_method(self, method_name: str, editing_data: Dict) -> None:
        """
            * edit_supply_method is a method that edits a supply method.
            * edit_supply_method should return True if the supply method was edited successfully, and False / raise
            exception otherwise.
        """
        if method_name not in self.supply_config:
            raise ValueError("supply method not supported")
        self.supply_config[method_name] = editing_data
        logger.info(f"Edited supply method {method_name}")

    def add_supply_method(self, method_name: str, config: Dict) -> None:
        """
            * add_supply_method is a method that marks a user's supply method as fully supported in the system.
        """
        if method_name in self.supply_config:
            raise ValueError("supply method already supported")
        self.supply_config[method_name] = config
        logger.info(f"Added supply method {method_name}")

    def remove_supply_method(self, method_name: str) -> None:
        """
            * remove_supply_method is a method that marks a user's supply method as unsupported in the system.
        """
        if method_name not in self.supply_config:
            raise ValueError("supply method not supported")
        del self.supply_config[method_name]
        logger.info(f"Removed supply method {method_name}")
