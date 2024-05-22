from flask import Blueprint, request, jsonify
from backend.business.store import StoreFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies


#-------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')
#---------------------------------------------------


# API endpoints and their corresponding route handlers
store_bp = Blueprint('store', __name__)
store_facade = StoreFacade()


@store_bp.route('/store_info', methods=['GET'])
@jwt_required()
def show_store_info():
    """
        Use Case 2.2.1.1:
        Show information about the stores in the system

        Data:
            store_id (int): the id of the store
    """
    logger.info('recieved request to send store info')
    try:
        user_id = get_jwt_identity()
        data = request.args
        store_id = data['store_id']
        info = None # TODO :: store_facade.
        logger.info('store info was sent successfully')
        return jsonify({'message': info}), 200
    except Exception as e:
        logger.error('show_store_info - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/store_products', methods=['GET'])
@jwt_required()
def show_store_products():
    """
        Use Case 2.2.1.2:
        Show products of a store

        Data:
            store_id (int): id of the store
    """
    logger.info('recieved request to send store products')
    try:
        user_id = get_jwt_identity()
        data = request.args
        store_id = data['store_id']
        products = None # TODO: store_facade.()
        logger.info('store products were sent successfully')
        return jsonify({'message': products}), 200
    except Exception as e:
        logger.error('show_store_products - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/add_store', methods=['POST'])
@jwt_required()
def add_store():
    """
        Use Case 2.3.2:
        Add a store to the system and set the user as the store owner

        Data:
            store_data (?): data of the store to be added

        Returns:
            ?
    """
    logger.info('recieved request to add store')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_data']
        # TODO: store_facade.()
        logger.info('store was added successfully')
        return jsonify({'message': 'store was added successfully'}), 200
    except Exception as e:
        logger.error('add_store - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/add_product', methods=['POST'])
@jwt_required()
def add_product():
    """
        Use Case 2.4.1:
        Add a product to a store

        Data:
            store_id (int): id of the store
            product_data (?): data of the product to be added
    """
    logger.info('recieved request to add product')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        product_data = data['product_data']
        #TODO: store_facade.()
        logger.info('product was added successfully')
        return jsonify({'message': 'product was successfully added'}), 200
    except Exception as e:
        logger.error('add_product - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/change_purchase_policy', methods=['POST'])
@jwt_required()
def change_purchase_policy():
    """
        Use Case 2.4.2.1:
        Change the purchase policy of a store

        Data:
            store_id (int): id of the store
            policy_data (?): data of the new purchase policy
    """
    logger.info('recieved request to change purchase policy')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        policy_data = data['policy_data']
        #TODO: store_facade.()
        logger.info('purchase policy was changed successfully')
        return jsonify({'message': 'purchase policy was successfully changed'}), 200
    except Exception as e:
        logger.error('change_purchase_policy - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/change_purchase_types', methods=['POST'])
@jwt_required()
def change_purchase_types():
    """
        Use Case 2.4.2.1:
        Change the purchase types of a store

        Data:
            store_id (int): id of the store
            types_data (?): data of the new purchase types
    """
    logger.info('recieved request to change purchase types')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        types_data = data['types_data']
        #TODO: store_facade.()
        logger.info('purchase types were changed successfully')
        return jsonify({'message': 'purchase types were successfully changed'}), 200
    except Exception as e:
        logger.error('change_purchase_types - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/change_discount_policy', methods=['POST'])
@jwt_required()
def change_discount_policy():
    """
        Use Case 2.4.2.1:
        Change the discount policy of a store

        Data:
            store_id (int): id of the store
            policy_data (?): data of the new discount policy
    """
    logger.info('recieved request to change discount policy')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        policy_data = data['policy_data']
        #TODO: store_facade.()
        logger.info('discount policy was changed successfully')
        return jsonify({'message': 'discount policy was successfully changed'}), 200
    except Exception as e:
        logger.error('change_discount_policy - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/change_discount_types', methods=['POST'])
@jwt_required()
def change_discount_types():
    """
        Use Case 2.4.2.1:
        Change the discount types of a store

        Data:
            store_id (int): id of the store
            types_data (?): data of the new discount types
    """
    logger.info('recieved request to change discount types')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        types_data = data['types_data']
        #TODO: store_facade.()
        logger.info('discount types were changed successfully')
        return jsonify({'message': 'discount types were successfully changed'}), 200
    except Exception as e:
        logger.error('change_discount_types - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/add_store_owner', methods=['POST'])
@jwt_required()
def add_store_owner():
    """
        Use Case 2.4.3.1:
        Send promototion to a new owner to a store.
        User still needs to accept the promotion!

        Data:
            store_id (int): id of the store
            new_owner_id (int): id of the new owner
    """
    logger.info('recieved request to add store owner')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        new_owner_id = data['new_owner_id']
        #TODO: store_facade.()
        logger.info('store owner was added successfully')
        return jsonify({'message': 'store owner was successfully added'}), 200
    except Exception as e:
        logger.error('add_store_owner - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/add_store_manager', methods=['POST'])
@jwt_required()
def add_store_manager():
    """
        Use Case 2.4.3.1:
        Send promototion to a new manager to a store.
        User still needs to accept the promotion!

        Data:
            store_id (int): id of the store
            new_manager_id (int): id of the new manager
            permissions (dict[str->bool]): permissions of the new manager
    """
    logger.info('recieved request to add store manager')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        new_manager_id = data['new_manager_id']
        permissions = data['permissions']
        #TODO: store_facade.()
        logger.info('store manager was added successfully')
        return jsonify({'message': 'store manager was successfully added'}), 200
    except Exception as e:
        logger.error('add_store_manager - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/edit_manager_permissions', methods=['POST'])
@jwt_required()
def edit_manager_permissions():
    """
        Use Case 2.4.7:
        Edit the permissions of a store manager

        Data:
            store_id (int): id of the store
            manager_id (int): id of the manager
            permissions (dict[str->bool]): new permissions of the manager
    """
    logger.info('recieved request to edit manager permissions')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        manager_id = data['manager_id']
        permissions = data['permissions']
        #TODO: store_facade.()
        logger.info('store manager\'s permissions were changed successfully')
        return jsonify({'message': 'store manager\'s permissions were successfully changed'}), 200
    except Exception as e:
        logger.error('edit_manager_permissions - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/closing_store', methods=['POST'])
@jwt_required()
def closing_store():
    """
        Use Case 2.4.9:
        Close a store

        Data:
            store_id (int): id of the store
    """
    logger.info('recieved request to close store')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        #TODO: store_facade.()
        logger.info('store was closed successfully')
        return jsonify({'message': 'store was successfully closed'}), 200
    except Exception as e:
        logger.error('closing_store - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/view_employees_info', methods=['GET'])
@jwt_required()
def view_employees_info():
    """
        Use Case 2.4.11:
        View information about the employees of a store

        Data:
            store_id (int): id of the store
    """
    logger.info('recieved request to view employees info')
    try:
        user_id = get_jwt_identity()
        data = request.args
        store_id = data['store_id']
        info = None #TODO: store_facade.()
        logger.info('employees info was sent successfully')
        return jsonify({'message': info}), 200
    except Exception as e:
        logger.error('view_employees_info - ', str(e))
        return jsonify({'message': str(e)}), 400
