# API endpoints and their corresponding route handlers

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
    user_token = authentication_facade.start_guest()
    if user_token:
        return jsonify({'token': user_token}), 200
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

        Returns:
            ?
    """
    data = request.get_json()
    register_credentials = data.get('register_credentials')
    try:
        userid = get_jwt_identity()
        authentication_facade.register_user(userid, register_credentials)
        return jsonify({'message': 'User registered successfully - great success'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@user_bp.route('/login', methods=['POST'])
@jwt_required()
def login():
    """
        Use Case 2.1.4:
        Login a user

        Data:
            username ()str: the username of the user
            password (str): the password of the user

        Returns:
            session_token (?): token of the session
    """
    data = request.get_json()
    try:
        username = data.get('username')
        password = data.get('password')
        user_token = authentication_facade.login_user(username, password)
        authentication_facade.logout_user(get_jwt()['jti'])
        return jsonify({'message': 'OK', 'token': user_token}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
        Use Case 2.3.1:
        Logout a user

        Data:
            token_jti (?): token_jti of the user

        Returns:
            ?
    """
    try:
        jti = get_jwt()['jti']
        authentication_facade.logout_user(jti)
        response = jsonify({'message': 'User logged out successfully'})
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


#---------------------------------------------------------------user usecase routes---------------------------------------------------------------


@user_bp.route('/notifications', methods=['GET'])
@jwt_required()
def show_notifications():
    try:
        user_id = get_jwt_identity()
        notifications = user_facade.get_notifications(user_id)
        return jsonify({'notifications': notifications}), 200
    except:
        return jsonify({'message': 'show_notifications -- failed'}), 400


@user_bp.route('/add_to_basket', methods=['POST'])
@jwt_required()
def add_product_to_basket():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        product_id = data['product_id']
        user_facade.add_product_to_basket(user_id, store_id, product_id)
        return jsonify({'message': 'successfully added product to basket'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@user_bp.route('/remove_from_basket', methods=['POST'])
@jwt_required()
def remove_product_from_basket():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = data['store_id']
        product_id = data['product_id']
        user_facade.remove_product_from_cart(user_id, store_id, product_id)
        return jsonify({'message': 'successfully removed the product from the basket'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@user_bp.route('/show_cart', methods=['GET'])
@jwt_required()
def show_cart():
    try:
        user_id = get_jwt_identity()
        shopping_cart = user_facade.get_shopping_cart(user_id)
        return jsonify({'message': shopping_cart}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
