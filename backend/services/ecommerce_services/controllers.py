# communication with business logic
from typing import Optional

from backend.business import MarketFacade
from flask import jsonify

import logging

logger = logging.getLogger('myapp')


class PurchaseService:
    def __init__(self):
        self.__market_facade = MarketFacade()

    def checkout(self, user_id: int, payment_details: dict, supply_method: str, address: dict):
        """
            Checkout the shopping cart
        """
        try:
            info = self.__market_facade.checkout(user_id, payment_details, supply_method, address)
            logger.info('checkout was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('checkout was not successful')
            return jsonify({'message': str(e)}), 400

    def show_purchase_history_in_store(self, user_id: int, store_id: int):
        """
            Show the purchase history in a store
        """
        try:
            info = self.__market_facade.view_purchases_of_store(user_id, store_id)
            logger.info('show_purchase_history_in_store was successful')
            info = [x.get() for x in info]
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('show_purchase_history_in_store was not successful')
            return jsonify({'message': str(e)}), 400

    def show_purchase_history_of_user(self, user_id: int):
        """
            Show the purchase history of a member
        """
        try:
            info = self.__market_facade.view_purchases_of_user(user_id)
            logger.info('show_purchase_history_of_user was successful')
            info = [x.get() for x in info]
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('show_purchase_history_of_user was not successful')
            return jsonify({'message': str(e)}), 400

    def search_products_by_category(self, category_id: int, store_id: Optional[int]):
        """
            Search products in the stores
        """
        try:
            info = self.__market_facade.search_by_category(category_id, store_id)
            logger.info('search_products_by_category was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('search_products_by_category was not successful')
            return jsonify({'message': str(e)}), 400

    def search_products_by_tags(self, tags: list[str], store_id: Optional[int]):
        """
            Search products by tags
        """
        try:
            info = self.__market_facade.search_by_tags(tags, store_id)
            logger.info('search_products_by_tags was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('search_products_by_tags was not successful')
            return jsonify({'message': str(e)}), 400

    def search_products_by_name(self, name: str, store_id: Optional[int]):
        """
            search products by name
        """
        try:
            info = self.__market_facade.search_by_name(name, store_id)
            logger.info('search_products_by_name was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('search_products_by_name was not successful')
            return jsonify({'message': str(e)}), 400

