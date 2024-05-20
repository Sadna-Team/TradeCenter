from abc import ABC, abstractmethod
from typing import Dict, List


class PaymentStrategy(ABC):
    """
        * PaymentStrategy is an abstract class that defines the interface for payment strategies.
        * Concrete implementations of PaymentStrategy should implement the pay method.
        * Each pay method is an adapter for a specific external payment gateway.
    """

    @abstractmethod
    def pay(self, amount: float, payment_config: Dict) -> bool:
        """
            * pay is an abstract method that should be implemented by concrete payment strategies.
            * pay should return True if the payment was successful, and False / raise exception otherwise.
        """
        pass


class BogoPayment(PaymentStrategy):
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

    def _resolve_payment_strategy(self, payment_details: Dict) -> PaymentStrategy:
        """
            * _resolve_payment_strategy is a method that resolves a payment strategy based on the payment method.
            * _resolve_payment_strategy should return an instance of a PaymentStrategy subclass.
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
            * process_payment is a method that processes a payment using the PaymentHandler's PaymentStrategy object.
            * process_payment should return True if the payment was successful, and False / raise exception otherwise.
        """
        # NOTE: << should log payment here >>
        return self._resolve_payment_strategy(payment_details).pay(amount, self.payment_config[payment_details.get("payment method")])
    
    def edit_payment_method(self, method_name: str, editing_data: Dict) -> None:
        """
            * edit_payment_method is a method that edits a user's payment method.
            * edit_payment_method should return True if the payment method was edited successfully, and False / raise exception otherwise.
        """
        # NOTE: << should log payment method edit here >>
        if method_name not in self.payment_config:
            raise ValueError("payment method not supported")
        self.payment_config[method_name] = editing_data
        
    def add_payment_method(self, method_name: str, config: Dict) -> None:
        """
            * add_payment_method is a method that marks a user's payment method as fully supported in the system.
        """
        # NOTE: << should log payment method add here >>
        if method_name in self.payment_config:
            raise ValueError("payment method already supported")
        self.payment_config[method_name] = config

    def remove_payment_method(self, method_name: str) -> None:
        """
            * remove_payment_method is a method that marks a user's payment method as unsupported in the system.
        """
        # NOTE: << should log payment method remove here >>
        if method_name not in self.payment_config:
            raise ValueError("payment method not supported")
        del self.payment_config[method_name]

class SupplyStrategy(ABC):
    """
        * SupplyStrategy is an abstract class that defines the interface for supply strategies.
        * Concrete implementations of SupplyStrategy should implement the pay method.
        * Each pay method is an adapter for a specific external payment gateway.
    """

    @abstractmethod
    def order(self, package_details: Dict, user_id: int, supply_config: Dict) -> bool:
        """
            * order is an abstract method that should be implemented by concrete supply strategies.
            * order should return True if the order was successful, and False / raise exception otherwise.
        """
        pass


class BogoSupply(SupplyStrategy):
    def order(self, package_details: Dict, user_id: int, supply_config: Dict) -> bool:
        """
            * For testing purposes, BogoSupply always returns True.
        """
        return True


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

    def _resolve_supply_strategy(self, package_details: Dict) -> SupplyStrategy:
        """
            * _resolve_supply_strategy is a private method that resolves a supply strategy based on the package details.
            * _resolve_supply_strategy should return an instance of a SupplyStrategy subclass.
        """
        method = package_details.get("supply method")
        if method not in self.supply_config:
            raise ValueError("supply method not supported")
        if method == "bogo":
            return BogoSupply()
        else:
            raise ValueError("Invalid supply method")

    def process_supply(self, package_details: Dict, user_id: int) -> bool:
        """
            * process_supply is a method that processes a supply using the SupplyHandler's SupplyStrategy object.
            * process_supply should return True if the supply was successful, and False / raise exception otherwise.
        """
        # NOTE: << should log supply here >>
        return self._resolve_supply_strategy(package_details).order(package_details, user_id, 
                                                                    self.supply_config[package_details.get("supply method")])
    
    def edit_supply_method(self, method_name: str, editing_data: Dict) -> None:
        """
            * edit_supply_method is a method that edits a user's supply method.
            * edit_supply_method should return True if the supply method was edited successfully, and False / raise exception otherwise.
        """
        # NOTE: << should log supply method edit here >>
        if method_name not in self.supply_config:
            raise ValueError("supply method not supported")
        self.supply_config[method_name] = editing_data
    
    def add_supply_method(self, method_name: str, config: Dict) -> None:
        """
            * add_supply_method is a method that marks a user's supply method as fully supported in the system.
        """
        # NOTE: << should log supply method add here >>
        if method_name in self.supply_config:
            raise ValueError("supply method already supported")
        self.supply_config[method_name] = config

    def remove_supply_method(self, method_name: str) -> None:
        """
            * remove_supply_method is a method that marks a user's supply method as unsupported in the system.
        """
        # NOTE: << should log supply method remove here >>
        if method_name not in self.supply_config:
            raise ValueError("supply method not supported")
        del self.supply_config[method_name]
