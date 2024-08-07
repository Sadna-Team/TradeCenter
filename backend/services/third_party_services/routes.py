# API endpoints and their corresponding route handlers

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.error_types import *
from backend.services.third_party_services.controllers import PaymentService, SupplyService
from typing import Dict

third_party_bp = Blueprint('third_party', __name__)
supply_service = SupplyService()
payment_service = PaymentService()


@third_party_bp.route('/payment/get_all', methods=['GET'])
@jwt_required()
def get_all_payment_methods():
    """
        Use Case 1.2.4:
        Get all third party payment methods supported by the platform

        Data:
            token (int): token of the user
    """
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return payment_service.get_all_methods(user_id)

@third_party_bp.route('/payment/get_all_active', methods=['GET'])
@jwt_required()
def get_all_active_payment_methods():
    """
        Use Case 1.2.4:
        Get all third party payment methods supported by the platform

        Data:
            token (int): token of the user
    """
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return payment_service.get_all_active_methods(user_id)

@third_party_bp.route('/payment/add', methods=['POST'])
@jwt_required()
def add_third_party_payment_service():
    """
        Use Case 1.2.1:
        Add a third party service to be supported by the platform

        Data:
            token (int): token of the user
            data (dict): data of the third party service to be added
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        method_name: str = str(data.get('method_name'))
        config_helper = data.get('config')
        if not isinstance(config_helper, dict):
            raise ServiceLayerError('config must be a dictionary', ServiceLayerErrorTypes.config_not_dict)
        config = {key: str(value) for key, value in config_helper.items()}
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return payment_service.add_third_party_service(user_id, method_name, config)


@third_party_bp.route('/payment/edit', methods=['PUT'])
@jwt_required()
def edit_third_party_payment_service():
    """
        Use Case 1.2.2:
        Edit a third party service supported by the platform

        Data:
            token (int): token of the user
            service_id (int): id of the third party service to be edited
            data (dict): data of the third party service to be edited
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        method_name = str(data.get('method_name'))
        editing_data_helper = data.get('editing_data')
        if not isinstance(editing_data_helper, dict):
            raise ServiceLayerError('config must be a dictionary', ServiceLayerErrorTypes.config_not_dict)
        editing_data = {key: str(value) for key, value in editing_data_helper.items()}
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return payment_service.edit_third_party_service(user_id, method_name, editing_data)


@third_party_bp.route('/payment/delete', methods=['DELETE', 'POST'])
@jwt_required()
def delete_third_party_payment_service():
    """
        Use Case 1.2.3:
        Delete a third party service supported by the platform

        Data:
            token (int): token of the user
            service_id (int): id of the third party service to be deleted
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        method_name = str(data.get('method_name'))
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return payment_service.delete_third_party_service(user_id, method_name)


@third_party_bp.route('/delivery/get_all', methods=['GET'])
@jwt_required()
def get_all_supply_methods():
    """
        Use Case 1.2.4:
        Get all third party delivery methods supported by the platform

        Data:
            token (int): token of the user
    """
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return supply_service.get_all_methods(user_id)

@third_party_bp.route('/delivery/get_all_active', methods=['GET'])
@jwt_required()
def get_all_active_supply_methods():
    """
        Use Case 1.2.4:
        Get all third party delivery methods supported by the platform

        Data:
            token (int): token of the user
    """
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return supply_service.get_all_active_methods(user_id)

@third_party_bp.route('/delivery/add', methods=['POST'])
@jwt_required()
def add_third_party_delivery_service():
    """
        Use Case 1.2.1:
        Add a third party service to be supported by the platform

        Data:
            token (int): token of the user
            data (dict): data of the third party service to be added
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        method_name = str(data.get('method_name'))
        config_helper = data.get('config')
        if not isinstance(config_helper, dict):
            raise ServiceLayerError('config must be a dictionary', ServiceLayerErrorTypes.config_not_dict)
        config = {key: str(value) for key, value in config_helper.items()}
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return supply_service.add_third_party_service(user_id, method_name, config)


@third_party_bp.route('/delivery/edit', methods=['PUT'])
@jwt_required()
def edit_third_party_delivery_service():
    """
        Use Case 1.2.2:
        Edit a third party service supported by the platform

        Data:
            token (int): token of the user
            service_id (int): id of the third party service to be edited
            data (dict): data of the third party service to be edited
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        method_name = str(data.get('method_name'))
        editing_data_helper = data.get('editing_data')
        if not isinstance(editing_data_helper, dict):
            raise ServiceLayerError('config must be a dictionary', ServiceLayerErrorTypes.config_not_dict)
        editing_data = {key: str(value) for key, value in editing_data_helper.items()}
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return supply_service.edit_third_party_service(user_id, method_name, editing_data)


@third_party_bp.route('/delivery/delete', methods=['DELETE'])
@jwt_required()
def delete_third_party_delivery_service():
    """
        Use Case 1.2.3:
        Delete a third party service supported by the platform

        Data:
            token (int): token of the user
            service_id (int): id of the third party service to be deleted
    """
    try:
        data: Dict = request.get_json()
        user_id = get_jwt_identity()
        method_name = str(data.get('method_name'))
    except Exception as e:
        return jsonify({'message': str(e)}), 400

    return supply_service.delete_third_party_service(user_id, method_name)
