from flask import Blueprint, request, jsonify
from backend.services.ecommerce_services.controllers import PurchaseService
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.error_types import *

# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')
# ---------------------------------------------------

# API endpoints and their corresponding route handlers
market_bp = Blueprint('market', __name__)

purchase_service = PurchaseService()

@market_bp.route('/test', methods=['GET'])
@jwt_required()
def test():
    user_id = get_jwt_identity()
    purchase_service.test(user_id)
    return jsonify({'message': 'test'}), 200

@market_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    """
        Use Case 2.2.5:
        Checkout the shopping cart
    """
    logger.info('recieved request to checkout the shopping cart')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        payment_details_helper = data['payment_details']
        if not isinstance(payment_details_helper, dict):
            raise ServiceLayerError('payment details must be a dictionary', ServiceLayerErrorTypes.payment_details_not_dict)
        payment_details = {str(key): str(value) for key, value in payment_details_helper.items()}

        supply_method = str(data['supply_method'])

        address_helper = data['address']
        if not isinstance(address_helper, dict):
            raise ServiceLayerError('address must be a dictionary', ServiceLayerErrorTypes.address_not_dict)
        address = {str(key): str(value) for key, value in address_helper.items()}
    except Exception as e:
        logger.error('checkout - ', str(e))
        return jsonify({'message': str(e)}), 400

    return purchase_service.checkout(user_id, payment_details, supply_method, address)


@market_bp.route('/store_purchase_history', methods=['GET', 'POST'])
@jwt_required()
def show_store_purchase_history():
    """
        Use Case 2.4.13:
        Show the purchase history in a store
    """
    logger.info('recieved request to show the purchase history of a store')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error('show_store_purchase_history - ', str(e))
        return jsonify({'message': str(e)}), 400

    return purchase_service.show_purchase_history_in_store(user_id, store_id)


@market_bp.route('/user_purchase_history', methods=['POST', 'GET'])
@jwt_required()
def show_user_purchase_history():
    """
        Use Case 2.2.4.13:
        Show the purchase history of a user (if store id is provided, show the purchase history in the store)
    """
    logger.info('recieved request to show the purchase history of a user')
    try:
        actor_id = get_jwt_identity()
        data = request.get_json()
        store_id = None
        if 'store_id' in data:
            store_id = int(data['store_id'])
        user_id = int(data['user_id'])

    except Exception as e:
        logger.error(('show_user_purchase_history - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return purchase_service.show_purchase_history_of_user(actor_id, user_id, store_id)


@market_bp.route('/show_purchase_history', methods=['GET'])
@jwt_required()
def show_purchase_history():
    """
        Use Case
        Show the purchase history of a user
    """
    logger.info('recieved request to show the purchase history of a user')
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        logger.error(('show_purchase_history - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return purchase_service.show_purchase_history_of_user(user_id, user_id)


@market_bp.route('/search_products_by_category', methods=['POST'])
@jwt_required()
def search_products_by_category():
    """
        Use Case 2.2.2.1:
        Search products in the stores
    """
    logger.info('recieved request to search for products')
    try:
        data = request.get_json()
        category_id = int(data['category_id'])
        # check if store_id is provided
        store_id = None
        if 'store_id' in data:
            store_id = int(data['store_id'])
    except Exception as e:
        logger.error('search_products - ', str(e))
        return jsonify({'message': str(e)}), 400

    return purchase_service.search_products_by_category(category_id, store_id)


@market_bp.route('/search_products_by_tags', methods=['POST'])
@jwt_required()
def search_products_by_tags():
    """
        Use Case 2.2.2.1:
        Search products in the stores
    """
    logger.info('recieved request to search for products')
    try:
        logger.info('checkpoint 1')
        data = request.get_json()
        logger.info('data- ', data)
        tags_helper = data.get('tags')
        if not isinstance(tags_helper, list):
            raise ServiceLayerError('tags must be a list', ServiceLayerErrorTypes.tags_not_list)
        tags = [str(tag) for tag in tags_helper]
        # check if store_id is provided
        if 'store_id' in data:
            store_id = int(data.get('store_id'))
        else:
            store_id = None
    except Exception as e:
        logger.error('search_products - ', str(e))
        return jsonify({'message': str(e)}), 400

    return purchase_service.search_products_by_tags(tags, store_id)


@market_bp.route('/search_products_by_name', methods=['POST'])
@jwt_required()
def search_products_by_name():
    """
        Use Case 2.2.2.1:
        Search products in the stores
    """
    logger.info('received request to search for products')
    try:
        data = request.get_json()
        name = str(data['name'])
        # check if store_id is provided
        if 'store_id' in data:
            store_id = int(data['store_id'])
        else:
            store_id = None
    except Exception as e:
        logger.error('search_products - ', str(e))
        return jsonify({'message': str(e)}), 400

    return purchase_service.search_products_by_name(name, store_id)


'''@market_bp.route('/search_store_products', methods=['GET'])
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
        storeId = data['store_id']
        name = data['name']
        sortType = data['sortType']
        market_facade.search_product_in_store(storeId, name, sortType)
        logger.info('search successful')
        return jsonify({'message': 'searched products'}), 200
    except Exception as e:
        logger.error('search_store_products - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/add_store_rating', methods=['POST'])
@jwt_required()
def add_store_rating():
    """
        Use Case :
        Add a rating to a store 2.2.3.4

        Data:
            user_id (int): id of the user
            purchase_id (int): id of the purchase related to the rating
            description (str): description of the rating
            rating (float): rating to add
    """
    logger.info('recieved request to add a rating to a store')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        purchase_id = data['purchase_id']
        description = data['description']
        rating = data['rating']
        market_facade.add_store_rating(user_id, purchase_id, description, rating)
        logger.info('rating added')
        return jsonify({'message': 'rating added'}), 200
    except Exception as e:
        logger.error('add_store_rating - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/add_product_rating', methods=['POST'])
@jwt_required()
def add_product_rating():
    """
        Use Case :
        Add a rating to a product 2.2.3.4

        Data:
            user_id (int): id of the user
            purchase_id (int): id of the purchase related to the rating
            description (str): description of the rating
            product_id (int): id of the product
            rating (float): rating to add
    """
    logger.info('recieved request to add a rating to a product')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        purchase_id = data['purchase_id']
        description = data['description']
        product_id = data['product_id']
        rating = data['rating']
        market_facade.add_product_rating(user_id, purchase_id, description, product_id, rating)
        logger.info('rating added')
        return jsonify({'message': 'rating added'}), 200
    except Exception as e:
        logger.error('add_product_rating - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/create_bid', methods=['POST'])
@jwt_required()
def create_bid():
    """
        Use Case:
        Create a bid on a product

        Data:
            user_id (int): id of the user
            proposed_price (float): proposed price of the bid
            product_id (int): id of the product
            store_id (int): id of the store
    """
    logger.info('recieved request to create a bid')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        proposed_price = data['proposed_price']
        product_id = data['product_id']
        store_id = data['store_id']
        market_facade.create_bid_purchase(user_id, proposed_price, product_id, store_id)
        logger.info('bid created')
        return jsonify({'message': 'bid created'}), 200
    except Exception as e:
        logger.error('create_bid - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/create_auction', methods=['POST'])
@jwt_required()
def create_auction():
    """
        Use Case:
        Create an auction on a product

        Data:
            user_id (int): id of the user
            basePrice (float): based price of the auction
            startingDate (datetime): starting date of the auction
            endingDate (datetime): ending date of the auction
            store_id (int): id of the store
            product_id (int): id of the product
    """
    logger.info('recieved request to create an auction')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        basePrice = data['basePrice']
        startingDate = data['startingDate']
        endingDate = data['endingDate']
        store_id = data['store_id']
        product_id = data['product_id']
        market_facade.create_auction_purchase(user_id, basePrice, startingDate, endingDate, store_id, product_id)
        logger.info('auction created')
        return jsonify({'message': 'auction created'}), 200
    except Exception as e:
        logger.error('create_auction - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/create_lottery', methods=['POST'])
@jwt_required()
def create_lottery():
    """
        Use Case:
        Create a lottery on a product

        Data:
            user_id (int): id of the user
            fullPrice (float): price of the lottery
            store_id (int): id of the store
            product_id (int): id of the product
            startingDate (datetime): starting date of the lottery
            endingDate (datetime): ending date of the lottery
    """
    logger.info('recieved request to create a lottery')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        fullPrice = data['fullPrice']
        store_id = data['store_id']
        product_id = data['product_id']
        startingDate = data['startingDate']
        endingDate = data['endingDate']
        market_facade.create_lottery_purchase(user_id, fullPrice, store_id, product_id, startingDate, endingDate)
        logger.info('lottery created')
        return jsonify({'message': 'lottery created'}), 200
    except Exception as e:
        logger.error('create_lottery - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/handle_accepted_purchases', methods=['POST'])
@jwt_required()
def handle_accepted_purchase():
    """
        Use Case:
        Handle accepted purchases

        Data:
            None
    """
    logger.info('recieved request to handle an accepted purchase')
    try:
        market_facade.handle_accepted_purchases()
        logger.info('purchase handled')
        return jsonify({'message': 'purchase handled'}), 200
    except Exception as e:
        logger.error('handle_accepted_purchase - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/store_accept_offer', methods=['POST'])
@jwt_required()
def store_accept_offer():
    """
        Use Case:
        Store accepts an offer

        Data:
            purchase_id (int): id of the purchase
    """
    logger.info('recieved request for a store to accept an offer')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        purchase_id = data['purchase_id']
        market_facade.store_accept_offer(purchase_id)
        logger.info('offer accepted')
        return jsonify({'message': 'offer accepted'}), 200
    except Exception as e:
        logger.error('store_accept_offer - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/store_decline_offer', methods=['POST'])
@jwt_required()
def store_decline_offer():
    """
        Use Case:
        Store declines an offer

        Data:
            purchase_id (int): id of the purchase
    """
    logger.info('recieved request for a store to decline an offer')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        purchase_id = data['purchase_id']
        market_facade.store_reject_offer(purchase_id)
        logger.info('offer declined')
        return jsonify({'message': 'offer declined'}), 200
    except Exception as e:
        logger.error('store_decline_offer - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/store_counter_offer', methods=['POST'])
@jwt_required()
def store_counter_offer():
    """
        Use Case:
        Store counters an offer

        Data:
            purchase_id (int): id of the purchase
            proposedPrice (float): proposed price of the counter offer
    """
    logger.info('recieved request for a store to counter an offer')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        purchase_id = data['purchase_id']
        proposedPrice = data['proposedPrice']
        market_facade.store_counter_offer(proposedPrice, purchase_id)
        logger.info('offer countered')
        return jsonify({'message': 'offer countered'}), 200
    except Exception as e:
        logger.error('store_counter_offer - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/user_accept_offer', methods=['POST'])
@jwt_required()
def user_accept_offer():
    """
        Use Case:
        User accepts an offer

        Data:
            user_id (int): id of the user
            purchase_id (int): id of the purchase
    """
    logger.info('recieved request for a user to accept an offer')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        purchase_id = data['purchase_id']
        market_facade.user_accept_offer(user_id, purchase_id)
        logger.info('offer accepted')
        return jsonify({'message': 'offer accepted'}), 200
    except Exception as e:
        logger.error('user_accept_offer - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/user_decline_offer', methods=['POST'])
@jwt_required()
def user_decline_offer():
    """
        Use Case:
        User declines an offer

        Data:
            user_id (int): id of the user
            purchase_id (int): id of the purchase
    """
    logger.info('recieved request for a user to decline an offer')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        purchase_id = data['purchase_id']
        market_facade.user_reject_offer(user_id, purchase_id)
        logger.info('offer declined')
        return jsonify({'message': 'offer declined'}), 200
    except Exception as e:
        logger.error('user_decline_offer - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/user_counter_offer', methods=['POST'])
@jwt_required()
def user_counter_offer():
    """
        Use Case:
        User counters an offer

        Data:
            user_id (int): id of the user
            purchase_id (int): id of the purchase
            proposedPrice (float): proposed price of the counter offer
    """
    logger.info('recieved request for a user to counter an offer')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        purchase_id = data['purchase_id']
        proposedPrice = data['proposedPrice']
        market_facade.user_counter_offer(user_id, proposedPrice, purchase_id)
        logger.info('offer countered')
        return jsonify({'message': 'offer countered'}), 200
    except Exception as e:
        logger.error('user_counter_offer - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/user_auction_bid', methods=['POST'])
@jwt_required()
def user_auction_bid():
    """
        Use Case:
        User bids on an auction

        Data:
            user_id (int): id of the user
            purchase_id (int): id of the purchase
            proposedPrice (float): proposed price of the bid
    """
    logger.info('recieved request for a user to bid on an auction')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        purchase_id = data['purchase_id']
        proposedPrice = data['proposedPrice']
        market_facade.add_auction_bid(purchase_id, user_id, proposedPrice)
        logger.info('bid placed')
        return jsonify({'message': 'bid placed'}), 200
    except Exception as e:
        logger.error('user_auction_bid - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/view_highest_bid', methods=['POST'])
@jwt_required()
def view_highest_bid():
    """
        Use Case:
        View the highest bid on an auction

        Data:
            user_id (int): id of the user
            purchase_id (int): id of the purchase
    """
    logger.info('recieved request to view the highest bid on an auction')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        purchase_id = data['purchase_id']
        bid = market_facade.view_highest_bid(purchase_id, user_id)
        logger.info('bid sent')
        return jsonify({'message': bid}), 200
    except Exception as e:
        logger.error('view_highest_bid - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/calculate_remaining_time_of_auction', methods=['POST'])
@jwt_required()
def calculate_remaining_time_of_auction():
    """
        Use Case:
        Calculate the remaining time of an auction

        Data:
            user_id (int): id of the user
            purchase_id (int): id of the purchase
    """
    logger.info('recieved request to calculate the remaining time of an auction')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        purchase_id = data['purchase_id']
        time = market_facade.calculate_remaining_time_of_auction(purchase_id, user_id)
        logger.info('time sent')
        return jsonify({'message': time}), 200
    except Exception as e:
        logger.error('calculate_remaining_time_of_auction - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/handle_ongoing_auctions', methods=['POST'])
@jwt_required()
def handle_ongoing_auctions():
    """
        Use Case:
        Handle ongoing auctions

        Data: none
    """
    logger.info('recieved request to handle ongoing auctions')
    try:
        user_id = get_jwt_identity()
        market_facade.handle_ongoing_auctions()
        logger.info('auctions handled')
        return jsonify({'message': 'auctions handled'}), 200
    except Exception as e:
        logger.error('handle_ongoing_auctions - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/add_lottery_ticket', methods=['POST'])
@jwt_required()
def add_lottery_ticket():
    """
        Use Case:
        Add a lottery ticket

        Data:
            user_id (int): id of the user
            proposed_price (float): proposed price of the bid
            purchase_id (int): id of the purchase
    """
    logger.info('recieved request to add a lottery ticket')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        proposed_price = data['proposed_price']
        purchase_id = data['purchase_id']
        market_facade.add_lottery_offer(user_id, proposed_price, purchase_id)
        logger.info('ticket added')
        return jsonify({'message': 'ticket added'}), 200
    except Exception as e:
        logger.error('add_lottery_ticket - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/calculate_remaining_time_of_lottery', methods=['POST'])
@jwt_required()
def calculate_remaining_time_of_lottery():
    """
        Use Case:
        Calculate the remaining time of a lottery

        Data:
            user_id (int): id of the user
            purchase_id (int): id of the purchase
    """
    logger.info('recieved request to calculate the remaining time of a lottery')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        purchase_id = data['purchase_id']
        time = market_facade.calculate_remaining_time_of_lottery(purchase_id, user_id)
        logger.info('time sent')
        return jsonify({'message': time}), 200
    except Exception as e:
        logger.error('calculate_remaining_time_of_lottery - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/calculate_probability_of_user', methods=['POST'])
@jwt_required()
def calculate_probability_of_user():
    """
        Use Case:
        Calculate the probability of a user winning a lottery

        Data:
            user_id (int): id of the user
            purchase_id (int): id of the purchase
    """
    logger.info('recieved request to calculate the probability of a user winning a lottery')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        purchase_id = data['purchase_id']
        probability = market_facade.calculate_probability_of_user(purchase_id, user_id)
        logger.info('probability sent')
        return jsonify({'message': probability}), 200
    except Exception as e:
        logger.error('calculate_probability_of_user - ', str(e))
        return jsonify({'message': str(e)}), 400'''

'''@market_bp.route('/handle_ongoing_lotteries', methods=['POST'])
@jwt_required()
def handle_ongoing_lotteries():
    """
        Use Case:
        Handle ongoing lotteries

        Data: none
    """
    logger.info('recieved request to handle ongoing lotteries')
    try:
        user_id = get_jwt_identity()
        market_facade.handle_ongoing_lotteries()
        logger.info('lotteries handled')
        return jsonify({'message': 'lotteries handled'}), 200
    except Exception as e:
        logger.error('handle_ongoing_lotteries - ', str(e))
        return jsonify({'message': str(e)}), 400'''

@market_bp.route('/get_store_role', methods=['POST'])
@jwt_required()
def get_store_role():
    logger.info('recieved request to get the role of a store')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error('get_store_role - ', str(e))
        return jsonify({'message': str(e)}), 400
    return purchase_service.get_store_role(user_id, store_id)

@market_bp.route('/get_user_stores', methods=['GET'])
@jwt_required()
def get_user_stores():
    logger.info('recieved request to get the stores of a user')
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        logger.error('get_user_stores - ', str(e))
        return jsonify({'message': str(e)}), 400
    return purchase_service.get_user_stores(user_id)