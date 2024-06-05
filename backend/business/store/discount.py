# --------------- imports ---------------#
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from backend.business.store.constraints import Constraint


# --------------- Discount interface ---------------#
class Discount(ABC):
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

    def change_discount_percentage(self, new_percentage: float) -> None:
        if new_percentage < 0 or new_percentage > 1:
            raise ValueError("Invalid percentage")
        self.__percentage = new_percentage        


    def change_discount_description(self, new_description: str) -> None:
        self.__discount_description = new_description

    def is_simple_discount(self) -> bool:
        if self.__predicate is None:
            return True
        return False        
    
    def change_predicate(self, new_predicate: Constraint) -> None:
        self.__predicate = new_predicate

# --------------- Category Discount ---------------#
class CategoryDiscount(Discount):
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
    

    def calculate_discount(self, basket: SOMETHING, user: UserDTO) -> float:
        pass

# --------------- Store Discount ---------------#
class StoreDiscount(Discount):
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


# --------------- Product Discount ---------------#
class ProductDiscount(Discount):
    def __init__(self, discount_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, product_id: int):
        super().__init__(discount_id, discount_description, starting_date, ending_date, percentage)
        self.product_id = product_id

    
    def calculate_discount(self, basket: SOMETHING, user: UserDTO) -> float:
        pass


# --------------- Max Discount classes ---------------#
class maxDiscount(Discount):
    # class responsible for returning the total price of the maximum discount.
    def __init__(self, ListDiscount: list[Discount]):
        self.__ListDiscount = ListDiscount

    def calculate_discount(self, basket: BasketDTO, user: UserDTO) -> float:
        """
        * Parameters: basket in BasketDTO, user in UserDTO
        * This function is responsible for calculating the discount based on the basket and user.
        * Returns: float
        """
        return max([discount.calculate_discount(basket, user) for discount in self.__ListDiscount])


class additiveDiscountStrategy(Discount):
    # class responsible for returning the total price of the maximum discount.
    def __init__(self, ListDiscount: list[Discount]):
        self.__ListDiscount = ListDiscount

    def calculate_discount(self, basket: BasketDTO, user: UserDTO) -> float:
        """
        * Parameters: basket in BasketDTO, user in UserDTO
        * This function is responsible for calculating the discount based on the basket and user.
        * Returns: float
        """
        return sum([discount.calculate_discount(basket, user) for discount in self.__ListDiscount])
