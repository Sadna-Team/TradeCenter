from flask import Blueprint, request, jsonify
from backend.business.market import MarketFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies


#-------------logging configuration----------------
from logging_config import setup_logging
import logging

logger = logging.getLogger('myapp')
#---------------------------------------------------


# API endpoints and their corresponding route handlers
market_bp = Blueprint('market', __name__)
market_facade = MarketFacade()


@market_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    """
        Use Case 2.2.5:
        Checkout the shopping cart

        Data:
            payment_details (?): payment details
    """
    logger.info('recieved request to checkout the shopping cart')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        payment_details = data['payment_details']
        address = data['address']
        market_facade.checkout(user_id, payment_details, address)
        logger.info('checkout successful')
        return jsonify({'message': 'successfully checked out'}), 200
    except Exception as e:
        logger.error('checkout - ', str(e))
        return jsonify({'message': str(e)}), 400


@market_bp.route('/promotion', methods=['POST'])
@jwt_required()
def accept_promotion():
    """
        Use Case 2.4.6.2:
        Accept a promotion to be store manager of a store with the given permissions

        Data:
            nomination_id (int): id of the nomination
            accept (bool): whether to accept the promotion
    """
    logger.info('recieved request to accept/deny a promotion')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        nomination_id = data['nomination_id']
        accept = data['accept']
        market_facade.accept_nomination(user_id, nomination_id, accept)
        logger.info('promotion accepted/denied')
        return jsonify({'message': 'decision registered'}), 200
    except Exception as e:
        logger.error('accept_promotion - ', str(e))
        return jsonify({'message': str(e)}), 400


@market_bp.route('/change_permissions', methods=['POST'])
@jwt_required()
def change_permissions():
    """
        Use Case 2.4.7:
        Edit the permissions of a store manager

        Data:
            store_id (int): id of the store
            manager_id (int): id of the manager
            permissions (dict[str->bool]): new permissions of the manager
    """
    logger.info('recieved request to change permissions')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        manager_id = data['manager_id']
        add_product = data['add_product']
        remove_product = data['remove_product']
        edit_product = data['edit_product']
        appoint_owner = data['appoint_owner']
        appoint_manager = data['appoint_manager']
        remove_owner = data['remove_owner']
        remove_manager = data['remove_manager']
        market_facade.change_permissions(user_id, store_id, manager_id, add_product, remove_product, edit_product,
                                         appoint_owner, appoint_manager, remove_owner, remove_manager)
        logger.info('permissions changed')
        return jsonify({'message': 'changed permissions'}), 200
    except Exception as e:
        logger.error('change_permissions - ', str(e))
        return jsonify({'message': str(e)}), 400


@market_bp.route('/search_products', methods=['GET'])
@jwt_required()
def search_products():
    """
        Use Case 2.2.2.1:
        Search products in the stores

        Data:
            filters (?): filters to search for products
    """
    logger.info('recieved request to search for products')
    try:
        user_id = get_jwt_identity()
        data = request.args
        filters = data['filters']
        # TODO :: market_facade.
        logger.info('search successful')
        return jsonify({'message': 'searched products'}), 200
    except Exception as e:
        logger.error('search_products - ', str(e))
        return jsonify({'message': str(e)}), 400


@market_bp.route('/search_store_products', methods=['GET'])
@jwt_required()
def search_store_products():
    """
            Use Case 2.2.2.2:
            Search products in a store

            Data:
                store_id (int): id of the store
                filters (?): filters to search for products
        """
    logger.info('recieved request to search for products in a store')
    try:
        user_id = get_jwt_identity()
        data = request.args
        store_id = data['store_id']
        filters = data['filters']
        # TODO ::market_facade.
        logger.info('search successful')
        return jsonify({'message': 'searched products'}), 200
    except Exception as e:
        logger.error('search_store_products - ', str(e))
        return jsonify({'message': str(e)}), 400


@market_bp.route('/store_purchase_history', methods=['GET'])
@jwt_required()
def show_store_purchase_history():
    """
        Use Case 2.4.13:
        Show the purchase history in a store

        Data:
            store_id (int): id of the store
    """
    logger.info('recieved request to show the purchase history of a store')
    try:
        user_id = get_jwt_identity()
        data = request.args
        store_id = data['store_id']
        history = None # TODO :: market_facade.
        logger.info('purchase history sent')
        return jsonify({'message': history}), 200
    except Exception as e:
        logger.error('show_store_purchase_history - ', str(e))
        return jsonify({'message': str(e)}), 400


@market_bp.route('/member_purchase_history', methods=['GET'])
@jwt_required() 
def show_member_purchase_history():
    """
        Use Case 2.6.4:
        Show the purchase history of a member
    """
    logger.info('recieved request to show the purchase history of a member')
    try:
        user_id = get_jwt_identity()
        history =  None  # TODO :: market_facade.
        logger.info('purchase history sent')
        return jsonify({'message': history}), 200
    except Exception as e:
        logger.error('show_member_purchase_history - ', str(e))
        return jsonify({'message': str(e)}), 400
