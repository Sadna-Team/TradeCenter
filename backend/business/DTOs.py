import datetime
from enum import Enum
# import the datetime type
from typing import List


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

    def get(self) -> dict:
        return {"product_id": self.__product_id, "name": self.__name, "description": self.__description,
                "price": self.__price, "amount": self.__amount}


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

    @property
    def purchase_id(self) -> int:
        return self.__purchase_id

    @property
    def store_id(self) -> int:
        return self.__store_id

    @property
    def date(self) -> datetime:
        return self.__date

    @property
    def total(self) -> float:
        return self.__total

    @property
    def total_price_after_discounts(self) -> float:
        return self._total_price_after_discounts

    @property
    def status(self) -> int:
        return self.__status

    @property
    def products(self) -> List[PurchaseProductDTO]:
        return self.__products

    def get(self) -> dict:
        return {"purchase_id": self.__purchase_id, "store_id": self.__store_id, "date": self.__date,
                "total": self.__total, "total_price_after_discounts": self._total_price_after_discounts,
                "status": self.__status, "products": [product.get() for product in self.__products]}

class ProductDTO:
    def __init__(self, product_id: int, store_id: int, name: str, weight: float, description: str, price: float, amount: int, tags: list[str]):
        self.__product_id: int = product_id
        self.__store_id: int = store_id
        self.__name: str = name
        self.__weight: float = weight
        self.__description: str = description
        self.__price: float = price
        self.__amount: int = amount
        self.__tags: list[str] = tags

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

    def get(self) -> dict:
        return {"product_id": self.__product_id, "name": self.__name, "description": self.__description,
                "price": self.__price, "amount": self.__amount}


class TransactionException(Exception):
    pass
