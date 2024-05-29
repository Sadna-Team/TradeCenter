# ----------------- imports -----------------#
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Tuple, Optional, Dict
from backend.business.DTOs import PurchaseProductDTO, PurchaseDTO

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


# ---------------------purchaseStatus Enum---------------------#
class PurchaseStatus(Enum):
    # Enum for the status of the purchase
    onGoing = 1
    accepted = 2
    completed = 3


# -----------------Purchase Class-----------------#
class Purchase(ABC):
    # interface for the purchase classes, contains the common attributes and methods for the purchase classes
    def __init__(self, purchase_id: int, user_id: int, date_of_purchase: Optional[datetime],
                 total_price: float, total_price_after_discounts: float, status: PurchaseStatus):
        self._purchase_id = purchase_id
        self._user_id = user_id
        self._date_of_purchase = date_of_purchase
        self._total_price = total_price
        self._total_price_after_discounts: float = total_price_after_discounts
        self._status = status

    def check_if_completed_purchase(self) -> bool:
        """
        * Parameters: none
        * This function is responsible for checking if the purchase is completed, and updating if it is
        * Returns: true if completed, false otherwise
        """
        return self._status == PurchaseStatus.completed

    # ---------------------------------Getters and Setters---------------------------------#
    @property
    def purchase_id(self):
        return self._purchase_id

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

    def accept(self):
        self._status = PurchaseStatus.accepted

    def complete(self):
        self._status = PurchaseStatus.completed


# -----------------ImmediateSubPurchases class-----------------#
class ImmediateSubPurchase(Purchase):
    # purchaseId and storeId are unique identifier of the immediate purchase, storeId used to retrieve the details of
    # the store
    def __init__(self, purchase_id: int, store_id: int, user_id: int, date_of_purchase: Optional[datetime],
                 total_price: float, total_price_after_discounts: float, status: PurchaseStatus,
                 products: List[PurchaseProductDTO]):
        super().__init__(purchase_id, user_id, date_of_purchase, total_price, total_price_after_discounts, status)
        self._store_id: int = store_id
        self._products: List[PurchaseProductDTO] = products
        logger.info('[ImmediateSubPurchases] successfully created immediate sub purchase object with purchase id: %s',
                    purchase_id)

    def accept(self):
        self._status = PurchaseStatus.accepted

    def complete(self):
        self._status = PurchaseStatus.completed

    # ---------------------------------Getters and Setters---------------------------------#
    @property
    def store_id(self):
        return self._store_id

    @property
    def products(self):
        return self._products


# -----------------ImmediatePurchase class-----------------#
class ImmediatePurchase(Purchase):
    # purchaseId is the unique identifier of the immediate purchase, purchase by a user of their shoppingCart
    # Note: storeId is -1 since immediatePurchase is not directly related to a store
    # Note: List[Tuple[Tuple[int,float],List[int]]] -> List of shoppingBaskets where shoppingBasket is a tuple of a
    #       tuple of storeId and totalPrice and a list of productIds
    def __init__(self, purchase_id: int, user_id: int, total_price: float,
                 shopping_cart: Dict[int, Tuple[List[PurchaseProductDTO], float, float]],
                 total_price_after_discounts: float = -1):
        super().__init__(purchase_id, user_id, datetime.now(), total_price, total_price_after_discounts,
                         PurchaseStatus.onGoing)
        self._delivery_date: Optional[datetime] = None  # for now, it will be updated once a purchase was accepted
        self._immediate_sub_purchases: List[ImmediateSubPurchase] = []
        self.__sub_purchase_id_serializer: int = 0
        for store_id in shopping_cart:
            products = shopping_cart[store_id][0]
            price = shopping_cart[store_id][1]
            price_after_discounts = shopping_cart[store_id][2]
            immediate_sub_purchase = ImmediateSubPurchase(self.__get_new_sub_purchase_id(), store_id, user_id,
                                                          None, price, price_after_discounts, PurchaseStatus.onGoing,
                                                          products)
            self._immediate_sub_purchases.append(immediate_sub_purchase)
        logger.info('[ImmediatePurchase] successfully created immediate purchase object with purchase id: %s',
                    purchase_id)

    @property
    def delivery_date(self):
        return self._delivery_date

    @delivery_date.setter
    def delivery_date(self, delivery_date: datetime):
        self._delivery_date = delivery_date

    @property
    def immediate_sub_purchases(self):
        return self._immediate_sub_purchases

    def __get_new_sub_purchase_id(self) -> int:
        new_id = self.__sub_purchase_id_serializer
        self.__sub_purchase_id_serializer += 1
        return new_id

    def accept(self):
        super().accept()
        for sub_purchase in self._immediate_sub_purchases:
            sub_purchase.accept()

    def complete(self):
        super().complete()
        for sub_purchase in self._immediate_sub_purchases:
            sub_purchase.complete()


# -----------------BidPurchase class-----------------#
'''class BidPurchase(Purchase):
    # purchaseId and productId are the unique identifiers for the product rating, productSpec used to retrieve the
    # details of product
    def __init__(self, purchase_id: int, user_id: int, proposed_price: float, product_id: int, product_spec_id: int,
                 store_id: int, is_offer_to_store: bool = True):
        super().__init__(purchase_id, user_id, store_id, None, -1, PurchaseStatus.onGoing)
        self._proposed_price = proposed_price
        self._product_id = product_id
        self._product_spec_id = product_spec_id
        self._delivery_date = None
        self._is_offer_to_store = is_offer_to_store
        self._counter_offer = -1
        logger.info('[BidPurchase] successfully created bid purchase object with purchase id: %s',
                    self._purchase_id)

    # ---------------------------------Getters and Setters---------------------------------#
    @property
    def proposed_price(self):
        return self._proposed_price

    @property
    def product_id(self):
        return self._product_id

    @property
    def delivery_date(self):
        return self._delivery_date

    # ---------------------------------Methods---------------------------------#
    def update_status(self, status: PurchaseStatus):
        self._status = status
        logger.info('[BidPurchase] attempting to update status of bid purchase with purchase id: %s',
                    self._purchase_id)

    def update_date_of_purchase(self, date_of_purchase: datetime):
        logger.info('[BidPurchase] attempting to update date of purchase of bid purchase with purchase id: %s',
                    self._purchase_id)
        self._date_of_purchase = date_of_purchase

    def calculate_total_price(self) -> float:
        return self._proposed_price

    def check_if_completed_purchase(self) -> bool:
        if self._status == PurchaseStatus.accepted:
            if self._delivery_date < datetime.now():
                self.update_status(PurchaseStatus.completed)
                logger.info('[BidPurchase] purchase with purchase id: %s has been completed',
                            self._purchase_id)
                return True
        return False

    def store_accept_offer(self, delivery_date: datetime):
        """
        * Parameters:
        * Validate that all store owners and managers with permissions accepted the offer and price paid and delivery
        * works
        * Returns: none
        """
        self.update_status(PurchaseStatus.accepted)
        self.update_date_of_purchase(datetime.now())
        self._delivery_date(delivery_date)
        logger.info('[BidPurchase] store accepted offer of bid purchase with purchase id: %s',
                    self._purchase_id)

    def user_accept_offer(self, user_id: int, delivery_date: datetime):
        """
        * Parameters: userId
        * Function to accept the offer by the store
        * Returns: none
        """
        if user_id == self._user_id:
            self.update_status(PurchaseStatus.accepted)
            self.update_date_of_purchase(datetime.now())
            self._delivery_date = delivery_date
            logger.info('[BidPurchase] user accepted offer of bid purchase with purchase id: %s',
                        self._purchase_id)

    def store_reject_offer(self):
        """
        * Parameters:
        * Validate that one store owner or managers with permissions rejected the offer
        * Returns: none
        """
        self._status = PurchaseStatus.failed
        logger.info('[BidPurchase] store rejected offer of bid purchase with purchase id: %s',
                    self._purchase_id)

    def user_reject_offer(self, user_id: int):
        """
        * Parameters: userId
        * Function to reject the offer by the store
        * Returns: none
        """
        if user_id == self._user_id:
            self._status = PurchaseStatus.failed
            logger.info('[BidPurchase] user rejected offer of bid purchase with purchase id: %s',
                        self._purchase_id)

    def store_counter_offer(self, counter_offer: float):
        """
        * Parameters: counterOffer
        * This function is responsible for updating the counter offer of the purchase
        * Returns: none
        """
        if self._status == PurchaseStatus.onGoing:
            if counter_offer >= 0:
                self._counter_offer = counter_offer
                self._is_offer_to_store = False
                logger.info('[BidPurchase] store counter offer of bid purchase with purchase id: %s',
                            self._purchase_id)
            else:
                raise ValueError("Counter offer must be a positive float")

    def user_counter_offer(self, counter_offer: float):
        """
        * Parameters: counterOffer
        * This function is responsible for updating the counter offer of the purchase
        * Returns: none
        """
        if self._status == PurchaseStatus.onGoing:
            if counter_offer >= 0:
                self._counter_offer = counter_offer
                self._is_offer_to_store = True
                logger.info('[BidPurchase] user counter offer of bid purchase with purchase id: %s',
                            self._purchase_id)
            else:
                raise ValueError("Counter offer must be a positive float")


# -----------------AuctionPurchase class-----------------#
class AuctionPurchase(Purchase):
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
            self._purchases: Dict[int, Purchase] = {}
            # self._ratings = []
            self._purchases_id_counter = 0
            # self._rating_id_counter = 0
            logger.info('[PurchaseFacade] successfully created purchase facade object')

    # -----------------Purchases in general-----------------#
    def create_immediate_purchase(self, user_id: int, total_price: float,
                                  shopping_cart: Dict[int, Tuple[List[PurchaseProductDTO], float, float]]) -> None:
        """
        * Parameters: userId, dateOfPurchase, deliveryDate, shoppingCart, total_price_after_discounts
        * This function is responsible for creating an immediate purchase
        * Note: total_price_after_discounts is not calculated yet! Initialized as -1!
        * Returns: bool
        """
        if total_price < 0:
            raise ValueError("Total price must be a positive float")

        pur = ImmediatePurchase(self.__get_new_purchase_id(), user_id, total_price, shopping_cart)

        self._purchases[pur.purchase_id] = pur

    def __get_new_purchase_id(self) -> int:
        new_id = self._purchases_id_counter
        self._purchases_id_counter += 1
        return new_id

    def get_purchases_of_user(self, user_id: int) -> List[PurchaseDTO]:
        """
        * Parameters: userId
        * This function is responsible for returning the purchases of the user
        * Returns: list of Purchase objects
        """
        purchases: List[PurchaseDTO] = []
        for purchase in self._purchases.values():
            if purchase.user_id == user_id:
                if isinstance(purchase, ImmediatePurchase):
                    for sub_purchase in purchase.immediate_sub_purchases:
                        purchases.append(PurchaseDTO(sub_purchase.purchase_id, sub_purchase.store_id,
                                                     sub_purchase.date_of_purchase, sub_purchase.total_price,
                                                     sub_purchase.total_price_after_discounts,
                                                     sub_purchase.status.value, sub_purchase.products))
                # if another type of purchase

        return purchases

    def get_purchases_of_store(self, store_id: int) -> List[PurchaseDTO]:
        """
        * Parameters: storeId
        * This function is responsible for returning the purchases of the store
        * Returns: list of Purchase objects
        """
        purchases: List[PurchaseDTO] = []
        for purchase in self._purchases.values():
            if isinstance(purchase, ImmediatePurchase):
                for sub_purchase in purchase.immediate_sub_purchases:
                    if sub_purchase.store_id == store_id:
                        purchases.append(PurchaseDTO(sub_purchase.purchase_id, sub_purchase.store_id,
                                                     sub_purchase.date_of_purchase, sub_purchase.total_price,
                                                     sub_purchase.total_price_after_discounts,
                                                     sub_purchase.status.value, sub_purchase.products))
        return purchases

    def accept_purchase(self, purchase_id: int) -> None:
        """
        * Parameters: purchaseId
        * This function is responsible for accepting the purchase
        * Returns: none
        """
        logger.info('[PurchaseFacade] attempting to accept purchase with purchase id: %s', purchase_id)
        purchase = self.__get_purchase_by_id(purchase_id)
        purchase.accept()

    def reject_purchase(self, purchase_id: int) -> None:
        """
        * Parameters: purchaseId
        * This function is responsible for rejecting the purchase
        * Returns: none
        """
        logger.info('[PurchaseFacade] attempting to reject purchase with purchase id: %s', purchase_id)
        if not self.__check_if_purchase_exists(purchase_id):
            raise ValueError("Purchase id is invalid")
        del self._purchases[purchase_id]

    def complete_purchase(self, purchase_id: int):
        """
        * Parameters: purchaseId
        * This function is responsible for completing the purchase
        * Returns: none
        """
        logger.info('[PurchaseFacade] attempting to complete purchase with purchase id: %s', purchase_id)
        purchase = self.__get_purchase_by_id(purchase_id)
        purchase.complete()

    def __get_purchase_by_id(self, purchase_id: int) -> Purchase:
        if self.__check_if_purchase_exists(purchase_id):
            return self._purchases[purchase_id]
        raise ValueError("Purchase id is invalid")

    def __check_if_purchase_exists(self, purchase_id: int) -> bool:
        return purchase_id in self._purchases

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
