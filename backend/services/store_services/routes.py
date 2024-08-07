from datetime import datetime
from typing import Optional, Tuple
from flask import Blueprint, request, jsonify
from .controllers import StoreService
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.error_types import *


# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')
# ---------------------------------------------------


# API endpoints and their corresponding route handlers
store_bp = Blueprint('store', __name__)
store_service = StoreService()

'''

@store_bp.route('/_discount', methods=['POST'])
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

"""
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
"""
"""
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
"""

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
        description: str = str(data['description'])
        start_date: datetime = data['start_date']
        end_date: datetime = data['end_date']
        percentage: float = float(data['percentage'])
        store_id: int = int(data['store_id'])
        product_id = None
        if 'product_id' in data:
            if data['product_id'] is not None:
                product_id = int(data['product_id'])
        category_id = None
        if 'category_id' in data:
            if data['category_id'] is not None:
                category_id = int(data['category_id'])
        applied_to_sub: Optional[bool] = None
        if 'applied_to_sub' in data:
            if data['applied_to_sub'] is not None:
                applied_to_sub = data['applied_to_sub']
       
    except Exception as e:
        logger.error('add_discount - ', str(e))
        return jsonify({'message': str(e)}), 400
    logger.info('discount was added successfully')
    return store_service.add_discount(user_id, description, start_date, end_date, percentage, store_id, product_id, category_id, applied_to_sub)


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
        discount_id = int(data['discount_id'])
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error('remove_discount - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.remove_discount(user_id, discount_id, store_id)


@store_bp.route('/create_logical_composite', methods=['POST'])
@jwt_required()
def create_logical_composite():
    """
        Use Case 2.4.2
        Create a logical composite discount
    """
    logger.info('received request to create logical composite')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        description = str(data['description'])
        store_id = int(data['store_id'])
        start_date = data['start_date']
        end_date = data['end_date']
        discount_id1 = int(data['discount_id1'])
        discount_id2 = int(data['discount_id2'])
        type_of_composite = int(data['type_of_composite'])
    except Exception as e:
        logger.error('create_logical_composite - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.create_logical_composite_discount(user_id, store_id, description, start_date, end_date, discount_id1, discount_id2, type_of_composite)

@store_bp.route('/create_numerical_composite', methods=['POST'])
@jwt_required()
def create_numerical_composite():
    """
        Use Case 2.4.2
        Create a numerical composite discount
    """
    logger.info('received request to create numerical composite')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        description = str(data['description'])
        store_id = int(data['store_id'])
        start_date = data['start_date']
        end_date = data['end_date']
        discount_ids = data['discount_ids']
        type_of_composite = int(data['type_of_composite'])
    except Exception as e:
        logger.error('create_numerical_composite - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.create_numerical_composite_discount(user_id, store_id, description, start_date, end_date, discount_ids, type_of_composite)

@store_bp.route('/assign_predicate_to_discount', methods=['POST'])
@jwt_required()
def assign_predicate_to_discount():
    """
        Use Case 2.4.2
        Assign a predicate to a discount
    """
    logger.info('received request to assign predicate to discount')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        discount_id = int(data['discount_id'])
        store_id = int(data['store_id'])
        predicate_builder = data['predicate_builder']
    except Exception as e:
        logger.error('assign_predicate_to_discount - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.assign_predicate_to_discount(user_id, discount_id, store_id, predicate_builder)

@store_bp.route('/change_discount_percentage', methods=['POST'])
@jwt_required()
def change_discount_percentage():
    """
        Use Case 2.4.2
        Change the percentage of a discount
    """
    logger.info('received request to change discount percentage')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        discount_id = int(data['discount_id'])
        store_id = int(data['store_id'])
        percentage = float(data['percentage'])
    except Exception as e:
        logger.error('change_discount_percentage - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.change_discount_percentage(user_id, discount_id, store_id, percentage)

@store_bp.route('/change_discount_description', methods=['POST'])
@jwt_required()
def change_discount_description():
    """
        Use Case 2.4.2
        Change the description of a discount
    """
    logger.info('received request to change discount description')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        discount_id = int(data['discount_id'])
        store_id = int(data['store_id'])
        description = str(data['description'])
    except Exception as e:
        logger.error(('change_discount_description - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return store_service.change_discount_description(user_id, discount_id, store_id, description)

@store_bp.route('/view_discounts_info', methods=['GET', 'POST'])
@jwt_required()
def view_discounts_info():
    """
        Use Case 2.4.2
        View information about the discounts of the system
    """
    logger.info('received request to view discounts info')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error('view_discounts_info - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.view_all_discount_info(user_id, store_id)

@store_bp.route('/store_info', methods=['GET', 'POST'])
@jwt_required()
def show_store_info():
    """
        Use Case 2.2.1.1:
        Show information about the stores in the system
    """
    logger.info('received request to send store info')
    try:
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error(('show_store_info - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return store_service.show_store_info(store_id)

@store_bp.route('/get_stores', methods=['GET', 'POST'])
@jwt_required()
def get_stores():
    """
        Get stores
        get page and limit from request
    """
    logger.info('received request to get stores')
    try:
        data = request.get_json()
        page = int(data['page'])
        limit = int(data['limit'])
    except Exception as e:
        logger.error('show_store_products - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.get_stores(page, limit)

@store_bp.route('/get_all_stores', methods=['GET'])
@jwt_required()
def get_all_stores():
    """
        Get stores
        get page and limit from request
    """
    logger.info('received request to get stores')
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        logger.error('show_store_products - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.get_all_stores(user_id)

@store_bp.route('/store_products', methods=['GET', 'POST'])
@jwt_required()
def show_store_products():
    """
        Use Case 2.2.1.2:
        Show products of a store
    """
    logger.info('received request to send store products')
    try:
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error('show_store_products - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.show_store_products(store_id)

@store_bp.route('/get_product_info', methods=['GET', 'POST'])
@jwt_required()
def get_product_info():
    """
        Use Case
        Get product info
    """
    logger.info('received request to get product info')
    try:
        data = request.get_json()
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
    except Exception as e:
        logger.error('get_product_info - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.get_product_info(store_id, product_id)


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
        address = str(data['address'])
        city = str(data['city'])
        state = str(data['state'])
        country = str(data['country'])
        zip_code = str(data['zip_code'])
        store_name = str(data['store_name'])
    except Exception as e:
        logger.error('add_store - ', str(e))
        return jsonify({'message': str(e)}), 400

    ret = store_service.add_new_store(user_id, address, city, state, country, zip_code, store_name)
    return ret


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
            raise ServiceLayerError("Tags must be a list", ServiceLayerErrorTypes.tags_not_list)
        tags = [str(tag) for tag in tags_helper]
        amount=0
        if 'amount' in data:
            if data['amount'] is not None:
                amount = int(data['amount'])
    except Exception as e:
        logger.error(f'add_product - {str(e)}')
        return jsonify({'message': str(e)}), 400

    return store_service.add_product_to_store(user_id, store_id, product_name, description, price, weight, tags, amount)


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


@store_bp.route('/restock_product', methods=['POST'])
@jwt_required()
def restock_product():
    """
        Use Case
        Restock a product in a store
    """
    logger.info('received request to restock product')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
        quantity = int(data['quantity'])
    except Exception as e:
        logger.error('restock_product - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.restock(user_id, store_id, product_id, quantity)

@store_bp.route('/remove_product_amount', methods=['POST'])
@jwt_required()
def remove_product_amount():
    """
        Use Case
        Remove a product amount from a store
    """
    logger.info('received request to remove product amount')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
        amount = int(data['amount'])
    except Exception as e:
        logger.error('remove_product_amount - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.remove_amount_from_product(user_id, store_id, product_id, amount)

@store_bp.route('/edit_product', methods=['POST'])
@jwt_required()
def edit_product_in_store():
    """
        Use Case 2.4.1:
        Add a product to a store

    """
    logger.info('received request to edit product')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
        product_name = str(data['product_name'])
        description = str(data['description'])
        price = float(data['price'])
        weight = float(data['weight'])
        tags_helper = data['tags']
        if not isinstance(tags_helper, list):
            raise ServiceLayerError("Tags must be a list", ServiceLayerErrorTypes.tags_not_list)
        tags = [str(tag) for tag in tags_helper]
        amount=0
        if 'amount' in data:
            if data['amount'] is not None:
                amount = int(data['amount'])
    except Exception as e:
        logger.error('edit_product - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.edit_product_in_store(user_id, store_id, product_id, product_name, description, price, weight, tags, amount)

@store_bp.route('/change_price_of_product', methods=['POST'])
@jwt_required()
def change_price_of_product():
    """
        Use Case
        Change the price of a product in a store
    """
    logger.info('received request to change price of product')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
        price = float(data['price'])
    except Exception as e:
        logger.error('change_price_of_product - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.change_price_of_product(user_id, store_id, product_id, price)

@store_bp.route('/change_product_description', methods=['POST'])
@jwt_required()
def change_product_description():
    """
        Use Case
        Change the description of a product in a store
    """
    logger.info('received request to change product description')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
        description = str(data['description'])
    except Exception as e:
        logger.error('change_product_description - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.change_description_of_product(user_id, store_id, product_id, description)

@store_bp.route('/change_product_weight', methods=['POST'])
@jwt_required()
def change_product_weight():
    """
        Use Case
        Change the weight of a product in a store
    """
    logger.info('received request to change product weight')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
        weight = float(data['weight'])
    except Exception as e:
        logger.error('change_product_weight - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.change_weight_of_product(user_id, store_id, product_id, weight)


@store_bp.route('/add_tag_to_product', methods=['POST'])
@jwt_required()
def add_tag_to_product():
    """
        Use Case
        Add a tag to a product in a store
    """
    logger.info('received request to add tag to product')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
        tag = str(data['tag'])
    except Exception as e:
        logger.error('add_tag_to_product - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.add_tag_to_product(user_id, store_id, product_id, tag)

@store_bp.route('/remove_tag_from_product', methods=['POST'])
@jwt_required()
def remove_tag_from_product():
    """
        Use Case
        Remove a tag from a product in a store
    """
    logger.info('received request to remove tag from product')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
        tag = str(data['tag'])
    except Exception as e:
        logger.error('remove_tag_from_product - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.remove_tag_from_product(user_id, store_id, product_id, tag)

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

    return store_service.add_subcategory_to_category(user_id, subcategory_id, parent_category_id)


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

    return store_service.remove_subcategory_from_category(user_id, subcategory_id, parent_category_id)


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

@store_bp.route('/remove_product_from_category', methods=['POST'])
@jwt_required()
def remove_product_from_category():
    """
        Use Case 
        Remove a product from a category
    """
    logger.info('received request to remove product from category')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_id = int(data['product_id'])
        store_id = int(data['store_id'])
        category_id = int(data['category_id'])
    except Exception as e:
        logger.error('remove_product_from_category - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.remove_product_from_category(user_id, category_id, store_id, product_id)



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


@store_bp.route('/remove_store_role', methods=['POST'])
@jwt_required()
def remove_store_role():
    """
        Remove a role from a store
    """
    logger.info('received request to remove store role')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        username = str(data['username'])
    except Exception as e:
        logger.error('remove_store_role - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.remove_store_role(user_id, store_id, username)


@store_bp.route('/give_up_role', methods=['POST'])
@jwt_required()
def give_up_role():
    """
        Give up a role in a store
    """
    logger.info('received request to give up role')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error('give_up_role - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.give_up_role(user_id, store_id)


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
        permissions = list(data['permissions'])

    except Exception as e:
        logger.error('edit_manager_permissions - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.edit_manager_permissions(user_id, store_id, manager_id, permissions)


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

@store_bp.route('/is_store_closed', methods=['POST'])
@jwt_required()
def is_store_closed():
    """
        Use Case 2.4.9:
        Check if a store is closed
    """
    logger.info('received request to check if store is closed')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error('is_store_closed - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.is_store_closed(store_id)

@store_bp.route('/opening_store', methods=['POST'])
@jwt_required()
def opening_store():
    """
        Use Case 2.4.9:
        Open a store
    """
    logger.info('received request to open store')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error('opening_store - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.opening_store(user_id, store_id)


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
        data = request.get_json()
        store_id = int(data['store_id'])
        info = store_service.view_employees_info(user_id, store_id)
    except Exception as e:
        logger.error('view_employees_info - ', str(e))
        return jsonify({'message': str(e)}), 400

    return info

@store_bp.route('/add_purchase_policy', methods=['POST'])
@jwt_required()
def add_purchase_policy():
    """
        Use Case ____(idk I need to check)
        Add a purchase policy to a store
    """
    logger.info('received request to add purchase policy')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        policy_name = str(data['policy_name'])
        category_id = None
        product_id = None
        if 'category_id' in data:
            if data['category_id'] is not None:
                category_id = int(data['category_id'])
        elif 'product_id' in data:
            if data['product_id'] is not None:
                product_id = int(data['product_id'])
    except Exception as e:
        logger.error('add_purchase_policy - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.add_purchase_policy(user_id, store_id, policy_name, category_id, product_id)


@store_bp.route('/remove_purchase_policy', methods=['POST'])
@jwt_required()
def remove_purchase_policy():
    """
        Use Case ____(idk I need to check)
        Remove a purchase policy from a store
    """
    logger.info('received request to remove purchase policy')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        policy_id = int(data['policy_id'])
    except Exception as e:
        logger.error('remove_purchase_policy - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.remove_purchase_policy(user_id, store_id, policy_id)


@store_bp.route('/create_composite_purchase_policy', methods=['POST'])
@jwt_required()
def create_composite_purchase_policy():
    """
        Use Case ____(idk I need to check)
        Create a composite purchase policy
    """
    logger.info('received request to create composite purchase policy')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        policy_name = str(data['policy_name'])
        policy_id1 = int(data['policy_id1'])
        policy_id2 = int(data['policy_id2'])
        type_of_composite = int(data['type_of_composite']) 
    except Exception as e:
        logger.error('create_composite_purchase_policy - ', str(e))
        return jsonify({'message': str(e)}), 400
    
    return store_service.create_composite_purchase_policy(user_id, store_id, policy_name, policy_id1,policy_id2, type_of_composite)

@store_bp.route('/assign_predicate_to_purchase_policy', methods=['POST'])
@jwt_required()
def assign_predicate_to_purchase_policy():
    """
        Use Case ____(idk I need to check)
        Assign a predicate to a purchase policy
    """
    logger.info('received request to assign predicate to purchase policy')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        policy_id = int(data['policy_id'])
        predicate_builder: Tuple = data['predicate_builder']
    except Exception as e:
        logger.error('assign_predicate_to_purchase_policy - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.assign_predicate_to_purchase_policy(user_id, store_id, policy_id, predicate_builder)

@store_bp.route('/view_all_policies_of_store', methods=['POST'])
@jwt_required()
def view_all_policies_of_store():
    """
        Use Case ____(idk I need to check)
        View all the policies of a store
    """
    logger.info('received request to view all policies of store')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error('view_all_policies_of_store - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.view_all_policies_of_store(user_id, store_id)

@store_bp.route('/my_stores', methods=['GET'])
@jwt_required()
def my_stores():
    """
        Use Case
        Get all the stores that user is a part of
    """
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        logger.error(('my_stores - ', str(e)))
        return jsonify({'message': str(e)}), 400
    
    return store_service.my_stores(user_id)

@store_bp.route('/tags', methods=['GET'])
@jwt_required()
def get_all_product_tags():
    """
        Helper for search by tags
        Get all the tags of a product
    """
    logger.info('received request to get all product tags')
    try:
        _ = get_jwt_identity()
    except Exception as e:
        logger.error('get_all_product_tags - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.get_all_product_tags()

@store_bp.route('/store_ids_to_names', methods=['GET'])
@jwt_required()
def get_all_store_names():
    """
        Helper for search by store
        Get all the names of the stores
    """
    logger.info('received request to get all store names')
    try:
        _ = get_jwt_identity()
    except Exception as e:
        logger.error('get_all_store_names - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.get_all_store_names()

@store_bp.route('/category_ids_to_names', methods=['GET'])
@jwt_required()
def get_all_category_names():
    """
        Helper for search by category
        Get all the names of the categories
    """
    logger.info('received request to get all category names')
    try:
        _ = get_jwt_identity()
    except Exception as e:
        logger.error('get_all_category_names - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.get_all_categories()

@store_bp.route('/get_product_categories', methods=['POST'])
@jwt_required()
def get_product_categories():
    """
        Get product categories
        get store_id from request
    """
    logger.info('received request to get product categories')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
    except Exception as e:
        logger.error('get_product_categories - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.get_product_categories(user_id, store_id, product_id)


@store_bp.route('/get_total_price_after_discounts', methods=['GET'])
@jwt_required()
def get_total_price_after_discounts():
    """
        Use Case
        Get total price after discounts
    """
    logger.info('received request to get total price after discounts')
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        logger.error('get_total_price_after_discounts - ', str(e))
        return jsonify({'message': str(e)}), 400

    return store_service.get_total_price_after_discount(user_id)