# API endpoints and their corresponding route handlers

from flask import Blueprint, request, jsonify
from backend.services.user_services.controllers import AuthenticationService
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)
authentication = AuthenticationService()


# route a default route to the start function
@auth_bp.route('/start', methods=['GET'])
def start():
    user_token = authentication.guest_login()
    if user_token:
        return jsonify({'token': user_token}), 200
    return jsonify({'message': 'App start failed'}), 400


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    token = data.get('token')
    register_credentials = data.get('register_credentials')
    user = AuthenticationService.register(token, register_credentials)
    if user:
        return jsonify({'message': 'User registered successfully'}), 201
    return jsonify({'message': 'Registration failed'}), 400


@auth_bp.route('/login', methods=['POST'])
@jwt_required()
def login():
    data = request.get_json()
    token = data.get('token')
    username = data.get('username')
    password = data.get('password')

    #extract userid from token
    userid = get_jwt_identity()
    print(userid)


    # if token:
    #     return jsonify({'token': token}), 200
    # return jsonify({'message': 'Invalid credentials'}), 401
    return jsonify({'message': 'OK'}), 200


@auth_bp.route('/whoami', methods=['GET'])
def whoami():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]  # Assuming the token is passed as Bearer token
        user = auth_service.get_logged_in_user(token)
        if user:
            return jsonify({'username': user.username, 'email': user.email}), 200
    return jsonify({'message': 'Invalid or expired token'}), 401
