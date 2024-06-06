from . import c
from typing import List, Dict, Optional, Set, Tuple
import datetime
from abc import ABC, abstractmethod
import threading
from collections import defaultdict


# NOTE: This is a workaround to avoid circular imports
#from .. import NotificationDTO

# NOTE: Solution:
from backend.business.DTOs import NotificationDTO, UserDTO, PurchaseUserDTO
from .. import NotificationDTO


class ShoppingBasket:
    # id of ShoppingBasket is (user_id, store_id)
    def __init__(self, store_id: int) -> None:
        self.__store_id: int = store_id
        self.__products: Dict = defaultdict(int)  # productId -> quantity

    def add_product(self, product_id: int, quantity: int) -> None:
        self.__products[product_id] += quantity

    def get_dto(self) -> Dict[int, int]:
        return self.__products

    def remove_product(self, product_id: int, quantity: int):
        if product_id not in self.__products:
            raise ValueError("Product not found")
        if self.__products[product_id] < quantity:
            raise ValueError("Not enough quantity")

        del self.__products[product_id]

    def subtract_product(self, product_id: int, quantity: int):
        if product_id not in self.__products:
            raise ValueError("Product not found")
        if self.__products[product_id] < quantity:
            raise ValueError("Not enough quantity")
        self.__products[product_id] -= quantity


class ShoppingCart:
    # id of ShoppingBasket is (user_id)
    def __init__(self, user_id: int) -> None:
        self.__user_id: int = user_id
        self.__shopping_baskets: dict[int, ShoppingBasket] = {}

    def add_product_to_basket(self, store_id: int, product_id: int, quantity: int) -> None:
        if store_id not in self.__shopping_baskets:
            self.__shopping_baskets[store_id] = ShoppingBasket(store_id)
        self.__shopping_baskets[store_id].add_product(product_id, quantity)

    def get_dto(self) -> Dict[int, Dict[int, int]]:
        return {store_id: basket.get_dto() for store_id, basket in self.__shopping_baskets.items()}

    def remove_product_from_cart(self, store_id: int, product_id: int, quantity: int) -> None:
        if store_id not in self.__shopping_baskets:
            raise ValueError("Store not found")
        self.__shopping_baskets[store_id].remove_product(product_id, quantity)

    def subtract_product_from_cart(self, store_id: int, product_id: int, quantity: int) -> None:
        if store_id not in self.__shopping_baskets:
            raise ValueError("Store not found")

        self.__shopping_baskets[store_id].subtract_product(product_id, quantity)


class Notification:
    def __init__(self, notification_id: int, message: str, date: datetime.datetime) -> None:
        self.__notification_id: int = notification_id
        self.__message: str = message
        self.__date: datetime.datetime = date

    def get_notification_dto(self) -> NotificationDTO:
        return NotificationDTO(self.__notification_id, self.__message, self.__date)


class State(ABC):
    @abstractmethod
    def get_password(self):
        pass

    @abstractmethod
    def get_notifications(self) -> List[Notification]:
        pass

    @abstractmethod
    def add_notification(self, notification: Notification):
        pass

    @abstractmethod
    def clear_notifications(self):
        pass

    @abstractmethod
    def get_email(self):
        pass

    @abstractmethod
    def get_username(self):
        pass

    @abstractmethod
    def get_birthdate(self) -> Optional[datetime.datetime]:
        pass

    @abstractmethod
    def get_phone(self):
        pass


class Guest(State):
    def get_password(self):
        raise ValueError("User is not registered")

    def get_notifications(self):
        raise ValueError("User is not registered")

    def add_notification(self, notification: Notification):
        raise ValueError("User is not registered")

    def clear_notifications(self):
        raise ValueError("User is not registered")

    def get_email(self):
        raise ValueError("User is not registered")

    def get_username(self):
        raise ValueError("User is not registered")

    def get_birthdate(self) -> Optional[datetime]:
        raise ValueError("User is not registered")

    def get_phone(self):
        raise ValueError("User is not registered")


class Member(State):
    def __init__(self, email: str, username, password: str, year: int, month: int, day: int,
                 phone: str) -> None:
        #  try to convert the birth

        self.__email: str = email
        self.__username: str = username
        self.__password: str = password
        self.__birthdate: datetime = datetime.date(year, month, day)
        self.__phone: str = phone
        self.__notifications: List[Notification] = []

    def get_password(self):
        return self.__password

    def get_notifications(self):
        return self.__notifications

    def add_notification(self, notification: Notification):
        self.__notifications.append(notification)

    def clear_notifications(self):
        self.__notifications.clear()

    def get_email(self):
        return self.__email

    def get_username(self):
        return self.__username

    def get_birthdate(self) -> Optional[datetime]:
        return self.__birthdate

    def get_phone(self):
        return self.__phone

class User:
    def __init__(self, user_id: int, currency: str = 'USD') -> None:
        if currency not in c.currencies:
            raise ValueError("Currency not supported")

        self.__id: int = user_id
        self.__currency: str = currency
        self.__member: State = Guest()
        self.__shopping_cart: ShoppingCart = ShoppingCart(user_id)

    def add_notification(self, notification: Notification) -> None:
        self.__member.add_notification(notification)

    def get_notifications(self) -> List[Notification]:
        return self.__member.get_notifications()

    def clear_notifications(self) -> None:
        self.__member.clear_notifications()

    def add_product_to_basket(self, store_id: int, product_id: int, quantity: int) -> None:
        self.__shopping_cart.add_product_to_basket(store_id, product_id, quantity)

    def get_shopping_cart(self) -> Dict[int, Dict[int, int]]:
        return self.__shopping_cart.get_dto()

    def register(self, email: str, username: str, password: str, year: int, month: int, day: int,
                 phone: str) -> None:
        if isinstance(self.__member, Member):
            raise ValueError("User is already registered")
        self.__member = Member(email, username, password, year, month, day, phone)

    def remove_product_from_cart(self, store_id: int, product_id: int, quantity: int):
        self.__shopping_cart.remove_product_from_cart(store_id, product_id, quantity)

    def subtract_product_from_cart(self, store_id: int, product_id: int, quantity: int):
        self.__shopping_cart.subtract_product_from_cart(store_id, product_id, quantity)

    def clear_basket(self):
        self.__shopping_cart = ShoppingCart(self.__id)

    def get_password(self):
        return self.__member.get_password()

    def is_member(self):
        return isinstance(self.__member, Member)
    
    def create_purchase_user_dto(self) -> PurchaseUserDTO:
        try:
            return PurchaseUserDTO(self.__id, self.__member.get_birthdate())
        except ValueError:
            return PurchaseUserDTO(self.__id)

    def get_user_dto(self, role: str = None) -> UserDTO:
        if not self.is_member():
            raise ValueError("User is not registered")
        return UserDTO(self.__id, self.__member.get_email(), self.__member.get_username(),
                       self.__member.get_birthdate().year, self.__member.get_birthdate().month,
                       self.__member.get_birthdate().day, self.__member.get_phone(), role)


class UserFacade:
    # singleton
    __create_lock = threading.Lock()
    __register_lock = threading.Lock()
    __notification_lock = threading.Lock()
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

    def clean_data(self):
        """
        For testing purposes only
        """
        self.__users.clear()
        self.__usernames.clear()
        UserFacade.__id_serializer = 0

    def __get_user(self, user_id: int) -> User:
        if user_id not in self.__users:
            raise ValueError("User not found")
        return self.__users[user_id]
    
    def get_userDTO(self, user_id: int, role: str = None) -> UserDTO:
        user = self.__get_user(user_id)
        return user.get_user_dto(role)

    def create_user(self, currency: str = "USD") -> int:
        with UserFacade.__create_lock:
            new_id = UserFacade.__id_serializer
            UserFacade.__id_serializer += 1
        user = User(new_id, currency)
        self.__users[new_id] = user
        return new_id

    def register_user(self, user_id: int, email: str, username: str, password: str,
                      year: int, month: int, day: int, phone: str) -> None:
        with UserFacade.__register_lock:
            if username in self.__usernames:
                raise ValueError("Username already exists")
            if user_id not in self.__users:
                raise ValueError("User not found")
            self.__get_user(user_id).register(email, username, password, year, month, day, phone)
            self.__usernames[username] = user_id

    def get_notifications(self, user_id: int) -> List[NotificationDTO]:
        with UserFacade.__notification_lock:
            notifications = self.__get_user(user_id).get_notifications()
            out = []
            for notification in notifications:
                out.append(notification.get_notification_dto())
            self.clear_notifications(user_id)
        return out

    def clear_notifications(self, user_id: int) -> None:
        with UserFacade.__notification_lock:
            self.__get_user(user_id).clear_notifications()

    def notify_user(self, user_id: int, notification: NotificationDTO) -> None:
        with UserFacade.__notification_lock:
            self.__get_user(user_id).add_notification(
                Notification(notification.get_notification_id(),
                             notification.get_message(), notification.get_date()))

    def add_product_to_basket(self, user_id: int, store_id: int, product_id: int, quantity: int) -> None:
        self.__get_user(user_id).add_product_to_basket(store_id, product_id, quantity)

    def get_shopping_cart(self, user_id: int) -> Dict[int, Dict[int, int]]:
        return self.__get_user(user_id).get_shopping_cart()

    def remove_product_from_cart(self, user_id: int, store_id: int, product_id: int, quantity: int) -> None:
        self.__get_user(user_id).remove_product_from_cart(store_id, product_id, quantity)

    def subtract_product_from_cart(self, user_id: int, store_id: int, product_id: int, quantity: int) -> None:
        self.__get_user(user_id).subtract_product_from_cart(store_id, product_id, quantity)

    def clear_basket(self, user_id: int) -> None:
        self.__get_user(user_id).clear_basket()

    def get_password(self, username: str) -> Tuple[int, str]:
        if username not in self.__usernames:
            raise ValueError("User not found")
        user_id = self.__usernames.get(username)
        return user_id, self.__get_user(user_id).get_password()

    def remove_user(self, user_id: int):
        if user_id in self.__users:
            del self.__users[user_id]
        else:
            raise ValueError("User not found")
        for username, u_id in self.__usernames.items():
            if u_id == user_id:
                del self.__usernames[username]
                break

    def is_member(self, user_id: int) -> bool:
        return self.__get_user(user_id).is_member()

    def get_users_dto(self, roles: Dict[int, str]) -> Dict[int, UserDTO]:  # user_id -> role
        out = {}
        for user_id, role in roles.items():
            out[user_id] = self.__get_user(user_id).get_user_dto(role)
        return out
      
    def restore_basket(self, user_id: int, cart: Dict[int, Dict[int, int]]):
        self.__get_user(user_id).clear_basket()
        for store_id, products in cart.items():
            for product_id, quantity in products.items():
                self.add_product_to_basket(user_id, store_id, product_id, quantity)
