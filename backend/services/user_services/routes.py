# API endpoints and their corresponding route handlers

# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')
# ---------------------------------------------------

from flask import Blueprint, request, jsonify
from backend.services.user_services.controllers import AuthenticationService, UserService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies

auth_bp = Blueprint('auth', __name__)
authentication_service = AuthenticationService()

user_bp = Blueprint('user', __name__)
user_service = UserService()


# ---------------------------------------------------------------authentication usecase
# routes---------------------------------------------------------------


@auth_bp.route('/', methods=['GET'])
def start():
    """
        Use Case 1.2:
        Start the application and generate token for guest

        Returns:
            token (str): token of the guest
    """
    logger.info('recieved request from a guest to enter the app')
    return authentication_service.start_guest()


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
    logger.info('received request to register a new user')
    try:
        data = request.get_json()
        register_credentials = data.get('register_credentials')
        userid = get_jwt_identity()

    except Exception as e:
        logger.error('register - ' + str(e))
        return jsonify({'message': str(e)}), 400

    return authentication_service.register(userid, register_credentials)


@auth_bp.route('/login', methods=['POST'])
@jwt_required()
def login():
    """
        Use Case 2.1.4:
        Login a user

        Data:
            username (str): the username of the user
            password (str): the password of the user
    """
    logger.info('received request to login a user')
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    except Exception as e:
        logger.error(('login - ' + str(e)))
        return jsonify({'message': str(e)}), 400
    return authentication_service.login(username, password)


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
    except Exception as e:
        logger.error('logout - ' + str(e))
        return jsonify({'message': str(e)}), 400
    return authentication_service.logout(jti, user_id)


@auth_bp.route('/logout_guest', methods=['POST'])
@jwt_required()
def logout_guest():
    """
        Use Case 2.1.2:
        Logout a guest
    """
    logger.info('received request to logout a guest')
    try:
        jti = get_jwt()['jti']
        user_id = get_jwt_identity()
    except Exception as e:
        logger.error('logout_guest - ' + str(e))
        return jsonify({'message': str(e)}), 400
    return authentication_service.logout_guest(jti, user_id)


# ---------------------------------------------------------------user usecase routes---------------------------------------------------------------


@user_bp.route('/notifications', methods=['GET'])
@jwt_required()
def show_notifications():
    """
        Use Case 1.5 + 1.6:
        Show notifications for a user which is logged in (member)
    """
    logger.info('received request to show notifications to the user')
    try:
        user_id = get_jwt_identity()

    except Exception as e:
        logger.error('show_notifications - ' + str(e))
        return jsonify({'message': str(e)}), 400
    return user_service.show_notifications(user_id)


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
    logger.info('received request to add a product to the basket')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
        quantity = int(data['quantity'])

    except Exception as e:
        logger.error('add_product_to_basket - ' + str(e))
        return jsonify({'message': str(e)}), 400

    return user_service.add_product_to_basket(user_id, store_id, product_id, quantity)


@user_bp.route('/remove_from_basket', methods=['POST'])
@jwt_required()
def remove_product_from_basket():
    """
        Use Case 2.2.4.2:
        Remove a product from the shopping cart

        Data:
            product_id (int): id of the product to be removed from the shopping cart
    """
    logger.info('received request to remove a product from the basket')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
        product_id = int(data['product_id'])
        quantity = int(data['quantity'])
    except Exception as e:
        logger.error('remove_product_from_basket - ', str(e))
        return jsonify({'message': str(e)}), 400
    return user_service.remove_product_from_basket(user_id, store_id, product_id, quantity)


@user_bp.route('/show_cart', methods=['GET'])
@jwt_required()
def show_cart():
    """
        Use Case 2.2.4.1:
        Show the shopping cart of a user
    """
    userid = get_jwt_identity()
    logger.info(f"user {userid} requested to show his cart")
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        logger.error('show_cart - ', str(e))
        return jsonify({'message': str(e)}), 400
    ans = user_service.show_shopping_cart(user_id)
    return ans

@user_bp.route('/set_cart', methods=['POST'])
@jwt_required()
def set_cart():
    """
        Set the shopping cart of a user
    """
    userid = get_jwt_identity()
    logger.info(f"user {userid} requested to set his cart")
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        cart = data['cart']
        logger.info(f"cart: {cart}")
    except Exception as e:
        logger.error('set_cart - ', str(e))
        return jsonify({'message': str(e)}), 400
    ans = user_service.set_shopping_cart(user_id, cart)
    return ans


@user_bp.route('/accept_promotion', methods=['POST'])
@jwt_required()
def accept_promotion():
    """
        Use Case 2.4.6:
        Accept a promotion

        Data:
            promotion_id (int): id of the promotion
    """
    logger.info('received request to accept a promotion')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        promotion_id = int(data['promotion_id'])
        accept = bool(data['accept'])
    except Exception as e:
        logger.error('accept_promotion - ', str(e))
        return jsonify({'message': str(e)}), 400
    return user_service.accept_promotion(user_id, promotion_id, accept)


@user_bp.route('/is_system_manager', methods=['GET'])
@jwt_required()
def is_system_manager():
    logger.info('received request to check if the user is a system manager')
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        logger.error(('is_system_manager - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return user_service.is_system_manager(user_id)


@user_bp.route('/is_store_owner', methods=['POST', 'GET'])
@jwt_required()
def is_store_owner():
    logger.info('received request to check if the user is a store owner')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error(('is_system_manager - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return user_service.is_store_owner(user_id, store_id)


@user_bp.route('/is_store_manager', methods=['POST', 'GET'])
@jwt_required()
def is_store_manager():
    logger.info('received request to check if the user is a store manager')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error(('is_system_manager - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return user_service.is_store_manager(user_id, store_id)


@user_bp.route('/has_add_product_permission', methods=['POST', 'GET'])
@jwt_required()
def has_add_product_permission():
    logger.info('received request to check if the user has add product permission')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error(('has_add_product_permission - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return user_service.has_add_product_permission(user_id, store_id)


@user_bp.route('/has_change_purchase_policy_permission', methods=['POST', 'GET'])
@jwt_required()
def has_change_purchase_policy_permission():
    logger.info('received request to check if the user has change purchase policy permission')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error(('has_change_purchase_policy_permission - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return user_service.has_change_purchase_policy_permission(user_id, store_id)


@user_bp.route('/has_change_purchase_types_permission', methods=['POST', 'GET'])
@jwt_required()
def has_change_purchase_types_permission():
    logger.info('received request to check if the user has change purchase types permission')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error(('has_change_purchase_types_permission - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return user_service.has_change_purchase_types_permission(user_id, store_id)


@user_bp.route('/has_change_discount_policy_permission', methods=['POST', 'GET'])
@jwt_required()
def has_change_discount_policy_permission():
    logger.info('received request to check if the user has change discount policy permission')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error(('has_change_discount_policy_permission - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return user_service.has_change_discount_policy_permission(user_id, store_id)


@user_bp.route('/has_change_discount_types_permission', methods=['POST', 'GET'])
@jwt_required()
def has_change_discount_types_permission():
    logger.info('received request to check if the user has change discount types permission')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error(('has_change_discount_types_permission - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return user_service.has_change_discount_types_permission(user_id, store_id)


@user_bp.route('/has_add_manager_permission', methods=['POST', 'GET'])
@jwt_required()
def has_add_manager_permission():
    logger.info('received request to check if the user has add manager permission')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error(('has_add_manager_permission - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return user_service.has_add_manager_permission(user_id, store_id)


@user_bp.route('/has_get_bid_permission', methods=['POST', 'GET'])
@jwt_required()
def has_get_bid_permission():
    logger.info('received request to check if the user has get bid permission')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error(('has_get_bid_permission - ', str(e)))
        return jsonify({'message': str(e)}), 400

    return user_service.has_get_bid_permission(user_id, store_id)


@user_bp.route('/add_system_manager', methods=['GET'])
@jwt_required()
def add_system_manager():
    logger.info('received request to add a system manager')
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        username = str(data['username'])
    except Exception as e:
        logger.error('add_system_manager - ', str(e))
        return jsonify({'message': str(e)}), 400

    return user_service.add_system_manager(user_id, username)


@user_bp.route('/suspend_user', methods=['POST'])
@jwt_required()
def suspend_user():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        suspended_user_id = str(data['suspended_user_id'])
        date = data['date']
    except Exception as e:
        logger.error('suspend_user - ', str(e))
        return jsonify({'message': str(e)}), 400

    return user_service.suspend_user(user_id, suspended_user_id, date)


@user_bp.route('/unsuspend_user', methods=['POST'])
@jwt_required()
def unsuspend_user():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        suspended_user_id = str(data['suspended_user_id'])
    except Exception as e:
        logger.error('unsuspend_user - ', str(e))
        return jsonify({'message': str(e)}), 400

    return user_service.unsuspend_user(user_id, suspended_user_id)


@user_bp.route('/view_suspended_users', methods=['GET'])
@jwt_required()
def view_suspended_users():
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        logger.error('view_suspended_users - ', str(e))
        return jsonify({'message': str(e)}), 400

    return user_service.view_suspended_users(user_id)


@user_bp.route('/get_user_nominations', methods=['GET'])
@jwt_required()
def get_user_nominations():
    try:
        user_id = get_jwt_identity()
    except Exception as e:
        logger.error('get_user_nominations - ', str(e))
        return jsonify({'message': str(e)}), 400

    return user_service.get_user_nominations(user_id)

@user_bp.route('/get_user_employees', methods=['GET', 'POST'])
@jwt_required()
def get_user_employees():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        store_id = int(data['store_id'])
    except Exception as e:
        logger.error('get_user_employees - ', str(e))
        return jsonify({'message': str(e)}), 400

    res = user_service.get_user_employees(user_id, store_id)
    return res
