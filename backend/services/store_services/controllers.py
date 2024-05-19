# communication with business logic

class StoreService():
    def show_store_info(self, token):
        """
            Use Case 2.2.1.1:
            Show information about the stores in the system

            Args:
                token (?): token of the user

            Returns:
                ?
        """
        pass

    def show_store_products(self, token, store_id):
        """
            Use Case 2.2.1.2:
            Show products of a store

            Args:
                token (?): token of the user
                store_id (int): id of the store

            Returns:
                ?
        """
        pass


    def add_new_store(self, token, store_data):
        """
            Use Case 2.3.2:
            Add a store to the system and set the user as the store owner

            Args:
                token (int): token of the user
                store_data (?): data of the store to be added

            Returns:
                ?
        """
        pass

    def add_product_to_store(self, token, store_id, product_data):
        """
            Use Case 2.4.1:
            Add a product to a store

            Args:
                token (?): token of the user
                store_id (int): id of the store
                product_data (?): data of the product to be added

            Returns:
                ?
        """
        pass

    def change_store_purchace_policy(self, token, store_id, policy_data):
        """
            Use Case 2.4.2.1:
            Change the purchase policy of a store

            Args:
                token (?): token of the user
                store_id (int): id of the store
                policy_data (?): data of the new purchase policy

            Returns:
                ?
        """
        pass

    def change_store_purchace_types(self, token, store_id, types_data):
        """
            Use Case 2.4.2.2:
            Change the purchase types of a store

            Args:
                token (?): token of the user
                store_id (int): id of the store
                types_data (?): data of the new purchase types

            Returns:
                ?
        """
        pass

    def change_store_discount_types(self, token, store_id, types_data):
        """
            Use Case 2.4.2.3:
            Change the discount types of a store

            Args:
                token (?): token of the user
                store_id (int): id of the store
                types_data (?): data of the new discount types

            Returns:
                ?
        """
        pass

    def change_store_discount_policy(self, token, store_id, policy_data):
        """
            Use Case 2.4.2.4:
            Change the discount policy of a store

            Args:
                token (?): token of the user
                store_id (int): id of the store
                policy_data (?): data of the new discount policy

            Returns:
                ?
        """
        pass

    def add_store_owner(self, token, store_id, owner_id):
        """
            Use Case 2.4.3.1:
            Send promototion to a new owner to a store.
            User still needs to accept the promotion!

            Args:
                token (?): token of the user
                store_id (int): id of the store
                owner_id (int): id of the new owner

            Returns:
                ?
        """
        pass

    def add_store_manager(self, token, store_id, manager_id, permissions):
        """
            Use Case 2.4.6.1:
            Send promototion to a new manager to a store.
            User still needs to accept the promotion!

            Args:
                token (?): token of the user
                store_id (int): id of the store
                manager_id (int): id of the new manager
                permissions (?): permissions of the new manager

            Returns:
                ?
        """
        pass

    def edit_manager_permissions(self, token, store_id, manager_id, permissions):
        """
            Use Case 2.4.7:
            Edit the permissions of a store manager

            Args:
                token (?): token of the user
                store_id (int): id of the store
                manager_id (int): id of the manager
                permissions (?): new permissions of the manager

            Returns:
                ?
        """
        pass

    def closing_store(self, token, store_id):
        """
            Use Case 2.4.9:
            Close a store

            Args:
                token (?): token of the user
                store_id (int): id of the store

            Returns:
                ?
        """
        pass

    def view_employees_info(self, token, store_id):
        """
            Use Case 2.4.11:
            View information about the employees of a store

            Args:
                token (?): token of the user
                store_id (int): id of the store

            Returns:
                ?
        """
        pass