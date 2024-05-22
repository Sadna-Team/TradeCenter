# communication with business logic
from abc import ABC, abstractmethod
from backend.business.ThirdPartyHandlers.third_party_handlers import PaymentHandler, SupplyHandler
from typing import Dict

class ThirdPartyService(ABC):
    @abstractmethod
    def add_third_party_service(self, method_name: str, config: Dict) -> None:
        """
            Use Case 1.2.1:
            Add a third party service to be supported by the platform

            Args:
                method_name (str): name of the third party service
                config (dict): configuration of the third party service

            Returns:
                ?
        """
        pass
    
    @abstractmethod
    def edit_third_party_service(self, method_name: str, editing_data: Dict) -> None:
        """
            Use Case 1.2.2:
            Edit a third party service supported by the platform

            Args:
                method_name (str): name of the third party service
                editing_data (dict): data to be edited

            Returns:
                ?
        """
        pass

    @abstractmethod
    def delete_third_party_service(self, method_name: str) -> None:
        """
            Use Case 1.2.3:
            Delete a third party service supported by the platform

            Args:
                method_name (str): name of the third party service

            Returns:
                ?
        """
        pass

class PaymentService(ThirdPartyService):

    def add_third_party_service(self, method_name: str, config: Dict) -> None:
        """
            Use Case 1.2.1:
            Add a third party service to be supported by the platform

            Args:
                method_name (str): name of the third party service
                config (dict): configuration of the third party service
        """
        PaymentHandler().add_payment_method(method_name, config)

    def edit_third_party_service(self, method_name: str, editing_data: Dict) -> None:
        """
            Use Case 1.2.2:
            Edit a third party service supported by the platform

            Args:
                method_name (str): name of the third party service
                editing_data (dict): data to be edited
        """
        PaymentHandler().edit_payment_method(method_name, editing_data)

    def delete_third_party_service(self, method_name: str) -> None:
        """
            Use Case 1.2.3:
            Delete a third party service supported by the platform

            Args:
                method_name (str): name of the third party service
        """
        PaymentHandler().remove_payment_method(method_name)

class SupplyService(ThirdPartyService):
    def add_third_party_service(self, method_name: str, config: Dict) -> None:
        """
            Use Case 1.2.1:
            Add a third party service to be supported by the platform

            Args:
                method_name (str): name of the third party service
                config (dict): configuration of the third party service
        """
        SupplyHandler().add_supply_method(method_name, config)

    def edit_third_party_service(self, method_name: str, editing_data: Dict) -> None:
        """
            Use Case 1.2.2:
            Edit a third party service supported by the platform

            Args:
                method_name (str): name of the third party service
                editing_data (dict): data to be edited
        """
        SupplyHandler().edit_supply_method(method_name, editing_data)

    def delete_third_party_service(self, method_name: str) -> None:
        """
            Use Case 1.2.3:
            Delete a third party service supported by the platform

            Args:
                method_name (str): name of the third party service
        """
        SupplyHandler().remove_supply_method(method_name)
