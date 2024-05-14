# communication with business logic

class ThirdPartyService():
    def add_third_party_service(self, token, data):
        """
            Use Case 1.2.1:
            Add a third party service to be supported by the platform

            Args:
                token (int): token of the user
                data (dict): data of the third party service to be added

            Returns:
                ?
        """
        pass

    def edit_third_party_service(self, token, service_id, data):
        """
            Use Case 1.2.2:
            Edit a third party service supported by the platform

            Args:
                token (int): token of the user
                service_id (int): id of the third party service to be edited
                data (dict): data of the third party service to be edited

            Returns:
                ?
        """
        pass

    def delete_third_party_service(self, token, service_id):
        """
            Use Case 1.2.3:
            Delete a third party service supported by the platform

            Args:
                token (int): token of the user
                service_id (int): id of the third party service to be deleted

            Returns:
                ?
        """
        pass

    def access_payment_service(self, token, payment_method, payment_details, price):
        """
            Use Case 1.3:
            Access a payment service to make a payment

            Args:
                token (int): token of the user
                payment_method (?): payment method to be used
                payment_details (?): payment details
                price (float): price to be paid
        """
        pass

    def access_supply_service(self, token, package_details, user_id):
        """
            Use Case 1.4:
            Access a supply service to deliver a package

            Args:
                token (int): token of the user
                package_details (?): package details
                user_id (int): id of the user to receive the package
        """
        pass