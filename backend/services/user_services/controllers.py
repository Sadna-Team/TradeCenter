# communication with business logic


class UserService():
    def show_notifications(self, token):
        """
            Use Case 1.5 + 1.6:
            Show notifications for a user which is logged in (member)

            Args:
                token (int): token of the user

            Returns:
                ?
        """
        pass

    def add_product_to_basket(self, token, product_id, amount):
        """
            Use Case 2.2.3:
            Add a product to the basket

            Args:
                token (?): token of the user
                product_id (int): id of the product to be added to the basket
                amount (int): amount of the product to be added to the basket

            Returns:
                ?
        """
        pass

    def show_shopping_cart(self, token):
        """
            Use Case 2.2.4.1:
            Show the shopping cart of a user

            Args:
                token (?): token of the user

            Returns:
                ?
        """
        pass

    def remove_product_from_cart(self, token, product_id, amount):
        """
            Use Case 2.2.4.2:
            Remove a product from the shopping cart

            Args:
                token (?): token of the user
                product_id (int): id of the product to be removed from the shopping cart
                amount (int): amount of the product to be removed from the shopping cart

            Returns:
                ?
        """
        pass

    def checkout(self, token, payment_method, payment_details):
        """
            Use Case 2.2.5:
            Checkout the shopping cart

            Args:
                token (?): token of the user
                payment_method (?): payment method to be used
                payment_details (?): payment details

            Returns:
                ?
        """
        pass

    def accept_promotion_to_owner(self, token, store_id, owner_id):
        """
            Use Case 2.4.3.2:
            Accept a promotion to be store owner of a store

            Args:
                token (?): token of the user
                store_id (int): id of the store
                owner_id (int): id of the owner which proposed the promotion

            Returns:
                ?
        """
        pass

    def accept_promotion_to_manager(self, token, store_id, manager_id, permissions):
        """
            Use Case 2.4.6.2:
            Accept a promotion to be store manager of a store with the given permissions

            Args:
                token (?): token of the user
                store_id (int): id of the store
                manager_id (int): id of the manager which proposed the promotion
                permissions (?): permissions of the manager

            Returns:
                ?
        """
        pass


class AuthenticationService():
    def start_app(self):
        """
            Use Case 1.1:
            Start the application and generate token for user

            Returns:
                ?
        """

    def login(self, token, user_credentials):
        """
            Use Case 2.1.4:
            Login a user

            Args:
                token (?): token of the user
                user_credentials (?): credentials of the user required for login

            Returns:
                ?
        """

    pass

    def logout(self, token):
        """
            Use Case 2.3.1:
            Logout a user

            Args:
                token (?): token of the user

            Returns:
                ?
        """
        pass

    def register(self, token, register_credentials):
        """
            Use Case 2.1.3:
            Register a new user

            Args:
                token (?): token of the user
                register_credentials (?): credentials of the new user required for registration

            Returns:
                ?
        """
        pass
