# communication with business logic
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from backend.business import MarketFacade
from flask import jsonify

import logging

logger = logging.getLogger('myapp')


class StoreService:
    def __init__(self):
        self.__market_facade = MarketFacade()

    def add_discount(self, user_id: int, description: str, start_date: datetime, end_date: datetime, percentage: float, 
                        store_id: Optional[int] = None, product_id: Optional[int] = None, category_id: Optional[int] = None, applied_to_sub: Optional[bool] = None):
        """
            Add a discount to the system
        """
        try:
            self.__market_facade.add_discount(user_id, description, start_date, end_date, percentage, store_id, product_id, category_id, applied_to_sub)
            logger.info('discount was added successfully')
            return jsonify({'message': 'discount was added successfully'}), 200
        except Exception as e:
            logger.error('discount was not added')
            return jsonify({'message': str(e)}), 400
        
    def remove_discount(self, user_id: int, discount_id: int):
        """
            Remove a discount from the system
        """
        try:
            self.__market_facade.remove_discount(user_id, discount_id)
            logger.info('discount was removed successfully')
            return jsonify({'message': 'discount was removed successfully'}), 200
        except Exception as e:
            logger.error('discount was not removed')
            return jsonify({'message': str(e)}), 400
        
        
    def create_logical_composite_discount(self, user_id: int, description: str, start_date: datetime, end_date: datetime, discount_id1: int, discount_id2: int, type_of_composite: int):
        """
            Create a logical composite discount
        """
        try:
            composite_discount_id = self.__market_facade.create_logical_composite_discount(user_id, description, start_date, end_date, discount_id1, discount_id2, type_of_composite)
            logger.info('composite discount was created successfully')
            return jsonify({'message': composite_discount_id}), 200
        except Exception as e:
            logger.error('composite discount was not created')
            return jsonify({'message': str(e)}), 400
        
    def create_numerical_composite_discount(self, user_id: int, description: str, start_date: datetime, end_date: datetime, discount_ids: List[int], type_of_composite: int):
        """
            Create a numerical composite discount
        """
        try:
            composite_discount_id = self.__market_facade.create_numerical_composite_discount(user_id, description, start_date, end_date, discount_ids, type_of_composite)
            logger.info('composite discount was created successfully')
            return jsonify({'message': composite_discount_id}), 200
        except Exception as e:
            logger.error('composite discount was not created')
            return jsonify({'message': str(e)}), 400
    
    def assign_predicate_to_discount(self, user_id: int, discount_id: int, predicate_builder: Tuple):
        """
            Assign a predicate to a discount
        """
        try:
            """ Maybe we have to receive the predicate_builder as a string and then build it here to a tuple?"""
            self.__market_facade.assign_predicate_to_discount(user_id, discount_id, predicate_builder)
            logger.info('predicate was assigned successfully')
            return jsonify({'message': 'predicate was assigned successfully'}), 200
        except Exception as e:
            logger.error('predicate was not assigned')
            return jsonify({'message': str(e)}), 400
        
    def change_discount_percentage(self, user_id: int, discount_id: int, new_percentage: float) :
        """
            Change the percentage of a discount
        """
        try:
            self.__market_facade.change_discount_percentage(user_id, discount_id, new_percentage)
            logger.info('discount percentage was changed successfully')
            return jsonify({'message': 'discount percentage was changed successfully'}), 200
        except Exception as e:
            logger.error('discount percentage was not changed')
            return jsonify({'message': str(e)}), 400
        
    def change_discount_description(self, user_id: int, discount_id: int, new_description: str) :
        """
            Change the description of a discount
        """
        try:
            self.__market_facade.change_discount_description(user_id, discount_id, new_description)
            logger.info('discount description was changed successfully')
            return jsonify({'message': 'discount description was changed successfully'}), 200
        except Exception as e:
            logger.error('discount description was not changed')
            return jsonify({'message': str(e)}), 400
        
    def view_all_discount_info(self, user_id: int):
        """
            View information about all discounts in the system
        """
        try:
            info = self.__market_facade.get_all_discount_info(user_id)
            logger.info('discount info was sent successfully')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('discount info was not sent')
            return jsonify({'message': str(e)}), 400

    def add_purchase_policy(self, user_id: int, store_id: int, policy_name: str, category_id: Optional[int] = None, product_id: Optional[int] = None):
        try:
            self.__market_facade.add_purchase_policy(user_id, store_id, policy_name, category_id, product_id)
            logger.info('purchase policy was added successfully')
            return jsonify({'message': 'purchase policy was added successfully'}), 200
        except Exception as e:
            logger.error('purchase policy was not added')
            return jsonify({'message': str(e)}), 400

     
    def remove_purchase_policy(self, user_id: int, store_id: int, policy_id: int):
        try:
            self.__market_facade.remove_purchase_policy(user_id, store_id, policy_id)
            logger.info('purchase policy was removed successfully')
            return jsonify({'message': 'purchase policy was removed successfully'}), 200
        except Exception as e:
            logger.error('purchase policy was not removed')
            return jsonify({'message': str(e)}), 400

    def create_composite_purchase_policy(self, user_id: int, store_id: int, policy_name: str, policy_id1: int, policy_id2: int, type_of_composite: int):
        try:
            composite_policy_id = self.__market_facade.create_composite_purchase_policy(user_id, store_id, policy_name, policy_id1, policy_id2, type_of_composite)
            logger.info('composite purchase policy was created successfully')
            return jsonify({'message': composite_policy_id}), 200
        except Exception as e:
            logger.error('composite purchase policy was not created')
            return jsonify({'message': str(e)}), 400
        
    def assign_predicate_to_purchase_policy(self, user_id: int, store_id:int, policy_id: int, predicate_builder: Tuple):
        try:
            """ Maybe we have to receive the predicate_builder as a string and then build it here to a tuple?"""
            self.__market_facade.assign_predicate_to_purchase_policy(user_id, store_id,policy_id, predicate_builder)
            logger.info('predicate was assigned successfully')
            return jsonify({'message': 'predicate was assigned successfully'}), 200
        except Exception as e:
            logger.error('predicate was not assigned')
            return jsonify({'message': str(e)}), 400


    def show_store_info(self, store_id: int):
        """
            Show information about the stores in the system
        """
        try:
            info = self.__market_facade.get_store_info(store_id).get()
            logger.info('store info was sent successfully')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('store info was not sent')
            return jsonify({'message': str(e)}), 400

    def show_store_products(self, store_id: int):
        """
            Show products of a store
        """
        try:
            info = [p.get() for p in self.__market_facade.get_store_product_info(store_id)]
            logger.info('store products info was sent successfully')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('store products info was not sent')
            return jsonify({'message': str(e)}), 400

    def add_new_store(self, user_id: int, location_id: int, store_name: str):
        """
            Add a store to the system and set the user as the store owner
        """
        try:
            self.__market_facade.add_store(user_id, location_id, store_name)
            logger.info('store was added successfully')
            return jsonify({'message': 'store was added successfully'}), 200
        except Exception as e:
            logger.error('store was not added')
            return jsonify({'message': str(e)}), 400

    def add_product_to_store(self, user_id: int, store_id: int, product_name: str, description: str, price: float,
                             weight: float, tags: list[str], amount: Optional[int]=0):
        """
            Add a product to a store
        """
        try:
            self.__market_facade.add_product(user_id, store_id, product_name, description, price, weight, tags, amount)
            logger.info('product was added successfully')
            return jsonify({'message': 'product was added successfully'}), 200
        except Exception as e:
            logger.error('product was not added')
            return jsonify({'message': str(e)}), 400

    def remove_product_from_store(self, user_id: int, store_id: int, product_id: int):
        """
            Remove a product from a store
        """
        try:
            self.__market_facade.remove_product(user_id, store_id, product_id)
            logger.info('product was removed successfully')
            return jsonify({'message': 'product was removed successfully'}), 200
        except Exception as e:
            logger.error('product was not removed')
            return jsonify({'message': str(e)}), 400
        
    def change_price_of_product(self, user_id: int, store_id: int, product_id: int, new_price: float):
        """
            Change the price of a product
        """
        try:
            self.__market_facade.change_product_price(user_id, store_id, product_id, new_price)
            logger.info('product price was changed successfully')
            return jsonify({'message': 'product price was changed successfully'}), 200
        except Exception as e:
            logger.error('product price was not changed')
            return jsonify({'message': str(e)}), 400
        
    
    def change_description_of_product(self, user_id: int, store_id: int, product_id: int, new_description: str):
        """
            Change the description of a product
        """
        try:
            self.__market_facade.change_product_description(user_id, store_id, product_id, new_description)
            logger.info('product description was changed successfully')
            return jsonify({'message': 'product description was changed successfully'}), 200
        except Exception as e:
            logger.error('product description was not changed')
            return jsonify({'message': str(e)}), 400
        
    def change_weight_of_product(self, user_id: int, store_id: int, product_id: int, new_weight: float):
        """
            Change the weight of a product
        """
        try:
            self.__market_facade.change_product_weight(user_id, store_id, product_id, new_weight)
            logger.info('product weight was changed successfully')
            return jsonify({'message': 'product weight was changed successfully'}), 200
        except Exception as e:
            logger.error('product weight was not changed')
            return jsonify({'message': str(e)}), 400
        
    def add_tag_to_product(self, user_id: int, store_id: int, product_id: int, tag: str):
        """
            Add a tag to a product
        """
        try:
            self.__market_facade.add_tag_to_product(user_id, store_id, product_id, tag)
            logger.info('tag was added successfully')
            return jsonify({'message': 'tag was added successfully'}), 200
        except Exception as e:
            logger.error('tag was not added')
            return jsonify({'message': str(e)}), 400
        
    def remove_tag_from_product(self, user_id: int, store_id: int, product_id: int, tag: str):
        """
            Remove a tag from a product
        """
        try:
            self.__market_facade.remove_tag_from_product(user_id, store_id, product_id, tag)
            logger.info('tag was removed successfully')
            return jsonify({'message': 'tag was removed successfully'}), 200
        except Exception as e:
            logger.error('tag was not removed')
            return jsonify({'message': str(e)}), 400
        
    def restock(self, user_id: int, store_id: int, product_id: int, amount: int):
        """
            Restock a product
        """
        try:
            self.__market_facade.add_product_amount(user_id, store_id, product_id, amount)
            logger.info('product was restocked successfully')
            return jsonify({'message': 'product was restocked successfully'}), 200
        except Exception as e:
            logger.error('product was not restocked')
            return jsonify({'message': str(e)}), 400
        
    def remove_amount_from_product(self, user_id: int, store_id: int, product_id: int, amount: int):
        """
            Remove amount from a product
        """
        try:
            self.__market_facade.remove_product_amount(user_id, store_id, product_id, amount)
            logger.info('amount was removed successfully')
            return jsonify({'message': 'amount was removed successfully'}), 200
        except Exception as e:
            logger.error('amount was not removed')
            return jsonify({'message': str(e)}), 400
    

    def add_category(self, user_id: int, category_name: str):
        """
            Add a category to a store
        """
        try:
            self.__market_facade.add_category(user_id, category_name)
            logger.info('category was added successfully')
            return jsonify({'message': 'category was added successfully'}), 200
        except Exception as e:
            logger.error('category was not added')
            return jsonify({'message': str(e)}), 400

    def remove_category(self, user_id: int, category_id: int):
        """
            Remove a category from a store
        """
        try:
            self.__market_facade.remove_category(user_id, category_id)
            logger.info('category was removed successfully')
            return jsonify({'message': 'category was removed successfully'}), 200
        except Exception as e:
            logger.error('category was not removed')
            return jsonify({'message': str(e)}), 400

    def add_subcategory_to_category(self, user_id: int, category_id: int, parent_category_id: int):
        """
            Add a subcategory to a category
        """
        try:
            self.__market_facade.add_sub_category_to_category(user_id, category_id, parent_category_id)
            logger.info('subcategory was added successfully')
            return jsonify({'message': 'subcategory was added successfully'}), 200
        except Exception as e:
            logger.error('subcategory was not added')
            return jsonify({'message': str(e)}), 400

    def remove_subcategory_from_category(self, user_id: int, category_id: int, parent_category_id: int):
        """
            Remove a subcategory from a category
        """
        try:
            self.__market_facade.remove_sub_category_from_category(user_id, category_id, parent_category_id)
            logger.info('subcategory was removed successfully')
            return jsonify({'message': 'subcategory was removed successfully'}), 200
        except Exception as e:
            logger.error('subcategory was not removed')
            return jsonify({'message': str(e)}), 400

    def assign_product_to_category(self, user_id: int, category_id: int, store_id: int, product_id: int):
        """
            Add a product to a category
        """
        try:
            self.__market_facade.assign_product_to_category(user_id, category_id, store_id, product_id)
            logger.info('product was added to category successfully')
            return jsonify({'message': 'product was added to category successfully'}), 200
        except Exception as e:
            logger.error('product was not added to category')
            return jsonify({'message': str(e)}), 400
        
    def remove_product_from_category(self, user_id: int, category_id: int, store_id: int, product_id: int):
        """
            Remove a product from a category
        """
        try:
            self.__market_facade.remove_product_from_category(user_id, category_id, store_id, product_id)
            logger.info('product was removed from category successfully')
            return jsonify({'message': 'product was removed from category successfully'}), 200
        except Exception as e:
            logger.error('product was not removed from category')
            return jsonify({'message': str(e)}), 400

    def add_store_owner(self, user_id: int, store_id: int, new_owner_username: str):
        """
            Send promotion to a new owner to a store.
            User still needs to accept the promotion! 
        """
        try:
            self.__market_facade.nominate_store_owner(store_id, user_id, new_owner_username)
            logger.info('store owner was added successfully')
            return jsonify({'message': 'store owner was added successfully'}), 200
        except Exception as e:
            logger.error('store owner was not added')
            return jsonify({'message': str(e)}), 400

    def add_store_manager(self, user_id: int, store_id: int, manager_username):
        """
            Add a store manager
        """
        try:
            self.__market_facade.nominate_store_manager(store_id, user_id, manager_username)
            logger.info('store manager was added successfully')
            return jsonify({'message': 'store manager was added successfully'}), 200
        except Exception as e:
            logger.error('store manager was not added')
            return jsonify({'message': str(e)}), 400

    def remove_store_role(self, user_id: int, store_id: int, username: str):
        """
            Remove a store role (owner/manager)
        """
        try:
            self.__market_facade.remove_store_role(user_id, store_id, username)
            logger.info('store role was removed successfully')
            return jsonify({'message': 'store role was removed successfully'}), 200
        except Exception as e:
            logger.error('store role was not removed')
            return jsonify({'message': str(e)}), 400

    def give_up_role(self, user_id: int, store_id: int):
        try:
            self.__market_facade.give_up_role(user_id, store_id)
            logger.info('role was given up successfully')
            return jsonify({'message': 'role was given up successfully'}), 200
        except Exception as e:
            logger.error('role was not given up')
            return jsonify({'message': str(e)}), 400

    def edit_manager_permissions(self, user_id: int, store_id: int, manager_id: int, permissions: list[str]):
        """
            Edit the permissions of a store manager
        """
        add_product = 'add_product' in permissions
        change_purchase_policy = 'change_purchase_policy' in permissions
        change_purchase_types = 'change_purchase_types' in permissions
        change_discount_policy = 'change_discount_policy' in permissions
        change_discount_types = 'change_discount_types' in permissions
        add_manager = 'add_manager' in permissions
        get_bid = 'get_bid' in permissions

        try:
            self.__market_facade.change_permissions(user_id, store_id, manager_id, add_product, change_purchase_policy,
                                                    change_purchase_types, change_discount_policy,
                                                    change_discount_types, add_manager, get_bid)
            logger.info('manager permissions were edited successfully')
            return jsonify({'message': 'manager permissions were edited successfully'}), 200
        except Exception as e:
            logger.error('manager permissions were not edited')
            return jsonify({'message': str(e)}), 400

    def closing_store(self, user_id, store_id):
        """
            Close a store
        """
        try:
            self.__market_facade.close_store(user_id, store_id)
            logger.info('store was closed successfully')
            return jsonify({'message': 'store was closed successfully'}), 200
        except Exception as e:
            logger.error('store was not closed')
            return jsonify({'message': str(e)}), 400
        
    def opening_store(self, user_id, store_id):
        """
            Open a store
        """
        try:
            self.__market_facade.open_store(user_id, store_id)
            logger.info('store was opened successfully')
            return jsonify({'message': 'store was opened successfully'}), 200
        except Exception as e:
            logger.error('store was not opened')
            return jsonify({'message': str(e)}), 400

    def view_employees_info(self, user_id: int, store_id: int):
        """
            View information about the employees of a store
        """
        try:
            info = self.__market_facade.get_employees_info(user_id, store_id)
            print(info)
            info = jsonify({'message': info}), 200
            logger.info('employees info was sent successfully')
            return info
        except Exception as e:
            logger.error('employees info was not sent')
            return jsonify({'message': str(e)}), 400
        
    def get_all_product_tags(self):
        """
            Get all the tags of the products in the system
        """
        try:
            tags = self.__market_facade.get_all_product_tags()
            logger.info('tags were sent successfully')
            return jsonify({'message': tags}), 200
        except Exception as e:
            logger.error('tags were not sent')
            return jsonify({'message': str(e)}), 400
        
    def get_all_store_names(self):
        """
            Get all the names of the stores in the system
        """
        try:
            names = self.__market_facade.get_all_store_names()
            logger.info('store ids to names were sent successfully')
            return jsonify({'message': names}), 200
        except Exception as e:
            logger.error('store ids to names were not sent')
            return jsonify({'message': str(e)}), 400
        
    def get_all_categories(self):
        """
            Get all the categories in the system
        """
        try:
            categories = self.__market_facade.get_all_categories()
            logger.info('categories were sent successfully')
            return jsonify({'message': categories}), 200
        except Exception as e:
            logger.error('categories were not sent')
            return jsonify({'message': str(e)}), 400
        