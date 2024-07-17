# communication with business logic
from typing import Optional

from backend.business import MarketFacade
from flask import jsonify

import logging

logger = logging.getLogger('myapp')


class PurchaseService:
    def __init__(self):
        self.__market_facade = MarketFacade()

    def test(self,user_id):
        self.__market_facade.test(user_id)

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

    def show_purchase_history_of_user(self, user_id: int, requested_id: int, store_id: Optional[int] = None):
        """
            Show the purchase history of a member
        """
        try:
            info = self.__market_facade.view_purchases_of_user(user_id, requested_id, store_id)
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
            for store_id in info:
                info[store_id] = [x.get() for x in info[store_id]]
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
            for store_id in info:
                info[store_id] = [x.get() for x in info[store_id]]
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
            for store_id in info:
                info[store_id] = [x.get() for x in info[store_id]]
            logger.info('search_products_by_name was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('search_products_by_name was not successful')
            return jsonify({'message': str(e)}), 400
        
        
    def get_store_role(self, user_id: int, store_id: int):
        """
            Get the roles of a user in a store
        """
        try:
            info = self.__market_facade.get_store_role(user_id, store_id)
            logger.info('get_store_roles was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('get_store_roles was not successful')
            return jsonify({'message': str(e)}), 400

    def get_user_stores(self, user_id: int):
        """
            Get the stores of a user
        """
        try:
            info = self.__market_facade.get_user_stores(user_id)
            logger.info('get_user_stores was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('get_user_stores was not successful')

    def bid_checkout(self, user_id: int, bid_id: int, payment_details: dict, supply_method: str, address: dict):
        """
            Checkout of a bid purchase
        """
        try:
            info = self.__market_facade.bid_checkout(user_id,bid_id, payment_details, supply_method, address)
            logger.info('bid_checkout was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('bid_checkout was not successful')
            return jsonify({'message': str(e)}), 400
        
    def user_bid_offer(self, user_id: int, proposed_price: int, store_id: int, product_id: int):
        """
            User bid offer
        """
        try:
            info = self.__market_facade.user_bid_offer(user_id, proposed_price, store_id, product_id)
            logger.info('user_bid_offer was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('user_bid_offer was not successful')
            return jsonify({'message': str(e)}), 400
        
    
    def store_worker_accept_bid(self, store_id: int, user_id: int, bid_id: int):
        """
            Store worker accept bid
        """
        try:
            info = self.__market_facade.store_worker_accept_bid(store_id, user_id, bid_id)
            logger.info('store_worker_accept_bid was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('store_worker_accept_bid was not successful')
            return jsonify({'message': str(e)}), 400
        
    
    def store_worker_decline_bid(self, store_id: int, user_id: int, bid_id: int):
        """
            Store worker decline bid
        """
        try:
            info = self.__market_facade.store_worker_decline_bid(store_id, user_id, bid_id)
            logger.info('store_worker_decline_bid was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('store_worker_decline_bid was not successful')
            return jsonify({'message': str(e)}), 400
        
    def store_worker_counter_bid(self, store_id: int, user_id: int, bid_id: int, proposed_price: int):
        """
            Store worker counter bid
        """
        try:
            info = self.__market_facade.store_worker_counter_bid(store_id, user_id, bid_id, proposed_price)
            logger.info('store_worker_counter_bid was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('store_worker_counter_bid was not successful')
            return jsonify({'message': str(e)}), 400
        
    def user_counter_bid_accept(self, user_id: int, bid_id: int):
        """
            User counter bid accept
        """
        try:
            info = self.__market_facade.user_counter_bid_accept(user_id, bid_id)
            logger.info('user_counter_bid_accept was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('user_counter_bid_accept was not successful')
            return jsonify({'message': str(e)}), 400
        
    
        
    def user_counter_bid_decline(self, user_id: int, bid_id: int):
        """
            User counter bid decline
        """
        try:
            info = self.__market_facade.user_counter_bid_decline(user_id, bid_id)
            logger.info('user_counter_bid_decline was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('user_counter_bid_decline was not successful')
            return jsonify({'message': str(e)}), 400
        

    def user_bid_cancel(self, user_id: int, bid_id: int):
        """
            User counter bid decline
        """
        try:
            info = self.__market_facade.user_bid_cancel(user_id, bid_id)
            logger.info('user_counter_bid_decline was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('user_counter_bid_decline was not successful')
            return jsonify({'message': str(e)}), 400
        
        
    def user_counter_bid(self, user_id: int, bid_id: int, proposed_price: int):
        """
            User counter bid
        """
        try:
            info = self.__market_facade.user_counter_bid(user_id, bid_id, proposed_price)
            logger.info('user_counter_bid was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('user_counter_bid was not successful')
            return jsonify({'message': str(e)}), 400
        
    def show_user_bids(self, system_manager_id:int, user_id: int):
        """
            Show user bids
        """
        try:
            info = self.__market_facade.show_user_bids(system_manager_id, user_id)
            logger.info('show_user_bids was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('show_user_bids was not successful')
            return jsonify({'message': str(e)}), 400
        
    def view_user_bids(self, user_id: int):
        """
            View user bids
        """
        try:
            info = self.__market_facade.view_user_bids(user_id)
            logger.info('view_user_bids was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('view_user_bids was not successful')
            return jsonify({'message': str(e)}), 400
        
    def show_store_bids(self, store_owner_id: int, store_id: int):
        """
            Show store bids
        """
        try:
            info = self.__market_facade.show_store_bids(store_owner_id, store_id)
            logger.info('show_store_bids was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('show_store_bids was not successful')
            return jsonify({'message': str(e)}), 400
        
    def view_all_bids_of_system(self, system_manager_id: int):
        """
            View all bids of the system
        """
        try:
            info = self.__market_facade.view_all_bids_of_system(system_manager_id)
            logger.info('view_all_bids_of_system was successful')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('view_all_bids_of_system was not successful')
            return jsonify({'message': str(e)}), 400
        
        
    def has_store_worker_accepted_bid(self, user_id: int, store_id: int, bid_id: int):
        """
            Has store worker accepted bid
        """
        try:
            info = self.__market_facade.has_store_worker_accepted_bid(user_id,store_id, bid_id)
            logger.info(f'has_store_worker_accepted_bid was successful for user {user_id}')
            return jsonify({'message': info}), 200
        except Exception as e:
            logger.error('has_store_worker_accepted_bid was not successful')
            return jsonify({'message': str(e)}), 400
