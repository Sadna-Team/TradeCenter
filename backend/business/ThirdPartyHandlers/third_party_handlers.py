from abc import ABC, abstractmethod
from typing import Dict, Tuple, Callable, List
from datetime import datetime, timedelta
import time
import threading
from backend.error_types import *
import requests
from backend.database import db
from sqlalchemy import Column, Integer, JSON
from typing import ClassVar
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker




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
    
class ExternalPayment(PaymentAdapter):
    HANDSHAKE = {"action_type": "handshake"}
    PAY = {"action_type": "pay"}
    CANCEL = {"action_type": "cancel_pay"}
    CANCEL = {"action_type": "cancel_pay"}
    URL = "https://damp-lynna-wsep-1984852e.koyeb.app/"
    def pay(self, amount: float, payment_config: Dict) -> int:
        """
            * makes POST request to external payment gateway to process payment.
            * first sends a handshake request to the gateway to confirm connection, expects "OK" message.
            * then sends a payment request to the gateway to process the payment. expect integer in the range [10000, 100000].
            * if -1, payment failed.
        """
        logger.info(f"Processing payment of {amount} with details {payment_config}")
        response = requests.post(self.URL, json=self.HANDSHAKE, timeout=5)
        if response.status_code != 200:
            raise ThirdPartyHandlerError("Failed to connect to external payment gateway", ThirdPartyHandlerErrorTypes.handshake_failed)
        if not response.ok or not response.reason == "OK":
            raise ThirdPartyHandlerError("Failed to connect to external payment gateway", ThirdPartyHandlerErrorTypes.handshake_failed)
        # add to payment_config the PAY
        
        payment_config["amount"] = str(amount)
        payment_config = payment_config | self.PAY
        response = requests.post(self.URL, data=payment_config, timeout=5)
        print(payment_config)
        if response.status_code != 200:
            raise ThirdPartyHandlerError("Failed to process payment", ThirdPartyHandlerErrorTypes.external_payment_failed)
        if not 10000 <= response.json() <= 100000:
            raise ThirdPartyHandlerError("Failed to process payment", ThirdPartyHandlerErrorTypes.external_payment_failed)
        return response.json()
        
    
    def cancel_payment(self, payment_id: int) -> int:
        """
            * makes POST request to external payment gateway to cancel payment.
            * first sends a handshake request to the gateway to confirm connection, expects "OK" message.
            * then sends a cancel payment request to the gateway to cancel the payment. expect 1.
        """
        response = requests.post(self.URL, json=self.HANDSHAKE, timeout=5)
        if response.status_code != 200:
            raise ThirdPartyHandlerError("Failed to connect to external payment gateway", ThirdPartyHandlerErrorTypes.handshake_failed)
        if not response.ok or not response.reason == "OK":
            raise ThirdPartyHandlerError("Failed to connect to external payment gateway", ThirdPartyHandlerErrorTypes.handshake_failed)
        # add to payment_config the CANCEL
        payment_config = self.CANCEL | {"transaction_id": payment_id}
        response = requests.post(self.URL, data=payment_config, timeout=5)
        if response.status_code != 200:
            raise ThirdPartyHandlerError("Failed to cancel payment", ThirdPartyHandlerErrorTypes.external_payment_failed)
        if not response.json() == 1:
            raise ThirdPartyHandlerError("Failed to cancel payment", ThirdPartyHandlerErrorTypes.external_payment_failed)
        return response.json()


class PaymentHandler(db.Model):
    __tablename__ = 'payment_handler'

    id = Column(Integer, primary_key=True)
    payment_config = Column(JSON, default={"bogo": {}, "external payment": {}})

    EXISTING_PAYMENT_METHODS: ClassVar[list] = ["bogo", "external payment"]

    __instance: ClassVar['PaymentHandler'] = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(PaymentHandler, cls).__new__(cls)
            with db.session() as session:
                instance = session.query(cls).first()
                logger.info(f"Instance: {instance}")
                if instance is None:
                    instance = cls()
                    session.add(instance)
                    session.commit()
                cls.__instance = instance
        return cls.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.payment_config = {"bogo": {}, "external payment": {}}  # Initialize payment_config if not initialized

    def reset(self) -> None:
        self.payment_config = {"bogo": {}, "external payment": {}}
        db.session.commit()

    def _resolve_payment_strategy(self, payment_details: dict):
        method = payment_details.get("payment method")
        if method not in self.payment_config:
            raise ThirdPartyHandlerError("payment method not supported",
                                         ThirdPartyHandlerErrorTypes.payment_method_not_supported)
        elif method == "bogo":
            return BogoPayment()
        elif method == "external payment":
            return ExternalPayment()
        else:
            raise ThirdPartyHandlerError("Invalid payment method", ThirdPartyHandlerErrorTypes.invalid_payment_method)

    def process_payment(self, amount: float, payment_details: dict) -> int:
        logger.info(f"Processing payment of {amount} with details {payment_details}")
        handler = self._resolve_payment_strategy(payment_details)
        if payment_details.get("payment method") == "bogo":
            return handler.pay(amount, {})
        elif payment_details.get("payment method") == "external payment":
            return handler.pay(amount, payment_details.get("additional details"))
        else:
            logger.info(f"Invalid payment method {payment_details.get('payment method')}")
            raise ThirdPartyHandlerError("Invalid payment method", ThirdPartyHandlerErrorTypes.invalid_payment_method)

    def process_payment_cancel(self, payment_details: dict, payment_id: int) -> int:
        return self._resolve_payment_strategy(payment_details).cancel_payment(payment_id)

    def edit_payment_method(self, method_name: str, editing_data: dict) -> None:
        if method_name not in self.payment_config:
            raise ThirdPartyHandlerError("payment method not supported",
                                         ThirdPartyHandlerErrorTypes.payment_method_not_supported)
        self.payment_config[method_name] = editing_data
        logger.info(f"Edited payment method {method_name}")
        db.session.flush()

    def add_payment_method(self, method_name: str, config: dict) -> None:
        if method_name in self.payment_config:
            raise ThirdPartyHandlerError("payment method already supported",
                                         ThirdPartyHandlerErrorTypes.payment_method_already_supported)
        self.payment_config[method_name] = config
        logger.info(f"Added payment method {method_name}")
        db.session.flush()

    def remove_payment_method(self, method_name: str) -> None:
        if method_name not in self.payment_config:
            raise ThirdPartyHandlerError("payment method not supported",
                                         ThirdPartyHandlerErrorTypes.payment_method_not_supported)
        logger.info(f"Removing payment method {method_name}")
        del self.payment_config[method_name]
        logger.info(f"Removed payment method {method_name}")
        db.session.flush()

    def get_payment_methods(self) -> list:
        return self.EXISTING_PAYMENT_METHODS

    def get_active_payment_methods(self) -> list:
        return list(self.payment_config.keys())


class SupplyAdapter(ABC):
    """
        * SupplyAdapter is an abstract class that defines the interface for supply strategies.
        * Concrete implementations of SupplyAdapter should implement the pay method.
        * Each pay method is an adapter for a specific external payment gateway.
    """

    @abstractmethod
    def order(self, package_details: Dict, on_arrival: Callable[[int], None]) -> int:
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
    def order(self, package_details: Dict, on_arrival: Callable[[int], None]) -> int:
        """
            * For testing purposes, BogoSupply always returns True.
        """
        arrival_time = package_details.get("arrival time")
        sleep_time = (arrival_time - datetime.now()).total_seconds()
        pur_id = package_details.get("purchase id")
        thread = threading.Thread(target=do_task, args=(pur_id, sleep_time, on_arrival))
        thread.start()
        return 1

    def cancel_order(self, order_id: int) -> int:
        """
            * For testing purposes, BogoSupply cancel_order always returns True.
        """
        return 1
    
class ExternalSupply(SupplyAdapter):
    HANDSHAKE = {"action_type": "handshake"}
    ORDER = {"action_type": "supply"}
    CANCEL = {"action_type": "cancel_supply"}
    URL = "https://damp-lynna-wsep-1984852e.koyeb.app/"
    def order(self, package_details: Dict, on_arrival: Callable[[int], None]) -> int:
        """
            * makes POST request to external supply gateway to process supply.
            * first sends a handshake request to the gateway to confirm connection, expects "OK" message.
            * then sends a supply request to the gateway to process the supply. expect integer in the range [10000, 100000].
            * if -1, supply failed.
        """
        logger.info(f"Processing supply with details {package_details}")
        response = requests.post(self.URL, json=self.HANDSHAKE, timeout=5)
        if response.status_code != 200:
            raise ThirdPartyHandlerError("Failed to connect to external supply gateway", ThirdPartyHandlerErrorTypes.handshake_failed)
        if not response.ok or not response.reason == "OK":
            raise ThirdPartyHandlerError("Failed to connect to external supply gateway", ThirdPartyHandlerErrorTypes.handshake_failed)
        # add to payment_config the ORDER
        package_details_to_send = package_details.copy()
        package_details_to_send = package_details_to_send.get("additional details") | self.ORDER
        response = requests.post(self.URL, data=package_details_to_send, timeout=5)
        if response.status_code != 200:
            raise ThirdPartyHandlerError("Failed to process supply", ThirdPartyHandlerErrorTypes.external_supply_failed)
        if not 10000 <= response.json() <= 100000:
            raise ThirdPartyHandlerError("Failed to process supply", ThirdPartyHandlerErrorTypes.external_supply_failed)
        order_id = response.json()
        arrival_time = package_details.get("arrival time")
        sleep_time = (arrival_time - datetime.now()).total_seconds()
        pur_id = package_details.get("purchase id")
        thread = threading.Thread(target=do_task, args=(pur_id, sleep_time, on_arrival))
        thread.start()
        return order_id


    def cancel_order(self, order_id: int) -> int:
        """
            * makes POST request to external supply gateway to cancel supply.
            * first sends a handshake request to the gateway to confirm connection, expects "OK" message.
            * then sends a cancel supply request to the gateway to cancel the supply. expect 1.
        """
        response = requests.post(self.URL, json=self.HANDSHAKE, timeout=5)
        if response.status_code != 200:
            raise ThirdPartyHandlerError("Failed to connect to external supply gateway", ThirdPartyHandlerErrorTypes.handshake_failed)
        if not response.ok or not response.reason == "OK":
            raise ThirdPartyHandlerError("Failed to connect to external supply gateway", ThirdPartyHandlerErrorTypes.handshake_failed)
        # add to payment_config the CANCEL
        package_details = self.CANCEL | {"transaction_id": order_id}
        response = requests.post(self.URL, data=package_details, timeout=5)
        if response.status_code != 200:
            raise ThirdPartyHandlerError("Failed to cancel supply", ThirdPartyHandlerErrorTypes.external_supply_failed)
        if not response.json() == 1:
            raise ThirdPartyHandlerError("Failed to cancel supply", ThirdPartyHandlerErrorTypes.external_supply_failed)
        return response.json()


# ----------------------------------------- Will be used for address validation using Google Maps API later on ----------------------------------------- #
class SupplyHandler(db.Model):
    __tablename__ = 'supply_handler'

    id = Column(Integer, primary_key=True)
    supply_config = Column(JSON, default={"bogo": {}, "external supply": {}})

    EXISTING_SUPPLY_METHODS: ClassVar[list] = ["bogo", "external supply"]

    __instance: ClassVar['SupplyHandler'] = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SupplyHandler, cls).__new__(cls)
            with db.session() as session:
                instance = session.query(cls).first()
                if instance is None:
                    instance = cls()
                    session.add(instance)
                    session.commit()
                cls.__instance = instance
        return cls.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.supply_config: Dict = {"bogo": {}, "external supply": {}}

    def reset(self) -> None:
        self.supply_config = {"bogo": {}, "external supply": {}}
        db.session.commit()

    def _validate_supply_method(self, method_name: str, address: dict) -> bool:
        """
        Validate the supply method for the given address.
        """
        logger.info(f"Validating supply method {method_name} for address {address}")
        return method_name in self.supply_config

    def get_delivery_time(self, package_details: Dict, address: Dict) -> datetime:
        """
        Get the estimated delivery time for a package.
        """
        if not self._validate_supply_method(package_details.get("supply method"), address):
            raise ThirdPartyHandlerError(f"supply method not supported for address: {address}",
                                         ThirdPartyHandlerErrorTypes.supply_method_not_supported)
        time = datetime.now() + timedelta(seconds=5)
        logger.info(f"Estimated delivery time: {time} - for package {package_details} to address {address}")
        return time

    def _resolve_supply_strategy(self, package_details: Dict):
        """
        Resolve the supply strategy based on the package details.
        """
        method = package_details.get("supply method")
        if method not in self.supply_config:
            raise ThirdPartyHandlerError("supply method not supported",
                                         ThirdPartyHandlerErrorTypes.supply_method_not_supported)
        if "arrival time" not in package_details:
            raise ThirdPartyHandlerError("Missing arrival time in package details",
                                         ThirdPartyHandlerErrorTypes.missing_arrival_time)
        date: datetime = package_details.get("arrival time")
        date_now = datetime.now()
        if date < date_now:
            raise ThirdPartyHandlerError("arrival time cannot be in the past",
                                         ThirdPartyHandlerErrorTypes.invalid_arrival_time)
        if method == "bogo":
            return BogoSupply()
        elif method == "external supply":
            return ExternalSupply()
        else:
            raise ThirdPartyHandlerError("Invalid supply method", ThirdPartyHandlerErrorTypes.invalid_supply_method)

    def process_supply(self, package_details: Dict, user_id: int, on_arrival: Callable[[int], None]) -> int:
        """
        Process the supply using the SupplyHandler's SupplyAdapter object.
        """
        if "supply method" not in package_details:
            raise ThirdPartyHandlerError("Missing supply method in package details",
                                         ThirdPartyHandlerErrorTypes.missing_supply_method)
        if not self._validate_supply_method(package_details.get("supply method"), package_details.get("address")):
            raise ThirdPartyHandlerError("supply method not supported for address",
                                         ThirdPartyHandlerErrorTypes.supply_method_not_supported)
        if "arrival time" not in package_details:
            raise ThirdPartyHandlerError("Missing arrival time in package details",
                                         ThirdPartyHandlerErrorTypes.missing_arrival_time)
        if "purchase id" not in package_details:
            raise ThirdPartyHandlerError("Missing purchase id in package details",
                                         ThirdPartyHandlerErrorTypes.missing_purchase_id)
        order_id = (self._resolve_supply_strategy(package_details)
                    .order(package_details, on_arrival))
        logger.info(f"Processed supply for package {package_details}")
        return order_id

    def process_supply_cancel(self, package_details: Dict, order_id: int) -> int:
        """
        Cancel the supply using the SupplyHandler's SupplyAdapter object.
        """
        return (self._resolve_supply_strategy(package_details)
                .cancel_order(order_id))

    def edit_supply_method(self, method_name: str, editing_data: Dict) -> None:
        """
        Edit a supply method.
        """
        if method_name not in self.supply_config:
            raise ThirdPartyHandlerError("supply method not supported",
                                         ThirdPartyHandlerErrorTypes.supply_method_not_supported)
        self.supply_config[method_name] = editing_data
        logger.info(f"Edited supply method {method_name}")
        db.session.flush()

    def add_supply_method(self, method_name: str, config: Dict) -> None:
        """
        Add a new supply method.
        """
        if method_name in self.supply_config:
            raise ThirdPartyHandlerError("supply method already supported",
                                         ThirdPartyHandlerErrorTypes.supply_method_already_supported)
        self.supply_config[method_name] = config
        logger.info(f"Added supply method {method_name}")
        db.session.flush()

    def remove_supply_method(self, method_name: str) -> None:
        """
        Remove a supply method.
        """
        if method_name not in self.supply_config:
            raise ThirdPartyHandlerError("supply method not supported",
                                         ThirdPartyHandlerErrorTypes.supply_method_not_supported)
        del self.supply_config[method_name]
        logger.info(f"Removed supply method {method_name}")
        db.session.flush()

    def get_supply_methods(self) -> List[str]:
        """
        Get the list of supported supply methods.
        """
        return self.EXISTING_SUPPLY_METHODS

    def get_active_supply_methods(self) -> List[str]:
        """
        Get the active supply methods.
        """
        return list(self.supply_config.keys())
