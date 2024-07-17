# ----------------- imports -----------------#
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple, Optional, Dict

from backend.business.DTOs import BidPurchaseDTO, PurchaseProductDTO, PurchaseDTO
import threading
from backend.error_types import *
from backend.database import db

# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')

# -----------------Rating class-----------------#
'''class Rating(ABC):
    def __init__(self, rating_id: int, rating: float, purchase_id: int, user_id: int, description: str,
                 creation_date: datetime):
        if not (0.0 <= rating <= 5.0):
            raise ValueError("Rating must be a float between 0 and 5")
        self._rating_id: int = rating_id
        self._rating: float = rating
        self._purchase_id: int = purchase_id
        self._user_id: int = user_id
        self._description: str = description
        self._creation_date: datetime = creation_date

    # ---------------------------------Getters and Setters---------------------------------#
    @property
    def purchase_id(self):
        return self._purchase_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def rating(self):
        return self._rating


# -----------------StoreRating class-----------------#
class StoreRating(Rating):
    # purchaseId and storeId are the unique identifiers for the store rating, storeId used to retrieve the details of
    # store
    def __init__(self, rating_id: int, rating: float, purchase_id: int, user_id: int, description: str, store_id: int,
                 creation_date: datetime = datetime.now()):
        super().__init__(rating_id, rating, purchase_id, user_id, description, creation_date)
        self.__store_id: int = store_id
        logger.info('[StoreRating] successfully created store rating object with rating id: %s', rating_id)

    # ---------------------------------Getters and Setters---------------------------------#
    @property
    def store_id(self):
        return self.__store_id

    @property
    def purchase_id(self):
        return self._purchase_id

    @property
    def user_id(self):
        return self._user_id


# -----------------ProductRating class-----------------#
class ProductRating(Rating):
    # purchaseId and productId are the unique identifiers for the product rating, productSpec used to retrieve the
    # details of product
    def __init__(self, rating_id: int, rating: float, purchase_id: int, user_id: int, description: str,
                 product_spec_id: int,
                 creation_date: datetime = datetime.now()):
        super().__init__(rating_id, rating, purchase_id, user_id, description, creation_date)
        self.__product_id = product_spec_id
        logger.info('[ProductRating] successfully created product rating object with rating id: %s', rating_id)

    # ---------------------------------Getters and Setters---------------------------------#
    @property
    def product_id(self):
        return self.__product_id'''

PURCHASE_ID_COUNTER_NAME = "purchase_id_counter"


# ---------------------purchaseStatus Enum---------------------#
class PurchaseStatus(Enum):
    # Enum for the status of the purchase
    onGoing = 1
    accepted = 2
    completed = 3
    offer_rejected = 4
    approved = 5


# -----------------Purchase Class-----------------#
class Purchase(db.Model):
    # interface for the purchase classes, contains the common attributes and methods for the purchase classes
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _user_id = db.Column(db.Integer, nullable=False)
    _date_of_purchase = db.Column(db.DateTime, nullable=True)
    _total_price = db.Column(db.Float, nullable=False)
    _total_price_after_discounts = db.Column(db.Float, nullable=False)
    _status = db.Column(db.Enum(PurchaseStatus), nullable=False)
    _delivery_date = db.Column(db.DateTime, nullable=True)

    type = db.Column(db.String(50), nullable=False)  # discriminator column

    __mapper_args__ = {
        'polymorphic_identity': 'purchase',
        'polymorphic_on': 'type'
    }

    #__table_args__ = {'extend_existing': True}

    def __init__(self, user_id: int, date_of_purchase: Optional[datetime],
                 total_price: float, total_price_after_discounts: float, status: PurchaseStatus):
        self._user_id = user_id
        self._date_of_purchase = date_of_purchase or datetime.now()
        self._total_price = total_price
        self._total_price_after_discounts: float = total_price_after_discounts
        self._status = status
        self._delivery_date: Optional[datetime] = None

    # ---------------------------------Getters and Setters---------------------------------#
    @property
    def purchase_id(self):
        return self.id

    @property
    def user_id(self):
        return self._user_id

    @property
    def date_of_purchase(self):
        return self._date_of_purchase

    @property
    def total_price(self):
        return self._total_price

    @property
    def total_price_after_discounts(self):
        return self._total_price_after_discounts

    @property
    def delivery_date(self):
        return self._delivery_date

    @delivery_date.setter
    def delivery_date(self, delivery_date: datetime):
        self._delivery_date = delivery_date

    @property
    def status(self):
        return self._status

    @abstractmethod
    def accept(self):
        pass

    @abstractmethod
    def complete(self):
        pass


# -----------------ImmediateSubPurchases class-----------------#
class ImmediateSubPurchase(db.Model):
    # purchaseId and storeId are unique identifier of the immediate purchase, storeId used to retrieve the details of
    # the store
    __tablename__ = 'immediate_sub_purchases'

    purchase_id = db.Column(db.Integer, db.ForeignKey('immediate_purchases.id'), primary_key=True)
    _user_id = db.Column(db.Integer)
    _date_of_purchase = db.Column(db.DateTime)
    _total_price = db.Column(db.Float)
    _total_price_after_discounts = db.Column(db.Float)
    _status = db.Column(db.Enum(PurchaseStatus))
    store_id = db.Column(db.Integer, primary_key=True)
    _products = db.relationship('PurchaseProduct', backref='immediate_sub_purchase', lazy=True)

    __table_args__ = (
        db.PrimaryKeyConstraint('purchase_id', 'store_id'),
        db.UniqueConstraint('purchase_id', 'store_id', name='uq_purchase_store'),
    )

    #__table_args__ = {'extend_existing': True}

    _status_lock = threading.Lock()

    def __init__(self, purchase_id: int, store_id: int, user_id: int, date_of_purchase: Optional[datetime],
                 total_price: float, total_price_after_discounts: float, status: PurchaseStatus,
                 products: List[PurchaseProductDTO]):
        self.purchase_id = purchase_id
        self._user_id = user_id
        self._date_of_purchase = date_of_purchase
        self._total_price = total_price
        self._total_price_after_discounts: float = total_price_after_discounts
        self._status = status
        self.store_id: int = store_id
        self._products: List[PurchaseProduct] = [PurchaseProduct(product.product_id, product.name, product.description,
                                                                 product.price, product.amount, purchase_id, store_id)
                                                 for product in products]
        #self._status_lock = threading.Lock()
        logger.info('[ImmediateSubPurchases] successfully created immediate sub purchase object with purchase id: %s',
                    purchase_id)

    def accept(self):
        with ImmediateSubPurchase._status_lock:
            if self._status != PurchaseStatus.onGoing:
                raise PurchaseError("Purchase is not on going", PurchaseErrorTypes.purchase_not_ongoing)
            self._status = PurchaseStatus.accepted

    def complete(self):
        with ImmediateSubPurchase._status_lock:
            if self._status != PurchaseStatus.accepted:
                raise PurchaseError("Purchase is not accepted", PurchaseErrorTypes.purchase_not_accepted)
            self._status = PurchaseStatus.completed

    # ---------------------------------Getters and Setters---------------------------------#
    @property
    def user_id(self):
        return self._user_id

    @property
    def date_of_purchase(self):
        return self._date_of_purchase

    @property
    def total_price(self):
        return self._total_price

    @property
    def total_price_after_discounts(self):
        return self._total_price_after_discounts

    @property
    def status(self):
        return self._status

    @property
    def products(self):
        return self._products


# -----------------ImmediatePurchase class-----------------#
class ImmediatePurchase(Purchase):
    # purchaseId is the unique identifier of the immediate purchase, purchase by a user of their shoppingCart
    # Note: storeId is -1 since immediatePurchase is not directly related to a store
    # Note: List[Tuple[Tuple[int,float],List[int]]] -> List of shoppingBaskets where shoppingBasket is a tuple of a
    #       tuple of storeId and totalPrice and a list of productIds
    __tablename__ = 'immediate_purchases'

    id = db.Column(db.Integer, db.ForeignKey('purchases.id'), primary_key=True)
    _immediate_sub_purchases = db.relationship('ImmediateSubPurchase', backref='immediate_purchase', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'immediate_purchase',
    }

    #__table_args__ = {'extend_existing': True}

    def __init__(self, user_id: int, total_price: float,
                 total_price_after_discounts: float = -1):
        super().__init__(user_id, datetime.now(), total_price, total_price_after_discounts,
                         PurchaseStatus.onGoing)
        self._immediate_sub_purchases: List[ImmediateSubPurchase] = []

    def set_shopping_cart(self, shopping_cart: Dict[int, Tuple[List[PurchaseProductDTO], float, float]], user_id: int):
        for store_id in shopping_cart:
            products = shopping_cart[store_id][0]
            price = shopping_cart[store_id][1]
            price_after_discounts = shopping_cart[store_id][2]
            immediate_sub_purchase = ImmediateSubPurchase(self.id, store_id, user_id,
                                                          self.date_of_purchase, price, price_after_discounts,
                                                          PurchaseStatus.onGoing,
                                                          products)
            self._immediate_sub_purchases.append(immediate_sub_purchase)
        logger.info('[ImmediatePurchase] successfully created immediate purchase object with purchase id: %s',
                    self.id)

    @property
    def immediate_sub_purchases(self):
        return self._immediate_sub_purchases

    def accept(self):
        if self._status != PurchaseStatus.onGoing:
            raise PurchaseError("Purchase is not on going", PurchaseErrorTypes.purchase_not_ongoing)
        self._status = PurchaseStatus.accepted
        for sub_purchase in self._immediate_sub_purchases:
            sub_purchase.accept()

    def complete(self):
        if self._status != PurchaseStatus.accepted:
            raise PurchaseError("Purchase is not accepted", PurchaseErrorTypes.purchase_not_accepted)
        self._status = PurchaseStatus.completed
        for sub_purchase in self._immediate_sub_purchases:
            sub_purchase.complete()

def create_immediate_purchase(user_id: int, total_price: float,
                 shopping_cart: Dict[int, Tuple[List[PurchaseProductDTO], float, float]],
                 total_price_after_discounts: float = -1) -> ImmediatePurchase:
    immediate_purchase = ImmediatePurchase(user_id, total_price, total_price_after_discounts)
    db.session.add(immediate_purchase)
    db.session.flush()

    immediate_purchase.set_shopping_cart(shopping_cart, user_id)
    return immediate_purchase


# -----------------BidPurchase class-----------------#
class BidPurchase(Purchase):
    # purchaseId and productId are the unique identifiers for the product rating, productSpec used to retrieve the
    # details of product
    __tablename__ = 'bid_purchases'

    id = db.Column(db.Integer, db.ForeignKey('purchases.id'), primary_key=True)
    _proposed_price = db.Column(db.Float)
    _product_id = db.Column(db.Integer)
    _store_id = db.Column(db.Integer)
    _is_offer_to_store = db.Column(db.Boolean)
    _list_of_store_owners_managers_that_accepted_offer_demo = db.Column(db.String)
    _user_who_rejected_id = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'bid_purchase',
    }

    #__table_args__ = {'extend_existing': True}

    _bid_lock = threading.Lock()

    def __init__(self, user_id: int, proposed_price: float, store_id: int, product_id: int):
        super().__init__(user_id, None, -1, -1, PurchaseStatus.onGoing)
        if proposed_price < 0:
            raise PurchaseError("Proposed price is invalid", PurchaseErrorTypes.invalid_proposed_price)
        self._proposed_price: float = proposed_price
        self._product_id: int = product_id
        self._store_id: int = store_id
        self._is_offer_to_store: bool = True
        self._list_of_store_owners_managers_that_accepted_offer_demo: str = ""
        self._user_who_rejected_id: int = -1
        logger.info('[BidPurchase] successfully created bid purchase object with purchase id: %s',
                    self.id)

    # ---------------------------------Getters and Setters---------------------------------#
    @property
    def proposed_price(self):
        return self._proposed_price

    @property
    def product_id(self):
        return self._product_id

    @property
    def store_id(self):
        return self._store_id

    @property
    def is_offer_to_store(self):
        return self._is_offer_to_store

    @property
    def _list_of_store_owners_managers_that_accepted_offer(self):
        if self._list_of_store_owners_managers_that_accepted_offer_demo == "":
            return []
        return [int(x) for x in self._list_of_store_owners_managers_that_accepted_offer_demo.split(",")]

    @property
    def list_of_store_owners_managers_that_accepted_offer(self) -> List[int]:
        return self._list_of_store_owners_managers_that_accepted_offer

    @_list_of_store_owners_managers_that_accepted_offer.setter
    def _list_of_store_owners_managers_that_accepted_offer(self, store_worker_ids: List[int]) -> None:
        if len(store_worker_ids) == 0:
            self._list_of_store_owners_managers_that_accepted_offer_demo = ""
        else:
            self._list_of_store_owners_managers_that_accepted_offer_demo = ','.join([str(x) for x in store_worker_ids])

    @list_of_store_owners_managers_that_accepted_offer.setter
    def list_of_store_owners_managers_that_accepted_offer(self, store_worker_ids: List[int]) -> None:
        self._list_of_store_owners_managers_that_accepted_offer = store_worker_ids

    def add_to_list_of_store_owners_managers_that_accepted_offer(self, store_worker_id: int) -> None:
        if len(self._list_of_store_owners_managers_that_accepted_offer_demo) == 0:
            self._list_of_store_owners_managers_that_accepted_offer_demo += str(store_worker_id)
        else:
            self._list_of_store_owners_managers_that_accepted_offer_demo += "," + str(store_worker_id)

    @property
    def user_who_rejected_id(self):
        return self._user_who_rejected_id

    # ---------------------------------Methods---------------------------------#    
    def store_owner_manager_accept_offer(self, store_worker_id: int) -> None:
        """
        Parameters: storeWorkerId
        This function is responsible for the store owner/manager accepting the offer
        NOTE: the store owner/manager can only accept the offer if the purchase is ongoing, and the store owner/manager
         is validated if they are connected to store in marketfacade
        Returns: none
        """
        with BidPurchase._bid_lock:
            if self._status != PurchaseStatus.onGoing:
                raise PurchaseError("Purchase is not on going", PurchaseErrorTypes.purchase_not_ongoing)
            if not self.is_offer_to_store:
                raise PurchaseError("Offer is not to store", PurchaseErrorTypes.offer_not_to_store)

            if store_worker_id not in self._list_of_store_owners_managers_that_accepted_offer:
                self.add_to_list_of_store_owners_managers_that_accepted_offer(store_worker_id)
                logger.info(
                    '[BidPurchase] store owner/manager with store worker id: %s accepted offer of bid purchase with'
                    ' purchase id: %s',
                    store_worker_id, self.id)
            else:
                raise PurchaseError("Store owner/manager already accepted offer",
                                    PurchaseErrorTypes.store_owner_manager_already_accepted_offer)

    def store_reject_offer(self, store_worker_id: int) -> int:
        """
        Parameters: storeWorkerId
        This function is responsible for the store owner/manager rejecting the offer
        NOTE: the store owner/manager can only reject the offer if the purchase is ongoing, and the store owner/manager
        is validated if they are connected to store in marketfacade
        Returns: the id of the user who rejected the offer
        """
        with BidPurchase._bid_lock:
            if self._status != PurchaseStatus.onGoing:
                raise PurchaseError("Purchase is not on going", PurchaseErrorTypes.purchase_not_ongoing)

            if not self.is_offer_to_store:
                raise PurchaseError("Offer is not to store", PurchaseErrorTypes.offer_not_to_store)

            self._status = PurchaseStatus.offer_rejected
            self._user_who_rejected_id = store_worker_id
            logger.info(
                '[BidPurchase] store owner/manager with store worker id: %s rejected offer of bid purchase with '
                'purchase id: %s',
                store_worker_id, self.id)
            return self._user_who_rejected_id

    def store_accept_offer(self, store_workers_ids: List[int]) -> bool:
        """
        Parameters: storeWorkersIds
        This function is responsible for the store accepting the offer
        NOTE: the store can only accept the offer if the purchase is ongoing and all store owners/managers accepted the
        offer
        Returns: true if the store accepted the offer
        """
        with BidPurchase._bid_lock:
            if self._status != PurchaseStatus.onGoing:
                logger.warning(
                    "[BidPurchase] store could not accept offer of bid purchase with purchase id: %s, since offer "
                    "is not ongoing",
                    self.id)
                return False

            if self.is_offer_to_store == False:
                logger.warning(
                    "[BidPurchase] store could not accept offer of bid purchase with purchase id: %s, since offer "
                    "is not to store",
                    self.id)
                raise PurchaseError("Offer is not to store", PurchaseErrorTypes.offer_not_to_store)

            for store_worker_id in set(store_workers_ids):
                if store_worker_id not in self._list_of_store_owners_managers_that_accepted_offer:
                    logger.info(
                        "[BidPurchase] store could not accept offer of bid purchase with purchase id: %s, since not"
                        " all store owners/managers accepted the offer",
                        self.id)
                    return False
            self._status = PurchaseStatus.approved
            logger.info("[BidPurchase] store accepted offer of bid purchase with purchase id: %s", self.id)
            return True

    def store_counter_offer(self, user_who_counter_offer: int, proposed_price: float) -> None:
        """
        Parameters: storeId, userWhoCounterOffer, proposedPrice
        This function is responsible for the store countering the offer
        NOTE: the store can only counter the offer if the purchase is ongoing, and the store is validated if they are
        connected to store in marketfacade
        Returns: none
        """
        with BidPurchase._bid_lock:
            if self._status != PurchaseStatus.onGoing:
                logger.info(
                    "[BidPurchase] store could not counter offer of bid purchase with purchase id: %s, since "
                    "purchase is not ongoing",
                    self.id)
                raise PurchaseError("Purchase is not on going", PurchaseErrorTypes.purchase_not_ongoing)
            if self.is_offer_to_store == False:
                logger.info(
                    "[BidPurchase] store could not counter offer of bid purchase with purchase id: %s, since offer "
                    "is not to store",
                    self.id)
                raise PurchaseError("Offer is not to store", PurchaseErrorTypes.offer_not_to_store)
            if user_who_counter_offer in self._list_of_store_owners_managers_that_accepted_offer:
                logger.info(
                    "[BidPurchase] store could not counter offer of bid purchase with purchase id: %s, since store "
                    "owner/manager already accepted offer",
                    self.id)
                raise PurchaseError("Store owner/manager already accepted offer",
                                    PurchaseErrorTypes.store_owner_manager_already_accepted_offer)

            if proposed_price < 0:
                raise PurchaseError("Proposed price is invalid", PurchaseErrorTypes.invalid_proposed_price)

            self._list_of_store_owners_managers_that_accepted_offer = []
            self.add_to_list_of_store_owners_managers_that_accepted_offer(user_who_counter_offer)
            self._proposed_price = proposed_price
            self._is_offer_to_store = False

    #FOR NOW THE IMPLEMENTATION IS AS FOLLOWS: if a manager counters the offer of a user, the user can either counter it back, reject, or accept 
    # NOTE: in the case of accept, the user will accept the counter and then propose the new price again to all store owners/managers to accept
    def user_accept_counter_offer(self, user_id: int) -> None:
        """
        Parameters: userId
        This function is responsible for the user accepting the counter offer
        NOTE: the user can only accept the counter offer if the purchase is ongoing
        Returns: none
        """
        if self._status != PurchaseStatus.onGoing:
            logger.info(
                "[BidPurchase] user could not accept counter offer of bid purchase with purchase id: %s, since "
                "purchase is not ongoing",
                self.id)
            raise PurchaseError("Purchase is not on going", PurchaseErrorTypes.purchase_not_ongoing)
        if self.is_offer_to_store == True:
            logger.info(
                "[BidPurchase] user could not accept counter offer of bid purchase with purchase id: %s, since "
                "offer is to store",
                self.id)
            raise PurchaseError("Offer is to store", PurchaseErrorTypes.offer_to_store)
        if self._user_id != user_id:
            logger.info(
                "[BidPurchase] user could not accept counter offer of bid purchase with purchase id: %s, since "
                "user id is invalid",
                self.id)
            raise PurchaseError("User id is invalid", PurchaseErrorTypes.invalid_user_id)
        self._is_offer_to_store = True

    #NOTE: in the case of the user rejecting the offer, the purchase will be rejected and the store will be notified
    def user_reject_counter_offer(self, user_id: int) -> None:
        """
        Parameters: userId
        This function is responsible for the user rejecting the offer
        NOTE: the user can only reject the offer if the purchase is ongoing
        Returns: none
        """
        if self._status != PurchaseStatus.onGoing:
            logger.info(
                "[BidPurchase] user could not reject offer of bid purchase with purchase id: %s, since purchase is "
                "not ongoing",
                self.id)
            raise PurchaseError("Purchase is not on going", PurchaseErrorTypes.purchase_not_ongoing)
        if self.is_offer_to_store == True:
            logger.info(
                "[BidPurchase] user could not reject offer of bid purchase with purchase id: %s, since offer is to "
                "store",
                self.id)
            raise PurchaseError("Offer is to store", PurchaseErrorTypes.offer_to_store)
        if self._user_id != user_id:
            logger.info(
                "[BidPurchase] user could not reject offer of bid purchase with purchase id: %s, since user id is "
                "invalid",
                self.id)
            raise PurchaseError("User id is invalid", PurchaseErrorTypes.invalid_user_id)

        self._status = PurchaseStatus.offer_rejected
        self._user_who_rejected_id = user_id
        logger.info("[BidPurchase] user rejected offer of bid purchase with purchase id: %s", self.id)

    #NOTE: in the case of the user countering again, the manager who originally countered will be removed from the list of store owners/managers that accepted the offer
    def user_counter_offer(self, user_id: int, proposed_price: float) -> None:
        """
        Parameters: userId, proposedPrice
        This function is responsible for the user countering the offer
        NOTE: the user can only counter the offer if the purchase is ongoing
        Returns: none
        """
        if self._status != PurchaseStatus.onGoing:
            logger.info(
                "[BidPurchase] user could not counter offer of bid purchase with purchase id: %s, since purchase is not ongoing",
                self.id)
            raise PurchaseError("Purchase is not on going", PurchaseErrorTypes.purchase_not_ongoing)
        if self.is_offer_to_store == True:
            logger.info(
                "[BidPurchase] user could not counter offer of bid purchase with purchase id: %s, since offer is to store",
                self.id)
            raise PurchaseError("Offer is to store", PurchaseErrorTypes.offer_to_store)
        if self._user_id != user_id:
            logger.info(
                "[BidPurchase] user could not counter offer of bid purchase with purchase id: %s, since user id is invalid",
                self.id)
            raise PurchaseError("User id is invalid", PurchaseErrorTypes.invalid_user_id)
        if proposed_price < 0:
            raise PurchaseError("Proposed price is invalid", PurchaseErrorTypes.invalid_proposed_price)

        self._proposed_price = proposed_price
        self._is_offer_to_store = True
        self._list_of_store_owners_managers_that_accepted_offer = []

    def accept(self):
        if self._status != PurchaseStatus.approved:
            raise PurchaseError("Purchase is not approved", PurchaseErrorTypes.purchase_not_approved)
        self._status = PurchaseStatus.accepted
        self._total_price = self._proposed_price
        self._total_price_after_discounts = self._proposed_price
        self._date_of_purchase = datetime.now()

    def complete(self):
        if self._status != PurchaseStatus.accepted:
            raise PurchaseError("Purchase is not accepted", PurchaseErrorTypes.purchase_not_accepted)
        self._status = PurchaseStatus.completed


class PurchaseProduct(db.Model):
    __tablename__ = 'purchase_products'

    product_id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(50))
    _description = db.Column(db.String(200))
    _price = db.Column(db.Float)
    _amount = db.Column(db.Integer)

    __table_args__ = (
        db.PrimaryKeyConstraint('product_id', 'purchase_id', 'store_id'),
        db.ForeignKeyConstraint(['purchase_id', 'store_id'],
                                ['immediate_sub_purchases.purchase_id', 'immediate_sub_purchases.store_id']),
    )

    # __table_args__ = (
    #     db.PrimaryKeyConstraint('product_id', 'purchase_id', 'store_id'),
    #     db.ForeignKeyConstraint(['purchase_id', 'store_id'],
    #                             ['immediate_sub_purchases.purchase_id', 'immediate_sub_purchases.store_id']),
    #     {'extend_existing': True}
    # )

    def __init__(self, product_id: int, name: str, description: str, price: float, amount: int, purchase_id: int, store_id: int):
        self.product_id: int = product_id
        self.purchase_id: int = purchase_id
        self.store_id: int = store_id
        self._name: str = name
        self._description: str = description
        self._price: float = price
        self._amount: int = amount


    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def price(self) -> float:
        return self._price

    @property
    def amount(self) -> int:
        return self._amount

    def get(self) -> dict:
        return {"product_id": self.product_id, "name": self._name, "description": self._description,
                "price": self._price, "amount": self._amount}

    def get_dto(self) -> PurchaseProductDTO:
        return PurchaseProductDTO(self.product_id, self._name, self._description, self._price, self._amount)


# -----------------AuctionPurchase class-----------------#
'''class AuctionPurchase(Purchase):
    # Note: userId of purchase is not initialized as user is determined at the end of auction.
    # Note: totalPrice is not known as determined by auction
    def __init__(self, purchase_id: int, base_price: float, starting_date: datetime, ending_date: datetime,
                 store_id: int, product_id: int, product_spec_id: int,
                 users_with_proposed_prices: List[Tuple[int, float]] = []):
        super().__init__(purchase_id, -1, store_id, None, -1, PurchaseStatus.onGoing)
        self._base_price = base_price
        self._starting_date = starting_date
        self._ending_date = ending_date
        self._product_id = product_id
        self._product_spec_id = product_spec_id
        self._delivery_date = None
        self._users_with_proposed_prices = users_with_proposed_prices
        logger.info('[AuctionPurchase] successfully created auction purchase object with purchase id: %s',
                    self._purchase_id)

    # ---------------------------------Getters and Setters---------------------------------#

    # ---------------------------------Methods---------------------------------#
    def update_status(self, status: PurchaseStatus):
        logger.info('[AuctionPurchase] attempting to update status of auction purchase with purchase id: %s',
                    self._purchase_id)
        self._status = status

    def update_date_of_purchase(self, date_of_purchase: datetime):
        logger.info('[AuctionPurchase] attempting to update date of purchase of auction purchase with purchase id: %s',
                    self._purchase_id)
        self._date_of_purchase = date_of_purchase

    # maybe add synchronization?!?!
    def add_auction_bid(self, user_id: int, proposed_price: float) -> bool:
        # For NEXT TIME, VALIDATE THAT THE USERID ISNT A STORE MANAGER/OWNER OF THE STORE PUTTING THE AUCTION
        if user_id is not None:
            if self.calculate_remaining_time() > timedelta(0) and self._status == PurchaseStatus.onGoing:
                if self._users_with_proposed_prices == [] and proposed_price > self._base_price:
                    self._users_with_proposed_prices.append((user_id, proposed_price))
                    logger.info(
                        '[AuctionPurchase] user with user id: %s added bid to auction purchase with purchase id: %s',
                        user_id, self._purchase_id)
                    return True
                # MAYBE ADD LATER ON SOME LIKE CONSTRAINTS THAT THE STORE CAN DECLARE, FOR EXAMPLE, CAN ONLY BID AT
                # LEAST 5 DOLLARS MORE THAN HIGHEST.
                if proposed_price > self.view_highest_bidding_offer():
                    self._users_with_proposed_prices.append((user_id, proposed_price))
                    logger.info(
                        '[AuctionPurchase] user with user id: %s added bid to auction purchase with purchase id:'
                        ' %s', user_id, self._purchase_id)
                    return True
            else:
                logger.warning(
                    '[AuctionPurchase] user with user id: %s could not add bid to auction purchase with purchase'
                    ' id: %s', user_id, self._purchase_id)
        raise ValueError("User id is invalid")

    def calculate_total_price(self) -> float:
        logger.info('[AuctionPurchase] calculating total price of auction purchase with purchase id: %s',
                    self._purchase_id)
        return self.view_highest_bidding_offer()

    def view_highest_bidding_offer(self) -> float:
        """
        * Parameters: none
        * This function is responsible for returning the highest bidding offer
        * Returns: float of highest bidding offer
        """
        logger.info('[AuctionPurchase] viewing highest bidding offer of auction purchase with purchase id: %s',
                    self._purchase_id)
        return max(self._users_with_proposed_prices, key=lambda x: x[1])[1]

    def calculate_remaining_time(self) -> timedelta:
        """
        * Parameters: none
        * This function is responsible for calculating the remaining time for the auction
        * Returns: datetime of remaining time
        """
        logger.info('[AuctionPurchase] calculating remaining time of auction purchase with purchase id: %s',
                    self._purchase_id)
        if self._starting_date < datetime.now():
            if self._ending_date > datetime.now():
                return datetime.now() - self._ending_date
        return timedelta(0)

    def check_if_auction_ended(self) -> bool:
        """
        * Parameters: none
        * This function is responsible for checking if the auction has ended
        * Returns: true if ended, false if not
        """
        if self._status == PurchaseStatus.onGoing and self._ending_date < datetime.now():
            if self._users_with_proposed_prices:
                user_with_highest_bid = max(self._users_with_proposed_prices, key=lambda x: x[1])
                self._user_id = user_with_highest_bid[0]
                self._total_price = user_with_highest_bid[1]
                logger.info('[AuctionPurchase] auction purchase with purchase id: %s has ended',
                            self._purchase_id)
            else:
                self._status = PurchaseStatus.failed
                logger.info('[AuctionPurchase] auction purchase failed with purchase id: %s',
                            self._purchase_id)
            return True
        return False

    def validate_purchase_of_user(self, user_id: int, delivery_date: datetime) -> bool:
        """
        * Parameters: userId
        * This function is responsible for validating that the user with the highest bid successfully paid for the
         product and the product is underway
        * Returns: bool
        """
        if self._user_id == user_id:
            self._status = PurchaseStatus.accepted
            self._date_of_purchase = datetime.now()
            self._delivery_date = delivery_date
            logger.info(
                '[AuctionPurchase] user with user id: %s validated purchase of auction purchase with purchase id: %s',
                user_id, self._purchase_id)
            return True
        logger.warning(
            '[AuctionPurchase] user with user id: %s could not validate purchase of auction purchase with purchase '
            'id: %s',
            user_id, self._purchase_id)
        raise ValueError("User id is invalid")

    def invalidate_purchase_of_user(self, user_id: int) -> bool:
        """
        * Parameters: userId
        * This function is responsible for invalidating the purchase of the user with the highest bid, whether it be due
         to not paying or not able to deliver
        * Returns: bool
        """
        if self._user_id == user_id:
            self._status = PurchaseStatus.failed
            logger.info(
                '[AuctionPurchase] user with user id: %s invalidated purchase of auction purchase with purchase id: %s',
                user_id, self._purchase_id)
            return True
        raise ValueError("User id is invalid")

    def check_if_completed_purchase(self) -> bool:
        """
        * Parameters: none
        * This function is responsible for checking if the purchase is completed, and updating if it is
        * Returns: true if completed, false otherwise
        """
        if self._status == PurchaseStatus.accepted:
            if self._delivery_date < datetime.now():
                self.update_status(PurchaseStatus.completed)
                logger.info('[AuctionPurchase] purchase with purchase id: %s has been completed',
                            self._purchase_id)
                return True
        return False

    # -----------------LotteryPurchase class-----------------#


class LotteryPurchase(Purchase):
    def __init__(self, purchase_id: int, full_price: float, store_id: int, product_id: int, product_spec_id: int,
                 starting_date: datetime, ending_date: datetime, users_with_prices: List[Tuple[int, float]] = []):
        super().__init__(purchase_id, -1, store_id, None, 0, PurchaseStatus.onGoing)
        self._full_price = full_price
        self._product_id = product_id
        self._product_spec_id = product_spec_id
        self._users_with_prices = users_with_prices
        self._starting_date = starting_date
        self._ending_date = ending_date
        self._delivery_date = None
        logger.info('[LotteryPurchase] successfully created lottery purchase object with purchase id: %s',
                    self._purchase_id)

    # ---------------------------------Getters and Setters---------------------------------#
    @property
    def ending_date(self):
        return self._ending_date

    # ---------------------------------Methods---------------------------------#
    def update_status(self, status: PurchaseStatus):
        logger.info('[LotteryPurchase] attempting to update status of lottery purchase with purchase id: %s',
                    self._purchase_id)
        self._status = status

    def update_date_of_purchase(self, date_of_purchase: datetime):
        logger.info('[LotteryPurchase] attempting to update date of purchase of lottery purchase with purchase id: %s',
                    self._purchase_id)
        self._date_of_purchase = date_of_purchase

    def calculate_total_price(self) -> float:
        logger.info('[LotteryPurchase] calculating total price of lottery purchase with purchase id: %s',
                    self._purchase_id)
        return sum([x[1] for x in self._users_with_prices])

    def check_if_completed_purchase(self) -> bool:
        if self._status == PurchaseStatus.accepted:
            if self._delivery_date < datetime.now():
                self.update_status(PurchaseStatus.completed)
                logger.info('[LotteryPurchase] purchase with purchase id: %s has been completed',
                            self._purchase_id)
                return True
            raise ValueError("Delivery date is not valid")
        return False

    def calculate_remaining_time(self) -> timedelta:
        """
        * Parameters: none
        * This function is responsible for calculating the remaining time for the auction
        * Returns: datetime of remaining time
        """
        if self._starting_date < datetime.now():
            if self._ending_date > datetime.now():
                return datetime.now() - self._ending_date
        return timedelta(0)

    def add_lottery_offer(self, user_id: int, proposed_price: float) -> bool:
        """
        * Parameters: userId, proposedPrice
        * This function is responsible for adding the user and their proposed price to the list of users with proposed
        prices, the same user can bid multiple times
        * Note: a bid can only be added if it is bigger than the current highest bid
        * Returns: true if bid was added
        """
        if user_id is not None:
            if self.calculate_remaining_time() > timedelta(0) and self._status == PurchaseStatus.onGoing:
                if proposed_price + self._total_price <= self._full_price:
                    self._users_with_prices.append((user_id, proposed_price))
                    self._total_price = self._total_price + proposed_price

                    if proposed_price + self._total_price == self._full_price:
                        self._status = PurchaseStatus.accepted
                        logger.info(
                            '[LotteryPurchase] user with user id: %s added bid to lottery purchase with purchase '
                            'id: %s', user_id, self._purchase_id)
                    return True
                else:
                    raise ValueError("Proposed price is too high")

            else:
                raise ValueError("Lottery has ended")
        else:
            raise ValueError("User id is invalid")

    def calculate_probability_of_user(self, user_id: int) -> float:
        """
        * Parameters: userId
        * This function is responsible for calculating the probability of the user winning the lottery
        * Returns: float of probability
        """
        logger.info(
            '[LotteryPurchase] calculating probability of user with user id: %s in lottery purchase with purchase id: '
            '%s',
            user_id, self._purchase_id)
        if user_id is not None:
            if self._status == PurchaseStatus.completed:
                return sum([x[1] for x in self._users_with_prices if x[0] == user_id]) / self._full_price
        return 0.0

    def validate_user_offers(self) -> bool:
        """
        * Parameters: none
        * This function is responsible for validating that all users with offers have paid the full price
        * Returns: true if all users have paid the full price
        """
        if self._ending_date < datetime.now():
            if self._total_price == self._full_price:
                self._status = PurchaseStatus.accepted
                logger.info(
                    '[LotteryPurchase] all users have paid the full price of lottery purchase with purchase id: %s',
                    self._purchase_id)
                return True
            if self._total_price < self._full_price:
                self._status = PurchaseStatus.failed
                logger.info(
                    '[LotteryPurchase] all users have not paid the full price of lottery purchase with purchase id: %s',
                    self._purchase_id)
                raise ValueError("Not all users have paid the full price")

    def check_if_lottery_ended_successfully(self) -> bool:
        """
        * Parameters: none
        * This function is responsible for checking if the lottery has ended
        * Returns: true if ended, false if not
        """
        if self._status == PurchaseStatus.onGoing and self._ending_date < datetime.now():
            if self._total_price != self._full_price:
                self.update_status(PurchaseStatus.failed)
                logger.info('[LotteryPurchase] lottery purchase failed with purchase id: %s', self._purchase_id)
            else:
                logger.info('[LotteryPurchase] lottery purchase with purchase id: %s has ended', self._purchase_id)
            return True
        return False

    def pick_winner(self) -> Optional[int]:
        """
        * Parameters: none
        * This function is responsible for picking the winner of the lottery
        * Returns: userId of the winner
        """
        if self.check_if_lottery_ended_successfully():
            if self._status != PurchaseStatus.failed:
                unique_users_with_sum_of_prices: List[Tuple[int, float]] = []
                for user in self._users_with_prices:
                    if user[0] not in [x[0] for x in unique_users_with_sum_of_prices]:
                        unique_users_with_sum_of_prices.append(
                            (user[0], sum([x[1] for x in self._users_with_prices if x[0] == user[0]])))

                # in the case of only one user
                if len(unique_users_with_sum_of_prices) == 1:
                    self._user_id = unique_users_with_sum_of_prices[0][0]
                    return unique_users_with_sum_of_prices[0][0]
                else:
                    # in the case of multiple users
                    user_winner = np.random.choice([x[0] for x in unique_users_with_sum_of_prices],
                                                   p=[x[1] / self._full_price for x in unique_users_with_sum_of_prices])
                    self._user_id = user_winner
                    return user_winner
            logger.info('[LotteryPurchase] could not pick winner of lottery purchase with purchase id: %s',
                        self._purchase_id)
        else:
            logger.info('[LotteryPurchase] could not pick winner of lottery purchase with purchase id: %s',
                        self._purchase_id)
            return None

    def validate_delivery_of_winner(self, user_id: int, delivery_date: datetime):
        """
        * Parameters: userId, deliveryDate
        * This function is responsible for validating that the winner of the lottery received the product
        * Returns: none
        """
        logger.info('[LotteryPurchase] validating delivery of winner of lottery purchase with purchase id: %s',
                    self._purchase_id)
        if user_id == self._user_id:
            self._status = PurchaseStatus.accepted
            self._date_of_purchase = datetime.now()
            self._delivery_date = delivery_date

    def invalidate_delivery_of_winner(self, user_id: int):
        """
        * Parameters: userId
        * This function is responsible for invalidating the delivery of the winner of the lottery
        * Returns: none
        """
        logger.info('[LotteryPurchase] invalidating delivery of winner of lottery purchase with purchase id: %s',
                    self._purchase_id)
        if user_id == self._user_id:
            self._status = PurchaseStatus.failed'''


class PurchaseFacade:
    # singleton
    __instance = None

    def __new__(cls):
        if PurchaseFacade.__instance is None:
            PurchaseFacade.__instance = object.__new__(cls)
        return PurchaseFacade.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # self._purchases: Dict[int, Purchase] = {}
            # self._ratings = []
            self._purchases_id_counter_lock = threading.Lock()
            # self._rating_id_counter = 0
            logger.info('[PurchaseFacade] successfully created purchase facade object')

    # -----------------Immediate Purchase Class related methods-----------------#
    '''def initialize_counter(self):
        """
        Initialize the purchase ID counter from the database or create it if it doesn't exist.
        """
        with self._purchases_id_counter_lock:
            try:
                counter = db.session.query(Counter).filter_by(name=PURCHASE_ID_COUNTER_NAME).first()
                if counter is None:
                    counter = Counter(name=PURCHASE_ID_COUNTER_NAME, value=0)
                    db.session.add(counter)
                    db.session.commit()
            except SQLAlchemyError as e:
                print(e)
                db.session.rollback()
                logger.error(f"Error initializing purchase ID counter: {e}")
                raise PurchaseError("Failed to initialize purchase ID counter", PurchaseErrorTypes.database_error)'''

    def create_immediate_purchase(self, user_id: int, total_price: float, total_price_after_discounts: float,
                                  shopping_cart: Dict[int, Tuple[List[PurchaseProductDTO], float, float]]) -> int:
        """
        * Parameters: userId, dateOfPurchase, deliveryDate, shoppingCart, total_price_after_discounts
        * This function is responsible for creating an immediate purchase
        * Note: total_price_after_discounts is not calculated yet! Initialized as -1!
        * Returns: bool
        """
        with self._purchases_id_counter_lock:
            if total_price < 0 or total_price_after_discounts < 0:
                raise PurchaseError("Total price must be a positive float", PurchaseErrorTypes.invalid_total_price)
            pur = create_immediate_purchase(user_id, total_price, shopping_cart, total_price_after_discounts)

            # no need to add because already added in the static function create_immediate_purchase
            db.session.commit()
            return pur.id

    """def __get_new_purchase_id(self) -> int:
        # new_id = self._purchases_id_counter
        # self._purchases_id_counter += 1
        # return new_id
        with self._purchases_id_counter_lock:
            try:
                with db.session.begin():
                    counter = db.session.query(Counter).filter_by(name=PURCHASE_ID_COUNTER_NAME).with_for_update().first()
                    if counter is None:
                        # If the counter doesn't exist, create it
                        raise PurchaseError("Purchase ID counter not found", PurchaseErrorTypes.database_error)
                    val = counter.value
                    counter.value += 1
                    # db.session.commit()
                return val
            except SQLAlchemyError as e:
                #db.session.rollback()
                raise e"""

    def get_purchases_of_user(self, user_id: int, store_id: Optional[int] = None) -> List[PurchaseDTO]:
        """
        * Parameters: userId
        * This function is responsible for returning the purchases of the user
        * Returns: list of Purchase objects
        """
        purchases: List[PurchaseDTO] = []
        for purchase in db.session.query(ImmediatePurchase).all():
            if purchase.user_id == user_id:
                if isinstance(purchase, ImmediatePurchase):
                    for sub_purchase in purchase.immediate_sub_purchases:
                        if store_id is None or sub_purchase.store_id == store_id:
                            conv_prod = [prod.get_dto() for prod in sub_purchase.products]
                            purchases.append(PurchaseDTO(sub_purchase.purchase_id, sub_purchase.store_id,
                                                         sub_purchase.date_of_purchase, sub_purchase.total_price,
                                                         sub_purchase.total_price_after_discounts,
                                                         sub_purchase.status.value, conv_prod))
                    # if another type of purchase
        return purchases

    def get_purchases_of_store(self, store_id: int) -> List[PurchaseDTO]:
        """
        * Parameters: storeId
        * This function is responsible for returning the purchases of the store
        * Returns: list of Purchase objects
        """
        purchases: List[PurchaseDTO] = []
        for purchase in db.session.query(ImmediatePurchase).all():
            if isinstance(purchase, ImmediatePurchase):
                for sub_purchase in purchase.immediate_sub_purchases:
                    if sub_purchase.store_id == store_id:
                        conv_prod = [prod.get_dto() for prod in sub_purchase.products]
                        purchases.append(PurchaseDTO(sub_purchase.purchase_id, sub_purchase.store_id,
                                                     sub_purchase.date_of_purchase, sub_purchase.total_price,
                                                     sub_purchase.total_price_after_discounts,
                                                     sub_purchase.status.value, conv_prod, purchase.user_id))
        return purchases

    # -----------------BidPurchase class related methods-----------------#
    def create_bid_purchase(self, user_id: int, proposed_price: float, store_id: int, product_id: int) -> int:
        """
        Parameters: userId, proposedPrice, storeId, productId
        This function is responsible for creating a bid purchase
        Returns: none
        """
        with self._purchases_id_counter_lock:
            if proposed_price < 0:
                raise PurchaseError("Proposed price is invalid", PurchaseErrorTypes.invalid_proposed_price)
            pur = BidPurchase(user_id, proposed_price, store_id, product_id)
            db.session.add(pur)
            db.session.commit()

            return pur.id

    def store_owner_manager_accept_offer(self, purchase_id: int, store_worker_id: int) -> None:
        """
        Parameters: purchaseId, storeWorkerId
        This function is responsible for the store owner/manager accepting the offer
        NOTE: the store owner/manager can only accept the offer if the purchase is ongoing, and the store owner/manager is validated if they are connected to store in marketfacade
        Returns: none
        """
        purchase = self.__get_purchase_by_id(purchase_id)
        if isinstance(purchase, BidPurchase):
            purchase.store_owner_manager_accept_offer(store_worker_id)
        else:
            raise PurchaseError("Purchase is not a bid purchase", PurchaseErrorTypes.purchase_not_bid_purchase)

        db.session.commit()

    def store_reject_offer(self, purchase_id: int, store_worker_id: int) -> int:
        """
        Parameters: purchaseId, storeWorkerId
        This function is responsible for the store rejecting the offer
        NOTE: the store owner/manager can only reject the offer if the purchase is ongoing, and the store owner/manager is validated if they are connected to store in marketfacade
        Returns: the id of the user who rejected the offer
        """
        purchase = self.__get_purchase_by_id(purchase_id)
        if isinstance(purchase, BidPurchase):
            ret = purchase.store_reject_offer(store_worker_id)
        else:
            raise PurchaseError("Purchase is not a bid purchase", PurchaseErrorTypes.purchase_not_bid_purchase)

        db.session.commit()
        return ret

    def store_accept_offer(self, purchase_id: int, store_workers_ids: List[int]) -> bool:
        """
        Parameters: purchaseId, storeWorkersIds
        This function is responsible for the store accepting the offer
        NOTE: the store can only accept the offer if the purchase is ongoing and all store owners/managers accepted the offer
        Returns: true if the store accepted the offer
        """
        purchase = self.__get_purchase_by_id(purchase_id)
        if isinstance(purchase, BidPurchase):
            ret = purchase.store_accept_offer(store_workers_ids)
        else:
            raise PurchaseError("Purchase is not a bid purchase", PurchaseErrorTypes.purchase_not_bid_purchase)
        db.session.commit()
        return ret

    def store_counter_offer(self, purchase_id: int, user_who_counter_offer: int, proposed_price: float) -> None:
        """
        Parameters: purchaseId, storeId, userWhoCounterOffer, proposedPrice
        This function is responsible for the store countering the offer
        NOTE: the store can only counter the offer if the purchase is ongoing, and the store is validated if they are connected to store in marketfacade
        Returns: none
        """
        purchase = self.__get_purchase_by_id(purchase_id)
        if isinstance(purchase, BidPurchase):
            purchase.store_counter_offer(user_who_counter_offer, proposed_price)
        else:
            raise PurchaseError("Purchase is not a bid purchase", PurchaseErrorTypes.purchase_not_bid_purchase)

        db.session.commit()

    def user_accept_counter_offer(self, purchase_id: int, user_id: int) -> None:
        """
        Parameters: purchaseId, userId
        This function is responsible for the user accepting the counter offer
        NOTE: the user can only accept the counter offer if the purchase is ongoing
        Returns: none
        """
        purchase = self.__get_purchase_by_id(purchase_id)
        if isinstance(purchase, BidPurchase):
            purchase.user_accept_counter_offer(user_id)
        else:
            raise PurchaseError("Purchase is not a bid purchase", PurchaseErrorTypes.purchase_not_bid_purchase)

        db.session.commit()

    def user_reject_counter_offer(self, purchase_id: int, user_id: int) -> None:
        """
        Parameters: purchaseId, userId
        This function is responsible for the user rejecting the offer
        NOTE: the user can only reject the offer if the purchase is ongoing
        Returns: none
        """
        purchase = self.__get_purchase_by_id(purchase_id)
        if isinstance(purchase, BidPurchase):
            purchase.user_reject_counter_offer(user_id)
        else:
            raise PurchaseError("Purchase is not a bid purchase", PurchaseErrorTypes.purchase_not_bid_purchase)

        db.session.commit()

    def user_counter_offer(self, purchase_id: int, user_id: int, proposed_price: float) -> None:
        """
        Parameters: purchaseId, userId, proposedPrice
        This function is responsible for the user countering the offer
        NOTE: the user can only counter the offer if the purchase is ongoing
        Returns: none
        """
        purchase = self.__get_purchase_by_id(purchase_id)
        if isinstance(purchase, BidPurchase):
            purchase.user_counter_offer(user_id, proposed_price)
        else:
            raise PurchaseError("Purchase is not a bid purchase", PurchaseErrorTypes.purchase_not_bid_purchase)

        db.session.commit()

    def is_bid_approved(self, purchase_id: int) -> bool:
        """
        Parameters: purchaseId
        This function is responsible for checking if the bid is approved
        Returns: bool
        """
        purchase = self.__get_purchase_by_id(purchase_id)
        if isinstance(purchase, BidPurchase):
            if purchase.status == PurchaseStatus.approved:
                return True
            return False
        raise PurchaseError("Purchase is not a bid purchase", PurchaseErrorTypes.purchase_not_bid_purchase)

    def get_bid_purchases_of_user(self, user_id: int) -> List[BidPurchaseDTO]:
        """
        Parameters: userId
        This function is responsible for returning the bid purchases of the user
        Returns: list of BidPurchase objects
        """
        purchases: List[BidPurchaseDTO] = []
        for purchase in db.session.query(BidPurchase).all():
            if isinstance(purchase, BidPurchase):
                if purchase.user_id == user_id:
                    purchases.append(BidPurchaseDTO(purchase.purchase_id, purchase.user_id, purchase.proposed_price,
                                                    purchase.store_id, purchase.product_id, purchase.date_of_purchase,
                                                    purchase.delivery_date, purchase.is_offer_to_store,
                                                    purchase.total_price, purchase.status.value,
                                                    purchase.list_of_store_owners_managers_that_accepted_offer,
                                                    purchase.user_who_rejected_id))
        return purchases

    def get_bid_purchases_of_store(self, store_id: int) -> List[BidPurchaseDTO]:
        """
        Parameters: storeId
        This function is responsible for returning the bid purchases of the store
        Returns: list of BidPurchase objects
        """
        purchases: List[BidPurchaseDTO] = []
        for purchase in db.session.query(BidPurchase).all():
            if isinstance(purchase, BidPurchase):
                if purchase.store_id == store_id:
                    purchases.append(BidPurchaseDTO(purchase.purchase_id, purchase.user_id, purchase.proposed_price,
                                                    purchase.store_id, purchase.product_id, purchase.date_of_purchase,
                                                    purchase.delivery_date, purchase.is_offer_to_store,
                                                    purchase.total_price, purchase.status.value,
                                                    purchase.list_of_store_owners_managers_that_accepted_offer,
                                                    purchase.user_who_rejected_id))
        return purchases
    
    def get_bid_purchase_by_id(self, purchase_id: int) -> BidPurchaseDTO:
        """
        Parameters: purchaseId
        This function is responsible for returning the bid purchase by id
        Returns: BidPurchase object
        """
        purchase = self.__get_purchase_by_id(purchase_id)
        if isinstance(purchase, BidPurchase):
            return BidPurchaseDTO(purchase.purchase_id, purchase.user_id, purchase.proposed_price,
                                  purchase.store_id, purchase.product_id, purchase.date_of_purchase,
                                  purchase.delivery_date, purchase.is_offer_to_store,
                                  purchase.total_price, purchase.status.value,
                                  purchase.list_of_store_owners_managers_that_accepted_offer,
                                  purchase.user_who_rejected_id)
        raise PurchaseError("Purchase is not a bid purchase", PurchaseErrorTypes.purchase_not_bid_purchase)

    # -----------------General Purchase class related methods-----------------#
    def accept_purchase(self, purchase_id: int, delivery_date: datetime) -> None:
        """
        * Parameters: purchaseId
        * This function is responsible for accepting the purchase
        * Returns: none
        """
        logger.info('[PurchaseFacade] attempting to accept purchase with purchase id: %s', purchase_id)
        purchase = self.__get_purchase_by_id(purchase_id)
        purchase.accept()
        if isinstance(purchase, ImmediatePurchase) or isinstance(purchase, BidPurchase):
            purchase.delivery_date = delivery_date

        db.session.commit()

    def reject_purchase(self, purchase_id: int) -> None:
        """
        * Parameters: purchaseId
        * This function is responsible for rejecting the purchase
        * Returns: none
        """
        logger.info('[PurchaseFacade] attempting to reject purchase with purchase id: %s', purchase_id)
        purchase = self.__get_purchase_by_id(purchase_id)
        if purchase.status == PurchaseStatus.accepted or purchase.status == PurchaseStatus.completed:
            raise PurchaseError("Purchase already accepted or completed",
                                PurchaseErrorTypes.purchase_already_accepted_or_completed)
        PurchaseProduct.query.filter_by(purchase_id=purchase_id).delete()
        ImmediateSubPurchase.query.filter_by(purchase_id=purchase_id).delete()
        ImmediatePurchase.query.filter_by(purchase_id=purchase_id).delete()
        BidPurchase.query.filter_by(purchase_id=purchase_id).delete()
        db.session.delete(purchase)
        db.session.commit()
        # del self._purchases[purchase_id]

    def cancel_accepted_purchase(self, purchase_id: int) -> None:
        """
        * Parameters: purchaseId
        * This function is responsible for canceling the accepted purchase
        * It removes the accepted purchase
        * Returns: none
        """
        logger.info('[PurchaseFacade] attempting to cancel accepted purchase with purchase id: %s', purchase_id)
        purchase = self.__get_purchase_by_id(purchase_id)
        if purchase.status != PurchaseStatus.accepted:
            raise PurchaseError("Purchase is not accepted", PurchaseErrorTypes.purchase_not_accepted)
        PurchaseProduct.query.filter_by(purchase_id=purchase_id).delete()
        ImmediateSubPurchase.query.filter_by(purchase_id=purchase_id).delete()
        ImmediatePurchase.query.filter_by(purchase_id=purchase_id).delete()
        BidPurchase.query.filter_by(purchase_id=purchase_id).delete()
        db.session.delete(purchase)
        db.session.commit()
        # del self._purchases[purchase_id]

    def complete_purchase(self, purchase_id: int):
        """
        * Parameters: purchaseId
        * This function is responsible for completing the purchase
        * Returns: none
        """
        logger.info('[PurchaseFacade] attempting to complete purchase with purchase id: %s', purchase_id)
        purchase = self.__get_purchase_by_id(purchase_id)
        purchase.complete()
        db.session.commit()

    def check_if_purchase_completed(self, purchase_id: int) -> bool:
        """
        * Parameters: purchaseId
        * This function is responsible for checking if the purchase is completed
        * Returns: bool
        """
        logger.info('[PurchaseFacade] attempting to check if purchase with purchase id: %s is completed', purchase_id)
        purchase = self.__get_purchase_by_id(purchase_id)
        return purchase.status == PurchaseStatus.completed

    def __get_purchase_by_id(self, purchase_id: int) -> Purchase:
        if self.__check_if_purchase_exists(purchase_id):
            return db.session.query(Purchase).get(purchase_id)
            #return self._purchases[purchase_id]
        raise PurchaseError("Purchase id is invalid", PurchaseErrorTypes.invalid_purchase_id)

    def __check_if_purchase_exists(self, purchase_id: int) -> bool:
        return db.session.query(Purchase).get(purchase_id) is not None
        # return purchase_id in self._purchases

    def clean_data(self):
        # self._purchases = {}
        # self._purchases_id_counter = 0
        # from backend.app import app
        # with app.app_context():
        db.session.query(PurchaseProduct).delete()
        db.session.query(ImmediateSubPurchase).delete()
        db.session.query(ImmediatePurchase).delete()
        db.session.query(BidPurchase).delete()
        db.session.query(Purchase).delete()
        # db.session.query(Counter).filter_by(name=PURCHASE_ID_COUNTER_NAME).update({"value": 0})
        db.session.commit()

    '''def create_bid_purchase(self, user_id: int, proposed_price: float, product_id: int, product_spec_id: int,
                            store_id: int,
                            is_offer_to_store: bool = True) -> bool:
        """
        * Parameters: userId, proposedPrice, productId, productSpecId, storeId, isOfferToStore
        * This function is responsible for creating a bid purchase
        * Note: totalPrice initialized as -1 until it is accepted!
        * Returns: bool
        """
        if user_id is not None:
            if proposed_price is not None and proposed_price >= 0:
                if product_id is not None and product_spec_id is not None and store_id is not None:
                    bid_purchase = BidPurchase(self._purchases_id_counter, user_id, proposed_price, product_id,
                                               product_spec_id, store_id, is_offer_to_store)
                    self._purchases.append(bid_purchase)
                    self._purchases_id_counter += 1
                    logger.info('[PurchaseFacade] created bid purchase with purchase id: %s',
                                bid_purchase.purchase_id)
                    return True
                else:
                    raise ValueError("Product id, product spec id or store id is invalid")
            else:
                raise ValueError("Proposed price is invalid")
        else:
            raise ValueError("User id is invalid")'''

    '''def create_auction_purchase(self, base_price: float, starting_date: datetime, ending_date: datetime, store_id: int,
                                product_id: int, product_spec_id: int,
                                users_with_proposed_prices: List[Tuple[int, float]] = []) -> bool:
        """
        * Parameters: basePrice, startingDate, endingDate, storeId, productId, productSpecId, usersWithProposedPrices
        * This function is responsible for creating an auction purchase
        * Returns: bool
        """
        if base_price is not None and base_price >= 0:
            if starting_date is not None:
                if ending_date is not None and ending_date > starting_date:
                    if store_id is not None and product_id is not None and product_spec_id is not None:
                        auction_purchase = AuctionPurchase(self._purchases_id_counter, base_price, starting_date,
                                                           ending_date, store_id, product_id, product_spec_id,
                                                           users_with_proposed_prices)
                        self._purchases.append(auction_purchase)
                        self._purchases_id_counter += 1
                        logger.info('[PurchaseFacade] created auction purchase with purchase id: %s',
                                    auction_purchase.purchase_id)
                        return True
                    else:
                        raise ValueError("Store id, product id or product spec id is invalid")
                else:
                    raise ValueError("Ending date is invalid")
            else:
                raise ValueError("Starting date is invalid")
        else:
            raise ValueError("Base price is invalid")'''

    '''def create_lottery_purchase(self, user_id: int, full_price: float, store_id: int, product_id: int,
                                product_spec_id: int,
                                starting_date: datetime, ending_date: datetime,
                                users_with_prices: List[Tuple[int, float]] = []) -> LotteryPurchase:
        """
        * Parameters: userId, totalPrice, fullPrice, storeId, productId, productSpecId, startingDate, endingDate,
        usersWithPrices
        * This function is responsible for creating a lottery purchase
        * Note: totalPrice initialized as 0 until people bought lottery tickets!
        * Returns: bool
        """

        if user_id is not None:
            if full_price is not None and full_price >= 0:
                if store_id is not None and product_id is not None and product_spec_id is not None:
                    if starting_date is not None:
                        if ending_date is not None and ending_date > starting_date:
                            lottery_purchase = LotteryPurchase(self._purchases_id_counter, full_price, store_id,
                                                               product_id, product_spec_id, starting_date, ending_date,
                                                               users_with_prices)
                            self._purchases.append(lottery_purchase)
                            self._purchases_id_counter += 1
                            logger.info('[PurchaseFacade] created lottery purchase with purchase id: %s',
                                        lottery_purchase.purchase_id)
                            return lottery_purchase
                        else:
                            raise ValueError("Ending date is invalid")
                    else:
                        raise ValueError("Starting date is invalid")
                else:
                    raise ValueError("Store id, product id or product spec id is invalid")
            else:
                raise ValueError("Full price is invalid")
        else:
            raise ValueError("User id is invalid")'''

    '''def get_on_going_purchases(self) -> List[Purchase]:
        """
        * Parameters: none
        * This function is responsible for returning the ongoing purchases
        * Returns: list of Purchase objects
        """
        logger.info('[PurchaseFacade] attempting to get ongoing purchases')
        return [purchase for purchase in self._purchases if purchase.get_status() == PurchaseStatus.onGoing]'''

    '''def get_completed_purchases(self) -> List[Purchase]:
        """
        * Parameters: none
        * This function is responsible for returning the completed purchases
        * Returns: list of Purchase objects
        """
        logger.info('[PurchaseFacade] attempting to get completed purchases')
        return [purchase for purchase in self._purchases if purchase.get_status() == PurchaseStatus.completed]'''

    '''def get_failed_purchases(self) -> List[Purchase]:
        """
        * Parameters: none
        * This function is responsible for returning the failed purchases
        * Returns: list of Purchase objects
        """
        logger.info('[PurchaseFacade] attempting to get failed purchases')
        return [purchase for purchase in self._purchases if purchase.get_status() == PurchaseStatus.failed]

    def get_accepted_purchases(self) -> List[Purchase]:
        """
        * Parameters: none
        * This function is responsible for returning the accepted purchases
        * Returns: list of Purchase objects
        """
        logger.info('[PurchaseFacade] attempting to get accepted purchases')
        return [purchase for purchase in self._purchases if purchase.get_status() == PurchaseStatus.accepted]'''

    '''def get_purchase_by_id(self, purchase_id: int) -> Purchase:
        """
        * Parameters: purchaseId
        * This function is responsible for returning the purchase by its id
        * Returns: Purchase object
        """
        if purchase_id is not None:
            for purchase in self._purchases:
                if purchase.purchase_id() == purchase_id:
                    return purchase
        else:
            raise ValueError("Purchase id is invalid")'''

    '''def update_status(self, purchase_id: int, status: PurchaseStatus):
        """
        * Parameters: purchaseId
        * This function is responsible for updating the status of the purchase
        * Returns: none
        """
        logger.info('[PurchaseFacade] attempting to update status of purchase with purchase id: %s', purchase_id)
        purchase = self.get_purchase_by_id(purchase_id)
        if purchase is not None:
            purchase.update_status(status)'''

    '''def update_date_of_purchase(self, purchase_id: int, date_of_purchase: datetime):
        """
        * Parameters: purchaseId
        * This function is responsible for updating the date of the purchase
        * Returns: none
        """
        logger.info('[PurchaseFacade] attempting to update date of purchase of purchase with purchase id: %s',
                    purchase_id)
        purchase = self.get_purchase_by_id(purchase_id)
        if purchase is not None:
            purchase.update_date_of_purchase(date_of_purchase)'''

    '''def calculate_total_price(self, purchase_id: int) -> float:
        """
        * Parameters: purchaseId
        * This function is responsible for calculating the total price of the purchase
        * Returns: float of total price
        """
        logger.info('[PurchaseFacade] calculating total price of purchase with purchase id: %s', purchase_id)
        purchase = self.get_purchase_by_id(purchase_id)
        if purchase is not None:
            return purchase.calculate_total_price()
        else:
            raise ValueError("Purchase id is invalid")'''

    '''def has_user_already_rated_store(self, purchase_id: int, user_id: int, store_id: int) -> bool:
        """
        * Parameters: purchaseId, userId, storeId
        * This function is responsible for checking if the user has already rated the store in a given purchase
         (this does not stop the user from rating the same store twice if they have two purchases)
        * Returns: true if rated, false if not
        """
        logger.info(
            '[PurchaseFacade] checking if user with user id: %s has already rated store with store id: %s in '
            'purchase with purchase id: %s',
            user_id, store_id, purchase_id)
        for rating in self._ratings:
            if isinstance(rating, StoreRating):
                if rating.purchase_id == purchase_id and rating.user_id == user_id and rating.store_id == store_id:
                    return True
        return False'''

    '''def has_user_already_rated_product(self, purchase_id: int, user_id: int, product_spec_id: int) -> bool:
        """
        * Parameters: purchaseId, userId, storeId
        * This function is responsible for checking if the user has already rated the product in a given purchase
        * Note: this does not stop the user from rating the product twice if they bought the product more than once
        * Returns: true if rated, false if not
        """
        logger.info(
            '[PurchaseFacade] checking if user with user id: %s has already rated product with product spec id: %s'
            ' in purchase with purchase id: %s',
            user_id, product_spec_id, purchase_id)
        for rating in self._ratings:
            if isinstance(rating, ProductRating):
                if (rating.purchase_id == purchase_id and rating.user_id == user_id
                        and rating.product_id == product_spec_id):
                    return True
        return False'''

    '''def calculate_new_store_rating(self, store_id: int) -> float:
        """
        * Parameters: storeId
        * This function is responsible for calculating the new rating of the store
        * Returns: the new value of the rating of the store
        """
        logger.info('[PurchaseFacade] calculating new rating of store with store id: %s', store_id)
        ratings = [rating for rating in self._ratings if
                   isinstance(rating, StoreRating) and rating.store_id == store_id]
        return sum([rating.rating() for rating in ratings]) / len(ratings)'''

    '''def calculate_new_product_rating(self, product_spec_id: int) -> float:
        """
        * Parameters: productSpecId
        * This function is responsible for calculating the new rating of the product
        * Returns: the new value of the rating of the product
        """
        logger.info('[PurchaseFacade] calculating new rating of product with product spec id: %s', product_spec_id)
        ratings = [rating for rating in self._ratings if
                   isinstance(rating, ProductRating) and rating.product_id == product_spec_id]
        return sum([rating.rating for rating in ratings]) / len(ratings)'''

    '''def rate_store(self, purchase_id: int, user_id: int, store_id: int, rating: float, description: str) -> float:
        """
        * Parameters: purchaseId, userId, rating, storeId
        * This function is responsible for rating the store
        * Returns: the new value of the rating of the store
        """
        purchase = self.get_purchase_by_id(purchase_id)
        if purchase is not None:
            if purchase.store_id == store_id:
                if purchase.status == PurchaseStatus.completed:
                    if not self.has_user_already_rated_store(purchase_id, user_id, store_id):
                        if purchase.user_id == user_id:
                            store_rating = StoreRating(self._rating_id_counter, rating, purchase_id, user_id,
                                                       description, store_id)
                            self._ratings.append(store_rating)
                            self._rating_id_counter += 1
                            return self.calculate_new_store_rating(store_id)
                        else:
                            raise ValueError("User id is invalid")
                    else:
                        raise ValueError("User has already rated store")
                else:
                    raise ValueError("Purchase is not completed")
            else:
                raise ValueError("Store id is invalid")
        else:
            raise ValueError("Purchase id is invalid")'''

    '''def rate_product(self, purchase_id: int, user_id: int, product_spec_id: int, rating: float, description: str) \
            -> float:
        """
        * Parameters: purchaseId, userId, rating, productSpecId
        * This function is responsible for rating the product
        * Returns: the new value of the rating of the product
        """
        purchase = self.get_purchase_by_id(purchase_id)
        if purchase is not None:
            if purchase.status == PurchaseStatus.completed:
                if not self.has_user_already_rated_product(purchase_id, user_id, product_spec_id):
                    if purchase.user_id == user_id:
                        product_rating = ProductRating(self._rating_id_counter, rating, purchase_id, user_id,
                                                       description, product_spec_id)
                        self._ratings.append(product_rating)
                        self._rating_id_counter += 1
                        return self.calculate_new_product_rating(product_spec_id)
                    else:
                        raise ValueError("User id is invalid")
                else:
                    raise ValueError("User has already rated product")
            else:
                raise ValueError("Purchase is not completed")
        else:
            raise ValueError("Purchase id is invalid")'''

    '''def check_if_completed_purchase(self, purchase_id: int) -> bool:
        """
        * Parameters: purchaseId
        * This function is responsible for checking if the purchase is completed, and updating if it is
        * Returns: true if completed, false otherwise
        """
        purchase = self.get_purchase_by_id(purchase_id)
        if purchase is not None:
            return purchase.check_if_completed_purchase()
        else:
            raise ValueError("Purchase id is invalid")'''

    # -----------------Immediate-----------------#
    # For now, we will return the price without any discounts.
    '''def calculate_total_price_after_discounts(self, purchase_id: int) -> float:
        """
        * Parameters: purchaseId
        * This function is responsible for calculating the total price of the purchase after discounts
        * Returns: float of total price after discounts
        """
        immediate_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(immediate_purchase, ImmediatePurchase):
            if (immediate_purchase.status == PurchaseStatus.onGoing
                    or immediate_purchase.status == PurchaseStatus.accepted):
                return immediate_purchase.calculate_total_price_after_discounts([])
            else:
                raise ValueError("Purchase is not ongoing")
        else:
            raise ValueError("Purchase is not immediate")'''

    '''def validate_purchase_of_user_immediate(self, purchase_id: int, user_id: int, delivery_date: datetime):
        """
        * Parameters: purchaseId, userId
        * This function is responsible for validating that the user successfully paid for the product and the product is
         underway
        * Returns: none
        """
        immediate_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(immediate_purchase, ImmediatePurchase):
            # TODO: what to do here? function is not implemented in ImmediatePurchase
            # immediate_purchase.validatePurchaseOfUser(user_id, delivery_date)
            pass
        else:
            raise ValueError("Purchase is not immediate")'''

    '''def invalidate_purchase_of_user_immediate(self, purchase_id: int, user_id: int):
        """
        * Parameters: purchaseId, userId
        * This function is responsible for invalidating the purchase of the user, whether it be due to not paying or not
         able to deliver
        * Returns: none
        """
        immediate_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(immediate_purchase, ImmediatePurchase):
            # TODO: what to do here? function is not implemented in ImmediatePurchase
            # immediate_purchase.invalidatePurchaseOfUser(user_id)
            pass
        else:
            raise ValueError("Purchase is not immediate")'''

    # -----------------Bid-----------------#
    '''def store_accept_offer(self, purchase_id: int):
        """
        * Parameters: purchaseId
        * Validate that all store owners and managers with permissions accepted the offer
        * Returns: none
        """
        bid_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(bid_purchase, BidPurchase):
            if bid_purchase.status == PurchaseStatus.onGoing:
                bid_purchase.store_accept_offer(bid_purchase.delivery_date)
            else:
                raise ValueError("Purchase is not ongoing")
        else:
            raise ValueError("Purchase is not bid")'''

    '''def user_accept_offer(self, purchase_id: int, user_id: int):
        """
        * Parameters: purchaseId, userId
        * Function to accept the offer by the store
        * Returns: none
        """
        bid_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(bid_purchase, BidPurchase):
            if bid_purchase.status == PurchaseStatus.onGoing:
                bid_purchase.user_accept_offer(user_id, bid_purchase.delivery_date)
            else:
                raise ValueError("Purchase is not ongoing")
        else:
            raise ValueError("Purchase is not bid")'''

    '''def store_reject_offer(self, purchase_id: int):
        """
        * Parameters: purchaseId
        * Validate that one store owner or managers with permissions rejected the offer
        * Returns: none
        """
        bid_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(bid_purchase, BidPurchase):
            if bid_purchase.status == PurchaseStatus.onGoing:
                bid_purchase.store_reject_offer()
            else:
                raise ValueError("Purchase is not ongoing")
        else:
            raise ValueError("Purchase is not bid")'''

    '''def user_reject_offer(self, purchase_id: int, user_id: int):
        """
        * Parameters: purchaseId, userId
        * Function to reject the offer by the store
        * Returns: none
        """
        bid_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(bid_purchase, BidPurchase):
            if bid_purchase.status == PurchaseStatus.onGoing:
                bid_purchase.user_reject_offer(user_id)
            else:
                raise ValueError("Purchase is not ongoing")
        else:
            raise ValueError("Purchase is not bid")'''

    '''def store_counter_offer(self, purchase_id: int, counter_offer: float):
        """
        * Parameters: purchaseId, counterOffer
        * This function is responsible for updating the counter offer of the purchase
        * Returns: none
        """
        bid_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(bid_purchase, BidPurchase):
            if bid_purchase.status == PurchaseStatus.onGoing:
                bid_purchase.store_counter_offer(counter_offer)
            else:
                raise ValueError("Purchase is not ongoing")
        else:
            raise ValueError("Purchase is not bid")'''

    '''def user_counter_offer(self, counter_offer: float, purchase_id: int):
        """
        * Parameters: purchaseId, counterOffer
        * This function is responsible for updating the counter offer of the purchase
        * Returns: none
        """
        bid_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(bid_purchase, BidPurchase):
            if bid_purchase.status == PurchaseStatus.onGoing:
                bid_purchase.user_counter_offer(counter_offer)
            else:
                raise ValueError("Purchase is not ongoing")
        else:
            raise ValueError("Purchase is not bid")'''

    # -----------------Auction-----------------#
    '''def add_auction_bid(self, user_id: int, proposed_price: float, purchase_id: int) -> bool:
        """
        * Parameters: userId, proposedPrice, purchaseId
        * This function is responsible for adding the user and their proposed price to the list of users with proposed
         prices, the same user can bid multiple times
        * Note: a bid can only be added if it is bigger than the current highest bid
        * Returns: true if bid was added
        """
        auction_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(auction_purchase, AuctionPurchase):
            if auction_purchase.status == PurchaseStatus.onGoing:
                return auction_purchase.add_auction_bid(user_id, proposed_price)
            else:
                raise ValueError("Purchase is not ongoing")
        else:
            raise ValueError("Purchase is not auction")'''

    '''def view_highest_bidding_offer(self, purchase_id: int) -> float:
        """
        * Parameters: purchaseId
        * This function is responsible for returning the highest bidding offer
        * Returns: float of highest bidding offer
        """
        auction_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(auction_purchase, AuctionPurchase):
            if auction_purchase.status == PurchaseStatus.onGoing or auction_purchase.status == PurchaseStatus.accepted:
                return auction_purchase.view_highest_bidding_offer()
            else:
                raise ValueError("Purchase is not ongoing")
        else:
            raise ValueError("Purchase is not auction")'''

    '''def check_if_auction_ended(self, purchase_id: int) -> bool:
        """
        * Parameters: purchaseId
        * This function is responsible for checking if the auction has ended
        * Returns: true if ended
        """
        auction_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(auction_purchase, AuctionPurchase):
            return auction_purchase.check_if_auction_ended()
        else:
            raise ValueError("Purchase is not auction")'''

    '''def validate_purchase_of_user_auction(self, purchase_id: int, user_id: int, delivery_date: datetime):
        """
        * Parameters: purchaseId, userId
        * This function is responsible for validating that the user with the highest bid successfully paid for the
        product and the product is underway
        * Returns: none
        """
        auction_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(auction_purchase, AuctionPurchase):
            auction_purchase.validate_purchase_of_user(user_id, delivery_date)
        else:
            raise ValueError("Purchase is not auction")'''

    '''def invalidate_purchase_of_user_auction(self, purchase_id: int, user_id: int):
        """
        * Parameters: purchaseId, userId
        * This function is responsible for invalidating the purchase of the user with the highest bid, whether it be due
         to not paying or not able to deliver
        * Returns: none
        """
        auction_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(auction_purchase, AuctionPurchase):
            auction_purchase.invalidate_purchase_of_user(user_id)
        else:
            raise ValueError("Purchase is not auction")'''

    # -----------------Lottery-----------------#

    '''def calculate_remaining_time(self, purchase_id: int) -> timedelta:
        """
        * Parameters: purchaseId
        * This function is responsible for calculating the remaining time for the auction
        * Returns: datetime of remaining time
        """
        purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(purchase, LotteryPurchase) or isinstance(purchase, AuctionPurchase):
            if purchase.status == PurchaseStatus.onGoing:
                return purchase.calculate_remaining_time()
            else:
                raise ValueError("Purchase is not ongoing")
        else:
            raise ValueError("Purchase is not lottery")'''

    '''def add_lottery_offer(self, user_id: int, proposed_price: float, purchase_id: int) -> bool:
        """
        * Parameters: userId, proposedPrice, purchaseId
        * This function is responsible for adding the user and their proposed price to the list of users with proposed
        prices, the same user can bid multiple times
        * Note: a bid can only be added if it is bigger than the current highest bid
        * Returns: true if bid was added
        """
        lottery_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(lottery_purchase, LotteryPurchase):
            if lottery_purchase.status == PurchaseStatus.onGoing:
                return lottery_purchase.add_lottery_offer(user_id, proposed_price)
            else:
                raise ValueError("Purchase is not ongoing")
        else:
            raise ValueError("Purchase is not lottery")'''

    '''def calculate_probability_of_user(self, user_id: int, purchase_id: int) -> float:
        """
        * Parameters: userId, purchaseId
        * This function is responsible for calculating the probability of the user winning the lottery
        * Returns: float of probability
        """
        lottery_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(lottery_purchase, LotteryPurchase):
            if lottery_purchase.status == PurchaseStatus.onGoing or lottery_purchase.status == PurchaseStatus.accepted:
                return lottery_purchase.calculate_probability_of_user(user_id)
            else:
                raise ValueError("Purchase is not ongoing")
        else:
            raise ValueError("Purchase is not lottery")

    def validate_user_offers(self, purchase_id: int) -> bool:
        """
        * Parameters: purchaseId
        * This function is responsible for validating that all users with offers have paid the full price
        * Returns: true if all users have paid the full price
        """
        lottery_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(lottery_purchase, LotteryPurchase):
            if lottery_purchase.ending_date < datetime.now():
                return lottery_purchase.validate_user_offers()
            else:
                raise ValueError("Lottery has ended")
        else:
            raise ValueError("Purchase is not lottery")

    def pick_winner(self, purchase_id: int) -> int:
        """
        * Parameters: purchaseId
        * This function is responsible for picking the winner of the lottery
        * Returns: userId of the winner
        """
        lottery_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(lottery_purchase, LotteryPurchase):
            if lottery_purchase.status == PurchaseStatus.accepted:
                return lottery_purchase.pick_winner()
            else:
                raise ValueError("Purchase is not accepted")
        else:
            raise ValueError("Purchase is not lottery")

    def validate_delivery_of_winner(self, purchase_id: int, user_id: int, delivery_date: datetime):
        """
        * Parameters: purchaseId, userId, deliveryDate
        * This function is responsible for validating that the winner of the lottery received the product
        * Returns: none
        """
        lottery_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(lottery_purchase, LotteryPurchase):
            lottery_purchase.validate_delivery_of_winner(user_id, delivery_date)
        else:
            raise ValueError("Purchase is not lottery")

    def invalidate_delivery_of_winner(self, purchase_id: int, user_id: int):
        """
        * Parameters: purchaseId, userId
        * This function is responsible for invalidating the delivery of the winner of the lottery
        * Returns: none
        """
        lottery_purchase = self.get_purchase_by_id(purchase_id)
        if isinstance(lottery_purchase, LotteryPurchase):
            lottery_purchase.invalidate_delivery_of_winner(user_id)
        else:
            raise ValueError("Purchase is not lottery")'''
