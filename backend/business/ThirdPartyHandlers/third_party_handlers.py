from abc import ABC, abstractmethod
from typing import Dict


class PaymentStrategy(ABC):
    """
        * PaymentStrategy is an abstract class that defines the interface for payment strategies.
        * Concrete implementations of PaymentStrategy should implement the pay method.
        * Each pay method is an adapter for a specific external payment gateway.
    """
    @abstractmethod
    def pay(self, amount: float) -> bool:
        """
            * pay is an abstract method that should be implemented by concrete payment strategies.
            * pay should return True if the payment was successful, and False / raise exception otherwise otherwise.
        """
        pass

class BogoPayment(PaymentStrategy):
    def pay(self, amount: float) -> bool:
        """
            * For testing purposes, BogoPayment always returns True.
        """
        return True

class PaymentHandler:
    def _resolve_payment_strategy(self, payment_details: Dict) -> PaymentStrategy:
        """
            * _resolve_payment_strategy is a private method that resolves a payment strategy based on the payment method.
            * _resolve_payment_strategy should return an instance of a PaymentStrategy subclass.
        """
        method = payment_details.get("payment method") # NOTE: << should make the requested value a constant >>
        if method == "bogo": # NOTE: << should make the requested value a constant >>
            return BogoPayment()
        else:
            raise ValueError("Invalid payment method")

    def process_payment(self, amount: float, payment_details: Dict) -> bool:
        """
            * process_payment is a method that processes a payment using the PaymentHandler's PaymentStrategy object.
            * process_payment should return True if the payment was successful, and False / raise exception otherwise.
        """
        # NOTE: << should log payment here >>
        return self._resolve_payment_strategy(payment_details).pay(amount)
        


class SupplyStrategy(ABC):
    """
        * SupplyStrategy is an abstract class that defines the interface for supply strategies.
        * Concrete implementations of SupplyStrategy should implement the pay method.
        * Each pay method is an adapter for a specific external payment gateway.
    """
    @abstractmethod
    def order(self, package_details: Dict, user_id: int) -> str:
        """
            * order is an abstract method that should be implemented by concrete supply strategies.
            * order should return True if the order was successful, and False / raise exception otherwise.
        """
        pass

class BogoSupply(SupplyStrategy):
    def order(self, package_details: Dict, user_id: int) -> bool:
        """
            * For testing purposes, BogoSupply always returns True.
        """
        return True
    
class SupplyHandler:
    def _resolve_supply_strategy(self, package_details: Dict) -> SupplyStrategy:
        """
            * _resolve_supply_strategy is a private method that resolves a supply strategy based on the package details.
            * _resolve_supply_strategy should return an instance of a SupplyStrategy subclass.
        """
        method = package_details.get("supply method")
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
        return self._resolve_supply_strategy(package_details).order(package_details, user_id)