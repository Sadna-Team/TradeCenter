# communication with business logic
from abc import ABC, abstractmethod
from backend.business.market import MarketFacade
from flask import jsonify
from typing import Dict

import logging

logger = logging.getLogger('myapp')


class ThirdPartyService(ABC):
    def __init__(self):
        self._market_facade = MarketFacade()

    @abstractmethod
    def add_third_party_service(self, user_id: int, method_name: str, config: Dict):
        """
            Add a third party service to be supported by the platform
        """
        pass

    @abstractmethod
    def edit_third_party_service(self, user_id: int, method_name: str, editing_data: Dict):
        """
            Edit a third party service supported by the platform
        """
        pass

    @abstractmethod
    def delete_third_party_service(self, user_id: int, method_name: str):
        """
            Delete a third party service supported by the platform
        """
        pass


class PaymentService(ThirdPartyService):
    def __init__(self):
        super().__init__()

    def get_all_methods(self, user_id: int):
        """
            Get all payment methods in the system
        """
        try:
            methods = self._market_facade.get_payment_methods(user_id)
            logger.info('Payment methods retrieved successfully')
            return jsonify({'message': methods}), 200
        except Exception as e:
            logger.error('Failed to retrieve payment methods')
            return jsonify({'message': str(e)}), 400
        
    def get_all_active_methods(self, user_id: int):
        """
            Get all active payment methods in the system
        """
        try:
            methods = self._market_facade.get_active_payment_methods(user_id)
            logger.info('Active payment methods retrieved successfully')
            return jsonify({'message': methods}), 200
        except Exception as e:
            logger.error('Failed to retrieve active payment methods')
            return jsonify({'message': str(e)}), 400

    def add_third_party_service(self, user_id: int, method_name: str, config: Dict):
        """
            Add a third party service to be supported by the platform
        """
        try:
            self._market_facade.add_payment_method(user_id, method_name, config)
            logger.info('Third party payment service added successfully')
            return jsonify({'message': 'Third party payment service added successfully'}), 200
        except Exception as e:
            logger.error('Failed to add third party payment service')
            return jsonify({'message': str(e)}), 400

    def edit_third_party_service(self, user_id: int, method_name: str, editing_data: Dict):
        """
            Edit a third party service supported by the platform
        """
        try:
            self._market_facade.edit_payment_method(user_id, method_name, editing_data)
            logger.info('Third party payment service edited successfully')
            return jsonify({'message': 'Third party payment service edited successfully'}), 200
        except Exception as e:
            logger.error('Failed to edit third party payment service')
            return jsonify({'message': str(e)}), 400

    def delete_third_party_service(self, user_id: int, method_name: str):
        """
            Delete a third party service supported by the platform
        """
        try:
            self._market_facade.remove_payment_method(user_id, method_name)
            logger.info('Third party payment service deleted successfully')
            return jsonify({'message': 'Third party payment service deleted successfully'}), 200
        except Exception as e:
            logger.error('Failed to delete third party payment service')
            return jsonify({'message': str(e)}), 400


class SupplyService(ThirdPartyService):
    def __init__(self):
        super().__init__()

    def get_all_methods(self, user_id: int):
        """
            Get all supply methods in the system
        """
        try:
            methods = self._market_facade.get_supply_methods(user_id)
            logger.info('Supply methods retrieved successfully')
            return jsonify({'message': methods}), 200
        except Exception as e:
            logger.error('Failed to retrieve supply methods')
            return jsonify({'message': str(e)}), 400
        
    def get_all_active_methods(self, user_id: int):
        """
            Get all active supply methods in the system
        """
        try:
            methods = self._market_facade.get_active_supply_methods(user_id)
            logger.info('Active supply methods retrieved successfully')
            return jsonify({'message': methods}), 200
        except Exception as e:
            logger.error('Failed to retrieve active supply methods')
            return jsonify({'message': str(e)}), 400

    def add_third_party_service(self, user_id: int, method_name: str, config: Dict):
        """
            Add a third party service to be supported by the platform
        """
        try:
            self._market_facade.add_supply_method(user_id, method_name, config)
            logger.info('Third party supply service added successfully')
            return jsonify({'message': 'Third party supply service added successfully'}), 200
        except Exception as e:
            logger.error('Failed to add third party supply service')
            return jsonify({'message': str(e)}), 400

    def edit_third_party_service(self, user_id: int, method_name: str, editing_data: Dict):
        """
            Edit a third party service supported by the platform
        """
        try:
            self._market_facade.edit_supply_method(user_id, method_name, editing_data)
            logger.info('Third party supply service edited successfully')
            return jsonify({'message': 'Third party supply service edited successfully'}), 200
        except Exception as e:
            logger.error('Failed to edit third party supply service')
            return jsonify({'message': str(e)}), 400

    def delete_third_party_service(self, user_id: int, method_name: str):
        """
            Delete a third party service supported by the platform
        """
        try:
            self._market_facade.remove_supply_method(user_id, method_name)
            logger.info('Third party supply service deleted successfully')
            return jsonify({'message': 'Third party supply service deleted successfully'}), 200
        except Exception as e:
            logger.error('Failed to delete third party supply service')
            return jsonify({'message': str(e)}), 400
