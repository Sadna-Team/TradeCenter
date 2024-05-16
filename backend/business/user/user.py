from . import c
from typing import Optional, List
import datetime
from abc import ABC, abstractmethod


class ShoppingBasket:
    # id of ShoppingBasket is (user_id, store_id)
    def __init__(self, store_id: int) -> None:
        self.__store_id: int = store_id
        self.__products: List[int] = []


class SoppingCart:
    # id of ShoppingBasket is (user_id)
    def __init__(self, user_id: int) -> None:
        self.__user_id: int = user_id
        self.__shopping_baskets: List[ShoppingBasket] = []


class State(ABC):
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
