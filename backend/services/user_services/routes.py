# API endpoints and their corresponding route handlers

#-------------logging configuration----------------
from logging_config import setup_logging
import logging

logger = logging.getLogger('myapp')
#---------------------------------------------------

from flask import Blueprint, request, jsonify
from backend.business.authentication.authentication import Authentication
from backend.business.user.user import UserFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies

auth_bp = Blueprint('auth', __name__)
authentication_facade = Authentication()

user_bp = Blueprint('user', __name__)
user_facade = UserFacade()


#---------------------------------------------------------------authentication usecase routes---------------------------------------------------------------


@auth_bp.route('/', methods=['GET'])
def start():
    """
        Use Case 1.2:
        Start the application and generate token for guest

        Returns:
            token (str): token of the guest
    """
    logger.info('recieved request from a guest to enter the app')
    user_token = authentication_facade.start_guest()
    if user_token:
        logger.info('guest entered the app successfully')
        return jsonify({'token': user_token}), 200
    logger.error('start - guest failed to enter the app')
    return jsonify({'message': 'App start failed'}), 400


@auth_bp.route('/register', methods=['POST'])
@jwt_required()
def register():
    """
        Use Case 2.1.3:
        Register a new user

        Data:
            user_id (int): id of the user
            register_credentials (?): credentials of the new user required for registration
    """
    logger.info('recieved request to register a new user')
    data = request.get_json()
    register_credentials = data.get('register_credentials')
    try:
        userid = get_jwt_identity()
        authentication_facade.register_user(userid, register_credentials)
        logger.info('User registered successfully - great success')
        return jsonify({'message': 'User registered successfully - great success'}), 201
    except Exception as e:
        logger.error('register - ' + str(e))
        return jsonify({'message': str(e)}), 400


@user_bp.route('/login', methods=['POST'])
@jwt_required()
def login():
    """
        Use Case 2.1.4:
        Login a user

        Data:
            username (str): the username of the user
            password (str): the password of the user
    """
    logger.info('recieved request to login a user')
    data = request.get_json()
    try:
        if not 'username' in data or not 'password' in data:
            raise ValueError('Missing username or password')
        username = data.get('username')
        password = data.get('password')
        user_token = authentication_facade.login_user(username, password)
        authentication_facade.logout_user(get_jwt()['jti'])
        logger.info('User logged in successfully')
        return jsonify({'message': 'OK', 'token': user_token}), 200
    except Exception as e:
        logger.error('login - ' + str(e))
        return jsonify({'message': str(e)}), 400



@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
        Use Case 2.3.1:
        Logout a user
    """
    logger.info('recieved request to logout a user')
    try:
        jti = get_jwt()['jti']
        user_id = get_jwt_identity()
        authentication_facade.logout_user(jti, user_id)
        response = jsonify({'message': 'User logged out successfully'})
        unset_jwt_cookies(response)
        logger.info('User logged out successfully')
        return response, 200
    except Exception as e:
        logger.error('logout - ' + str(e))
        return jsonify({'message': str(e)}), 400


#---------------------------------------------------------------user usecase routes---------------------------------------------------------------


@user_bp.route('/notifications', methods=['GET'])
@jwt_required()
def show_notifications():
    """
        Use Case 1.5 + 1.6:
        Show notifications for a user which is logged in (member)
    """
    logger.info('recieved request to show notifications to the user')
    try:
        user_id = get_jwt_identity()
        notifications = user_facade.get_notifications(user_id)
        logger.info('sent notifications to the user successfully')
        return jsonify({'notifications': notifications}), 200
    except Exception as e:
        logger.error('show_notifications -- failed ', str(e))
        msg = 'show_notifications - ', str(e)
        return jsonify({'message': msg}), 400


@user_bp.route('/add_to_basket', methods=['POST'])
@jwt_required()
def add_product_to_basket():
    """
        Use Case 2.2.3:
        Add a product to the basket

        Data:
            store_id (int): id of the store
            product_id (int): id of the product to be added to the basket
    """
    logger.info('recieved request to add a product to the basket')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        product_id = data['product_id']
        user_facade.add_product_to_basket(user_id, store_id, product_id)
        logger.info('successfully added product to basket')
        return jsonify({'message': 'successfully added product to basket'}), 200
    except Exception as e:
        logger.error('add_product_to_basket - ', str(e))
        return jsonify({'message': str(e)}), 400


@user_bp.route('/remove_from_basket', methods=['POST'])
@jwt_required()
def remove_product_from_basket():
    """
        Use Case 2.2.4.2:
        Remove a product from the shopping cart

        Data:
            product_id (int): id of the product to be removed from the shopping cart
    """
    logger.info('recieved request to remove a product from the basket')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        product_id = data['product_id']
        user_facade.remove_product_from_cart(user_id, store_id, product_id)
        logger.info('successfully removed the product from the basket')
        return jsonify({'message': 'successfully removed the product from the basket'}), 200
    except Exception as e:
        logger.error('remove_product_from_basket - ', str(e))
        return jsonify({'message': str(e)}), 400


@user_bp.route('/show_cart', methods=['GET'])
@jwt_required()
def show_cart():
    """
        Use Case 2.2.4.1:
        Show the shopping cart of a user
    """
    logger.info('recieved request to show the shopping cart')
    try:
        user_id = get_jwt_identity()
        shopping_cart = user_facade.get_shopping_cart(user_id)
        logger.info('successfully sent the shopping cart')
        return jsonify({'message': shopping_cart}), 200
    except Exception as e:
        logger.error('show_cart - ', str(e))
        return jsonify({'message': str(e)}), 400
