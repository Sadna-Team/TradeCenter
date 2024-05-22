from flask import Blueprint, request, jsonify
from backend.business.market import MarketFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies


#-------------logging configuration----------------
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
    logger.info('received request to change permissions')
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


@market_bp.route('/search_products_by_category', methods=['GET'])
@jwt_required()
def search_products():
    """
        Use Case 2.2.2.1:
        Search products in the stores

        Data:
            categoryId (int): id of the category
            sortType (str): type of sorting (1 being price low to high, 2 being price high to low, 3 being rating high to low, 4 being rating low to high)
    """
    logger.info('recieved request to search for products')
    try:
        user_id = get_jwt_identity()
        data = request.args
        categoryId = data['categoryId']
        sortType = data['sortType']
        market_facade.searchByCategory(categoryId, sortType)
        logger.info('search successful')
        return jsonify({'message': 'searched products'}), 200
    except Exception as e:
        logger.error('search_products - ', str(e))
        return jsonify({'message': str(e)}), 400
    
    
@market_bp.route('/search_products_by_tags', methods=['GET'])
@jwt_required()
def search_products():
    """
        Use Case 2.2.2.1:
        Search products in the stores

        Data:
            tags (list): tags to search for products
            sortType (str): type of sorting (1 being price low to high, 2 being price high to low, 3 being rating high to low, 4 being rating low to high)
    """
    logger.info('recieved request to search for products')
    try:
        user_id = get_jwt_identity()
        data = request.args
        tags = data['tags']
        sortType = data['sortType']
        market_facade.searchByTags(tags, sortType)
        logger.info('search successful')
        return jsonify({'message': 'searched products'}), 200
    except Exception as e:
        logger.error('search_products - ', str(e))
        return jsonify({'message': str(e)}), 400

@market_bp.route('/search_products_by_name', methods=['GET'])
@jwt_required()
def search_products():
    """
        Use Case 2.2.2.1:
        Search products in the stores

        Data:
            name (str): name of the product
            sortType (str): type of sorting (1 being price low to high, 2 being price high to low, 3 being rating high to low, 4 being rating low to high)
    """
    logger.info('recieved request to search for products')
    try:
        user_id = get_jwt_identity()
        data = request.args
        name = data['name']
        sortType = data['sortType']
        market_facade.searchByName(name, sortType)
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
        storeId = data['store_id']
        name = data['name']
        sortType = data['sortType']
        market_facade.searchStoreProducts(storeId, name, sortType)
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
            user_id (int): id of the user
            store_id (int): id of the store
    """
    logger.info('recieved request to show the purchase history of a store')
    try:
        user_id = get_jwt_identity()
        data = request.args
        store_id = data['store_id']
        history = market_facade.viewPurchasesOfStore(user_id, store_id)
        logger.info('purchase history sent')
        return jsonify({'message': history}), 200
    except Exception as e:
        logger.error('show_store_purchase_history - ', str(e))
        return jsonify({'message': str(e)}), 400



@market_bp.route('/user_purchase_history_in_store', methods=['GET'])
@jwt_required()
def show_user_purchase_history_in_store():
    """
        Use Case 2.2.4.13:
        Show the purchase history of a user in a store

        Data:
            user_id (int): id of the user
            store_id (int): id of the store
    """
    logger.info('recieved request to show the purchase history of a user in a store')
    try:
        user_id = get_jwt_identity()
        data = request.args
        store_id = data['store_id']
        history = market_facade.viewPurchasesOfUserInStore(user_id, store_id)
        logger.info('purchase history sent')
        return jsonify({'message': history}), 200
    except Exception as e:
        logger.error('show_user_purchase_history_in_store - ', str(e))
        return jsonify({'message': str(e)}), 400



@market_bp.route('/member_purchase_history', methods=['GET'])
@jwt_required() 
def show_member_purchase_history():
    """
        Use Case 2.6.4:
        Show the purchase history of a member
        
        Data: 
            user_id (int): id of the user
    """
    logger.info('recieved request to show the purchase history of a member')
    try:
        user_id = get_jwt_identity()
        history =  market_facade.viewPurchasesOfUser(user_id)
        logger.info('purchase history sent')
        return jsonify({'message': history}), 200
    except Exception as e:
        logger.error('show_member_purchase_history - ', str(e))
        return jsonify({'message': str(e)}), 400
    
    
@market_bp.route('/add_store_rating', methods=['POST'])
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
        market_facade.addStoreRating(user_id, purchase_id, description, rating)
        logger.info('rating added')
        return jsonify({'message': 'rating added'}), 200
    except Exception as e:
        logger.error('add_store_rating - ', str(e))
        return jsonify({'message': str(e)}), 400
    
    
    
@market_bp.route('/add_product_rating', methods=['POST'])
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
        market_facade.addProductRating(user_id, purchase_id, description, product_id, rating)
        logger.info('rating added')
        return jsonify({'message': 'rating added'}), 200
    except Exception as e:
        logger.error('add_product_rating - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@market_bp.route('/create_bid', methods=['POST'])
@jwt_required()
def create_bid():
    """
        Use Case:
        Create a bid on a product

        Data:
            user_id (int): id of the user
            proposedPrice (float): proposed price of the bid
            product_id (int): id of the product
            store_id (int): id of the store
    """
    logger.info('recieved request to create a bid')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        proposedPrice = data['proposedPrice']
        product_id = data['product_id']
        store_id = data['store_id']
        market_facade.createBidPurchase(user_id, proposedPrice, product_id, store_id)
        logger.info('bid created')
        return jsonify({'message': 'bid created'}), 200
    except Exception as e:
        logger.error('create_bid - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@market_bp.route('/create_auction', methods=['POST'])
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
        market_facade.createAuctionPurchase(user_id, basePrice, startingDate, endingDate, store_id, product_id)
        logger.info('auction created')
        return jsonify({'message': 'auction created'}), 200
    except Exception as e:
        logger.error('create_auction - ', str(e))
        return jsonify({'message': str(e)}), 400


@market_bp.route('/create_lottery', methods=['POST'])
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
        market_facade.createLotteryPurchase(user_id, fullPrice, store_id, product_id, startingDate, endingDate)
        logger.info('lottery created')
        return jsonify({'message': 'lottery created'}), 200
    except Exception as e:
        logger.error('create_lottery - ', str(e))
        return jsonify({'message': str(e)}), 400


@market_bp.route('/handle_accepted_purchases', methods=['POST'])
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
        market_facade.handleAcceptedPurchase()
        logger.info('purchase handled')
        return jsonify({'message': 'purchase handled'}), 200
    except Exception as e:
        logger.error('handle_accepted_purchase - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@market_bp.route('/store_accept_offer', methods=['POST'])
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
        market_facade.storeAcceptOffer(purchase_id)
        logger.info('offer accepted')
        return jsonify({'message': 'offer accepted'}), 200
    except Exception as e:
        logger.error('store_accept_offer - ', str(e))
        return jsonify({'message': str(e)}), 400

@market_bp.route('/store_decline_offer', methods=['POST'])
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
        market_facade.storeRejectOffer(purchase_id)
        logger.info('offer declined')
        return jsonify({'message': 'offer declined'}), 200
    except Exception as e:
        logger.error('store_decline_offer - ', str(e))
        return jsonify({'message': str(e)}), 400
    
@market_bp.route('/store_counter_offer', methods=['POST'])
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
        market_facade.storeCounterOffer(proposedPrice,purchase_id)
        logger.info('offer countered')
        return jsonify({'message': 'offer countered'}), 200
    except Exception as e:
        logger.error('store_counter_offer - ', str(e))
        return jsonify({'message': str(e)}), 400
    
    
@market_bp.route('/user_accept_offer', methods=['POST'])
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
        market_facade.userAcceptOffer(user_id, purchase_id)
        logger.info('offer accepted')
        return jsonify({'message': 'offer accepted'}), 200
    except Exception as e:
        logger.error('user_accept_offer - ', str(e))
        return jsonify({'message': str(e)}), 400
 
    
@market_bp.route('/user_decline_offer', methods=['POST'])
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
        market_facade.userRejectOffer(user_id, purchase_id)
        logger.info('offer declined')
        return jsonify({'message': 'offer declined'}), 200
    except Exception as e:
        logger.error('user_decline_offer - ', str(e))
        return jsonify({'message': str(e)}), 400

@market_bp.route('/user_counter_offer', methods=['POST'])
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
        market_facade.userCounterOffer(user_id, proposedPrice, purchase_id)
        logger.info('offer countered')
        return jsonify({'message': 'offer countered'}), 200
    except Exception as e:
        logger.error('user_counter_offer - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@market_bp.route('/user_auction_bid', methods=['POST'])
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
        market_facade.addAuctionBid(purchase_id, user_id, proposedPrice)
        logger.info('bid placed')
        return jsonify({'message': 'bid placed'}), 200
    except Exception as e:
        logger.error('user_auction_bid - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@market_bp.route('/view_highest_bid', methods=['POST'])
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
        bid = market_facade.viewHighestBid(purchase_id, user_id)
        logger.info('bid sent')
        return jsonify({'message': bid}), 200
    except Exception as e:
        logger.error('view_highest_bid - ', str(e))
        return jsonify({'message': str(e)}), 400
    


@market_bp.route('/calculate_remaining_time_of_auction', methods=['POST'])
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
        time = market_facade.calculateRemainingTimeOfAuction(purchase_id, user_id)
        logger.info('time sent')
        return jsonify({'message': time}), 200
    except Exception as e:
        logger.error('calculate_remaining_time_of_auction - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@market_bp.route('/handle_ongoing_auctions', methods=['POST'])
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
        market_facade.handleOngoingAuctions()
        logger.info('auctions handled')
        return jsonify({'message': 'auctions handled'}), 200
    except Exception as e:
        logger.error('handle_ongoing_auctions - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@market_bp.route('/add_lottery_ticket', methods=['POST'])
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
        proposedPrice = data['proposedPrice']
        purchase_id = data['purchase_id']
        market_facade.addLotteryTicket(user_id, proposedPrice , purchase_id)
        logger.info('ticket added')
        return jsonify({'message': 'ticket added'}), 200
    except Exception as e:
        logger.error('add_lottery_ticket - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@market_bp.route('/calculate_remaining_time_of_lottery', methods=['POST'])
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
        time = market_facade.calculateRemainingTimeOfLottery(purchase_id, user_id)
        logger.info('time sent')
        return jsonify({'message': time}), 200
    except Exception as e:
        logger.error('calculate_remaining_time_of_lottery - ', str(e))
        return jsonify({'message': str(e)}), 400
    
    
@market_bp.route('/calculate_probability_of_user', methods=['POST'])
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
        probability = market_facade.calculateProbabilityOfUser(purchase_id, user_id)
        logger.info('probability sent')
        return jsonify({'message': probability}), 200
    except Exception as e:
        logger.error('calculate_probability_of_user - ', str(e))
        return jsonify({'message': str(e)}), 400
    

@market_bp.route('/handle_ongoing_lotteries', methods=['POST'])
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
        market_facade.handleOngoingLotteries()
        logger.info('lotteries handled')
        return jsonify({'message': 'lotteries handled'}), 200
    except Exception as e:
        logger.error('handle_ongoing_lotteries - ', str(e))
        return jsonify({'message': str(e)}), 400
