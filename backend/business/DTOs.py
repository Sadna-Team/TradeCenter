import datetime
from enum import Enum
# import the datetime type
from typing import List


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

    def get(self) -> dict:
        return {"notification_id": self.__notification_id, "message": self.__message, "date": self.__date}


class PurchaseProductDTO:
    def __init__(self, product_id: int, name: str, description: str, price: float, amount: int):
        self.__product_id: int = product_id
        self.__name: str = name
        self.__description: str = description
        self.__price: float = price
        self.__amount: int = amount

    @property
    def product_id(self) -> int:
        return self.__product_id
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def price(self) -> float:
        return self.__price
    
    @property
    def amount(self) -> int:
        return self.__amount


class PurchaseDTO:
    def __init__(self, purchase_id: int, store_id: int, date: datetime, total_price: float,
                 total_price_after_discounts: float, status: int, products: List[PurchaseProductDTO]):
        self.__purchase_id: int = purchase_id
        self.__store_id: int = store_id
        self.__date: datetime = date
        self.__total: float = total_price
        self._total_price_after_discounts: float = total_price_after_discounts
        self.__status: int = status
        self.__products: list[PurchaseProductDTO] = products
