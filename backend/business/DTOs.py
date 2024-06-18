from datetime import datetime

# import the datetime type
from typing import List, Optional
from datetime import date, datetime



class AddressDTO:
    def __init__(self, address_id: int, address: str, city: str, state: str, country: str, postal_code: str):
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
    
    def to_json(self):
        return {
            'notification_id': self.__notification_id,
            'message': self.__message,
            'date': self.__date
        }


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
    def __init__(self, product_id: int, name: str, description: str, price: float, tags: list[str], weight: float,
                 amount: int):
        self.__product_id: int = product_id
        self.__name: str = name
        self.__description: str = description
        self.__price: float = price
        self.__tags: list[str] = tags
        self.__weight: float = weight
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
    def tags(self) -> list[str]:
        return self.__tags

    @property
    def weight(self) -> float:
        return self.__weight

    @property
    def amount(self) -> int:
        return self.__amount

    def get(self) -> dict:
        return {"product_id": self.__product_id, "name": self.__name, "description": self.__description,
                "price": self.__price, "amount": self.__amount}


class StoreDTO:
    def __init__(self, store_id: int, location_id: int, store_name: str, store_founder_id: int, is_active: bool,
                 found_date: datetime, products: List[ProductDTO] = []):
        self.__store_id: int = store_id
        self.__location_id: int = location_id
        self.__store_name: str = store_name
        self.__store_founder_id: int = store_founder_id
        self.__is_active: bool = is_active
        self.__found_date: datetime = found_date
        self.__products: List[ProductDTO] = products

    @property
    def store_id(self) -> int:
        return self.__store_id

    @property
    def location_id(self) -> int:
        return self.__location_id

    @property
    def store_name(self) -> str:
        return self.__store_name

    @property
    def store_founder_id(self) -> int:
        return self.__store_founder_id

    @property
    def is_active(self) -> bool:
        return self.__is_active

    @property
    def found_date(self) -> datetime:
        return self.__found_date

    @property
    def products(self) -> List[ProductDTO]:
        return self.__products

    @products.setter
    def products(self, products: List[ProductDTO]):
        self.__products = products

    def get(self) -> dict:
        return {"store_id": self.__store_id, "location_id": self.__location_id, "store_name": self.__store_name,
                "store_founder_id": self.__store_founder_id, "is_active": self.__is_active,
                "found_date": self.__found_date,
                "products": [product.get() for product in self.__products]}


class UserInformationForConstraintDTO:
    def __init__(self, user_id: int, birthdate: Optional[date], address: AddressDTO):
        self.__user_id: int = user_id
        self.__birthdate: Optional[date] = birthdate
        self.__address: AddressDTO = address

    @property
    def user_id(self):
        return self.__user_id
    
    @property
    def birthdate(self):
        return self.__birthdate
    
    @property
    def address(self):
        return self.__address
    
    def get(self):
        return {"user_id": self.__user_id, "birthdate": self.__birthdate, "address": self.__address.to_dict()}

class ProductForConstraintDTO:
    def __init__(self, product_id: int, store_id: int, price: float, weight: float, amount: int):
        self.__product_id: int = product_id
        self.__store_id: int = store_id
        self.__price: float = price
        self.__weight: float = weight
        self.__amount: int = amount

    @property
    def product_id(self) -> int:
        return self.__product_id

    @property
    def store_id(self) -> int:
        return self.__store_id

    @property
    def price(self) -> float:
        return self.__price
    
    @property
    def weight(self) -> float:
        return self.__weight

    @property
    def amount(self) -> int:
        return self.__amount
    
    def get(self) -> dict:
        return {"product_id": self.__product_id, "store_id": self.__store_id, "price": self.__price, "weight": self.__weight, "amount": self.__amount}



class CategoryForConstraintDTO:
    def __init__(self, category_id: int, category_name: str, parent_category_id: int, sub_categories: List['CategoryForConstraintDTO'], products: List[ProductForConstraintDTO]):
        self.__category_id: int = category_id
        self.__category_name: str = category_name
        self.__parent_category_id: int = parent_category_id
        self.__sub_categories: List['CategoryForConstraintDTO'] = sub_categories
        self.__products: List[ProductForConstraintDTO] = products

    @property
    def category_id(self) -> int:
        return self.__category_id

    @property
    def category_name(self) -> str:
        return self.__category_name

    @property
    def parent_category_id(self) -> int:
        return self.__parent_category_id

    @property
    def sub_categories(self) -> List['CategoryForConstraintDTO']:
        return self.__sub_categories
    
    @property
    def products(self) -> List[ProductForConstraintDTO]:
        return self.__products



class BasketInformationForConstraintDTO:
    def __init__(self, store_id: int, products: List[ProductForConstraintDTO], total_price_of_basket: float, time_of_purchase: datetime, user_info: UserInformationForConstraintDTO, categories: List[CategoryForConstraintDTO]):
        self.__store_id: int = store_id
        self.__products: List[ProductForConstraintDTO] = products
        self.__total_price_of_basket: float = total_price_of_basket
        self.__time_of_purchase: datetime = time_of_purchase
        self.__user_info: UserInformationForConstraintDTO = user_info
        self.__categories: List[CategoryForConstraintDTO] = categories

    @property
    def store_id(self) -> int:
        return self.__store_id
    
    @property
    def products(self) -> List[ProductForConstraintDTO]:
        return self.__products
    
    @property
    def total_price_of_basket(self) -> float:
        return self.__total_price_of_basket
    
    @property
    def time_of_purchase(self) -> datetime:
        return self.__time_of_purchase
    
    @property
    def user_info(self) -> UserInformationForConstraintDTO:
        return self.__user_info
    
    @property
    def categories(self) -> List[CategoryForConstraintDTO]:
        return self.__categories

    def get(self) -> dict:
        return {"store_id": self.__store_id, "products": [product.get() for product in self.__products], "total_price_of_basket": self.__total_price_of_basket,
                "time_of_purchase": self.__time_of_purchase, "user_info": self.__user_info.get(), "categories": [category.__dict__ for category in self.__categories]}
    

class TransactionException(Exception):
    pass


class CategoryDTO:
    def __init__(self, category_id: int, category_name: str, parent_category_id: int):
        self.__category_id: int = category_id
        self.__category_name: str = category_name
        self.__parent_category_id: int = parent_category_id

    @property
    def category_id(self) -> int:
        return self.__category_id

    @property
    def category_name(self) -> str:
        return self.__category_name

    @property
    def parent_category_id(self) -> int:
        return self.__parent_category_id

    def get(self) -> dict:
        return {"category_id": self.__category_id, "category name": self.__category_name,
                "parent_category_id": self.__parent_category_id}


class UserDTO:
    def __init__(self, user_id: int, email: Optional[str]=None, username: Optional[str]=None, year: 
                 Optional[int]=None, month: Optional[int]=None, day: Optional[int]=None, phone: Optional[str]=None,
                 role: Optional[str] = None):
        self.__user_id: int = user_id
        self.__email: Optional[str] = email
        self.__username: Optional[str] = username
        self.__year: Optional[int] = year
        self.__month: Optional[int] = month
        self.__day: Optional[int] = day
        self.__phone: Optional[str] = phone
        self.__role: Optional[str] = role

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def email(self):
        return self.__email

    @property
    def username(self):
        return self.__username

    @property
    def year(self):
        return self.__year

    @property
    def month(self):
        return self.__month

    @property
    def day(self):
        return self.__day

    @property
    def phone(self):
        return self.__phone

    @property
    def role(self):
        return self.__role


class PurchaseUserDTO:
    def __init__(self, user_id: int, birthdate: Optional[date] = None):
        self.__user_id: int = user_id
        self.__birthdate: Optional[date] = birthdate

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def birthdate(self) -> Optional[date]:
        return self.__birthdate

    def get(self) -> dict:
        return {"user_id": self.__user_id, "birthdate": self.__birthdate}
