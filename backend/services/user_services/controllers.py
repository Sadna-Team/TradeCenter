# communication with business logic
from backend.business.authentication.authentication import Authentication
from backend.business.user import UserFacade
from backend.business.roles.roles import RolesFacade
from backend.business.market import MarketFacade
from flask import jsonify
import logging

logger = logging.getLogger('myapp')


class UserService:
    # singleton
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(UserService, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.user_facade = UserFacade()
        self.roles_facade = RolesFacade()
        self.market_facade = MarketFacade()

    def show_notifications(self, user_id: int):
        """
            Use Case 1.5 + 1.6:
            Show notifications for a user which is logged in (member)

            Args:
                user_id (int): id of the user

            Returns:
                list: list of notifications
        """
        try:
            notifications = self.user_facade.get_notifications(user_id)
            notifications = [notification.get() for notification in notifications]
            logger.info('notifications retrieved successfully')
            return jsonify({'notifications': notifications}), 200

        except Exception as e:
            logger.error('show_notifications - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def add_product_to_basket(self, user_id: int, store_id: int, product_id: int, quantity: int):
        """
            Use Case 2.2.3:
            Add a product to the basket

            Args:
                user_id (int): id of the user
                store_id (int): id of the store
                product_id (int): id of the product to be added to the basket
                quantity (int): quantity of the product to be added

            Returns:
                response (str): response of the operation
        """
        try:
            self.market_facade.add_product_to_basket(user_id, store_id, product_id, quantity)
            logger.info('product added to the basket successfully')
            return jsonify({'message': 'product added to the basket successfully'}), 200

        except Exception as e:
            logger.error('add_product_to_basket - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def show_shopping_cart(self, user_id: int):
        """
            Use Case 2.2.4.1:
            Show the shopping cart of a user

            Args:
                user_id (int): id of the user

            Returns:
                ?
        """
        try:
            shopping_cart = self.user_facade.get_shopping_cart(user_id)
            logger.info('shopping cart retrieved successfully')
            return jsonify({'shopping_cart': shopping_cart}), 200
        except Exception as e:
            logger.error('show_shopping_cart - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def remove_product_from_basket(self, user_id: int, store_id: int, product_id: int, quantity: int):
        """
            Use Case 2.2.4.2:
            Remove a product from the shopping cart

            Args:
                user_id (int): id of the user
                store_id (int): id of the store
                product_id (int): id of the product to be removed from the shopping cart
                quantity (int): quantity of the product to be removed

            Returns:
                response (str): response of the operation
        """
        try:
            self.market_facade.remove_product_from_basket(user_id, store_id, product_id, quantity)
            logger.info('product removed from the basket successfully')
            return jsonify({'message': 'product removed from the basket successfully'}), 200

        except Exception as e:
            logger.error('remove_product_from_basket - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def checkout(self, user_id: int, payment_method: str, payment_details: dict):
        """
            Use Case 2.2.5:
            Checkout the shopping cart

            Args:
                user_id (int): id of the user
                payment_method (?): payment method to be used
                payment_details (?): payment details

            Returns:
                response (str): response of the operation
        """
        pass

    def accept_promotion(self, user_id: int, nomination_id: int, accept: bool):
        """
            Use Case 2.4.6.2:
            Accept a promotion to be store manager of a store with the given permissions

            Args:
                user_id (int): id of the user
                nomination_id (int): id of the nomination
                accept (bool): whether to accept the promotion


            Returns:
                ?
        """
        try:
            if accept:
                self.roles_facade.accept_nomination(nomination_id, user_id)
                logger.info('promotion accepted successfully')
                return jsonify({'message': 'promotion accepted successfully'}), 200
            else:
                self.roles_facade.decline_nomination(nomination_id, user_id)
                logger.info('promotion declined successfully')
                return jsonify({'message': 'promotion declined successfully'}), 200

        except Exception as e:
            logger.error('accept_promotion - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def is_system_manager(self, user_id: int):
        """
            Check if the user is a system manager

            Args:
                user_id (int): id of the user

            Returns:
                response (str): response of the operation
        """
        try:
            is_system_manager = self.roles_facade.is_system_manager(user_id)
            return jsonify({'is_system_manager': is_system_manager}), 200
        except Exception as e:
            logger.error('is_system_manager - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def is_store_owner(self, user_id: int, store_id: int):
        """
            Check if the user is a store owner

            Args:
                user_id (int): id of the user
                store_id (int): id of the store

            Returns:
                response (str): response of the operation
        """
        try:
            is_store_owner = self.roles_facade.is_owner(store_id, user_id)
            return jsonify({'is_store_owner': is_store_owner}), 200
        except Exception as e:
            logger.error('is_store_owner - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def is_store_manager(self, user_id: int, store_id: int):
        """
            Check if the user is a store manager

            Args:
                user_id (int): id of the user
                store_id (int): id of the store

            Returns:
                response (str): response of the operation
        """
        try:
            is_store_manager = self.roles_facade.is_manager(store_id, user_id)
            return jsonify({'is_store_manager': is_store_manager}), 200
        except Exception as e:
            logger.error('is_store_manager - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def has_add_product_permission(self, user_id: int, store_id: int):
        """
            Check if the user has permission to add a product to the store

            Args:
                user_id (int): id of the user
                store_id (int): id of the store

            Returns:
                response (str): response of the operation
        """
        try:
            has_permission = self.roles_facade.has_add_product_permission(store_id, user_id)
            return jsonify({'has_permission': has_permission}), 200
        except Exception as e:
            logger.error('has_add_product_permission - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def has_change_purchase_policy_permission(self, user_id: int, store_id: int):
        """
            Check if the user has permission to change the purchase policy of the store

            Args:
                user_id (int): id of the user
                store_id (int): id of the store

            Returns:
                response (str): response of the operation
        """
        try:
            has_permission = self.roles_facade.has_change_purchase_policy_permission(store_id, user_id)
            return jsonify({'has_permission': has_permission}), 200
        except Exception as e:
            logger.error('has_change_purchase_policy_permission - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def has_change_purchase_types_permission(self, user_id: int, store_id: int):
        """
            Check if the user has permission to change the purchase types of the store

            Args:
                user_id (int): id of the user
                store_id (int): id of the store

            Returns:
                response (str): response of the operation
        """
        try:
            has_permission = self.roles_facade.has_change_purchase_types_permission(store_id, user_id)
            return jsonify({'has_permission': has_permission}), 200
        except Exception as e:
            logger.error('has_change_purchase_types_permission - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def has_change_discount_policy_permission(self, user_id: int, store_id: int):
        """
            Check if the user has permission to change the discount policy of the store

            Args:
                user_id (int): id of the user
                store_id (int): id of the store

            Returns:
                response (str): response of the operation
        """
        try:
            has_permission = self.roles_facade.has_change_discount_policy_permission(store_id, user_id)
            return jsonify({'has_permission': has_permission}), 200
        except Exception as e:
            logger.error('has_change_discount_policy_permission - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def has_change_discount_types_permission(self, user_id: int, store_id: int):
        """
            Check if the user has permission to change the discount types of the store

            Args:
                user_id (int): id of the user
                store_id (int): id of the store

            Returns:
                response (str): response of the operation
        """
        try:
            has_permission = self.roles_facade.has_change_discount_types_permission(store_id, user_id)
            return jsonify({'has_permission': has_permission}), 200
        except Exception as e:
            logger.error('has_change_discount_types_permission - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def has_add_manager_permission(self, user_id: int, store_id: int):
        """
            Check if the user has permission to add a manager to the store

            Args:
                user_id (int): id of the user
                store_id (int): id of the store

            Returns:
                response (str): response of the operation
        """
        try:
            has_permission = self.roles_facade.has_add_manager_permission(store_id, user_id)
            return jsonify({'has_permission': has_permission}), 200
        except Exception as e:
            logger.error('has_add_manager_permission - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def has_get_bid_permission(self, user_id: int, store_id: int):
        """
            Check if the user has permission to get a bid from the store

            Args:
                user_id (int): id of the user
                store_id (int): id of the store

            Returns:
                response (str): response of the operation
        """
        try:
            has_permission = self.roles_facade.has_get_bid_permission(store_id, user_id)
            return jsonify({'has_permission': has_permission}), 200
        except Exception as e:
            logger.error('has_get_bid_permission - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def add_system_manager(self, user_id: int, username: str):
        """
            Add a system manager

            Args:
                user_id (int): id of the user
                username (str): username of the new system manager

            Returns:
                response (str): response of the operation
        """
        try:
            self.market_facade.add_system_manager(user_id, username)
            return jsonify({'message': 'system manager added successfully'}), 200
        except Exception as e:
            logger.error('add_system_manager - ' + str(e))
            return jsonify({'message': str(e)}), 400


class AuthenticationService:
    # singleton
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(AuthenticationService, cls).__new__(cls)
            cls.instance.authentication = Authentication()
        return cls.instance

    def __init__(self):
        self.authentication = Authentication()

    def start_guest(self):
        """
            Use Case 1.2:
            Start the application and generate token for guest

            Returns:
                token (str): token of the guest
        """
        try:
            user_token = self.authentication.start_guest()
            return jsonify({'token': user_token}), 200

        except Exception as e:
            logger.error('start - guest failed to enter the app')
            return jsonify({'message': str(e)}), 400

    def register(self, user_id: int, register_credentials: dict):
        """
            Use Case 2.1.3:
            Register a new user

            Args:
                user_id (int): id of the user
                register_credentials (?): credentials of the new user required for registration

            Returns:
                token (str): token of the user
        """
        try:
            self.authentication.register_user(user_id, register_credentials)
            logger.info('User registered successfully')
            return jsonify({'message': 'User registered successfully - great success'}), 201

        except Exception as e:
            logger.error('register - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def login(self, username: str, password: str):
        """
            Use Case 2.1.4:
            Login a user

            Args:
                username (str): the username of the user
                password (str): the password of the user

            Returns:
                token (str): token of the user
                notification (list[str]): list of delayed notifications
        """
        try:
            user_token, notification = self.authentication.login_user(username, password)
            logger.info('User logged in successfully')
            return jsonify({'token': user_token, 'notification': notification}), 200


        except Exception as e:
            logger.error('login - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def logout(self, jti: str, user_id: int):
        """
            Use Case 2.3.2:
            Logout a user

            Args:
                jti (str): token of the user
                user_id (int): id of the user

            Returns:
                response (str): response of the operation
        """
        try:
            token = self.authentication.logout_user(jti, user_id)
            logger.info('User logged out successfully')
            return jsonify({'message': 'User logged out successfully', 'token': token}), 200

        except Exception as e:
            logger.error('logout - ' + str(e))
            return jsonify({'message': str(e)}), 400

    def logout_guest(self, jti: str, user_id: int):
        """
            Use Case 2.1.2:
            Logout a guest

            Args:
                jti (str): token of the user
                user_id (int): id of the user

            Returns:
                response (str): response of the operation
        """
        try:
            self.authentication.logout_guest(jti, user_id)
            logger.info('Guest logged out successfully')
            return jsonify({'message': 'Guest logged out successfully'}), 200

        except Exception as e:
            logger.error('logout_guest - ' + str(e))
            return jsonify({'message': str(e)}), 400
