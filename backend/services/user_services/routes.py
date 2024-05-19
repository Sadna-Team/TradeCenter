# API endpoints and their corresponding route handlers

from flask import Blueprint, request, jsonify
#from backend.business.authentication.authentication import Authentication
#from backend.business.user.user import UserFacade
from .controllers import UserService, AuthenticationService

from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies

auth_bp = Blueprint('auth', __name__)
authentication = AuthenticationService()

user_bp = Blueprint('user', __name__)
user_facade = UserService()


#---------------------------------------------------------------authentication usecase routes---------------------------------------------------------------


@auth_bp.route('/', methods=['GET'])
def start():
    """
                Use Case 1.2:
                Start the application and generate token for guest

                Returns:
                    token (str): token of the guest
    """
    user_token = authentication.guest_login()
    if user_token:
        return jsonify({'token': user_token}), 200
    return jsonify({'message': 'App start failed'}), 400


@auth_bp.route('/register', methods=['POST'])
@jwt_required()
def register():
    """
                Use Case 2.1.4:
                Login a user

                Data:
                    token (?): token of the user
                    user_credentials (?): credentials of the user required for login

                Returns:
                    great success
    """
    data = request.get_json()
    userid = get_jwt_identity()
    register_credentials = data.get('register_credentials')
    try:
        authentication.register(userid, register_credentials)
        return jsonify({'message': 'User registered successfully - great success'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@user_bp.route('/', methods=['POST'])
@jwt_required()
def login():
    data = request.get_json()
    try:
        user_id = get_jwt_identity()
        """username = data.get('username')
        password = data.get('password')"""
        user_token = authentication.login(user_id, data)
        return jsonify({'message': 'OK', 'token': user_token}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@auth_bp.route('/', methods=['POST'])
@jwt_required()
def logout():
    """
            Use Case 2.3.1:
            Logout a user

            Returns:
                ?
    """
    try:
        jti = get_jwt()['jti']
        authentication.logout(jti)
        response = jsonify({'message': 'User logged out successfully'})
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


#---------------------------------------------------------------user usecase routes---------------------------------------------------------------


@user_bp.route('/', methods=['GET'])
@jwt_required()
def show_stores_info():
    """
                Use Case 2.2.1.1:
                recieve information about the stores in the market

                Returns:
                    data (str): info about the stores
    """
    user_id = get_jwt_identity()
    if user_id:
        #TODO: store facade returns default stores info
        info = ""
        return jsonify({'info': info}), 200
    return jsonify({'message': 'show_stores_info -- failed'}), 400


