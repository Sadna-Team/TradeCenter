from flask import Blueprint, request, jsonify
from .controllers import StoreService
from flask_jwt_extended import jwt_required, get_jwt_identity

# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')
# ---------------------------------------------------


# API endpoints and their corresponding route handlers
store_bp = Blueprint('store', __name__)
store_service = StoreService()

'''
@store_bp.route('/add_discount', methods=['POST'])
@jwt_required()
def add_discount():
    """
        Use Case 2.4.2
        Add a discount to a store
        
    """
    logger.info('received request to add discount')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        description = data['description']
        start_date = data['start_date']
        end_date = data['end_date']
        percentage = data['percentage']
        market_facade.add_discount(user_id, description, start_date, end_date, percentage)
        logger.info('discount was added successfully')
        return jsonify({'message': 'discount was added successfully'}), 200
    except Exception as e:
        logger.error('add_discount - ', str(e))
        return jsonify({'message': str(e)}), 400
    pass


@store_bp.route('/remove_discount', methods=['POST'])
@jwt_required()
def remove_discount():
    """
        Use Case 2.4.2
        Remove a discount from a store
    """
    logger.info('received request to remove discount')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        discount_id = data['discount_id']
        market_facade.remove_discount(user_id, discount_id)
        logger.info('discount was removed successfully')
        return jsonify({'message': 'discount was removed successfully'}), 200
    except Exception as e:
        logger.error('remove_discount - ', str(e))
        return jsonify({'message': str(e)}), 400
    pass


@store_bp.route('/edit_discount', methods=['POST'])
@jwt_required()
def edit_discount():
    """
        Use Case 2.4.2
        Edit a discount of a store
    """
    logger.info('received request to edit discount')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        discount_id = data['discount_id']
        market_facade.change_discount(user_id, discount_id)
        logger.info('discount was edited successfully')
        return jsonify({'message': 'discount was edited successfully'}), 200
    except Exception as e:
        logger.error('edit_discount - ', str(e))
        return jsonify({'message': str(e)}), 400
    pass


@store_bp.route('/add_purchase_policy', methods=['POST'])
@jwt_required
def add_purchase_policy():
    """
        Use Case 2.2.4.2
        Add a purchase policy to a store
            TODO: later on the details of policy!
    """
    logger.info('received request to add purchase policy')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        market_facade.add_purchase_policy(user_id, store_id)
        logger.info('purchase policy was added successfully')
        return jsonify({'message': 'purchase policy was added successfully'}), 200
    except Exception as e:
        logger.error('add_purchase_policy - ', str(e))
        return jsonify({'message': str(e)}), 400
    pass


@store_bp.route('/remove_purchase_policy', methods=['POST'])
@jwt_required
def remove_purchase_policy():
    """
        Use Case 2.2.4.2
        Remove a purchase policy from a store
    """
    logger.info('received request to remove purchase policy')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        policy_id = data['policy_id']
        market_facade.remove_purchase_policy(user_id, store_id, policy_id)
        logger.info('purchase policy was removed successfully')
        return jsonify({'message': 'purchase policy was removed successfully'}), 200
    except Exception as e:
        logger.error('remove_purchase_policy - ', str(e))
        return jsonify({'message': str(e)}), 400
    pass


@store_bp.route('/change_purchase_policy', methods=['POST'])
@jwt_required
def edit_purchase_policy():
    """
        Use Case 2.2.4.2
        Edit a purchase policy of a store
    """
    logger.info('received request to edit purchase policy')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        policy_id = data['policy_id']
        market_facade.change_purchase_policy(user_id, store_id, policy_id)
        logger.info('purchase policy was edited successfully')
        return jsonify({'message': 'purchase policy was edited successfully'}), 200
    except Exception as e:
        logger.error('edit_purchase_policy - ', str(e))
        return jsonify({'message': str(e)}), 400
    pass'''


@store_bp.route('/store_info', methods=['GET'])
@jwt_required()
def show_store_info():
    """
        Use Case 2.2.1.1:
        Show information about the stores in the system
    """
    logger.info('received request to send store info')
    try:
        data = request.args
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error('show_store_info - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.show_store_info(store_id)


@store_bp.route('/store_products', methods=['GET'])
@jwt_required()
def show_store_products():
    """
        Use Case 2.2.1.2:
        Show products of a store
    """
    logger.info('received request to send store products')
    try:
        data = request.args
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error('show_store_products - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.show_store_products(store_id)


@store_bp.route('/add_store', methods=['POST'])
@jwt_required()
def add_store():
    """
        Use Case 2.3.2:
        Add a store to the system and set the user as the store owner
    """
    logger.info('received request to add store')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        location_id = int(data['location_id'])
        store_name = str(data['store_name'])
    except Exception as e:
        logger.error('add_store - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.add_new_store(user_id, location_id, store_name)


@store_bp.route('/add_product', methods=['POST'])
@jwt_required()
def add_product_to_store():
    """
        Use Case 2.4.1:
        Add a product to a store
            
    """
    logger.info('received request to add product')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        product_name = str(data['product_name'])
        description = str(data['description'])
        price = float(data['price'])
        weight = float(data['weight'])
        tags_helper = data['tags']
        if not isinstance(tags_helper, list):
            raise ValueError("Tags must be a list")
        tags = [str(tag) for tag in tags_helper]
    except Exception as e:
        logger.error('add_product - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.add_product_to_store(user_id, store_id, product_name, description, price, weight, tags)


@store_bp.route('/remove_product', methods=['POST'])
@jwt_required()
def remove_product():
    """
        Use Case: 2.2.4.1
        Remove a product from a store
            
    """
    logger.info('received request to remove product')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
    except Exception as e:
        logger.error('remove_product - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.remove_product_from_store(user_id, store_id, product_id)


@store_bp.route('/add_category', methods=['POST'])
@jwt_required()
def add_category():
    """
        Use Case 
        Add a category to a store
            
    """
    logger.info('received request to add category')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        category_name = str(data['category_name'])
    except Exception as e:
        logger.error('add_category - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.add_category(user_id, category_name)


@store_bp.route('/remove_category', methods=['POST'])
@jwt_required()
def remove_category():
    """
        Use Case 
        Remove a category from a store
    """
    logger.info('received request to remove category')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        category_id = int(data['category_id'])
    except Exception as e:
        logger.error('remove_category - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.remove_category(user_id, category_id)


@store_bp.route('/add_subcategory_to_category', methods=['POST'])
@jwt_required()
def add_subcategory_to_category():
    """
        Use Case 
        Add a subcategory to a category
            
    """
    logger.info('received request to add subcategory to category')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        subcategory_id = int(data['subcategory_id'])
        parent_category_id = int(data['parent_category_id'])
    except Exception as e:
        logger.error('add_subcategory_to_category - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.add_subcategory_to_category(user_id, parent_category_id, subcategory_id)


@store_bp.route('/remove_subcategory_from_category', methods=['POST'])
@jwt_required()
def remove_subcategory_from_category():
    """
        Use Case 
        Remove a subcategory from a category
            
    """
    logger.info('received request to remove subcategory from category')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        subcategory_id = int(data['subcategory_id'])
        parent_category_id = int(data['parent_category_id'])
    except Exception as e:
        logger.error('remove_subcategory_from_category - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.remove_subcategory_from_category(user_id, parent_category_id, subcategory_id)


@store_bp.route('/assign_product_to_category', methods=['POST'])
@jwt_required()
def assign_product_to_category():
    """
        Use Case 
        Assign a product specification to a category
    """
    logger.info('received request to assign product specification to category')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_id = int(data['product_id'])
        store_id = int(data['store_id'])
        category_id = int(data['category_id'])
    except Exception as e:
        logger.error('assign_product_specification_to_category - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.assign_product_to_category(user_id, category_id, store_id, product_id)


'''@store_bp.route('/remove_product_specification_from_category', methods=['POST'])
@jwt_required()
def remove_product_specification_from_category():
    """
        Use Case 
        Remove a product specification from a category
        
        Data:
            user_id (int): id of the user
            category_id (int): id of the category
            product_spec_id (int): id of the product specification
            
    """
    logger.info('received request to remove product specification from category')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_spec_id = data['product_spec_id']
        category_id = data['category_id']
        market_facade.remove_product_spec_from_category(user_id, category_id, product_spec_id)
        logger.info('product specification was removed from category successfully')
        return jsonify({'message': 'product specification was removed from category successfully'}), 200
    except Exception as e:
        logger.error('remove_product_specification_from_category - ', str(e))
        return jsonify({'message': str(e)}), 400'''


@store_bp.route('/add_store_owner', methods=['POST'])
@jwt_required()
def add_store_owner():
    """
        Use Case 2.4.3.1:
        Send promototion to a new owner to a store.
        User still needs to accept the promotion!
    """
    logger.info('received request to add store owner')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        username = data['username']
    except Exception as e:
        logger.error('add_store_owner - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.add_store_owner(user_id, store_id, username)


@store_bp.route('/add_store_manager', methods=['POST'])
@jwt_required()
def add_store_manager():
    """
        Use Case 2.4.3.1:
        Send promototion to a new manager to a store.
        User still needs to accept the promotion!
    """
    logger.info('received request to add store manager')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        new_manager_username = data['username']
    except Exception as e:
        logger.error('add_store_manager - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.add_store_manager(user_id, store_id, new_manager_username)


@store_bp.route('/edit_manager_permissions', methods=['POST'])
@jwt_required()
def edit_manager_permissions():
    """
        Use Case 2.4.7:
        Edit the permissions of a store manager
    """
    logger.info('received request to edit manager permissions')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        manager_id = int(data['manager_id'])
        add_product = bool(data['add_product'])
        change_purchase_policy = bool(data['change_purchase_policy'])
        change_purchase_types = bool(data['change_purchase_types'])
        change_discount_policy = bool(data['change_discount_policy'])
        change_discount_types = bool(data['change_discount_types'])
        add_manager = bool(data['add_manager'])
        get_bid = bool(data['get_bid'])
    except Exception as e:
        logger.error('edit_manager_permissions - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.edit_manager_permissions(user_id, store_id, manager_id, add_product, change_purchase_policy,
                                                  change_purchase_types, change_discount_policy, change_discount_types,
                                                  add_manager, get_bid)


@store_bp.route('/closing_store', methods=['POST'])
@jwt_required()
def closing_store():
    """
        Use Case 2.4.9:
        Close a store
    """
    logger.info('received request to close store')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error('closing_store - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.closing_store(user_id, store_id)


@store_bp.route('/view_employees_info', methods=['GET'])
@jwt_required()
def view_employees_info():
    """
        Use Case 2.4.11:
        View information about the employees of a store
    """
    logger.info('received request to view employees info')
    try:
        user_id = int(get_jwt_identity())
        data = request.args
        store_id = int(data['store_id'])
        info = store_service.view_employees_info(user_id, store_id)
        logger.info('employees info was sent successfully')
        return jsonify({'message': info}), 200
    except Exception as e:
        logger.error('view_employees_info - ', str(e))
        return jsonify({'message': str(e)}), 400
