from . import c
from typing import Optional, List, Dict
import datetime
from _collections import defaultdict
from abc import ABC, abstractmethod
import threading


class ShoppingBasket:
    # id of ShoppingBasket is (user_id, store_id)
    def __init__(self, store_id: int) -> None:
        self.__store_id: int = store_id
        self.__products: Dict[int, int] = defaultdict(int)

    def add_product(self, product_id: int, amount: int) -> None:
        if amount < 0:
            raise ValueError("Amount must be positive")
        self.__products[product_id] += amount

    def get_dto(self) -> Dict[int, int]:
        return {
            product_id: amount for product_id, amount in self.__products.items()
        }

    def remove_product(self, product_id: int, amount: int):
        if product_id not in self.__products:
            raise ValueError("Product not found")

        if self.__products[product_id] < amount:
            raise ValueError("Amount is greater than the amount of the product in the basket")

        self.__products[product_id] -= amount
        if self.__products[product_id] == 0:
            del self.__products[product_id]


class SoppingCart:
    # id of ShoppingBasket is (user_id)
    def __init__(self, user_id: int) -> None:
        self.__user_id: int = user_id
        self.__shopping_baskets: dict[int, ShoppingBasket] = {}

    def add_product_to_basket(self, store_id: int, product_id: int, amount: int) -> None:
        if store_id not in self.__shopping_baskets:
            self.__shopping_baskets[store_id] = ShoppingBasket(store_id)
        self.__shopping_baskets[store_id].add_product(product_id, amount)

    def get_dto(self) -> Dict[int, Dict[int, int]]:
        return {
            store_id: shopping_basket.get_dto() for store_id, shopping_basket in self.__shopping_baskets.items()
        }

    def remove_product_from_cart(self, store_id: int, product_id: int, amount: int) -> None:
        if store_id not in self.__shopping_baskets:
            raise ValueError("Store not found")

        self.__shopping_baskets[store_id].remove_product(product_id, amount)


class State(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_password(self):
        pass


class Guest(State):
    def __init__(self):
        pass

    def get_password(self):
        raise ValueError("User is not registered")


class Member(State):
    def __init__(self, location_id: int, email: str, username, password: str, year: int, month: int, day: int,
                 phone: str) -> None:
        #  try to convert the birth

        self.__locationId: int = location_id
        self.__email: str = email
        self.__username: str = username
        self.__password: str = password
        self.__birthdate: datetime = datetime.date(year, month, day)
        self.__phone: str = phone

    def get_password(self):
        return self.__password


class NotificationDTO:
    def __init__(self, notification_id: int, message: str, date: datetime) -> None:
        self.__notification_id: int = notification_id
        self.__message: str = message
        self.__date: datetime = date

    def get_notification_id(self) -> int:
        return self.__notification_id

    def get_message(self) -> str:
        return self.__message

    def get_date(self) -> datetime:
        return self.__date


class Notification:
    def __init__(self, notification_id: int, message: str, date: datetime) -> None:
        self.__notification_id: int = notification_id
        self.__message: str = message
        self.__date: datetime = date

    def get_notification_dto(self) -> NotificationDTO:
        return NotificationDTO(self.__notification_id, self.__message, self.__date)


class User:
    def __init__(self, user_id: int, currency: str = 'USD') -> None:
        if currency not in c.currencies:
            raise ValueError("Currency not supported")

        self.__id: int = user_id
        self.__currency: str = currency
        self.__member: State = Guest()
        self.__shopping_cart: SoppingCart = SoppingCart(user_id)
        self.__notifications: List[Notification] = []

    def get_notifications(self) -> List[Notification]:
        return self.__notifications

    def add_product_to_basket(self, store_id: int, product_id: int, amount: int) -> None:
        self.__shopping_cart.add_product_to_basket(store_id, product_id, amount)

    def get_shopping_cart(self) -> Dict[int, Dict[int, int]]:
        return self.__shopping_cart.get_dto()

    def register(self, location_id: int, email: str, username: str, password: str, year: int, month: int, day: int,
                 phone: str) -> None:
        self.__member = Member(location_id, email, username, password, year, month, day, phone)

    def remove_product_from_cart(self, store_id: int, product_id: int, amount: int) -> None:
        self.__shopping_cart.remove_product_from_cart(store_id, product_id, amount)

    def clear_basket(self):
        self.__shopping_cart = SoppingCart(self.__id)

    def get_password(self):
        return self.__member.get_password()


class UserFacade:
    # singleton
    __lock = threading.Lock()
    _instance = None
    __id_serializer: int = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserFacade, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.__users: Dict[int, User] = {}
            self.__usernames: Dict[str, int] = {}  # username -> user_id

    def create_user(self, currency: str = "USD") -> int:
        with UserFacade.__lock:
            new_id = UserFacade.__id_serializer
            UserFacade.__id_serializer += 1
        user = User(new_id, currency)
        self.__users[new_id] = user
        return new_id

    def register_user(self, user_id: int, location_id: int, email: str, username: str, password: str,
                      year: int, month: int, day: int, phone: str) -> None:
        self.__get_user(user_id).register(location_id, email, username, password, year, month, day, phone)
        self.__usernames[username] = user_id

    def get_notifications(self, user_id: int) -> List[NotificationDTO]:
        return [notification.get_notification_dto() for notification in self.__get_user(user_id).get_notifications()]

    def add_product_to_basket(self, user_id: int, store_id: int, product_id: int, amount: int) -> None:
        self.__get_user(user_id).add_product_to_basket(store_id, product_id, amount)

    def __get_user(self, user_id: int) -> User:
        if user_id not in self.__users:
            raise ValueError("User not found")
        return self.__users[user_id]

    def get_shopping_cart(self, user_id: int) -> Dict[int, Dict[int, int]]:
        return self.__get_user(user_id).get_shopping_cart()

    def remove_product_from_cart(self, user_id: int, store_id: int, product_id: int, amount: int) -> None:
        self.__get_user(user_id).remove_product_from_cart(store_id, product_id, amount)

    def clear_basket(self, user_id: int) -> None:
        self.__get_user(user_id).clear_basket()

    def get_password(self, username: str) -> (int, str):
        if username not in self.__usernames:
            raise ValueError("User not found")
        user_id = self.__usernames.get(username)
        return user_id, self.__get_user(user_id).get_password()

    def remove_user(self, user_id: int):
        if user_id in self.__users:
            del self.__users[user_id]
        for username, id in self.__usernames.items():
            if id == user_id:
                del self.__usernames[username]
                break
