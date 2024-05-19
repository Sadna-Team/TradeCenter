# communication with business logic

class PurchaseService:

    #is this not the job of the market facade???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
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

    def show_purchase_history_in_store(self, token, store_id):
        """
            Use Case 2.4.13:
            Show the purchase history in a store

            Args:
                token (?): token of the user
                store_id (int): id of the store

            Returns:
                ?
        """
        pass

    def show_purchase_history_of_member(self, token, user_id):
        """
            Use Case 2.6.4:
            Show the purchase history of a member

            Args:
                token (?): token of the user
                user_id (int): id of the user

            Returns:
                ?
        """
        pass

    def search_products(self, token, filters):
        """
            Use Case 2.2.2.1:
            Search products in the stores

            Args:
                token (?): token of the user
                filters (?): filters to search for products

            Returns:
                ?
        """
    pass

    def search_store_products(self, token, store_id, filters):
        """
            Use Case 2.2.2.2:
            Search products in a store

            Args:
                token (?): token of the user
                store_id (int): id of the store
                filters (?): filters to search for products

            Returns:
                ?
        """
        pass