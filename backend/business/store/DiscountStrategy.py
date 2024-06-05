# --------------- imports ---------------#
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from backend.business.store.constraints import Constraint


# --------------- Discount class ---------------#
class DiscountStrategy(ABC):
    # interface responsible for representing discounts in general. discountId unique verifier.
    def __init__(self, discount_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, predicate: Optional[Constraint]):
        self.__discount_id = discount_id
        self.__discount_description = discount_description
        self.__starting_date = starting_date
        self.__ending_date = ending_date
        self.__percentage = percentage
        self.__predicate = predicate

    @property
    def discount_id(self):
        return self.__discount_id
    
    @property
    def discount_description(self):
        return self.__discount_description
    
    @property
    def starting_date(self):
        return self.__starting_date
    
    @property
    def ending_date(self):
        return self.__ending_date
    
    @property
    def percentage(self):
        return self.__percentage
    
    @property
    def predicate(self):
        return self.__predicate

    @abstractmethod
    def calculate_discount(self, basket: SOMETHING, user: UserDTO) -> float:
        pass

    @abstractmethod
    def change_discount_percentage(self, new_percentage: float) -> None:
        pass

    @abstractmethod
    def change_discount_description(self, new_description: str) -> None:
        pass

    @abstractmethod
    def is_simple_discount(self) -> bool:
        pass

    @abstractmethod
    def change_predicate(self, new_predicate: Constraint) -> None:
        pass


class CategoryDiscount(DiscountStrategy):
    def __init__(self, discount_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, predicate: Optional[Constraint], category_id: int, applied_to_subcategories: bool):
        super().__init__(discount_id, discount_description, starting_date, ending_date, percentage, predicate)
        self.__category_id = category_id //OR THE CATEGORY ITSELF IDK
        self.__applied_to_subcategories = applied_to_subcategories

    @property
    def category_id(self):
        return self.__category_id
    
    @property
    def applied_to_subcategories(self):
        return self.__applied_to_subcategories
    
    def calculate_discount(self, basket: BasketDTO) -> float:


class StoreDiscount(DiscountStrategy):
    # not implemented at this version
    @abstractmethod
    def calculate_discount(self, price: float) -> float:
        pass

    @abstractmethod
    def change_discount_percentage(self, new_percentage: float) -> None:
        pass

    @abstractmethod
    def change_discount_description(self, new_description: str) -> None:
        pass


class ProductDiscount(DiscountStrategy):
    def __init__(self, discount_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, product_id: int):
        super().__init__(discount_id, discount_description, starting_date, ending_date, percentage)
        self.product_id = product_id

    def calculate_discount(self, price: float) -> float:
        """
        * Parameters: price in float
        * This function is responsible for verifying if the discount is valid and returning the price with the discount.
        * Returns: price after discount in float or without depending on if the discount is valid.
        """
        if self._starting_date <= datetime.now() <= self._ending_date:
            return price - price * self._percentage
        return price

    def change_discount_percentage(self, new_percentage: float) -> bool:
        """
        * Parameters: new_percentage in float
        * This function is responsible for changing the discount percentage.
        * Returns: None
        """
        if new_percentage < 0 or new_percentage > 1:
            return False
        self._percentage = new_percentage
        return True

    def change_discount_description(self, new_description: str) -> bool:
        """
        * Parameters: newDescription in str
        * This function is responsible for changing the discount description.
        * Returns: None
        """
        self._discount_description = new_description
        return True


class maxDiscountStrategy(DiscountStrategy):


class additiveDiscountStrategy(DiscountStrategy):
    