from .user import UserFacade
from .authentication.authentication import Authentication
from .roles import RolesFacade
from .DTOs import AddressDTO, BidPurchaseDTO, NotificationDTO, PurchaseDTO, PurchaseProductDTO, StoreDTO, ProductDTO, UserDTO, \
    PurchaseUserDTO, UserInformationForConstraintDTO, RoleNominationDTO, NominationDTO, CategoryDTO
from .store import StoreFacade
from .purchase import PurchaseFacade
from .ThirdPartyHandlers import PaymentHandler, SupplyHandler
from .notifier import Notifier
from typing import List, Dict, Tuple, Optional
from datetime import date, datetime
import threading
from backend.error_types import *


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
            self.create_admin()

            # self.default_setup2()

    def test(self,user_id):
        self.notifier.send_real_time_notification(user_id, NotificationDTO(-1, "test", datetime.now()))
        logger.info("test notification sent")


    def create_admin(self, currency: str = "USD") -> None:
        if self.roles_facade.is_admin_created():
            return
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
        self.create_admin()

    def default_setup2(self):
        uid1 = self.user_facade.create_user("USD")

        uc1 = {
            "username": "user1",
            "password": "1234",
            "email": "example1@gmail.com",
            "year": 2001,
            "month": 2,
            "day": 2,
            "phone": "0522222222"
        }

        default_payment_method = {'payment method': 'bogo'}

        default_supply_method = "bogo"

        default_address_checkout = {'address': 'randomstreet 34th',
                                    'city': 'arkham',
                                    'state': 'gotham',
                                    'country': 'Wakanda',
                                    'zip_code': '12345'}

        self.auth_facade.register_user(uid1, uc1)

        store_id = self.add_store(uid1, "Rager 130", "Beer Sheva", "Israel", "Israel", "12345678", "store1")
        product1 = self.store_facade.add_product_to_store(store_id, "product1", "description1", 100, 1, ["tag1"], 10)

        #self.add_product_to_basket(0, store_id, 0, 1)

        #self.checkout(0, default_payment_method, default_supply_method, default_address_checkout)

    def default_setup(self):
        self.clean_data()

        # users:
        uid1 = self.user_facade.create_user("USD")
        uid2 = self.user_facade.create_user("USD")
        uid3 = self.user_facade.create_user("USD")
        uid4 = self.user_facade.create_user("USD")

        uc1 = {
            "username": "user1",
            "password": "1234",
            "email": "example1@gmail.com",
            "year": 2001,
            "month": 2,
            "day": 2,
            "phone": "0522222222"
        }

        uc2 = {
            "username": "user2",
            "password": "5678",
            "email": "example2@gmail.com",
            "year": 2002,
            "month": 2,
            "day": 2,
            "phone": "0522222222"
        }

        uc3 = {
            "username": "user3",
            "password": "5678",
            "email": "example3@gmail.com",
            "year": 2002,
            "month": 2,
            "day": 2,
            "phone": "0522222222"
        }

        uc4 = {
            "username": "user4",
            "password": "5678",
            "email": "example4@gmai.com",
            "year": 2002,
            "month": 2,
            "day": 2,
            "phone": "0522222222"
        }

        default_payment_method = {'payment method': 'bogo'}

        default_supply_method = {'supply method': 'bogo'}

        default_address_checkout = { 'address': 'randomstreet 34th', 
                                    'city': 'arkham', 
                                    'state': 'gotham',
                                    'country': 'Wakanda', 
                                    'zip_code': '12345'}

        self.auth_facade.register_user(uid1, uc1)
        self.auth_facade.register_user(uid2, uc2)
        self.auth_facade.register_user(uid3, uc3)
        self.auth_facade.register_user(uid4, uc4)
        
        # stores:
        store_id = self.add_store(uid1, "Rager 130","Beer Sheva","Israel","Israel","12345678","store1")
        product1 = self.store_facade.add_product_to_store(store_id, "product1", "description1", 100, 1, ["tag1"], 10)
        product2 = self.store_facade.add_product_to_store(store_id, "product2", "description2", 200, 2, ["tag1", "tag2"], 20)
        product3 = self.store_facade.add_product_to_store(store_id, "product3", "description3", 300, 3, ["tag2"], 30)
        product4 = self.store_facade.add_product_to_store(store_id, "product4", "description4", 400, 4, ["tag3", "tag4"], 40)

        store_id2 = self.add_store(uid1, "BGU","Beer Shave","Israel","Israel","99999999","store2")

        product5 = self.store_facade.add_product_to_store(store_id2, "product5", "description5", 500, 5, ["tag5"], 50)

        self.nominate_store_owner(store_id, uid1, "user2")
        self.accept_nomination(uid2, 0, True)

        self.nominate_store_manager(store_id, uid1, "user3")
        self.accept_nomination(uid3, 1, True)

        self.nominate_store_manager(store_id, uid2, "user4")
        self.accept_nomination(uid4, 2, True)

        self.change_permissions(uid1, store_id, uid4, True, True, False, True, False, False, True)


        # add 3 categories
        category1 = self.store_facade.add_category("category1")
        category2 = self.store_facade.add_category("category2")
        category3 = self.store_facade.add_category("sub-category1")
        self.store_facade.assign_sub_category_to_category(2, 0)
        
        # assign products to categories
        self.store_facade.assign_product_to_category(0, 0, 0)
        self.store_facade.assign_product_to_category(0, 0, 1)
        self.store_facade.assign_product_to_category(1, 0, 2)
        self.store_facade.assign_product_to_category(2, 0, 3)

        # user 2 adds product 1 to basket
        self.add_product_to_basket(uid2, 0, 0, 1)

        # user 2 checks out
        self.checkout(uid2, default_payment_method, default_supply_method, default_address_checkout)
        
         # add test notifications to admin
        self.notifier.notify_general_message(0, "test notification 1")
        self.notifier.notify_general_message(0, "test notification 2")
       

    def show_notifications(self, user_id: int) -> List[NotificationDTO]:
        return self.user_facade.get_notifications(user_id)

    def add_product_to_basket(self, user_id: int, store_id: int, product_id: int, amount: int):
        if self.store_facade.check_product_availability(store_id, product_id, amount):
            self.user_facade.add_product_to_basket(user_id, store_id, product_id, amount)
            logger.info(f"User {user_id} has added {amount} of product {product_id} to the basket")
        else:
            raise StoreError("Product is not available", StoreErrorTypes.product_not_available) 

    def remove_product_from_basket(self, user_id: int, store_id: int, product_id: int, amount: int):
        self.user_facade.remove_product_from_basket(user_id, store_id, product_id, amount)
        logger.info(f"User {user_id} has removed {amount} of product {product_id} from the basket")

    def checkout(self, user_id: int, payment_details: Dict, supply_details: Dict, address: Dict) -> int:
        products_removed = False
        purchase_accepted = False
        basket_cleared = False
        cart: Dict[int, Dict[int, int]] = {}  # store_id -> product_id -> amount
        pur_id = -1
        try:
            # Check if the user is suspended
            if self.user_facade.suspended(user_id):
                raise UserError("User is suspended", UserErrorTypes.user_suspended)

            cart = self.user_facade.get_shopping_cart(user_id)

            if not cart:
                raise StoreError("Cart is empty", StoreErrorTypes.cart_is_empty)

            user_dto = self.user_facade.get_userDTO(user_id)
            birthdate = None
            if user_dto.day is not None and user_dto.month is not None and user_dto.year is not None:
                birthdate = date(user_dto.year, user_dto.month, user_dto.day)
            user_purchase_dto = PurchaseUserDTO(user_dto.user_id, birthdate)

            if 'address' not in address or 'city' not in address or 'state' not in address or 'country' not in address or 'zip_code' not in address:
                raise ThirdPartyHandlerError("Address information is missing", ThirdPartyHandlerErrorTypes.missing_address)
            address_of_user_for_discount: AddressDTO = AddressDTO(address['address'],
                                                                  address['city'], address['state'],
                                                                  address['country'], address['zip_code'])


            user_info_for_constraint_dto = UserInformationForConstraintDTO(user_id, user_purchase_dto.birthdate,
                                                                       address_of_user_for_discount)
            # calculate the total price
            if not self.store_facade.validate_purchase_policies(cart, user_info_for_constraint_dto):
                raise StoreError("Purchase policies are not met", StoreErrorTypes.policy_not_satisfied)
            

            total_price = self.store_facade.get_total_price_before_discount(cart)

            total_price_after_discounts = self.store_facade.get_total_price_after_discount(cart,
                                                                                           user_info_for_constraint_dto)

            # purchase facade immediate
            purchase_shopping_cart: Dict[int, Tuple[List[PurchaseProductDTO], float, float]] = (
                self.store_facade.get_purchase_shopping_cart(user_info_for_constraint_dto, cart))

            pur_id = self.purchase_facade.create_immediate_purchase(user_id, total_price, total_price_after_discounts,
                                                                    purchase_shopping_cart)

            # remove the products from the store
            self.store_facade.check_and_remove_shopping_cart(cart)

            products_removed = True

            # find the delivery date
            if "supply method" not in supply_details:
                raise ThirdPartyHandlerError("Supply method not specified", ThirdPartyHandlerErrorTypes.support_not_specified)
            if supply_details.get("supply method") not in SupplyHandler().supply_config:
                raise ThirdPartyHandlerError("Invalid supply method", ThirdPartyHandlerErrorTypes.invalid_supply_method)
            package_details = {'stores': cart.keys(), "supply method": supply_details["supply method"]}
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
                raise ThirdPartyHandlerError("Payment method not specified", ThirdPartyHandlerErrorTypes.payment_not_specified)

            payment_id = PaymentHandler().process_payment(total_price_after_discounts, payment_details)

            if payment_id == -1:
                # invalidate Purchase
                # self.purchase_facade.invalidate_purchase_of_user_immediate(purchase.purchase_id, user_id)
                raise ThirdPartyHandlerError("Payment failed", ThirdPartyHandlerErrorTypes.payment_failed)

            on_arrival = lambda purchase_id: self.on_arrival_lambda(purchase_id)
            supply_details["arrival time"] = delivery_date
            supply_details["purchase id"] = pur_id
            supply_id = SupplyHandler().process_supply(supply_details, user_id, on_arrival)
            if supply_id == -1:
                # invalidate Purchase
                # self.purchase_facade.invalidate_purchase_of_user_immediate(purchase.purchase_id, user_id)
                raise ThirdPartyHandlerError("Supply failed", ThirdPartyHandlerErrorTypes.supply_failed)

            # notify the store owners
            for store_id in cart.keys():
                self.notifier.notify_new_purchase(store_id, pur_id)

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
            # check if payment_id is defined
            if "payment_id" in locals() and payment_id != -1:
                PaymentHandler().process_payment_cancel(payment_details, payment_id)
            if "supply_id" in locals() and supply_id != -1:
                SupplyHandler().process_supply_cancel(supply_details, supply_id)
            raise e

    def on_arrival_lambda(self, purchase_id: int):
        from backend.app import app
        with app.app_context():
            self.purchase_facade.complete_purchase(purchase_id)

    def get_stores(self, page: int, limit: int) -> Dict[int, StoreDTO]:
        return self.store_facade.get_stores(page, limit)
    
    def get_all_stores(self, user_id)-> Dict[int, StoreDTO]:
        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        return self.store_facade.get_all_stores()

    def nominate_store_owner(self, store_id: int, owner_id: int, new_owner_username):
        if self.user_facade.suspended(owner_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)

        # get user_id of new_owner_username
        new_owner_id = self.user_facade.get_user_id_from_username(new_owner_username)

        # nominate the new owner
        nomination_id = self.roles_facade.nominate_owner(store_id, owner_id, new_owner_id)

        # send notification to the new owner
        notification = NotificationDTO(-1, f"You have been nominated to be the owner of store"
                                           f" {store_id}. nomination id: {nomination_id} ",
                                       datetime.now())

        self.notifier.notify_general_message(new_owner_id, notification.get_message())

        logger.info(f"User {owner_id} has nominated user {new_owner_id} to be the owner of store {store_id}")

    def nominate_store_manager(self, store_id: int, owner_id: int, new_manager_username):
        if self.user_facade.suspended(owner_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        # get user_id of new_manager_username
        new_manager_id = self.user_facade.get_user_id_from_username(new_manager_username)

        # nominate the new manager
        nomination_id = self.roles_facade.nominate_manager(store_id, owner_id, new_manager_id)

        # send notification to the new manager
        notification = NotificationDTO(-1, f"You have been nominated to be the manager of store"
                                           f" {store_id}. nomination id: {nomination_id} ",
                                       datetime.now())
        self.notifier.notify_general_message(new_manager_id, notification.get_message())

        logger.info(f"User {owner_id} has nominated user {new_manager_id} to be the manager of store {store_id}")

    def accept_nomination(self, user_id: int, nomination_id: int, accept: bool):
        if accept:
            self.roles_facade.accept_nomination(nomination_id, user_id)
        else:
            self.roles_facade.decline_nomination(nomination_id, user_id)

    def change_permissions(self, actor_id: int, store_id: int, manager_id: int, add_product: bool,
                           change_purchase_policy: bool, change_purchase_types: bool, change_discount_policy: bool,
                           change_discount_types: bool, add_manager: bool, get_bid: bool):
        if self.user_facade.suspended(actor_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        self.roles_facade.set_manager_permissions(store_id, actor_id, manager_id, add_product, change_purchase_policy,
                                                  change_purchase_types, change_discount_policy, change_discount_types,
                                                  add_manager, get_bid)

        logger.info(f"User {actor_id} has changed the permissions of user {manager_id} in store {store_id}")

    def remove_store_role(self, actor_id: int, store_id: int, username: str):
        if self.user_facade.suspended(actor_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        user_id = self.user_facade.get_user_id_from_username(username)
        self.roles_facade.remove_role(store_id, actor_id, user_id)
        logger.info(f"User {actor_id} has removed user {user_id} from store {store_id}")

    def give_up_role(self, actor_id: int, store_id: int):
        if self.user_facade.suspended(actor_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        self.roles_facade.remove_role(store_id, actor_id, actor_id)
        logger.info(f"User {actor_id} has given up his role in store {store_id}")

    def remove_system_manager(self, actor: int, user_id: int):
        """"
        Removes a system manager from the system
        """
        if self.user_facade.suspended(actor):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        self.roles_facade.remove_system_manager(actor, user_id)
        logger.info(f"User {actor} has removed user {user_id} as a system manager")

    def suspend_user_permanently(self, actor_id: int, user_id: int):
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.is_system_manager(actor_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        
        self.user_facade.suspend_user_permanently(user_id)
        logger.info(f"User {actor_id} has suspended user {user_id} permanently")

    def suspend_user_temporarily(self, actor_id: int, user_id: int, date_details: dict, time_details: dict):
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.is_system_manager(actor_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        
        self.user_facade.suspend_user_temporarily(user_id, date_details, time_details)
        logger.info(f"User {actor_id} has suspended user {user_id} temporarily")

    def unsuspend_user(self, actor_id: int, user_id: int):
        if self.user_facade.suspended(actor_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.is_system_manager(actor_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        
        self.user_facade.unsuspend_user(user_id)
        logger.info(f"User {actor_id} has unsuspended user {user_id}")

    def show_suspended_users(self, actor_id: int):
        if self.user_facade.suspended(actor_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.is_system_manager(actor_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        
        return self.user_facade.get_suspended_users()

    def add_system_manager(self, actor: int, username: str):
        if self.user_facade.suspended(actor):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
          
        user_id = self.user_facade.get_user_id_from_username(username)
        if self.user_facade.suspended(user_id):
            raise UserError("New wanted system manager is suspended", UserErrorTypes.user_suspended)
            
        self.roles_facade.add_system_manager(actor, user_id)
        logger.info(f"User {actor} has added user {user_id} as a system manager")

    def get_user_nominations(self, user_id: int):
        nominations = self.roles_facade.get_user_nominations(user_id)
        ret = {}
        for nid, nomination in nominations.items():
            ret[nid] = NominationDTO(nid, nomination.store_id,
                                     self.store_facade.get_store_info(nomination.store_id).store_name,
                                     nomination.nominator_id,
                                     self.user_facade.get_userDTO(nomination.nominator_id, "").username,
                                     user_id, nomination.role)
        return ret


    def add_payment_method(self, user_id: int, method_name: str, payment_config: Dict):
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        
        PaymentHandler().add_payment_method(method_name, payment_config)
        logger.info(f"User {user_id} has added payment method {method_name}")

    def edit_payment_method(self, user_id: int, method_name: str, editing_data: Dict):
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)

        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        PaymentHandler().edit_payment_method(method_name, editing_data)
        logger.info(f"User {user_id} has edited payment method {method_name}")

    def remove_payment_method(self, user_id: int, method_name: str):
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)

        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        PaymentHandler().remove_payment_method(method_name)
        logger.info(f"User {user_id} has removed payment method {method_name}")

    def add_supply_method(self, user_id: int, method_name: str, supply_config: Dict):
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        SupplyHandler().add_supply_method(method_name, supply_config)

    def edit_supply_method(self, user_id: int, method_name: str, editing_data: Dict):
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        SupplyHandler().edit_supply_method(method_name, editing_data)

    def remove_supply_method(self, user_id: int, method_name: str):
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
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

    def get_product_info(self, store_id: int, product_id: int) -> Tuple[ProductDTO, str]:
        """
        * Parameters: storeId, productId
        * This function returns the product information
        * Returns the product information
        """
        products = self.get_store_product_info(store_id)
        store_name = self.get_store_info(store_id).store_name
        for product in products:
            if product.product_id == product_id:
                return product, store_name
        raise StoreError("Product not found", StoreErrorTypes.product_not_found)


    # -------------Discount related methods-------------------#
    def add_discount(self, user_id: int, description: str, start_date: datetime, end_date: datetime, percentage: float,
                     store_id: int, product_id: Optional[int] = None,
                     category_id: Optional[int] = None, applied_to_sub: Optional[bool] = None) -> int:
        """
        * Parameters: userId, description, startDate, endDate, percentage, storeId(optional), productId(optional), categoryId(optional), appliedToSub(optional)
        * This function adds a simple discount to the system
        *NOTE: the discount is initialized with no predicate!
        * Returns none
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.has_change_discount_policy_permission(store_id, user_id):
            raise UserError("User does not have necessary permissions to manage discount", UserErrorTypes.user_does_not_have_necessary_permissions)
        return self.store_facade.add_discount(description, store_id, start_date, end_date, percentage, category_id,
                                              product_id, applied_to_sub)

    def create_logical_composite_discount(self, user_id: int, store_id: int, description: str, start_date: datetime,
                                          end_date: datetime, discount_id1: int, discount_id2: int,
                                          type_of_composite: int) -> int:
        """
        * Parameters: userId, description, startDate, endDate, discountId1, discountId2, typeOfComposite
        * This function creates a composite discount
        * NOTE: the percentage of a composite discount is initialized to 0.0 since it is not used
        * NOTE: type_of_connection: 1 is AND, 2 OR, 3 XOR
        * Returns none
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.has_change_discount_policy_permission(store_id, user_id):
            raise UserError("User does not have necessary permissions to manage discount", UserErrorTypes.user_does_not_have_necessary_permissions)
        return self.store_facade.create_logical_composite_discount(description, store_id, start_date, end_date, 0.0, discount_id1,
                                                                   discount_id2, type_of_composite)

    def create_numerical_composite_discount(self, user_id: int, store_id: int, description: str, start_date: datetime,
                                            end_date: datetime, discount_ids: List[int], type_of_composite: int) -> int:
        """
        * Parameters: userId, description, startDate, endDate, discountIds, typeOfComposite
        * This function creates a composite discount
        * NOTE: the percentage of a composite discount is initialized to 0.0 since it is not used
        * NOTE: type_of_connection: 1 is MAX, 2 is ADDITIVE
        * Returns none
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.has_change_discount_policy_permission(store_id, user_id):
            raise UserError("User does not have necessary permissions to manage discount", UserErrorTypes.user_does_not_have_necessary_permissions)
        return self.store_facade.create_numerical_composite_discount(description, store_id, start_date, end_date, 0.0,
                                                                     discount_ids, type_of_composite)

    def assign_predicate_to_discount(self, user_id: int, discount_id: int, store_id:int, predicate_properties: Tuple) -> None:
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.has_change_discount_policy_permission(store_id, user_id):
            logger.warning(f"User {user_id} does not have permissions to assign a predicate to a discount")
            raise UserError("User does not have necessary permissions to manage discount", UserErrorTypes.user_does_not_have_necessary_permissions)
        self.store_facade.assign_predicate_to_discount(discount_id, predicate_properties)

    def change_discount_percentage(self, user_id: int, discount_id: int, store_id: int, new_percentage: float) -> None:
        """
        * Parameters: userId, discountId, newPercentage
        * This function changes the percentage of a discount
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.has_change_discount_policy_permission(store_id, user_id):
            logger.warning(f"User {user_id} does not have permissions to change the percentage of a discount")
            raise UserError("User does not have necessary permissions to manage discount", UserErrorTypes.user_does_not_have_necessary_permissions)
        self.store_facade.change_discount_percentage(discount_id, new_percentage)

    def change_discount_description(self, user_id: int, discount_id: int, store_id: int, new_description: str) -> None:
        """
        * Parameters: userId, discountId, newDescription
        * This function changes the description of a discount
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.roles_facade.has_change_discount_policy_permission(store_id, user_id):
            logger.warning(f"User {user_id} does not have permissions to change the description of a discount")
            raise UserError("User does not have necessary permissions to manage discount", UserErrorTypes.user_does_not_have_necessary_permissions)

        self.store_facade.change_discount_description(discount_id, new_description)

    def remove_discount(self, user_id: int, discount_id: int, store_id: int) -> None:
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.has_change_discount_policy_permission(store_id, user_id):
            raise UserError("User does not have necessary permissions to manage discount", UserErrorTypes.user_does_not_have_necessary_permissions)
        if self.store_facade.remove_discount(discount_id):
            logger.info(f"User {user_id} has removed a discount")
        else:
            logger.info(f"User {user_id} has failed to remove a discount")

    def view_all_discount_information_of_store(self, user_id: int, store_id: int) -> dict:
        """
        * This function returns all the discount information
        * Returns a list of dictionaries
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.has_change_discount_policy_permission(store_id, user_id):
            raise UserError("User does not have necessary permissions to manage discount", UserErrorTypes.user_does_not_have_necessary_permissions)
        return self.store_facade.view_all_discount_information_of_store(store_id)
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
    def add_purchase_policy(self, user_id: int, store_id: int, policy_name: str, category_id: Optional[int] = None, product_id: Optional[int] = None) -> int:
        """
        * Parameters: userId, store_id, policy_name, categoryId(optional), productId(optional)
        * This function adds a purchase policy to the store
        * Returns int of the policy id
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if self.roles_facade.has_change_purchase_policy_permission(store_id, user_id):
            toreturn = self.store_facade.add_purchase_policy_to_store(store_id, policy_name,category_id, product_id)
            logger.info(f"User {user_id} has added a policy to store {store_id}")
            return toreturn
            
        else:
            raise UserError("User does not have the necessary permissions to add a policy to the store", UserErrorTypes.user_does_not_have_necessary_permissions)

    def remove_purchase_policy(self, user_id, store_id: int, policy_id: int) -> None:
        """
        * Parameters: store_id, policy_name
        * This function removes a purchase policy from the store
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if self.roles_facade.has_change_purchase_policy_permission(store_id, user_id):
            self.store_facade.remove_purchase_policy_from_store(store_id, policy_id)
            logger.info(f"User {user_id} has removed a policy from store {store_id}")
        else:
            raise UserError("User does not have the necessary permissions to remove a policy from the store", UserErrorTypes.user_does_not_have_necessary_permissions)
    
    def create_composite_purchase_policy(self, user_id: int, store_id: int, policy_name: str, left_policy_id: int, right_policy_id: int, type_of_composite: int) -> int:
        """
        * Parameters: userId, store_id, policy_name, left_policy_id, right_policy_id, type_of_composite
        * This function creates a composite purchase policy
        * NOTE: type_of_connection: 1 is AND, 2 OR, 3 XOR
        * Returns int of the policy id
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if self.roles_facade.has_change_purchase_policy_permission(store_id, user_id):
            toreturn = self.store_facade.create_composite_purchase_policy_to_store(store_id, policy_name, left_policy_id, right_policy_id, type_of_composite)
            logger.info(f"User {user_id} has created a composite policy in store {store_id}")
            return toreturn
        else:
            raise UserError("User does not have the necessary permissions to create a composite policy in the store", UserErrorTypes.user_does_not_have_necessary_permissions)
    
    
    def assign_predicate_to_purchase_policy(self, user_id: int, store_id: int, policy_id: int, predicate_properties: Tuple) -> None:
        if self.user_facade.suspended(user_id):
            logger.warn(f"User {user_id} is suspended")
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if self.roles_facade.has_change_purchase_policy_permission(store_id, user_id):
            self.store_facade.assign_predicate_to_purchase_policy(store_id, policy_id, predicate_properties)
        else:
            raise UserError("User does not have the necessary permissions to assign a predicate to a policy in the store", UserErrorTypes.user_does_not_have_necessary_permissions)
        

    def view_all_policies_of_store(self, user_id: int , store_id:int) -> dict:
        """
        * Parameters: user_id, store_id
        * This function returns all the purchase policies of a store
        * Returns a dict of policies
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if self.roles_facade.has_change_purchase_policy_permission(store_id, user_id) or self.roles_facade.is_owner(store_id, user_id):
            return self.store_facade.view_all_purchase_policies_of_store(store_id)
        else:
            raise UserError("User does not have the necessary permissions to view the policies of the store", UserErrorTypes.user_does_not_have_necessary_permissions)
       
    # -------------Products related methods-------------------#
    def add_product(self, user_id: int, store_id: int, product_name: str, description: str, price: float,
                    weight: float, tags: List[str], amount: Optional[int] = 0) -> int:
        """
        * Parameters: user_id, store_id, productSpecId, expirationDate, condition, price
        * This function adds a product to the store
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to add a product to the store", UserErrorTypes.user_does_not_have_necessary_permissions)
        return self.store_facade.add_product_to_store(store_id, product_name, description, price, weight, tags, amount)

    def remove_product(self, user_id: int, store_id: int, product_id: int):
        """
        * Parameters: store_id, product_id
        * This function removes a product from the store
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to remove a product from the store", UserErrorTypes.user_does_not_have_necessary_permissions)
        self.store_facade.remove_product_from_store(store_id, product_id)

    def add_product_amount(self, user_id: int, store_id: int, product_id: int, amount: int):
        """
        * Parameters: userId, store_id, product_id, amount
        * This function adds an amount of a product to the store
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to add an amount of a product to the store", UserErrorTypes.user_does_not_have_necessary_permissions)
        self.store_facade.add_product_amount(store_id, product_id, amount)

    def remove_product_amount(self, user_id: int, store_id: int, product_id: int, amount: int):
        """
        * Parameters: userId, store_id, product_id, amount
        * This function removes an amount of a product from the store
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to remove an amount of a product from the "
                             "store", UserErrorTypes.user_does_not_have_necessary_permissions)
        self.store_facade.remove_product_amount(store_id, product_id, amount)

    # -------------Store related methods-------------------#
    def add_store(self, founder_id: int, address: str, city: str, state: str, country: str, zip_code: str, store_name: str) -> int:
        """
        * Parameters: founderId, address, storeName
        * This function adds a store to the system
        * Returns None
        """
        # TODO: add transaction
        if self.user_facade.suspended(founder_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        
        if not self.user_facade.is_member(founder_id):
            raise UserError("User is not a member", UserErrorTypes.user_not_a_member)

        address_of_store: AddressDTO = AddressDTO(address, city, state, country, zip_code)
        store_id = self.store_facade.add_store(address_of_store, store_name, founder_id)
        self.roles_facade.add_store(store_id, founder_id)
        # Notifier().sign_listener(founder_id, store_id) -- already happened inside roles.add_store()

        return store_id

    def close_store(self, user_id: int, store_id: int):
        """
        * Parameters: userId, store_id
        * This function closes a store
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        self.store_facade.close_store(store_id, user_id)
        self.notifier.notify_update_store_status(store_id, True)

    def open_store(self, user_id: int, store_id: int):
        """
        * Parameters: userId, store_id
        * This function opens a store
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        self.store_facade.open_store(store_id, user_id)
        self.notifier.notify_update_store_status(store_id, False)

    def get_employees_info(self, user_id: int, store_id: int) -> Dict[int, str]:
        """
        * Parameters: userId, storeId
        * This function returns the employees of a store
        * Returns a dict of employees (user_id: role)
        """
        if not self.roles_facade.is_manager(store_id, user_id) and not self.roles_facade.has_add_manager_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to get the employees of the store", UserErrorTypes.user_does_not_have_necessary_permissions)
        return self.roles_facade.get_employees_info(store_id, user_id)

    # -------------Tags related methods-------------------#
    def add_tag_to_product(self, user_id: int, store_id: int, product_id: int, tag: str):
        """
        * Parameters: user_id, product_id, tag
        * This function adds a tag to a product specification
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to add a tag to a product in the store", UserErrorTypes.user_does_not_have_necessary_permissions)
        self.store_facade.add_tag_to_product(store_id, product_id, tag)

    def remove_tag_from_product(self, user_id: int, store_id: int, product_id: int, tag: str):
        """
        * Parameters: userId, productSpecId, tag
        * This function removes a tag from a product specification
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to remove a tag to a product in the store", UserErrorTypes.user_does_not_have_necessary_permissions)
        self.store_facade.remove_tag_from_product(store_id, product_id, tag)

    # -------------Product related methods-------------------#
    def change_product_price(self, user_id: int, store_id: int, product_id: int, new_price: float):
        """
        * Parameters: userId, store_id, product_id, newPrice
        * This function changes the price of a product
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise UserError(
                "User does not have the necessary permissions to change the price of a product in the store", UserErrorTypes.user_does_not_have_necessary_permissions)
        self.store_facade.change_price_of_product(store_id, product_id, new_price)

    def change_product_description(self, user_id: int, store_id: int, product_id: int, description: str):
        """
        * Parameters: user_id, product_id, description
        * This function changes the description of a product
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to change the price of a product in the store", UserErrorTypes.user_does_not_have_necessary_permissions)
        self.store_facade.change_description_of_product(store_id, product_id, description)

    def change_product_weight(self, user_id: int, store_id: int, product_id: int, weight: float):
        """
        * Parameters: user_id, store_id, product_id, weight
        * This function changes the weight of a product
        * Returns None
        """
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to change the price of a product in the store", UserErrorTypes.user_does_not_have_necessary_permissions)
        self.store_facade.change_weight_of_product(store_id, product_id, weight)

    # -------------Category related methods-------------------#
    def add_category(self, user_id: int, category_name: str) -> int:
        """
        * Parameters: userId, categoryName
        * This function adds a category to the system
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        return self.store_facade.add_category(category_name)

    def remove_category(self, user_id: int, category_id: int):
        """
        * Parameters: userId, categoryId
        * This function removes a category from the system
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        self.store_facade.remove_category(category_id)

    def add_sub_category_to_category(self, user_id: int, sub_category_id: int, parent_category_id: int):
        """
        * Parameters: userId, subCategoryId, parentCategoryId
        * This function adds a sub category to a category
        * NOTE: It is assumed that the subCategory is already created and exists in the system
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        self.store_facade.assign_sub_category_to_category(sub_category_id, parent_category_id)
        logger.info(f"User {user_id} has added a sub category to category {parent_category_id}")

    def remove_sub_category_from_category(self, user_id: int, category_id: int, sub_category_id: int):
        """
        * Parameters: userId, categoryId, subCategoryId
        * This function removes a sub category from a category
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        self.store_facade.delete_sub_category_from_category(category_id, sub_category_id)
        logger.info(f"User {user_id} has removed a sub category from category {category_id}")

    def assign_product_to_category(self, user_id: int, category_id: int, store_id: int, product_id: int):
        """
        * Parameters: user_id, category_id, product_id
        * This function assigns a product to a category
        * NOTE: it is assumed that the product exists in the system
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to assign a product to a category", UserErrorTypes.user_does_not_have_necessary_permissions)
        self.store_facade.assign_product_to_category(category_id, store_id, product_id)
        logger.info(f"User {user_id} has assigned a product to category {category_id}")

    def remove_product_from_category(self, user_id: int, category_id: int, store_id: int, product_id: int):
        """
        * Parameters: user_id, category_id, product_id
        * This function removes a product from a category
        * Returns None
        """
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to remove a product from a category", UserErrorTypes.user_does_not_have_necessary_permissions)
        self.store_facade.remove_product_from_category(category_id, store_id, product_id)
        logger.info(f"User {user_id} has removed a product from category {category_id}")

    # -------------Bid Related methods:-------------------#
    def bid_checkout(self, user_id: int, bid_id: int,  payment_details: Dict, supply_details: Dict, address: Dict) -> int:
        product_removed = False
        purchase_accepted = False
        try:
            # Check if the user is suspended
            if self.user_facade.suspended(user_id):
                raise UserError("User is suspended", UserErrorTypes.user_suspended)
            # Get the bid
            bid = self.purchase_facade.get_bid_purchase_by_id(bid_id)
            if not self.purchase_facade.is_bid_approved(bid_id):
                raise PurchaseError("Bid is not approved", PurchaseErrorTypes.purchase_not_approved)
            
            cart: Dict[int, Dict[int, int]] = {bid.store_id: {bid.product_id: 1}} 

            user_dto = self.user_facade.get_userDTO(user_id)
            birthdate = None
            if user_dto.day is not None and user_dto.month is not None and user_dto.year is not None:
                birthdate = date(user_dto.year, user_dto.month, user_dto.day)
            user_purchase_dto = PurchaseUserDTO(user_dto.user_id, birthdate)

            if 'address' not in address or 'city' not in address or 'state' not in address or 'country' not in address or 'zip_code' not in address:
                raise ThirdPartyHandlerError("Address information is missing", ThirdPartyHandlerErrorTypes.missing_address)
            address_of_user_for_discount: AddressDTO = AddressDTO(address['address'],
                                                                  address['city'], address['state'],
                                                                  address['country'], address['zip_code'])


            user_info_for_constraint_dto = UserInformationForConstraintDTO(user_id, user_purchase_dto.birthdate,
                                                                       address_of_user_for_discount)
            # calculate the total price
            if not self.store_facade.validate_purchase_policies(cart, user_info_for_constraint_dto):
                raise StoreError("Purchase policies are not met", StoreErrorTypes.policy_not_satisfied)
            

            total_price = bid.proposed_price

            # remove the products from the store
            self.store_facade.check_and_remove_shopping_cart(cart)

            product_removed = True

            # find the delivery date
            if "supply method" not in supply_details:
                raise ThirdPartyHandlerError("Supply method not specified", ThirdPartyHandlerErrorTypes.support_not_specified)
            if supply_details.get("supply method") not in SupplyHandler().supply_config:
                raise ThirdPartyHandlerError("Invalid supply method", ThirdPartyHandlerErrorTypes.invalid_supply_method)
            package_details = {'stores': cart.keys(), "supply method": supply_details["supply method"]}
            delivery_date = SupplyHandler().get_delivery_time(package_details, address)

            # accept the purchase
            self.purchase_facade.accept_purchase(bid_id, delivery_date)
            purchase_accepted = True

            # TODO: fix discounts
            if "payment method" not in payment_details:
                # self.purchase_facade.invalidate_purchase_of_user_immediate(purchase.purchase_id, user_id)
                raise ThirdPartyHandlerError("Payment method not specified", ThirdPartyHandlerErrorTypes.payment_not_specified)

            payment_id = PaymentHandler().process_payment(total_price, payment_details)

            if payment_id == -1:
                # invalidate Purchase
                # self.purchase_facade.invalidate_purchase_of_user_immediate(purchase.purchase_id, user_id)
                raise ThirdPartyHandlerError("Payment failed", ThirdPartyHandlerErrorTypes.payment_failed)

            on_arrival = lambda purchase_id: self.on_arrival_lambda(purchase_id)
            supply_details["arrival time"] = delivery_date
            supply_details["purchase id"] = bid_id
            supply_id = SupplyHandler().process_supply(supply_details, user_id, on_arrival)
            if supply_id == -1:
                # invalidate Purchase
                # self.purchase_facade.invalidate_purchase_of_user_immediate(purchase.purchase_id, user_id)
                raise ThirdPartyHandlerError("Supply failed", ThirdPartyHandlerErrorTypes.supply_failed)

            # notify the store owners
            for store_id in cart.keys():
                self.notifier.notify_new_purchase(store_id, bid_id)

            logger.info(f"User {user_id} has checked out")
            return bid_id
        except Exception as e:
            if product_removed:
                for store_id, products in cart.items():
                    for product_id in products:
                        amount = products[product_id]
                        self.store_facade.add_product_amount(store_id, product_id, amount)
            if purchase_accepted:
                self.purchase_facade.cancel_accepted_purchase(bid_id)
            # check if payment_id is defined
            if "payment_id" in locals() and payment_id != -1:
                PaymentHandler().process_payment_cancel(payment_details, payment_id)
            if "supply_id" in locals() and supply_id != -1:
                SupplyHandler().process_supply_cancel(supply_details, supply_id)
            raise e
    
    #TODO: send a notification to all store workers under the store_id to accept/decline/counter the bid
    def user_bid_offer(self, user_id: int, proposed_price: float, store_id: int, product_id: int) -> int:
        """
        Parameters: userId, proposedPrice, storeId, productId
        This function creates a bid purchase
        Returns the id of the bid purchase
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        pur_id = self.purchase_facade.create_bid_purchase(user_id, proposed_price, product_id, store_id)
        logger.info(f"User {user_id} has created a bid purchase")
        return pur_id
        
    
    def store_worker_accept_bid(self, store_id: int, store_worker_id: int, bid_id: int) -> None:
        """
        Parameters: store_worker_id, bidId
        This function accepts a bid
        Returns None
        """
        if self.user_facade.suspended(store_worker_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if self.roles_facade.has_get_bid_permission(store_id, store_worker_id):
            self.purchase_facade.store_owner_manager_accept_offer(bid_id, store_worker_id)
            logger.info(f"Store worker {store_worker_id} has accepted a bid")
            
            #checking if all store owners/managers accepted the bid now
            list_of_workers_in_store_with_bid_permissions = self.roles_facade.get_bid_owners_managers(store_id) #TODO
            if self.purchase_facade.store_accept_offer(bid_id, list_of_workers_in_store_with_bid_permissions):
                logger.info(f"Store {store_id} has accepted the bid") #TODO SEND A NOTIF TO USER THAT STORE ACCEPTED AND TO PROCEED TO CHECKOUT

        else:
            raise UserError("User does not have the necessary permissions to accept a bid", UserErrorTypes.user_does_not_have_necessary_permissions)
        
    
    #TODO: remove all notifications of store workers who have not yet accepted the bid and send to them all that the bid is declined, also send a notif to the user that the bid is declined
    def store_worker_decline_bid(self, store_id: int, store_worker_id: int, bid_id: int) -> int:
        """
        Parameters: store_worker_id, bidId
        This function declines a bid
        Returns the id of the user who rejected the bid
        """
        if self.user_facade.suspended(store_worker_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if self.roles_facade.has_get_bid_permission(store_id, store_worker_id):
            rejected = self.purchase_facade.store_reject_offer(bid_id, store_worker_id)
            logger.info(f"Store worker {store_worker_id} has declined a bid")
            return rejected
        else:
            raise UserError("User does not have the necessary permissions to decline a bid", UserErrorTypes.user_does_not_have_necessary_permissions)
    
    
    #TODO: send a notification to the user that the bid is counter offered and ask the user to accept/decline the counter offer, also remove all notifications of store workers who have not yet accepted the bid and send to them all that the bid is counter offered
    def store_worker_counter_bid(self, store_id: int, store_worker_id: int, bid_id: int, counter_price: float) -> None:
        """
        Parameters: store_worker_id, bidId, counterPrice
        This function counter offers a bid
        Returns None
        """
        if self.user_facade.suspended(store_worker_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if self.roles_facade.has_get_bid_permission(store_id, store_worker_id):
            self.purchase_facade.store_counter_offer(bid_id, store_worker_id, counter_price)
            logger.info(f"Store worker {store_worker_id} has counter offered a bid")
        else:
            raise UserError("User does not have the necessary permissions to counter offer a bid", UserErrorTypes.user_does_not_have_necessary_permissions)

    #TODO send a notification to all store workers under the store_id to accept/decline/counter the new proposed bid, 
    #TODO NO NEED TO SEND TO THE STORE_WORKER THAT HAS COUNTERED THE BID THE NOTIFICATION.
    def user_counter_bid_accept(self, user_id: int, bid_id: int) -> None:
        """
        Parameters: userId, bidId
        This function accepts a counter bid
        Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        self.purchase_facade.user_accept_counter_offer(bid_id, user_id)
        logger.info(f"User {user_id} has accepted a counter bid")
        
    
    #TODO send a notification to the store that the bid is declined
    def user_counter_bid_decline(self, user_id: int, bid_id: int) -> None:
        """
        Parameters: userId, bidId
        This function declines a counter bid
        Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        self.purchase_facade.user_decline_counter_offer(bid_id, user_id)
        logger.info(f"User {user_id} has declined a counter bid")
        
        
    #TODO send a notification to the store that the bid is accepted and ask the store to proceed to checkout
    def user_counter_bid(self, user_id: int, bid_id: int, counter_price: float) -> None:
        """
        Parameters: userId, bidId, counterPrice
        This function counter offers a counter bid
        Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        self.purchase_facade.user_counter_offer(bid_id, user_id, counter_price)
        logger.info(f"User {user_id} has counter offered a counter bid")
        
    
    def show_user_bids(self, system_manager_id: int, user_id: int) -> List[BidPurchaseDTO]:
        """
        Parameters: userId
        This function shows the bids of a user
        Returns a list of bids
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.is_system_manager(system_manager_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        return self.purchase_facade.get_bids_of_user(user_id)
        
    def show_store_bids(self, user_id: int, store_id: int) -> List[BidPurchaseDTO]:
        """
        Parameters: userId, storeId
        This function shows the bids of a store
        Returns a list of bids
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.has_get_bid_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to get the bids of the store", UserErrorTypes.user_does_not_have_necessary_permissions)
        return self.purchase_facade.get_bids_of_store(store_id)
        
    # -------------Purchase management related methods-------------------#

    '''def create_bid_purchase(self, user_id: int, proposed_price: float, product_id: int, store_id: int):
        """
        * Parameters: userId, proposedPrice, productId, storeId
        * This function creates a bid purchase
        * Returns None
        """
        if not self.user_facade.is_member(user_id) or not self.auth_facade.is_logged_in(user_id):
            raise UserError("User is not a member or is not logged in", UserErrorTypes.user_not_logged_in)
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
            raise UserError("User is not a member or is not logged in", UserErrorTypes.user_not_logged_in)
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
            raise UserError("User is not a member or is not logged in", UserErrorTypes.user_not_logged_in)
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
        if not self.roles_facade.is_system_manager(user_id) and (user_id != requested_id):
            raise UserError("User is not a system manager so can't view history of other users", UserErrorTypes.user_not_system_manager)
        return self.purchase_facade.get_purchases_of_user(requested_id, store_id)

    def view_purchases_of_store(self, user_id: int, store_id: int) -> List[PurchaseDTO]:
        """
        * Parameters: userId, store_id
        * This function returns the purchases of a store
        * Returns a string
        """
        if not self.roles_facade.is_owner(store_id, user_id) and not self.roles_facade.is_manager(store_id,
                                                                                                  user_id) and not self.roles_facade.is_system_manager(
            user_id):
            raise UserError("User is not a store owner or manager", UserErrorTypes.user_not_a_manager_or_owner)
        return self.purchase_facade.get_purchases_of_store(store_id)


    def get_payment_methods(self, user_id: int)-> List[str]:
        """
        * Parameters: userId
        * This function returns the payment methods of a user
        * Returns a list of strings
        """
        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        return PaymentHandler().get_payment_methods()
    
    def get_active_payment_methods(self, user_id: int)-> List[str]:
        """
        * Parameters: userId
        * This function returns the active payment methods of a user
        * Returns a list of strings
        """
        return PaymentHandler().get_active_payment_methods()

    def get_supply_methods(self, user_id: int) -> List[str]:
        """
        * Parameters: userId
        * This function returns the supply methods of a user
        * Returns a list of strings
        """
        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        return SupplyHandler().get_supply_methods()
    
    def get_active_supply_methods(self, user_id: int) -> List[str]:
        """
        * Parameters: userId
        * This function returns the active supply methods of a user
        * Returns a list of strings
        """
        return SupplyHandler().get_active_supply_methods()
    

    '''def view_purchases_of_user_in_store(self, user_id: int, store_id: int) -> str:
        """
        * Parameters: userId, store_id
        * This function returns the purchases of a user in a store
        * Returns a string
        """
        if not self.user_facade.is_member(user_id) or not self.auth_facade.is_logged_in(user_id):
            raise UserError("User is not a member or is not logged in", UserErrorTypes.user_not_logged_in)
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
            raise UserError("User is not a member or is not logged in", UserErrorTypes.user_not_logged_in)
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
            raise UserError("User is not a member or is not logged in", UserErrorTypes.user_not_logged_in)
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
            raise UserError("User is not a member or is not logged in", UserErrorTypes.user_not_logged_in)
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
            raise UserError("User is not a member or is not logged in", UserErrorTypes.user_not_logged_in)
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
            raise UserError("User is not logged in", UserErrorTypes.user_not_logged_in)
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
            raise UserError("User is not logged in", UserErrorTypes.user_not_logged_in)
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
            raise UserError("User is not logged in", UserErrorTypes.user_not_logged_in)
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
            raise UserError("User is not logged in", UserErrorTypes.user_not_logged_in)
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
            raise UserError("User is not logged in", UserErrorTypes.user_not_logged_in)

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
            raise UserError("User is not logged in", UserErrorTypes.user_not_logged_in)

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
                    #if third party services work, then:
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
            raise UserError("User is not logged in or is not a member", UserErrorTypes.user_not_logged_in)

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
            raise UserError("User is not logged in", UserErrorTypes.user_not_logged_in)

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
            raise UserError("User is not logged in", UserErrorTypes.user_not_logged_in)

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
                        #if third party services work, then:
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
      
    def get_my_stores(self, user_id) -> Dict[int, StoreDTO]:
        store_ids = self.roles_facade.get_my_stores(user_id)
        open_stores = self.store_facade.get_open_stores(user_id, store_ids)
        stores = {store_id: self.store_facade.get_store_info(store_id) for store_id in open_stores}
        return stores
    
    def get_all_product_tags(self) -> List[str]:
        return self.store_facade.get_all_tags()
    
    def get_all_store_names(self) -> Dict[int, str]:
        return self.store_facade.get_all_store_names()
    
    def get_all_categories(self) -> Dict[int, CategoryDTO]:
        return self.store_facade.get_all_categories()
    
    def edit_product(self, user_id: int, store_id: int, product_id: int, product_name: str, description: str, price: float,
                    weight: float, tags: List[str], amount: Optional[int] = None) -> None:
        """
        * Parameters: user_id, store_id, productSpecId, expirationDate, condition, price
        * This function adds a product to the store
        * Returns None
        """
        if self.user_facade.suspended(user_id):
            raise UserError("User is suspended", UserErrorTypes.user_suspended)
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to add a product to the store", UserErrorTypes.user_does_not_have_necessary_permissions)
        self.store_facade.edit_product_in_store(store_id, product_id, product_name, description, price, weight, tags, amount)

    def get_store_role(self, user_id: int, store_id: int) -> str:
        return self.roles_facade.get_store_role(user_id, store_id)

    def get_user_stores(self, user_id: int) -> List[int]:
        return self.roles_facade.get_user_stores(user_id)

    def set_user_shopping_cart(self, user_id: int, shopping_cart: Dict[int, Dict[int, int]]) -> None:
        # validate all products exist
        self.store_facade.validate_cart(shopping_cart)
        self.user_facade.set_user_shopping_cart(user_id, shopping_cart)

    def is_store_closed(self, store_id: int) -> bool:
        return self.store_facade.is_store_closed(store_id)

    def get_user_employees(self, user_id: int, store_id: int):
        employees = self.roles_facade.get_user_employees(user_id, store_id)
        for employee in employees:
            user_dto = self.user_facade.get_userDTO(employee.user_id)
            employee.username = user_dto.username
        return employees

    def get_unemployed_users(self, store_id) -> List[UserDTO]:
        employed = self.roles_facade.get_employed_users(store_id)
        all_users = self.user_facade.get_all_members()
        unemployed = []
        for user in all_users:
            if user.user_id not in employed:
                unemployed.append(user)

        return unemployed
    
    def get_all_members(self, user_id) -> List[UserDTO]:
        if not self.roles_facade.is_system_manager(user_id):
            raise UserError("User is not a system manager", UserErrorTypes.user_not_system_manager)
        return self.user_facade.get_all_members()

    def is_suspended(self, user_id: int) -> bool:
        return self.user_facade.suspended(user_id)

    def get_product_categories(self, user_id: int, store_id: int, product_id: int) -> Dict[int, CategoryDTO]:
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise UserError("User does not have the necessary permissions to get the product categories", UserErrorTypes.user_does_not_have_necessary_permissions)
        return self.store_facade.get_product_categories(store_id, product_id)

    def get_total_price_after_discount(self, user_id: int):
        cart = self.user_facade.get_shopping_cart(user_id)
        return self.store_facade.get_total_price_after_discount(cart, None)