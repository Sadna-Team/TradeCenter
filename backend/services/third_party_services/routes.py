# API endpoints and their corresponding route handlers

from flask import Blueprint, request, jsonify
from backend.business.authentication.authentication import Authentication
from backend.business.user.user import UserFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies
from backend.services.third_party_services.controllers import PaymentService, SupplyService
from typing import Dict

third_party_bp = Blueprint('third_party', __name__)
supply_service = SupplyService()
payment_service = PaymentService()

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
    data = request.get_json()
    token = get_jwt_identity()
    method_name = data.get('method_name')
    config = data.get('config')
    payment_service.add_third_party_service(method_name, config)

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
    data = request.get_json()
    token = get_jwt_identity()
    method_name = data.get('method_name')
    editing_data = data.get('editing_data')
    payment_service.edit_third_party_service(method_name, editing_data)

@third_party_bp.route('/payment/delete', methods=['DELETE'])
@jwt_required()
def delete_third_party_payment_service():
    """
        Use Case 1.2.3:
        Delete a third party service supported by the platform

        Data:
            token (int): token of the user
            service_id (int): id of the third party service to be deleted
    """
    data = request.get_json()
    token = get_jwt_identity()
    method_name = data.get('method_name')
    payment_service.delete_third_party_service(method_name)

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
    data = request.get_json()
    token = get_jwt_identity()
    method_name = data.get('method_name')
    config = data.get('config')
    supply_service.add_third_party_service(method_name, config)

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
    data = request.get_json()
    token = get_jwt_identity()
    method_name = data.get('method_name')
    editing_data = data.get('editing_data')
    supply_service.edit_third_party_service(method_name, editing_data)

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
    data: Dict = request.get_json()
    token = get_jwt_identity()
    method_name = data.get('method_name')
    supply_service.delete_third_party_service(method_name)