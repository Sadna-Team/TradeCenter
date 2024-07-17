# -------------------------------------- Imports --------------------------------------
from enum import Enum 

# -------------------------------------- Enums --------------------------------------
class StoreErrorTypes(Enum):
    store_not_found = 1
    product_not_found = 2
    category_not_found = 3
    policy_not_found = 4
    parent_category_not_found = 5
    tag_not_found = 6
    invalid_price = 7
    invalid_description = 8
    invalid_tag = 9
    invalid_weight = 10
    invalid_amount = 11
    invalid_policy_name = 12
    invalid_category_name = 13
    invalid_store_name = 14
    tag_already_exists = 15
    parent_category_already_exists = 16
    product_already_exists = 17
    store_already_open = 18
    policy_already_exists = 19
    sub_category_error = 20
    user_not_founder_of_store = 21
    store_not_active = 22
    policy_not_satisfied = 23
    product_not_available = 24
    no_listeners_for_store = 25
    cart_is_empty = 27
    invalid_purchase_policy_input = 28
    unexpected_error = 29
    invalid_product_name = 30
    invalid_user_id = 31

class UserErrorTypes(Enum):
    user_suspended = 1
    user_not_found = 2
    username_already_exists = 3
    user_already_registered = 4
    username_not_found = 5
    user_not_registered = 6
    currency_not_supported = 7
    missing_credentials = 8
    invalid_credentials = 9
    user_logged_in = 10
    user_not_logged_in = 11
    user_is_not_guest = 12
    user_already_listener_for_store = 13
    user_not_system_manager = 14
    user_does_not_have_necessary_permissions = 15
    user_not_a_member = 16
    user_not_a_manager_or_owner = 17

class RoleErrorTypes(Enum):
    actor_not_member_of_store = 1
    actor_not_owner = 2
    nominator_not_owner = 3
    nominator_cant_nominate_manager = 4
    nominator_not_member_of_store = 5
    nominee_already_exists_in_store = 6
    nomination_does_not_exist = 7
    nominee_id_error = 8
    manager_not_member_of_store = 9
    user_not_manager = 10
    actor_is_not_owner_of_manager = 11
    user_not_member_of_store = 12
    actor_not_authorized_to_remove_role = 13
    actor_not_ancestor_of_role = 14
    cant_remove_founder = 15
    actor_not_system_manager = 16
    cant_remove_system_admin = 17
    user_not_system_manager = 18
    user_is_manager = 19
    store_already_exists = 20
    actor_not_founder = 21
    invalid_role = 22


class PurchaseErrorTypes(Enum):
    purchase_not_ongoing = 1
    purchase_not_accepted = 2
    invalid_total_price = 3
    purchase_already_accepted_or_completed = 4
    invalid_purchase_id = 5
    product_not_in_basket = 6
    category_not_in_basket = 7
    invalid_country_code = 8
    invalid_basket = 9
    basket_not_for_store = 10
    store_owner_manager_already_accepted_offer = 11
    offer_not_to_store = 12
    invalid_proposed_price = 13
    invalid_user_id = 14
    offer_to_store = 15
    purchase_not_bid_purchase = 16
    database_error = 17
    invalid_name = 18
    purchase_not_approved = 19


class ThirdPartyHandlerErrorTypes(Enum):
    payment_method_not_supported = 1
    supply_method_not_supported = 2
    payment_method_already_supported = 3
    supply_method_already_supported = 4
    invalid_payment_method = 5
    invalid_supply_method = 6
    missing_arrival_time = 7
    invalid_arrival_time = 8
    missing_supply_method = 9
    missing_address = 10
    missing_purchase_id = 11
    payment_not_specified = 12
    payment_failed = 13
    support_not_specified = 14
    supply_failed = 15
    handshake_failed = 16
    external_payment_failed = 17
    external_supply_failed = 18

class DiscountAndConstraintsErrorTypes(Enum):
    discount_not_found = 1
    invalid_percentage = 2
    discount_creation_error = 3
    invalid_type_of_composite_discount = 4
    not_enough_discounts = 5
    predicate_creation_error = 6
    missing_predicate_builder = 7
    no_predicate_found = 8
    invalid_season = 9
    invalid_date = 10
    invalid_age_limit = 11
    invalid_location = 12
    invalid_time_constraint = 13
    invalid_day_of_month = 14
    invalid_day_of_week = 15
    invalid_price = 16
    invalid_amount = 17
    invalid_weight = 18

class ServiceLayerErrorTypes(Enum):
    payment_details_not_dict = 1
    address_not_dict = 2
    tags_not_list = 3
    config_not_dict = 4
    additional_details_not_dict = 5


# -------------------------------------- StoreErrors --------------------------------------
class StoreError(ValueError):
    def __init__(self, message: str, store_error_type: StoreErrorTypes):
        self.__message = message
        super().__init__(self.__message)
        self.__store_error_type = store_error_type
    
    @property
    def message(self) -> str:
        return self.__message
    
    @property 
    def store_error_type(self) -> StoreErrorTypes:
        return self.__store_error_type


# -------------------------------------- discount Errors --------------------------------------
class DiscountAndConstraintsError(ValueError):
    def __init__(self, message: str, discount_error_type: DiscountAndConstraintsErrorTypes):
        self.__message = message
        super().__init__(self.__message)
        self.__discount_error_type = discount_error_type

    @property
    def message(self) -> str:
        return self.__message
    
    @property
    def discount_error_type(self) -> DiscountAndConstraintsErrorTypes:
        return self.__discount_error_type

# -------------------------------------- User Errors --------------------------------------
class UserError(ValueError):
    def __init__(self, message: str, user_error_type: UserErrorTypes):
        self.__message = message
        super().__init__(self.__message)
        self.__user_error_type = user_error_type

    @property
    def message(self) -> str:
        return self.__message
    
    @property
    def user_error_type(self) -> UserErrorTypes:
        return self.__user_error_type

# -------------------------------------- Role Errors --------------------------------------
class RoleError(ValueError):
    def __init__(self, message: str, role_error_type: RoleErrorTypes):
        self.__message = message
        super().__init__(self.__message)
        self.__role_error_type = role_error_type

    @property
    def message(self) -> str:
        return self.__message

    @property
    def role_error_type(self) -> RoleErrorTypes:
        return self.__role_error_type

# -------------------------------------- Purchase Errors --------------------------------------
class PurchaseError(ValueError):
    def __init__(self, message: str, purchase_error_type: PurchaseErrorTypes):
        self.__message = message
        super().__init__(self.message)
        self.__purchase_error_type = purchase_error_type

    @property
    def message(self) -> str:
        return self.__message
    
    @property
    def purchase_error_type(self) -> PurchaseErrorTypes:
        return self.__purchase_error_type
    

# -------------------------------------- ThirdPartyHandler Errors --------------------------------------
class ThirdPartyHandlerError(ValueError):
    def __init__(self, message: str, third_party_handler_error_type: ThirdPartyHandlerErrorTypes):
        self.__message = message
        super().__init__(self.__message)
        self.__third_party_handler_error_type = third_party_handler_error_type

    @property
    def message(self) -> str:
        return self.__message
    
    @property
    def third_party_handler_error_type(self) -> ThirdPartyHandlerErrorTypes:
        return self.__third_party_handler_error_type


# -------------------------------------- ServiceLayer Errors --------------------------------------
class ServiceLayerError(ValueError):
    def __init__(self, message: str, service_layer_error_type: ServiceLayerErrorTypes):
        self.__message = message
        super().__init__(self.__message)
        self.__service_layer_error_type = service_layer_error_type

    @property
    def message(self) -> str:
        return self.__message
    
    @property
    def service_layer_error_type(self) -> ServiceLayerErrorTypes:
        return self.__service_layer_error_type