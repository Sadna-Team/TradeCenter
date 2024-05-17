from typing import Optional, List
from collections import defaultdict
import datetime
from abc import ABC, abstractmethod

from . import c


class ShoppingBasket:
    # id of ShoppingBasket is (user_id, store_id)
    def __init__(self, store_id: int) -> None:
        self.__store_id: int = store_id
        self.__products: defaultdict[int,int] = defaultdict(int)

    def add_product(self, product_id: int) -> None:
        self.__products[product_id] += 1

    def remove_product(self, product_id: int) -> None:
        if product_id in self.__products:
            self.__products[product_id] -= 1
            if self.__products[product_id] == 0:
                del self.__products[product_id]
        else:
            raise ValueError("Product not in basket")

    def get_all_products(self) -> dict[int, int]:
        return self.__products


class SoppingCart:
    # id of ShoppingBasket is (user_id)
    def __init__(self, user_id: int) -> None:
        self.__user_id: int = user_id
        self.__shopping_baskets: dict[int, ShoppingBasket] = {}

    def add_product_to_basket(self, store_id: int, product_id: int) -> None:
        if store_id in self.__shopping_baskets:
            self.__shopping_baskets[store_id].add_product(product_id)
        else:
            self.__shopping_baskets[store_id] = ShoppingBasket(store_id)
            self.__shopping_baskets[store_id].add_product(product_id)

    def remove_product_from_basket(self, store_id: int, product_id: int) -> None:
        if store_id in self.__shopping_baskets:
            self.__shopping_baskets[store_id].remove_product(product_id)
        else:
            raise ValueError("Store not in basket")

    def get_all_products(self) -> dict[int, dict[int,int]]:
        #dict that key is store id and value is dict of product id and quantity
        return {store_id: basket.get_all_products() for store_id, basket in self.__shopping_baskets.items()}

class State(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def update_basket(self, SoppingCart) -> None:
        pass


class Guest(State):
    def __init__(self):
        pass


class Member(State):
    def __init__(self, location_id: int, email: str, username, year: int, month: int, day: int, phone: str) -> None:
        #  try to convert the birth

        self.__locationId: int = location_id
        self.__email: str = email
        self.__username: str = username
        self.__birthdate: datetime = datetime.date(year, month, day)
        self.__phone: str = phone


class Notification:
    def __init__(self, notification_id: int, message: str, date: datetime) -> None:
        self.__notification_id: int = notification_id
        self.__message: str = message
        self.__date: datetime = date


class User:
    def __init__(self, user_id: int, currency: str) -> None:
        if currency not in c.currencies:
            raise ValueError("Currency not supported")

        self.__id: int = user_id
        self.__currency: str = currency
        self.__member: State = Guest()
        self.__ShoppingCart: SoppingCart = SoppingCart(user_id)
        self.__notifications: List[Notification] = []

    def change_currency(self, currency: str) -> None:
        if currency not in c.currencies:
            raise ValueError("Currency not supported")
        self.__currency = currency

    def add_notification(self, notification_id: int, message: str) -> None:
        self.__notifications.append(Notification(notification_id, message, datetime.datetime.now()))

    def get_notifications(self) -> List[Notification]:
        return self.__notifications

    def add_product_to_basket(self, store_id: int, product_id: int) -> None:
        self.__ShoppingCart.add_product_to_basket(store_id, product_id)

    def remove_product_from_basket(self, store_id: int, product_id: int) -> None:
        self.__ShoppingCart.remove_product_from_basket(store_id, product_id)

    def get_all_products(self) -> dict[int, dict[int, int]]:
        return self.__ShoppingCart.get_all_products()

    def become_member(self, location_id: int, email: str, username, year: int, month: int, day: int, phone: str) -> None:
        self.__member = Member(location_id, email, username, year, month, day, phone)

