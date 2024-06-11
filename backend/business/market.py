from .user import UserFacade
from .authentication.authentication import Authentication
from .roles import RolesFacade
from .DTOs import AddressDTO, NotificationDTO, PurchaseDTO, PurchaseProductDTO, StoreDTO, ProductDTO, UserDTO, \
    PurchaseUserDTO, UserInformationForDiscountDTO
from .store import StoreFacade
from .purchase import PurchaseFacade
from .ThirdPartyHandlers import PaymentHandler, SupplyHandler
from .notifier import Notifier
from typing import List, Dict, Tuple, Optional
from datetime import date, datetime
import threading

import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Market logger")


class MarketFacade:
    # singleton
    __instance = None
    __lock = threading.Lock()

    def __new__(cls):
        if MarketFacade.__instance is None:
            MarketFacade.__instance = object.__new__(cls)
        return MarketFacade.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True

            # initialize all the facades
            self.user_facade = UserFacade()
            self.store_facade = StoreFacade()
            self.roles_facade = RolesFacade()
            self.purchase_facade = PurchaseFacade()
            self.addresses = []
            self.auth_facade = Authentication()
            self.notifier = Notifier()

            # create the admin?
            self.__create_admin()

    def __create_admin(self, currency: str = "USD") -> None:
        man_id = self.user_facade.create_user(currency)
        hashed_password = self.auth_facade.hash_password("admin")
        self.user_facade.register_user(man_id, "admin@admin.com", "admin", hashed_password,
                                       2000, 1, 1, "123456789")
        self.roles_facade.add_admin(man_id)
        logger.info(f"Admin was created")

    def clean_data(self):
        """
        For testing purposes only
        """
        self.user_facade.clean_data()
        self.store_facade.clean_data()
        self.roles_facade.clean_data()
        self.purchase_facade.clean_data()
        self.notifier.clean_data()
        PaymentHandler().reset()
        SupplyHandler().reset()

        # create the admin?
        self.__create_admin()

    def show_notifications(self, user_id: int) -> List[NotificationDTO]:
        return self.user_facade.get_notifications(user_id)

    def add_product_to_basket(self, user_id: int, store_id: int, product_id: int, amount: int):
        if self.store_facade.check_product_availability(store_id, product_id, amount):
            self.user_facade.add_product_to_basket(user_id, store_id, product_id, amount)
            logger.info(f"User {user_id} has added {amount} of product {product_id} to the basket")
        else:
            raise ValueError("Product is not available")

    def remove_product_from_basket(self, user_id: int, store_id: int, product_id: int, amount: int):
        self.user_facade.remove_product_from_basket(user_id, store_id, product_id, amount)
        logger.info(f"User {user_id} has removed {amount} of product {product_id} from the basket")

    def checkout(self, user_id: int, payment_details: Dict, supply_method: str, address: Dict) -> int:
        products_removed = False
        purchase_accepted = False
        basket_cleared = False
        cart: Dict[int, Dict[int, int]] = {}  # store_id -> product_id -> amount
        pur_id = -1
        try:
            cart = self.user_facade.get_shopping_cart(user_id)

            if not cart:
                raise ValueError("Cart is empty")

            user_dto = self.user_facade.get_userDTO(user_id)
            birthdate = None
            if user_dto.day is not None and user_dto.month is not None and user_dto.year is not None:
                birthdate = date(user_dto.year, user_dto.month, user_dto.day)
            user_purchase_dto = PurchaseUserDTO(user_dto.user_id, birthdate)

            if 'address_id' not in address or 'address' not in address or 'city' not in address or 'state' not in address or 'country' not in address or 'postal_code' not in address:
                raise ValueError("Address information is missing")
            address_of_user_for_discount: AddressDTO = AddressDTO(address['address_id'], address['address'],
                                                                  address['city'], address['state'],
                                                                  address['country'], address['postal_code'])


            user_info_for_discount_dto = UserInformationForDiscountDTO(user_id, user_purchase_dto.birthdate,
                                                                       address_of_user_for_discount)
            # calculate the total price
            self.store_facade.validate_purchase_policies(cart, user_purchase_dto)

            total_price = self.store_facade.get_total_price_before_discount(cart)

            total_price_after_discounts = self.store_facade.get_total_price_after_discount(cart,
                                                                                           user_info_for_discount_dto)

            # purchase facade immediate
            purchase_shopping_cart: Dict[int, Tuple[List[PurchaseProductDTO], float, float]] = (
                self.store_facade.get_purchase_shopping_cart(user_info_for_discount_dto, cart))

            pur_id = self.purchase_facade.create_immediate_purchase(user_id, total_price, total_price_after_discounts,
                                                                    purchase_shopping_cart)

            # remove the products from the store
            self.store_facade.check_and_remove_shopping_cart(cart)

            products_removed = True

            # find the delivery date
            package_details = {'stores': cart.keys(), "supply method": supply_method}
            delivery_date = SupplyHandler().get_delivery_time(package_details, address)

            # accept the purchase
            self.purchase_facade.accept_purchase(pur_id, delivery_date)
            purchase_accepted = True

            # clear the cart
            self.user_facade.clear_basket(user_id)
            basket_cleared = True

            # TODO: fix discounts
            if "payment method" not in payment_details:
                # self.purchase_facade.invalidate_purchase_of_user_immediate(purchase.purchase_id, user_id)
                raise ValueError("Payment method not specified")

            if not PaymentHandler().process_payment(total_price_after_discounts, payment_details):
                # invalidate Purchase
                # self.purchase_facade.invalidate_purchase_of_user_immediate(purchase.purchase_id, user_id)
                raise ValueError("Payment failed")

            package_detail = {'shopping cart': cart, 'address': address, 'arrival time': delivery_date,
                               'purchase id': pur_id, "supply method": supply_method}
            if "supply method" not in package_detail:
                raise ValueError("Supply method not specified")
            if package_detail.get("supply method") not in SupplyHandler().supply_config:
                raise ValueError("Invalid supply method")
            on_arrival = lambda purchase_id: self.purchase_facade.complete_purchase(purchase_id)
            SupplyHandler().process_supply(package_detail, user_id, on_arrival)
            for store_id in cart.keys():
                Notifier().notify_new_purchase(store_id, user_id)

            logger.info(f"User {user_id} has checked out")
            return pur_id
        except Exception as e:
            if products_removed:
                for store_id, products in cart.items():
                    for product_id in products:
                        amount = products[product_id]
                        self.store_facade.add_product_amount(store_id, product_id, amount)
            if purchase_accepted:
                self.purchase_facade.cancel_accepted_purchase(pur_id)
            if basket_cleared:
                self.user_facade.restore_basket(user_id, cart)
            raise e

    def nominate_store_owner(self, store_id: int, owner_id: int, new_owner_username):
        # get user_id of new_owner_username
        new_owner_id = self.user_facade.get_user_id_from_username(new_owner_username)
        nomination_id = self.roles_facade.nominate_owner(store_id, owner_id, new_owner_id)
        # TODO: different implementation later
        self.user_facade.notify_user(new_owner_id,
                                     NotificationDTO(-1, f"You have been nominated to be the owner of store"
                                                         f" {store_id}. nomination id: {nomination_id} ",
                                                     datetime.now()))
        logger.info(f"User {owner_id} has nominated user {new_owner_id} to be the owner of store {store_id}")

    def nominate_store_manager(self, store_id: int, owner_id: int, new_manager_username):
        # get user_id of new_manager_username
        new_manager_id = self.user_facade.get_user_id_from_username(new_manager_username)
        nomination_id = self.roles_facade.nominate_manager(store_id, owner_id, new_manager_id)
        # TODO: different implementation later
        self.user_facade.notify_user(new_manager_id,
                                     NotificationDTO(-1, f"You have been nominated to be the manager of store"
                                                         f" {store_id}. nomination id: {nomination_id} ",
                                                     datetime.now()))
        logger.info(f"User {owner_id} has nominated user {new_manager_id} to be the manager of store {store_id}")

    def accept_nomination(self, user_id: int, nomination_id: int, accept: bool):
        if accept:
            self.roles_facade.accept_nomination(nomination_id, user_id)
        else:
            self.roles_facade.decline_nomination(nomination_id, user_id)

    def change_permissions(self, actor_id: int, store_id: int, manager_id: int, add_product: bool,
                           change_purchase_policy: bool, change_purchase_types: bool, change_discount_policy: bool,
                           change_discount_types: bool, add_manager: bool, get_bid: bool):
        self.roles_facade.set_manager_permissions(store_id, actor_id, manager_id, add_product, change_purchase_policy,
                                                  change_purchase_types, change_discount_policy, change_discount_types,
                                                  add_manager, get_bid)

        logger.info(f"User {actor_id} has changed the permissions of user {manager_id} in store {store_id}")

    def remove_store_role(self, actor_id: int, store_id: int, username: str):
        user_id = self.user_facade.get_user_id_from_username(username)
        self.roles_facade.remove_role(store_id, actor_id, user_id)
        logger.info(f"User {actor_id} has removed user {user_id} from store {store_id}")

    def give_up_role(self, actor_id: int, store_id: int):
        self.roles_facade.remove_role(store_id, actor_id, actor_id)
        logger.info(f"User {actor_id} has given up his role in store {store_id}")

    def add_system_manager(self, actor: int, user_id: int):
        self.roles_facade.add_system_manager(actor, user_id)
        logger.info(f"User {actor} has added user {user_id} as a system manager")

    def remove_system_manager(self, actor: int, user_id: int):
        self.roles_facade.remove_system_manager(actor, user_id)
        logger.info(f"User {actor} has removed user {user_id} as a system manager")

    def add_payment_method(self, user_id: int, method_name: str, payment_config: Dict):
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        PaymentHandler().add_payment_method(method_name, payment_config)

    def edit_payment_method(self, user_id: int, method_name: str, editing_data: Dict):
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        PaymentHandler().edit_payment_method(method_name, editing_data)

    def remove_payment_method(self, user_id: int, method_name: str):
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        PaymentHandler().remove_payment_method(method_name)

    def add_supply_method(self, user_id: int, method_name: str, supply_config: Dict):
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        SupplyHandler().add_supply_method(method_name, supply_config)

    def edit_supply_method(self, user_id: int, method_name: str, editing_data: Dict):
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        SupplyHandler().edit_supply_method(method_name, editing_data)

    def remove_supply_method(self, user_id: int, method_name: str):
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        SupplyHandler().remove_supply_method(method_name)

    # -------------------------------------- Store Related Methods --------------------------------------#
    def search_by_category(self, category_id: int, store_id: Optional[int] = None) -> Dict[int, List[ProductDTO]]:
        """
        * Parameters: categoryId, storeId(optional)
        * This function gets all necessary information of the products in the category with categoryId
        * Returns a dict from storeId to a list of ProductDTOs
        """
        product_dtos = self.store_facade.search_by_category(category_id, store_id)
        return product_dtos

    def search_by_tags(self, tags: List[str], store_id: Optional[int] = None) -> Dict[int, List[ProductDTO]]:
        """
        * Parameters: tags, storeId(optional)
        * This function returns all necessary information of the products with the tags
        * Returns a dict from storeId to a list of ProductDTOs
        """
        product_dtos = self.store_facade.search_by_tags(tags, store_id)
        return product_dtos

    def search_by_name(self, name: str, store_id: Optional[int] = None) -> Dict[int, List[ProductDTO]]:
        """
        * Parameters: name, storeId(optional)
        * This function returns all necessary information of the products with the name
        * Returns a dict from storeId to a list of ProductDTOs
        """
        product_dtos = self.store_facade.search_by_name(name, store_id)
        return product_dtos

    '''    def search_product_in_store(self, store_id: int, name: str, sort_type: int) \
            -> Dict[int, Tuple[Tuple[int, float], float]]:
        """
        * Parameters: storeId, names, sortByLowesToHighestPrice
        * This function returns the list of all productIds
        * Note: if sortType is 1, the list will be sorted by lowest to highest price, 2 is highest to lowest, 3 is by
        rating lowest to Highest, 4 is by highest to lowest
        * Returns a dict of <productId, <amount, price> rating> of the product in a store
 product ids of the products with the names in names
        """
        product_ids_to_store = self.store_facade.search_product_in_store(store_id, name)

        if sort_type == 1:
            product_ids_to_store.sort(key=lambda x: x[1][0])
        elif sort_type == 2:
            product_ids_to_store.sort(key=lambda x: x[1][0], reverse=True)
        elif sort_type == 3:
            product_ids_to_store.sort(key=lambda x: x[1][1])
        elif sort_type == 4:
            product_ids_to_store.sort(key=lambda x: x[1][1], reverse=True)
        return product_ids_to_store
    '''

    def get_store_info(self, store_id: int) -> StoreDTO:
        """
            * Parameters: storeId
            * This function returns the store information
            * Returns the store information
            """
        return self.store_facade.get_store_info(store_id)

    def get_store_product_info(self, store_id: int) -> List[ProductDTO]:
        """
        * Parameters: storeId
        * This function returns the store product information
        * Returns the store product information
        """
        return self.get_store_info(store_id).products

    # -------------Discount related methods-------------------#
    def add_discount(self, user_id: int, description: str, start_date: datetime, end_date: datetime, percentage: float, 
                        store_id: Optional[int] = None, product_id: Optional[int] = None, category_id: Optional[int] = None, applied_to_sub: Optional[bool] = None) -> int:
        """
        * Parameters: userId, description, startDate, endDate, percentage, storeId(optional), productId(optional), categoryId(optional), appliedToSub(optional)
        * This function adds a simple discount to the system
        *NOTE: the discount is initialized with no predicate!
        * Returns none
        """
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        return self.store_facade.add_discount(description, start_date, end_date, percentage, category_id, store_id, product_id, applied_to_sub) 
    
    
    def create_logical_composite_discount(self, user_id: int, description: str, start_date: datetime, end_date: datetime, discount_id1: int, discount_id2: int, type_of_composite: int) -> int:
        """
        * Parameters: userId, description, startDate, endDate, discountId1, discountId2, typeOfComposite
        * This function creates a composite discount
        * NOTE: the percentage of a composite discount is initialized to 0.0 since it is not used
        * NOTE: type_of_connection: 1 is AND, 2 OR, 3 XOR
        * Returns none
        """
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        return self.store_facade.create_logical_composite_discount(description, start_date, end_date, 0.0, discount_id1, discount_id2, type_of_composite)

    def create_numerical_composite_discount(self, user_id: int, description: str, start_date: datetime, end_date: datetime, discount_ids: List[int], type_of_composite: int) -> int:
        """
        * Parameters: userId, description, startDate, endDate, discountIds, typeOfComposite
        * This function creates a composite discount
        * NOTE: the percentage of a composite discount is initialized to 0.0 since it is not used
        * NOTE: type_of_connection: 1 is MAX, 2 is ADDITIVE
        * Returns none
        """
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        return self.store_facade.create_numerical_composite_discount(description, start_date, end_date, 0.0, discount_ids, type_of_composite)

    def assign_predicate_to_discount(self, user_id: int, discount_id: int, ages: List[Optional[int]],
                                     locations: List[Optional[Dict]],
                                     starting_times: List[Optional[datetime.time]],
                                     ending_times: List[Optional[datetime.time]], min_prices: List[Optional[float]],
                                     max_prices: List[Optional[float]], min_weights: List[Optional[float]],
                                     max_weights: List[Optional[float]], min_amounts: List[Optional[int]],
                                     store_ids: List[Optional[int]], product_ids: List[Optional[int]],
                                     category_ids: List[Optional[int]],
                                     type_of_connection: List[Optional[int]]) -> None:
        if not self.roles_facade.is_system_manager(user_id):
            logger.warning(f"User {user_id} does not have permissions to assign a predicate to a discount")
            raise ValueError("User is not a system manager")
        self.store_facade.assign_predicate_to_discount(discount_id, ages, locations, starting_times, ending_times,
                                                       min_prices, max_prices, min_weights, max_weights, min_amounts,
                                                       store_ids, product_ids, category_ids, type_of_connection)

    def change_discount_percentage(self, user_id: int, discount_id: int, new_percentage: float) -> None:
        """
        * Parameters: userId, discountId, newPercentage
        * This function changes the percentage of a discount
        * Returns None
        """
        if not self.roles_facade.is_system_manager(user_id):
            logger.warning(f"User {user_id} does not have permissions to change the percentage of a discount")
            raise ValueError("User is not a system manager")
        self.store_facade.change_discount_percentage(discount_id, new_percentage)

    def change_discount_description(self, user_id: int, discount_id: int, new_description: str) -> None:
        """
        * Parameters: userId, discountId, newDescription
        * This function changes the description of a discount
        * Returns None
        """
        if not self.roles_facade.is_system_manager(user_id):
            logger.warning(f"User {user_id} does not have permissions to change the description of a discount")
            raise ValueError("User is not a system manager")
        self.store_facade.change_discount_description(discount_id, new_description)

    def remove_discount(self, user_id: int, discount_id: int) -> None:
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        if self.store_facade.remove_discount(discount_id):
            logger.info(f"User {user_id} has removed a discount")
        else:
            logger.info(f"User {user_id} has failed to remove a discount")

    # -------------Rating related methods-------------------#
    '''def add_store_rating(self, user_id: int, purchase_id: int, description: str, rating: float):
        """
        * Parameters: user_id, purchase_id, description, rating
        * This function adds a rating to a store
        * Returns None
        """
        store_id = self.purchase_facade.get_purchase_by_id(purchase_id).store_id
        new_rating = self.purchase_facade.rate_store(purchase_id, user_id, store_id, rating, description)
        if new_rating is not None:
            self.store_facade.update_store_rating(store_id, new_rating)
            logger.info(f"User {user_id} has rated store {store_id} with {rating}")
        else:
            logger.info(f"User {user_id} has failed to rate store {store_id}")'''

    '''def add_product_rating(self, user_id: int, purchase_id: int, description: str, product_spec_id: int, rating: float):
        """
        * Parameters: user_id, purchase_id, description, productSpec_id, rating
        * This function adds a rating to a product
        * Returns None
        """
        store_id = self.purchase_facade.get_purchase_by_id(purchase_id).store_id
        new_rating = self.purchase_facade.rate_product(purchase_id, user_id, product_spec_id, rating, description)
        if new_rating is not None:
            self.store_facade.update_product_spec_rating(store_id, product_spec_id, new_rating)
            logger.info(f"User {user_id} has rated product {product_spec_id} with {rating}")
        else:
            logger.info(f"User {user_id} has failed to rate product {product_spec_id}")'''

    # -------------Policies related methods-------------------#
    def add_purchase_policy(self, user_id: int, store_id: int, policy_name: str):

        # for now, we dont support the creation of different types of policies
        """
        * Parameters: userId, store_id, policy_name
        * This function adds a purchase policy to the store
        * Returns None
        """
        if self.roles_facade.has_change_purchase_policy_permission(store_id, user_id):
            self.store_facade.add_purchase_policy_to_store(store_id, policy_name)
            logger.info(f"User {user_id} has added a policy to store {store_id}")
        else:
            raise ValueError("User does not have the necessary permissions to add a policy to the store")

    def remove_purchase_policy(self, user_id, store_id: int, policy_name: str):
        """
        * Parameters: store_id, policy_name
        * This function removes a purchase policy from the store
        * Returns None
        """
        if self.roles_facade.has_change_purchase_policy_permission(store_id, user_id):
            self.store_facade.remove_purchase_policy_from_store(store_id, policy_name)
            logger.info(f"User {user_id} has removed a policy from store {store_id}")
        else:
            raise ValueError("User does not have the necessary permissions to remove a policy from the store")

    # -------------Products related methods-------------------#
    def add_product(self, user_id: int, store_id: int, product_name: str, description: str, price: float,
                    weight: float, tags: List[str], amount: Optional[int]=0) -> int:
        """
        * Parameters: user_id, store_id, productSpecId, expirationDate, condition, price
        * This function adds a product to the store
        * Returns None
        """
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError("User does not have the necessary permissions to add a product to the store")
        return self.store_facade.add_product_to_store(store_id, product_name, description, price, weight, tags, amount)

    def remove_product(self, user_id: int, store_id: int, product_id: int):
        """
        * Parameters: store_id, product_id
        * This function removes a product from the store
        * Returns None
        """
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError("User does not have the necessary permissions to remove a product from the store")
        self.store_facade.remove_product_from_store(store_id, product_id)

    def add_product_amount(self, user_id: int, store_id: int, product_id: int, amount: int):
        """
        * Parameters: userId, store_id, product_id, amount
        * This function adds an amount of a product to the store
        * Returns None
        """
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError("User does not have the necessary permissions to add an amount of a product to the store")
        self.store_facade.add_product_amount(store_id, product_id, amount)

    def remove_product_amount(self, user_id: int, store_id: int, product_id: int, amount: int):
        """
        * Parameters: userId, store_id, product_id, amount
        * This function removes an amount of a product from the store
        * Returns None
        """
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError("User does not have the necessary permissions to remove an amount of a product from the "
                             "store")
        self.store_facade.remove_product_amount(store_id, product_id, amount)

    # -------------Store related methods-------------------#
    def add_store(self, founder_id: int, location_id: int, store_name: str) -> int:
        """
        * Parameters: founderId, locationId, storeName
        * This function adds a store to the system
        * Returns None
        """
        # TODO: add transaction
        if not self.user_facade.is_member(founder_id):
            raise ValueError("User is not a member")

        store_id = self.store_facade.add_store(location_id, store_name, founder_id)
        self.roles_facade.add_store(store_id, founder_id)
        Notifier().sign_listener(founder_id, store_id)

        return store_id

    def close_store(self, user_id: int, store_id: int):
        """
        * Parameters: userId, store_id
        * This function closes a store
        * Returns None
        """
        self.store_facade.close_store(store_id, user_id)

    def open_store(self, user_id: int, store_id: int):
        """
        * Parameters: userId, store_id
        * This function opens a store
        * Returns None
        """
        self.store_facade.open_store(store_id, user_id)

    def get_employees_info(self, user_id: int, store_id: int) -> Dict[int, str]:
        """
        * Parameters: userId, storeId
        * This function returns the employees of a store
        * Returns a dict of employees (user_id: role)
        """
        if not self.roles_facade.is_manager(store_id, user_id) and not self.roles_facade.is_owner(store_id, user_id):
            raise ValueError("User does not have the necessary permissions to get the employees of the store")
        return self.roles_facade.get_employees_info(store_id, user_id)

    # -------------Tags related methods-------------------#
    def add_tag_to_product(self, user_id: int, store_id: int, product_id: int, tag: str):
        """
        * Parameters: user_id, product_id, tag
        * This function adds a tag to a product specification
        * Returns None
        """
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError("User does not have the necessary permissions to add a tag to a product in the store")
        self.store_facade.add_tag_to_product(store_id, product_id, tag)

    def remove_tag_from_product(self, user_id: int, store_id: int, product_id: int, tag: str):
        """
        * Parameters: userId, productSpecId, tag
        * This function removes a tag from a product specification
        * Returns None
        """
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError("User does not have the necessary permissions to remove a tag to a product in the store")
        self.store_facade.remove_tag_from_product(store_id, product_id, tag)

    # -------------Product related methods-------------------#
    def change_product_price(self, user_id: int, store_id: int, product_id: int, new_price: float):
        """
        * Parameters: userId, store_id, product_id, newPrice
        * This function changes the price of a product
        * Returns None
        """
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError(
                "User does not have the necessary permissions to change the price of a product in the store")
        self.store_facade.change_price_of_product(store_id, product_id, new_price)

    def change_product_description(self, user_id: int, store_id: int, product_id: int, description: str):
        """
        * Parameters: user_id, product_id, description
        * This function changes the description of a product
        * Returns None
        """
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError("User is not a system manager")
        self.store_facade.change_description_of_product(store_id, product_id, description)

    def change_product_weight(self, user_id: int, store_id: int, product_id: int, weight: float):
        """
        * Parameters: user_id, store_id, product_id, weight
        * This function changes the weight of a product
        * Returns None
        """
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError("User is not an owner of the store")
        self.store_facade.change_weight_of_product(store_id, product_id, weight)

    # -------------Category related methods-------------------#
    def add_category(self, user_id: int, category_name: str) -> int:
        """
        * Parameters: userId, categoryName
        * This function adds a category to the system
        * Returns None
        """
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        return self.store_facade.add_category(category_name)

    def remove_category(self, user_id: int, category_id: int):
        """
        * Parameters: userId, categoryId
        * This function removes a category from the system
        * Returns None
        """
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        self.store_facade.remove_category(category_id)

    def add_sub_category_to_category(self, user_id: int, sub_category_id: int, parent_category_id: int):
        """
        * Parameters: userId, subCategoryId, parentCategoryId
        * This function adds a sub category to a category
        * NOTE: It is assumed that the subCategory is already created and exists in the system
        * Returns None
        """
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        self.store_facade.assign_sub_category_to_category(sub_category_id, parent_category_id)
        logger.info(f"User {user_id} has added a sub category to category {parent_category_id}")

    def remove_sub_category_from_category(self, user_id: int, category_id: int, sub_category_id: int):
        """
        * Parameters: userId, categoryId, subCategoryId
        * This function removes a sub category from a category
        * Returns None
        """
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        self.store_facade.delete_sub_category_from_category(category_id, sub_category_id)
        logger.info(f"User {user_id} has removed a sub category from category {category_id}")

    def assign_product_to_category(self, user_id: int, category_id: int, store_id: int, product_id: int):
        """
        * Parameters: user_id, category_id, product_id
        * This function assigns a product to a category
        * NOTE: it is assumed that the product exists in the system
        * Returns None
        """
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError("User does not have the necessary permissions to assign a product to a category")
        self.store_facade.assign_product_to_category(category_id, store_id, product_id)
        logger.info(f"User {user_id} has assigned a product to category {category_id}")

    def remove_product_from_category(self, user_id: int, category_id: int, store_id: int, product_id: int):
        """
        * Parameters: user_id, category_id, product_id
        * This function removes a product from a category
        * Returns None
        """
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError("User does not have the necessary permissions to remove a product from a category")
        self.store_facade.remove_product_from_category(category_id, store_id, product_id)
        logger.info(f"User {user_id} has removed a product from category {category_id}")

    # -------------PurchaseFacade methods:-------------------#

    # -------------Purchase management related methods-------------------#

    '''def create_bid_purchase(self, user_id: int, proposed_price: float, product_id: int, store_id: int):
        """
        * Parameters: userId, proposedPrice, productId, storeId
        * This function creates a bid purchase
        * Returns None
        """
        if not self.user_facade.is_member(user_id) or not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not a member or is not logged in")
        product = self.store_facade.get_store_by_id(store_id).get_product_by_id(product_id)
        product_spec_id = product.specification_id

        if self.purchase_facade.create_bid_purchase(user_id, proposed_price, product_id, product_spec_id, store_id):
            logger.info(f"User {user_id} has created a bid purchase")
            self.notifier.notify_new_bid(store_id, user_id)  # Notify each listener of the store about the bid
            # TODO: await for their reaction and handle them
        else:
            logger.info(f"User {user_id} has failed to create a bid purchase")

    def create_auction_purchase(self, user_id: int, base_price: float, starting_date: datetime, ending_date: datetime,
                                store_id: int, product_id: int):
        """
        * Parameters: userId, basePrice, startingDate, endingDate, productId, storeId
        * This function creates an auction purchase
        * Returns None
        """
        if not self.user_facade.is_member(user_id) or not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not a member or is not logged in")
        product = self.store_facade.get_store_by_id(store_id).get_product_by_id(product_id)
        product_spec_id = product.specification_id
        if self.purchase_facade.create_auction_purchase(base_price, starting_date, ending_date, store_id, product_id,
                                                        product_spec_id):
            logger.info(f"User {user_id} has created an auction purchase")

    def create_lottery_purchase(self, user_id: int, full_price: float, store_id: int, product_id: int,
                                starting_date: datetime, ending_date: datetime):
        """
        * Parameters: userId, fullPrice, storeId, productId, startingDate, endingDate
        * This function creates a lottery purchase
        * Returns None
        """
        if not self.user_facade.is_member(user_id) or not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not a member or is not logged in")
        product = self.store_facade.get_store_by_id(store_id).get_product_by_id(product_id)
        product_spec_id = product.specification_id
        if self.purchase_facade.create_lottery_purchase(user_id, full_price, store_id, product_id, product_spec_id,
                                                        starting_date, ending_date):
            logger.info(f"User {user_id} has created a lottery purchase")
        else:
            logger.info(f"User {user_id} has failed to create a lottery purchase")'''

    def view_purchases_of_user(self, user_id: int, requested_id: int, store_id: Optional[int]=None) -> List[PurchaseDTO]:
        """
        * Parameters: user_id
        * This function returns the purchases of a user
        * Returns a string
        """
        if not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a system manager")
        return self.purchase_facade.get_purchases_of_user(requested_id, store_id)

    def view_purchases_of_store(self, user_id: int, store_id: int) -> List[PurchaseDTO]:
        """
        * Parameters: userId, store_id
        * This function returns the purchases of a store
        * Returns a string
        """
        if not self.roles_facade.is_owner(store_id, user_id) and not self.roles_facade.is_manager(store_id, user_id) and not self.roles_facade.is_system_manager(user_id):
            raise ValueError("User is not a store owner or manager")
        return self.purchase_facade.get_purchases_of_store(store_id)

    '''def view_purchases_of_user_in_store(self, user_id: int, store_id: int) -> str:
        """
        * Parameters: userId, store_id
        * This function returns the purchases of a user in a store
        * Returns a string
        """
        if not self.user_facade.is_member(user_id) or not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not a member or is not logged in")
        purchases = self.purchase_facade.get_purchases_of_user(user_id)
        str_output = ""
        for purchase in purchases:
            if purchase.store_id == store_id:
                str_output += purchase.__str__()
        return str_output

    def view_on_going_purchases(self, user_id: int) -> str:
        """
        * Parameters: userId
        * This function returns the ongoing purchases
        * Returns a string
        """
        if not self.user_facade.is_member(user_id) or not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not a member or is not logged in")
        purchases = self.purchase_facade.get_on_going_purchases()
        str_output = ""
        for purchase in purchases:
            str_output += purchase.__str__()
        return str_output

    def view_completed_purchases(self, user_id: int) -> str:
        """
        * Parameters: userId
        * This function returns the completed purchases
        * Returns a string
        """
        if not self.user_facade.is_member(user_id) or not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not a member or is not logged in")
        purchases = self.purchase_facade.get_completed_purchases()
        str_output = ""
        for purchase in purchases:
            str_output += purchase.__str__()
        return str_output

    def view_failed_purchases(self, user_id: int) -> str:
        """
        * Parameters: userId
        * This function returns the failed purchases
        * Returns a string
        """
        if not self.user_facade.is_member(user_id) or not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not a member or is not logged in")
        purchases = self.purchase_facade.get_failed_purchases()
        str_output = ""
        for purchase in purchases:
            str_output += purchase.__str__()
        return str_output

    def view_accepted_purchases(self, user_id: int) -> str:
        """
        * Parameters: userId
        * This function returns the accepted purchases
        * Returns a string
        """
        if not self.user_facade.is_member(user_id) or not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not a member or is not logged in")
        purchases = self.purchase_facade.get_accepted_purchases()
        str_output = ""
        for purchase in purchases:
            str_output += purchase.__str__()
        return str_output

    def handle_accepted_purchases(self):
        """
        * Parameters: None
        * This function handles the accepted purchases
        * Returns None
        """
        accepted_purchases = self.purchase_facade.get_accepted_purchases()
        for purchase in accepted_purchases:
            if self.purchase_facade.check_if_completed_purchase(purchase.purchase_id):
                logger.info(f"Purchase {purchase.purchase_id} has been completed")'''

    # -------------Bid Purchase related methods-------------------#
    '''def store_accept_offer(self, purchase_id: int):
        pass  # cant be implemented yet without notifications

    def store_reject_offer(self, purchase_id: int):
        pass  # cant be implemented yet without notifications

    def store_counter_offer(self, new_price: float, purchase_id: int):
        pass  # cant be implemented yet without notifications

    def user_accept_offer(self, user_id: int, purchase_id: int):  # TODO
        """
        * Parameters: userId, purchase_id
        * This function accepts an offer
        * Returns None
        """
        if not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not logged in")
        self.purchase_facade.user_accept_offer(purchase_id, user_id)

        # notify the store owners and all relevant parties
        store_id = self.purchase_facade.get_purchase_by_id(purchase_id).store_id
        # Notify each listener of the store about the bid
        self.notifier.notify_general_listeners(store_id,
                                               f"User {user_id} has accepted the offer in purchase {purchase_id}")

    def user_reject_offer(self, user_id: int, purchase_id: int):
        """
        * Parameters: userId, purchase_id
        * This function rejects an offer
        * Returns None
        """
        if not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not logged in")
        self.purchase_facade.user_reject_offer(purchase_id, user_id)

        # notify the store owners and all relevant parties
        msg = f"User {user_id} has rejected the offer in purchase {purchase_id}"
        store_id = self.purchase_facade.get_purchase_by_id(purchase_id).store_id
        self.notifier.notify_general_listeners(store_id, msg)  # Notify each listener of the store about the bid

    def user_counter_offer(self, user_id: int, counter_offer: float, purchase_id: int):
        """
        * Parameters: userId, counterOffer, purchase_id
        * This function makes a counter offer
        * Returns None
        """
        if not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not logged in")
        self.purchase_facade.user_counter_offer(counter_offer, purchase_id)

        # notify the store owners and all relevant parties
        store_id = self.purchase_facade.get_purchase_by_id(purchase_id).store_id
        msg = f"User {user_id} has made a counter offer in purchase {purchase_id}"
        self.notifier.notify_general_listeners(store_id, msg)  # Notify each listener of the store about the bid'''

    # -------------Auction Purchase related methods-------------------#
    '''def add_auction_bid(self, purchase_id: int, user_id: int, price: float):
        """
        * Parameters: purchase_id, user_id, price
        * This function adds a bid to an auction purchase
        * Returns None
        """
        if not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not logged in")
        if self.purchase_facade.add_auction_bid(user_id, price, purchase_id):
            logger.info(f"User {user_id} has added a bid to purchase {purchase_id}")

            # notify the store owners and all relevant parties
            msg = f"User {user_id} has added a bid to purchase {purchase_id}"
            store_id = self.purchase_facade.get_purchase_by_id(purchase_id).store_id
            self.notifier.notify_general_listeners(store_id, msg)  # Notify each listener of the store about the bid
        else:
            logger.info(f"User {user_id} has failed to add a bid to purchase {purchase_id}")

    def view_highest_bid(self, purchase_id: int, user_id: int) -> float:
        """
        * Parameters: purchase_id, userId
        * This function returns the highest bid of an auction purchase
        * Returns a float
        """
        if not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not logged in")

        # notify the store owners and all relevant parties
        store_id = self.purchase_facade.get_purchase_by_id(purchase_id).store_id
        msg = f"User {user_id} has viewed the highest bid in purchase {purchase_id}"
        self.notifier.notify_general_listeners(store_id, msg)  # Notify each listener of the store about the bid

        return self.purchase_facade.view_highest_bidding_offer(purchase_id)

    def calculate_remaining_time_of_auction(self, purchase_id: int, user_id: int) -> timedelta:
        """
        * Parameters: purchase_id, userId
        * This function calculates the remaining time of an auction purchase
        * Returns a float
        """
        if not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not logged in")

        # TODO: notify the store owners and all relevant parties
        # NOTE: I did it, but why?
        store_id = self.purchase_facade.get_purchase_by_id(purchase_id).store_id
        msg = f"User {user_id} has calculated the remaining time of auction {purchase_id}"
        self.notifier.notify_general_listeners(store_id, msg)  # Notify each listener of the store about the bid

        return self.purchase_facade.calculate_remaining_time(purchase_id)

    def handle_ongoing_auctions(self):
        """
        * Parameters: None
        * This function handles the ongoing auctions
        * Returns None
        """
        ongoing_purchases = self.purchase_facade.get_on_going_purchases()
        for purchase in ongoing_purchases:
            # NOTE: what does "2" mean?, maybe we should use magic numbers
            # TODO: getPurchaseType does not exist in Purchase, should be added
            """if purchase.getPurchaseType(purchase.purchase_id()) == 2:
                if self.purchase_facade.check_if_auction_ended(purchase.purchase_id()):
                    #TODO: notify the store owners and all relevant parties

                    #TODO: notify the user who won the auction
                    #NOTE: How do we know who won the auction? 

                    #TODO: third party services
                    #if thirdparty services work, then:
                    #TODO: call validatePurchaseOfUser(purchase.get_purchaseId(), purchase.get_userId(), deliveryDate)
                    #else:
                    #TODO: call invalidatePurchase(purchase.get_purchaseId(), purchase.get_userId()
                    logger.info(f"Auction {purchase.purchase_id()} has been completed")"""'''

    # -------------Lottery Purchase related methods-------------------#
    '''def add_lottery_offer(self, user_id: int, proposed_price: float, purchase_id: int):
        """
        * Parameters: user_id, proposedPrice, purchase_id
        * This function adds a lottery ticket to a lottery purchase
        * Returns None
        """

        if not self.auth_facade.is_logged_in(user_id) or not self.user_facade.is_member(user_id):
            raise ValueError("User is not logged in or is not a member")

        if self.purchase_facade.add_lottery_offer(user_id, proposed_price, purchase_id):
            logger.info(f"User {user_id} has added a lottery ticket to purchase {purchase_id}")

            # notify the store owners and all relevant parties
            store_id = self.purchase_facade.get_purchase_by_id(purchase_id).store_id
            msg = f"User {user_id} has added a lottery ticket to purchase {purchase_id}"
            self.notifier.notify_general_listeners(store_id, msg)  # Notify each listener of the store about the bid

        else:
            logger.info(f"User {user_id} has failed to add a lottery ticket to purchase {purchase_id}")

    def calculate_remaining_time_of_lottery(self, purchase_id: int, user_id: int) -> timedelta:
        """
        * Parameters: purchase_id, userId
        * This function calculates the remaining time of a lottery purchase
        * Returns a float
        """
        if not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not logged in")

        remaining_time = self.purchase_facade.calculate_remaining_time(purchase_id)

        # notify the store owners and all relevant parties
        msg = f"The remaining time of lottery {purchase_id} is {remaining_time} of user {user_id}"
        store_id = self.purchase_facade.get_purchase_by_id(purchase_id).store_id
        self.notifier.notify_general_listeners(store_id, msg)  # Notify each listener of the store about the bid

        return remaining_time

    def calculate_probability_of_user(self, purchase_id: int, user_id: int) -> float:
        """
        * Parameters: purchase_id, user_id
        * This function calculates the probability of a user in a lottery purchase
        * Returns a float
        """
        if not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not logged in")

            # NOTE: I did it, but do we really need to notify the store owners and all relevant parties?
        # notify the store owners and all relevant parties

        probability = self.purchase_facade.calculate_probability_of_user(purchase_id, user_id)
        store_id = self.purchase_facade.get_purchase_by_id(purchase_id).store_id

        msg = f"The probability of user {user_id} in lottery {purchase_id} is {probability}"
        self.notifier.notify_general_listeners(store_id, msg)
        self.notifier.notify_general_message(user_id, msg)

        return probability

    def handle_ongoing_lotteries(self):
        """
        * Parameters: None
        * This function handles the ongoing lotteries
        * Returns None
        """
        ongoing_purchases = self.purchase_facade.get_on_going_purchases()
        for purchase in ongoing_purchases:
            # TODO: getPurchaseType does not exist in Purchase, should be added
            """if purchase.getPurchaseType(purchase.purchase_id()) == 3:
                if self.purchase_facade.validate_user_offers(purchase.purchase_id()):
                    userIdOfWinner = self.purchase_facade.pick_winner(purchase.purchase_id())
                    if userIdOfWinner is not None:
                        #notify the user who won the lottery
                        msg = "You have won the lottery on purchase" + purchase.purchase_id()
                        Notifier.notify_general_message(userIdOfWinner, msg)

                        #TODO: third party services
                        #if thirdparty services work, then:
                        #TODO: call validateDeliveryOfWinner(purchase.get_purchaseId(), purchase.get_userId(), deliveryDate)
                        #else:
                        #TODO: call invali  dateDeliveryOfWinner(purchase.get_purchaseId(), purchase.get_userId()
                        # logger.info(f"Lottery {purchase.get_purchaseId()} has been won!")
                    else:
                        #TODO: refund users who participated in the lottery
                        logger.info(f"Lottery {purchase.purchase_id()} has failed! Refunded all participants")"""'''

    def get_usersDTO_by_store(self, store_id: int) -> Dict[int, UserDTO]:
        roles = self.roles_facade.get_store_owners(store_id)
        return self.user_facade.get_users_dto(roles)
