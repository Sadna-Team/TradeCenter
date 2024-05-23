from flask import Blueprint, request, jsonify
from backend.business.store import StoreFacade
from backend.business import MarketFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies


#-------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')
#---------------------------------------------------


# API endpoints and their corresponding route handlers
store_bp = Blueprint('store', __name__)
store_facade = StoreFacade()
market_facade = MarketFacade()

@store_bp.route('/add_discount', methods=['POST'])
@jwt_required()
def add_discount():
    """
        Use Case 2.4.2
        Add a discount to a store
        
        Data:
            description (str): description of the discount
            startDate (datetime): start date of the discount
            endDate (datetime): end date of the discount
            percentage (float): percentage of the discount
        
    """
    logger.info('received request to add discount')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        description = data['description']
        startDate = data['startDate']
        endDate = data['endDate']
        percentage = data['percentage']
        market_facade.add_discount(user_id, description, startDate, endDate, percentage)
        logger.info('discount was added successfully')
        return jsonify({'message': 'discount was added successfully'}), 200
    except Exception as e:
        logger.error('add_discount - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/remove_discount', methods=['POST'])
@jwt_required()
def remove_discount():
    """
        Use Case 2.4.2
        Remove a discount from a store
        
        Data:
            user_id (int): id of the user
            discount_id (int): id of the discount to remove
            
        
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


@store_bp.route('/edit_discount', methods=['POST'])
@jwt_required()
def edit_discount():
    """
        Use Case 2.4.2
        Edit a discount of a store
        
        Data:
            user_id (int): id of the user
            discount_id (int): id of the discount to edit
        
    """
    logger.info('received request to edit discount')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        discount_id = data['discount_id']
        market_facade.editDiscount(user_id, discount_id)
        logger.info('discount was edited successfully')
        return jsonify({'message': 'discount was edited successfully'}), 200
    except Exception as e:
        logger.error('edit_discount - ', str(e))
        return jsonify({'message': str(e)}), 400

@store_bp.route('/add_purchase_policy', methods=['POST'])
@jwt_required
def add_purchase_policy():
    """
        Use Case 2.2.4.2
        Add a purchase policy to a store
        
        Data:
            user_id (int): id of the user
            store_id (int): id of the store
            TODO: later on the details of policy!
        
    """
    logger.info('received request to add purchase policy')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        market_facade.addPurchasePolicy(user_id, store_id)
        logger.info('purchase policy was added successfully')
        return jsonify({'message': 'purchase policy was added successfully'}), 200
    except Exception as e:
        logger.error('add_purchase_policy - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@store_bp.route('/remove_purchase_policy', methods=['POST'])
@jwt_required
def remove_purchase_policy():
    """
        Use Case 2.2.4.2
        Remove a purchase policy from a store
        
        Data:
            user_id (int): id of the user
            store_id (int): id of the store
            policy_id (int): id of the policy to remove
            
    """
    logger.info('received request to remove purchase policy')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        policy_id = data['policy_id']
        market_facade.removePurchasePolicy(user_id, store_id, policy_id)
        logger.info('purchase policy was removed successfully')
        return jsonify({'message': 'purchase policy was removed successfully'}), 200
    except Exception as e:
        logger.error('remove_purchase_policy - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@store_bp.route('/change_purchase_policy', methods=['POST'])
@jwt_required
def edit_purchase_policy():
    """
        Use Case 2.2.4.2
        Edit a purchase policy of a store
        
        Data:
            user_id (int): id of the user
            store_id (int): id of the store
            policy_id (int): id of the policy to edit
            
    """
    logger.info('received request to edit purchase policy')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        policy_id = data['policy_id']
        market_facade.changePurchasePolicy(user_id, store_id, policy_id)
        logger.info('purchase policy was edited successfully')
        return jsonify({'message': 'purchase policy was edited successfully'}), 200
    except Exception as e:
        logger.error('edit_purchase_policy - ', str(e))
        return jsonify({'message': str(e)}), 400


    
@store_bp.route('/store_info', methods=['GET'])
@jwt_required()
def show_store_info():
    """
        Use Case 2.2.1.1:
        Show information about the stores in the system

        Data:
            store_id (int): the id of the store
    """
    logger.info('received request to send store info')
    try:
        user_id = get_jwt_identity()
        data = request.args
        store_id = data['store_id']
        info = market_facade.get_store_info(user_id, store_id)
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
    logger.info('received request to send store products')
    try:
        user_id = get_jwt_identity()
        data = request.args
        store_id = data['store_id']
        products = store_facade.get_store_product_information(store_id)
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
            founder_id (int): id of the user
            location_id (int): id of the location
            store_name (str): name of the store

        Returns:
            ?
    """
    logger.info('received request to add store')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        location_id = data['location_id']
        store_name = data['store_name']
        market_facade.addStore(user_id, location_id, store_name)
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
            user_id (int): id of the user
            store_id (int): id of the store
            product_spec_id (int): id of the product specification
            expirationDate (datetime): expiration date of the product
            condition (str): condition of the product
            price (float): price of the product
            
    """
    logger.info('received request to add product')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        product_spec_id = data['product_spec_id']
        expirationDate = data['expirationDate']
        condition = data['condition']
        price = data['price']
        market_facade.addProduct(user_id, store_id, product_spec_id, expirationDate, condition, price)
        logger.info('product was added successfully')
        return jsonify({'message': 'product was successfully added'}), 200
    except Exception as e:
        logger.error('add_product - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/remove_product', methods=['POST'])
@jwt_required()
def remove_product():
    """
        Use Case: 2.2.4.1
        Remove a product from a store

        Data:
            user_id (int): id of the user
            store_id (int): id of the store
            product_id (int): id of the product to remove
            
    """
    logger.info('received request to remove product')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        product_id = data['product_id']
        market_facade.removeProduct(user_id, store_id, product_id)
        logger.info('product was removed successfully')
        return jsonify({'message': 'product was successfully removed'}), 200
    except Exception as e:
        logger.error('remove_product - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/change_price', methods=['POST'])
@jwt_required()
def change_price():
    """
        Use Case 2.2.4.1:
        Change the price of a product in a store

        Data:
            user_id (int): id of the user
            store_id (int): id of the store
            product_id (int): id of the product
            new_price (float): new price of the product
    """
    logger.info('received request to change price')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        product_id = data['product_id']
        new_price = data['new_price']
        market_facade.changeProductPrice(user_id, store_id, product_id, new_price)
        logger.info('price was changed successfully')
        return jsonify({'message': 'price was successfully changed'}), 200
    except Exception as e:
        logger.error('change_price - ', str(e))
        return jsonify({'message': str(e)}), 400

@store_bp.route('/add_product_specification', methods=['POST'])
@jwt_required()
def add_product_specification():
    """
        Use Case 2.2.4.1:
        Add a product specification to a store
        
        Data:
            user_id (int): id of the user
            name (str): name of the product
            weight (float): weight of the product
            description (str): description of the product
            tags (list[str]): tags of the product
            manufacturer (str): manufacturer of the product
            
    """
    logger.info('received request to add product specification')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        name = data['name']
        weight = data['weight']
        description = data['description']
        tags = data['tags']
        manufacturer = data['manufacturer']
        market_facade.addProductSpec(user_id, name, weight, description, tags, manufacturer)
        logger.info('product specification was added successfully')
        return jsonify({'message': 'product specification was successfully added'}), 200
    except Exception as e:
        logger.error('add productSpecification -', str(e))
        return jsonify({'message': str(e)}), 400
    
    
@store_bp.route('/change_product_specification_name', methods=['POST'])
@jwt_required()
def change_product_specification_name():
    """
        Use Case 2.2.4.1:
        Change the name of a product specification
        
        Data:
            user_id (int): id of the user
            product_spec_id (int): id of the product specification
            name (str): new name of the product specification
    """
    logger.info('received request to change product specification name')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_spec_id = data['product_spec_id']
        name = data['name']
        market_facade.changeProductSpecName(user_id, product_spec_id, name)
        logger.info('product specification name was changed successfully')
        return jsonify({'message': 'product specification name was changed successfully'}), 200
    except Exception as e:
        logger.error('change_product_specification_name - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@store_bp.route('/change_product_specification_weight', methods=['POST'])
@jwt_required()
def change_product_specification_weight():
    """
        Use Case 2.2.4.1:
        Change the weight of a product specification
        
        Data:
            user_id (int): id of the user
            product_spec_id (int): id of the product specification
            weight (float): new weight of the product specification
    """
    logger.info('received request to change product specification weight')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_spec_id = data['product_spec_id']
        weight = data['weight']
        market_facade.changeProductSpecWeight(user_id, product_spec_id, weight)
        logger.info('product specification weight was changed successfully')
        return jsonify({'message': 'product specification weight was changed successfully'}), 200
    except Exception as e:
        logger.error('change_product_specification_weight - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@store_bp.route('/change_product_specification_description', methods=['POST'])
@jwt_required()
def change_product_specification_description():
    """
        Use Case 2.2.4.1:
        Change the description of a product specification
        
        Data:
            user_id (int): id of the user
            product_spec_id (int): id of the product specification
            description (str): new description of the product specification
    """
    logger.info('received request to change product specification description')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_spec_id = data['product_spec_id']
        description = data['description']
        market_facade.changeProductSpecDescription(user_id, product_spec_id, description)
        logger.info('product specification description was changed successfully')
        return jsonify({'message': 'product specification description was changed successfully'}), 200
    except Exception as e:
        logger.error('change_product_specification_description - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@store_bp.route('/change_product_specification_manufacturer', methods=['POST'])
@jwt_required()
def change_product_specification_manufacturer():
    """
        Use Case 2.2.4.1:
        Change the manufacturer of a product specification

        Data:
            user_id (int): id of the user
            product_spec_id (int): id of the product specification
            manufacturer (str): new manufacturer of the product specification
            
    """
    logger.info('received request to change product specification manufacturer')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_spec_id = data['product_spec_id']
        manufacturer = data['manufacturer']
        market_facade.changeProductSpecManufacturer(user_id, product_spec_id, manufacturer)
        logger.info('product specification manufacturer was changed successfully')
        return jsonify({'message': 'product specification manufacturer was changed successfully'}), 200
    except Exception as e:
        logger.error('change_product_specification_manufacturer - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/add_tag_to_product_specification', methods=['POST'])
@jwt_required()
def add_tag_to_product_specification():
    """
        Use Case: 2.2.4.1
        Add a tag to a product specification
        
        Data:
            user_id (int): id of the user
            product_spec_id (int): id of the product specification
            tag (str): tag to add
    """
    logger.info('received request to add tag to product specification')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_spec_id = data['product_spec_id']
        tag = data['tag']
        market_facade.addTagToProductSpec(user_id, product_spec_id, tag)
        logger.info('tag was added successfully')
        return jsonify({'message': 'tag was added successfully'}), 200
    except Exception as e:
        logger.error('add_tag_to_product_specification - ', str(e))
        return jsonify({'message': str(e)}), 400
        
        
@store_bp.route('/remove_tag_from_product_specification', methods=['POST'])
@jwt_required()
def remove_tag_from_product_specification():
    """
        Use Case: 2.2.4.1
        Remove a tag from a product specification
        
        Data:
            user_id (int): id of the user
            product_spec_id (int): id of the product specification
            tag (str): tag to remove
    """
    logger.info('received request to remove tag from product specification')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_spec_id = data['product_spec_id']
        tag = data['tag']
        market_facade.removeTagFromProductSpec(user_id, product_spec_id, tag)
        logger.info('tag was removed successfully')
        return jsonify({'message': 'tag was removed successfully'}), 200
    except Exception as e:
        logger.error('remove_tag_from_product_specification - ', str(e))
        return jsonify({'message': str(e)}), 400
    
    
@store_bp.route('/add_category', methods=['POST'])
@jwt_required()
def add_category():
    """
        Use Case 
        Add a category to a store
        
        Data:
            user_id (int): id of the user
            category_name (str): name of the category
            
    """
    logger.info('received request to add category')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        category_name = data['category_name']
        market_facade.addCategory(user_id, category_name)
        logger.info('category was added successfully')
        return jsonify({'message': 'category was added successfully'}), 200
    except Exception as e:
        logger.error('add_category - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@store_bp.route('/remove_category', methods=['POST'])
@jwt_required()
def remove_category():
    """
        Use Case 
        Remove a category from a store
        
        Data:
            user_id (int): id of the user
            category_id (int): id of the category
            
    """
    logger.info('received request to remove category')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        category_id = data['category_id']
        market_facade.removeCategory(user_id, category_id)
        logger.info('category was removed successfully')
        return jsonify({'message': 'category was removed successfully'}), 200
    except Exception as e:
        logger.error('remove_category - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@store_bp.route('/add_subcategory_to_category', methods=['POST'])
@jwt_required()
def add_subcategory_to_category():
    """
        Use Case 
        Add a subcategory to a category
        
        Data:
            user_id (int): id of the user
            sub_category_id (int): id of the subcategory
            parent_category_id (int): id of the parentcategory
            
    """
    logger.info('received request to add subcategory to category')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        subcategory_id = data['subcategory_id']
        parentcategory_id = data['parentcategory_id']
        market_facade.addSubcategoryToCategory(user_id, subcategory_id, parentcategory_id)
        logger.info('subcategory was added successfully')
        return jsonify({'message': 'subcategory was added successfully'}), 200
    except Exception as e:
        logger.error('add_subcategory_to_category - ', str(e))
        return jsonify({'message': str(e)}), 400
            
            
@store_bp.route('/remove_subcategory_from_category', methods=['POST'])
@jwt_required()
def remove_subcategory_from_category():
    """
        Use Case 
        Remove a subcategory from a category
        
        Data:
            user_id (int): id of the user
            sub_category_id (int): id of the subcategory
            parent_category_id (int): id of the parentcategory
            
    """
    logger.info('received request to remove subcategory from category')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        subcategory_id = data['subcategory_id']
        parentcategory_id = data['parentcategory_id']
        market_facade.removeSubcategoryFromCategory(user_id, parentcategory_id, subcategory_id)
        logger.info('subcategory was removed successfully')
        return jsonify({'message': 'subcategory was removed successfully'}), 200
    except Exception as e:
        logger.error('remove_subcategory_from_category - ', str(e))
        return jsonify({'message': str(e)}), 400


@store_bp.route('/assign_product_specification_to_category', methods=['POST'])
@jwt_required()
def assign_product_specification_to_category():
    """
        Use Case 
        Assign a product specification to a category
        
        Data:
            user_id (int): id of the user
            category_id (int): id of the category
            product_spec_id (int): id of the product specification
            
    """
    logger.info('received request to assign product specification to category')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_spec_id = data['product_spec_id']
        category_id = data['category_id']
        market_facade.assignProductSpecToCategory(user_id, category_id, product_spec_id)
        logger.info('product specification was assigned to category successfully')
        return jsonify({'message': 'product specification was assigned to category successfully'}), 200
    except Exception as e:
        logger.error('assign_product_specification_to_category - ', str(e))
        return jsonify({'message': str(e)}), 400

@store_bp.route('/remove_product_specification_from_category', methods=['POST'])
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
        market_facade.removeProductSpecFromCategory(user_id, category_id, product_spec_id)
        logger.info('product specification was removed from category successfully')
        return jsonify({'message': 'product specification was removed from category successfully'}), 200
    except Exception as e:
        logger.error('remove_product_specification_from_category - ', str(e))
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
    logger.info('received request to add store owner')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        new_owner_id = data['new_owner_id']
        #TODO: store_facade.() -> this is not ours i have no clue how
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
    logger.info('received request to add store manager')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        new_manager_id = data['new_manager_id']
        permissions = data['permissions']
        #TODO: store_facade.() -> this is not ours I have no clue lmao XD :P :D :3
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
    logger.info('received request to edit manager permissions')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        manager_id = data['manager_id']
        permissions = data['permissions']
        #TODO: store_facade.() -> this is not ours i have no clue how
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
            user_id (int): id of the user
            store_id (int): id of the store
    """
    logger.info('received request to close store')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        market_facade.closeStore(user_id, store_id)
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
    logger.info('received request to view employees info')
    try:
        user_id = get_jwt_identity()
        data = request.args
        store_id = data['store_id']
        info = None #TODO: store_facade.() -> NOT STORE
        logger.info('employees info was sent successfully')
        return jsonify({'message': info}), 200
    except Exception as e:
        logger.error('view_employees_info - ', str(e))
        return jsonify({'message': str(e)}), 400
