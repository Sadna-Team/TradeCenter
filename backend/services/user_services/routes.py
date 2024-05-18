# API endpoints and their corresponding route handlers

from flask import Blueprint, request, jsonify
from backend.business.authentication.authentication import Authentication
from backend.business.user.user import UserFacade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies

auth_bp = Blueprint('auth', __name__)
authentication = Authentication()


@auth_bp.route('/', methods=['GET'])
def start():
    """
                Use Case 1.2:
                Start the application and generate token for guest

                Returns:
                    token (str): token of the guest
    """
    user_token = authentication.start_guest()
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
        authentication.register_user(userid, register_credentials)
        return jsonify({'message': 'User registered successfully - great success'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@auth_bp.route('/login', methods=['POST'])
@jwt_required()
def login():
    data = request.get_json()
    try:
        user_id = get_jwt_identity()
        username = data.get('username')
        password = data.get('password')
        user_token = authentication.login_user(user_id, username, password)
        return jsonify({'message': 'OK', 'token': user_token}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
            Use Case 2.3.1:
            Logout a user

            Data
                token (?): token of the user

            Returns:
                ?
    """
    try:
        jti = get_jwt()['jti']
        authentication.logout_user(jti)
        response = jsonify({'message': 'User logged out successfully'})
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
