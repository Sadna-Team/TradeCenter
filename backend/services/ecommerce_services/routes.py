from flask import Blueprint, request, jsonify
from backend.business.market import MarketFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies

# API endpoints and their corresponding route handlers
market_bp = Blueprint('market', __name__)
market_facade = MarketFacade()


@market_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        payment_details = data['payment_details']
        address = data['address']
        market_facade.checkout(user_id, payment_details, address)
        return jsonify({'message': 'successfully checked out'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@market_bp.route('/promotion', methods=['POST'])
@jwt_required()
def accept_promotion():
    """
        Use Case 2.4.6.2:
        Accept a promotion to be store manager of a store with the given permissions

        Data:
            user_id (int): id of the user
            nomination_id (int): id of the nomination
            accept (bool): whether to accept the promotion


        Returns:
            ?
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        nomination_id = data['nomination_id']
        accept = data['accept']
        market_facade.accept_nomination(user_id, nomination_id, accept)
        return jsonify({'message': 'decision registered'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@market_bp.route('/change_permissions', methods=['POST'])
@jwt_required()
def change_permissions():
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
        return jsonify({'message': 'changed permissions'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@market_bp.route('/search_products', methods=['GET'])
@jwt_required()
def search_products():
    """
        Use Case 2.2.2.1:
        Search products in the stores

        Data:
            filters : filters to search for products

        Returns:
            ?
    """
    try:
        user_id = get_jwt_identity()
        data = request.args
        filters = data['filters']
        # TODO :: market_facade.
        return jsonify({'message': 'searched products'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@market_bp.route('/search_store_products', methods=['GET'])
@jwt_required()
def search_store_products():
    """
            Use Case 2.2.2.2:
            Search products in a store

            Data:
                token (?): token of the user
                store_id (int): id of the store
                filters (?): filters to search for products

            Returns:
                ?
        """

    try:
        user_id = get_jwt_identity()
        data = request.args
        store_id = data['store_id']
        filters = data['filters']
        # TODO ::market_facade.
        return jsonify({'message': 'searched products'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@market_bp.route('/store_purchase_history', methods=['GET'])
@jwt_required()
def show_store_purchase_history():
    """
        Use Case 2.4.13:
        Show the purchase history in a store

        Data:
            store_id (int): id of the store

        Returns:
            ?
    """
    try:
        user_id = get_jwt_identity()
        data = request.args
        store_id = data['store_id']
        history = None # TODO :: market_facade.
        return jsonify({'message': history}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@market_bp.route('/member_purchase_history', methods=['GET'])
@jwt_required()
def show_member_purchase_history():
    """
        Use Case 2.6.4:
        Show the purchase history of a member

        Returns:
            ?
    """
    try:
        user_id = get_jwt_identity()
        history =  None  # TODO :: market_facade.
        return jsonify({'message': history}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
