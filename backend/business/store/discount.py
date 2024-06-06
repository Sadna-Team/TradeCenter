# --------------- imports ---------------#
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from backend.business.DTOs import BasketInformationForDiscountDTO, CategoryDTO
from backend.business.store.constraints import Constraint



# --------------- Discount interface ---------------#
class DiscountInterface(ABC):
    @abstractmethod
    def calculate_discount(self, basket_information: BasketInformationForDiscountDTO) -> float:
        pass

# --------------- Discount base ---------------#
class Discount(DiscountInterface):
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
    def calculate_discount(self, basket_information: BasketInformationForDiscountDTO) -> float:
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
    """
    * This class is responsible for creating a discount that is applied to a specific category.
    """
    def __init__(self, discount_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, predicate: Optional[Constraint], category_id: int, applied_to_subcategories: bool):
        super().__init__(discount_id, discount_description, starting_date, ending_date, percentage, predicate)
        self.__category_id = category_id
        self.__applied_to_subcategories = applied_to_subcategories

    @property
    def category_id(self) -> int:
        return self.__category_id
    
    @property
    def applied_to_subcategories(self) -> bool:
        return self.__applied_to_subcategories
    

    def calculate_discount(self, basket_information: BasketInformationForDiscountDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForDiscountDTO
        * This function is responsible for calculating the discount based on the basket information, the discount is only applied to the products that fall under the category.
        * Returns: float of the amount the discount will deduce from the total price.
        """

        if self.__predicate is not None and not self.__predicate.is_satisfied(basket_information):
            raise ValueError("Discount not applicable")
        if self.starting_date > datetime.now() or self.ending_date < datetime.now():
            raise ValueError("Discount expired!")
        
        discount_reduction = 0.0
        for category in basket_information.categories:
            if category.category_id == self.__category_id:
                products_of_category = set(category.products)
                if self.__applied_to_subcategories:
                    for subcategory in category.sub_categories:
                        products_of_category.update(set(subcategory.products))
                    
                for product in products_of_category:
                    discount_reduction += product.price * self.percentage
        return discount_reduction


# --------------- Store Discount ---------------#
class StoreDiscount(Discount):
    """
    * This class is responsible for creating a discount that is applied to a specific store.
    """
    def __init__(self, discount_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, predicate: Optional[Constraint], store_id: int):
        super().__init__(discount_id, discount_description, starting_date, ending_date, percentage, predicate)
        self.__store_id = store_id

    @property
    def store_id(self) -> int:
        return self.__store_id

    def calculate_discount(self, basket_information: BasketInformationForDiscountDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForDiscountDTO
        * This function is responsible for calculating the discount based on the basket information, the discount is only applied to the products that fall under the store.
        * Returns: float of the amount the discount will deduce from the total price.
        """
        if self.__predicate is not None and not self.__predicate.is_satisfied(basket_information):
            raise ValueError("Discount not applicable")
        if self.starting_date > datetime.now() or self.ending_date < datetime.now():
            raise ValueError("Discount expired!")
        
        discount_reduction = 0.0
        if self.__store_id == basket_information.store_id:
            for product in basket_information.products:
                if product.store_id == self.__store_id:
                    discount_reduction += product.price * self.percentage
        return discount_reduction

# --------------- Product Discount ---------------#
class ProductDiscount(Discount):
    # class responsible for returning the total price of the product discount.
    def __init__(self, discount_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, predicate: Optional[Constraint], product_id: int, store_id: int):
        super().__init__(discount_id, discount_description, starting_date, ending_date, percentage, predicate)
        self.__product_id = product_id
        self.__store_id = store_id

    @property
    def product_id(self) -> int:
        return self.__product_id
    
    @property
    def store_id(self) -> int:
        return self.__store_id
    
    def calculate_discount(self, basket_information: BasketInformationForDiscountDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForDiscountDTO
        * This function is responsible for calculating the discount based on the basket information, the discount is only applied to the products that fall under the product.
        * Returns: float of the amount the discount will deduce from the total price.
        """
        if self.__predicate is not None and not self.__predicate.is_satisfied(basket_information):
            raise ValueError("Discount not applicable")
        if self.starting_date > datetime.now() or self.ending_date < datetime.now():
            raise ValueError("Discount expired!")
        
        if self.__store_id != basket_information.store_id:
            raise ValueError("Discount not applicable")

        discount_reduction = 0.0
        for product in basket_information.products:
            if product.product_id == self.__product_id and product.store_id == self.__store_id:
                discount_reduction += product.price * self.percentage
        return discount_reduction


# --------------- And Discount ---------------#
class AndDiscount(DiscountInterface):
    """
    * This class is responsible for creating a discount composite that is applied when both discounts are applicable.
    """
    def __init__(self, discount1: Discount, discount2: Discount):
        self.__discount1 = discount1
        self.__discount2 = discount2

    def calculate_discount(self, basket_information: BasketInformationForDiscountDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForDiscountDTO
        * This function is responsible for calculating the discount based on the basket information. It is only applied when both discounts have satisfied predicates and returns the sum of the discounts
        """
        if self.__discount1.predicate.is_satisfied(basket_information) and self.__discount2.predicate.is_satisfied(basket_information):
            return self.__discount1.calculate_discount(basket_information) + self.__discount2.calculate_discount(basket_information)
        else:
            raise ValueError("Discount not applicable")
        

# --------------- Or Discount ---------------#
class OrDiscount(DiscountInterface):
    """
    * This class is responsible for creating a discount composite that is applied when at least one of the discounts is applicable.
    """
    def __init__(self, discount1: Discount, discount2: Discount): # add decision rule
        self.__discount1 = discount1
        self.__discount2 = discount2

    def calculate_discount(self, basket_information: BasketInformationForDiscountDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForDiscountDTO
        * This function is responsible for calculating the discount based on the basket information. It is only applied when at least one of the discounts have satisfied predicates and returns the sum of the discounts
        * NOTE: for simplicity, we assume that if both discounts are applicable, we would use both, but if only one is applicable, we would use only that one.
        """
        if self.__discount1.predicate.is_satisfied(basket_information) and self.__discount2.predicate.is_satisfied(basket_information):
            return self.__discount1.calculate_discount(basket_information) + self.__discount2.calculate_discount(basket_information)
        elif self.__discount1.predicate.is_satisfied(basket_information):
            return self.__discount1.calculate_discount(basket_information)
        elif self.__discount2.predicate.is_satisfied(basket_information):
            return self.__discount2.calculate_discount(basket_information)
        else:
            raise ValueError("Discount not applicable")

# --------------- Xor Discount ---------------#
class XorDiscount(DiscountInterface):
    def __init__(self, discount1: Discount, discount2: Discount): # add decision rule
        self.__discount1 = discount1
        self.__discount2 = discount2

    def calculate_discount(self, basket_information: BasketInformationForDiscountDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForDiscountDTO
        * This function is responsible for calculating the discount based on the basket information.
        * Returns: float of the amount the discount will deduce from the total price.
        """
        if self.__discount1.predicate.is_satisfied(basket_information):
            return self.__discount1.calculate_discount(basket_information)
        elif self.__discount2.predicate.is_satisfied(basket_information):
            return self.__discount2.calculate_discount(basket_information)
        else:
            raise ValueError("Discount not applicable")


# --------------- Max Discount classes ---------------#
class maxDiscount(DiscountInterface):
    # class responsible for returning the total price of the maximum discount.
    def __init__(self, ListDiscount: list[Discount]):
        self.__ListDiscount = ListDiscount

    def calculate_discount(self, basket_information: BasketInformationForDiscountDTO) -> float:
        """
        * Parameters: basket in BasketDTO, user in UserDTO
        * This function is responsible for calculating the discount based on the basket and user.
        * Returns: float
        """
        return max([discount.calculate_discount(basket_information) for discount in self.__ListDiscount])


# --------------- Additive Discount classes ---------------#
class additiveDiscountStrategy(Discount):
    # class responsible for returning the total price of the maximum discount.
    def __init__(self, ListDiscount: list[Discount]):
        self.__ListDiscount = ListDiscount

    def calculate_discount(self, basket_information: BasketInformationForDiscountDTO) -> float:
        """
        * Parameters: basket in BasketDTO, user in UserDTO
        * This function is responsible for calculating the discount based on the basket and user.
        * Returns: float
        """
        return sum([discount.calculate_discount(basket_information) for discount in self.__ListDiscount])