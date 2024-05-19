# communication with business logic
from backend.business.authentication.authentication import Authentication


class UserService:
    def show_notifications(self, user_id):
        """
            Use Case 1.5 + 1.6:
            Show notifications for a user which is logged in (member)

            Args:
                user_id (int): token of the user

            Returns:
                ?
        """
        pass

    def add_product_to_basket(self, user_id, store_id, product_id):
        """
            Use Case 2.2.3:
            Add a product to the basket

            Args:
                user_id (int): id of the user
                store_id (int): id of the store
                product_id (int): id of the product to be added to the basket

            Returns:
                success (str): success message
        """
        pass

    def show_shopping_cart(self, user_id):
        """
            Use Case 2.2.4.1:
            Show the shopping cart of a user

            Args:
                user_id (int): id of the user

            Returns:
                shopping cart data
        """
        pass

    def remove_product_from_cart(self, user_id, product_id):
        """
            Use Case 2.2.4.2:
            Remove a product from the shopping cart

            Args:
                user_id (?): user_id of the user
                product_id (int): id of the product to be removed from the shopping cart

            Returns:
                ?
        """
        pass

    def checkout(self, user_id, payment_method, payment_details):
        """
            Use Case 2.2.5:
            Checkout the shopping cart

            Args:
                user_id (?): user_id of the user
                payment_method (?): payment method to be used
                payment_details (?): payment details

            Returns:
                ?
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
        pass

    def change_admin_permissions(self, user_id: int, store_id: int, manager_id: int, add_product: bool,
                                 remove_product: bool, edit_product: bool, appoint_owner: bool, appoint_manager: bool,
                                 remove_owner: bool, remove_manager: bool):
        pass


class AuthenticationService:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(AuthenticationService, cls).__new__(cls)
            cls.instance.authentication = Authentication()
        return cls.instance

    def __init__(self):
        self.authentication = Authentication()

    def guest_login(self):
        """
            Use Case 1.2:
            Start the application and generate token for guest

            Returns:
                token (str): token of the guest
        """
        return self.authentication.start_guest()

    def login(self, user_id, user_credentials):
        """
            Use Case 2.1.4:
            Login a user

            Args:
                user_id (?): user_id of the user
                user_credentials (?): credentials of the user required for login

            Returns:
                session_token (?): token of the session
        """

    pass

    def logout(self, token_jti):
        """
            Use Case 2.3.1:
            Logout a user

            Args:
                token_jti (?): token_jti of the user

            Returns:
                ?
        """
        self.authentication.logout_user(token_jti)

    def register(self, user_id, register_credentials):
        """
            Use Case 2.1.3:
            Register a new user

            Args:
                user_id (int): id of the user
                register_credentials (?): credentials of the new user required for registration

            Returns:
                ?
        """
        self.authentication.register_user(user_id, register_credentials)
