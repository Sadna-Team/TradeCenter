# communication with business logic
from backend.business import MarketFacade
from flask import jsonify

import logging

logger = logging.getLogger('myapp')


class StoreService:
    def __init__(self):
        self.__market_facade = MarketFacade()

    def add_discount(self):
        pass

    def remove_discount(self):
        pass

    def edit_discount(self):
        pass

    def add_purchase_policy(self):
        pass

    def remove_purchase_policy(self):
        pass

    def edit_purchase_policy(self):
        pass

    def show_store_info(self, store_id: int):
        """
            Show information about the stores in the system
        """
        try:
            info = self.__market_facade.get_store_info(store_id)
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
            info = self.__market_facade.get_store_product_info(store_id)
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
                             weight: float, tags: list[str]):
        """
            Add a product to a store
        """
        try:
            self.__market_facade.add_product(user_id, store_id, product_name, description, price, weight, tags)
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

    def add_store_owner(self, user_id: int, store_id: int, new_owner_username):
        """
            Send promotion to a new owner to a store.
            User still needs to accept the promotion! 
        """
        try:
            self.__market_facade.nominate_store_owner(user_id, store_id, new_owner_username)
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

    def get_nominations_data_structure(self):
        return self.__market_facade.get_nominations_data_structure()

    def edit_manager_permissions(self, user_id: int, store_id: int, manager_id: int, add_product: bool,
                           change_purchase_policy: bool, change_purchase_types: bool, change_discount_policy: bool,
                           change_discount_types: bool, add_manager: bool, get_bid: bool):
        """
            Edit the permissions of a store manager
        """
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

    def view_employees_info(self, user_id: int, store_id: int):
        """
            View information about the employees of a store
        """
        '''try:
            info = self.__market_facade.get_employees_info(user_id, store_id)
            logger.info('employees info was sent successfully')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('employees info was not sent')
            return jsonify({'message': str(e)}), 400'''
        pass
