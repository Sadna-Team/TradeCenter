from .user import UserFacade
from .roles import RolesFacade
from .DTOs import NotificationDTO
from .store import StoreFacade
from .ThirdPartyHandlers import PaymentHandler
from typing import Optional, List, Dict
import threading


class AddressDTO:
    def __init__(self, address_id, address, city, state, country, postal_code):
        self.address_id = address_id
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code

    def to_dict(self):
        return {
            'address_id': self.address_id,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code
        }


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
            # here you can add fields
            self.user_facade = UserFacade()
            self.store_facade = StoreFacade()
            self.payment_handler = PaymentHandler()
            self.roles_facade = RolesFacade()

    def show_notifications(self, user_id: int) -> List[NotificationDTO]:
        return self.user_facade.get_notifications(user_id)

    def add_product_to_basket(self, user_id: int, store_id: int, product_id: int, amount: int):
        with MarketFacade.__lock:
            if self.store_facade.check_product_availability(store_id, product_id, amount):
                self.user_facade.add_product_to_basket(user_id, store_id, product_id, amount)

    def checkout(self, user_id: int, payment_details: Dict):
        basket = self.user_facade.get_shopping_cart(user_id)
        # lock the __lock
        with MarketFacade.__lock:

            # check if the products are still available
            for store_id, products in basket.items():
                for product_id, amount in products.items():
                    if not self.store_facade.check_product_availability(store_id, product_id, amount):
                        raise ValueError(f"Product {product_id} is not available in the required amount")

            # charge the user
            amount = self.store_facade.calculate_total_price(basket)
            if not self.payment_handler.process_payment(amount, payment_details):
                raise ValueError("Payment failed")

            # remove the products from the store
            for store_id, products in basket.items():
                for product_id, amount in products.items():
                    self.store_facade.remove_product(store_id, product_id, amount)

        # clear the basket
        self.user_facade.clear_basket(user_id)

        # TODO: create a purchase
        # TODO: deliver the products
        # TODO: notify (?)

    def nominate_store_owner(self, store_id: int, owner_id: int, new_owner_id: int):
        nomination_id = self.roles_facade.nominate_owner(store_id, owner_id, new_owner_id)
        # TODO: different implementation later
        self.user_facade.notify_user(-1, NotificationDTO(
            f"You have been nominated to be the owner of store {store_id}", nomination_id))

    def nominate_store_manager(self, store_id: int, owner_id: int, new_manager_id: int):
        nomination_id = self.roles_facade.nominate_manager(store_id, owner_id, new_manager_id)
        self.user_facade.notify_user(-1, NotificationDTO(
            f"You have been nominated to be the manager of store {store_id}", nomination_id))

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
