# --------------- imports ---------------#
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from backend.business.DTOs import BasketInformationForConstraintDTO, CategoryDTO
from backend.business.store.constraints import Constraint
from backend.error_types import *
from backend.database import db


# -------------logging configuration----------------
import logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Discount Logger')
# ---------------------------------------------------
DATE_FORMAT = '%Y-%m-%d'

# --------------- Discount base ---------------#
class Discount(ABC):
    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, predicate: Optional[Constraint]):
        if isinstance(starting_date,str):
            starting_date = datetime.strptime(starting_date, DATE_FORMAT)
        if isinstance(ending_date,str):
            ending_date = datetime.strptime(ending_date, DATE_FORMAT)
        if starting_date > ending_date:
            logger.error("[Discount] Invalid dates")
            raise DiscountAndConstraintsError("invalid dates", DiscountAndConstraintsErrorTypes.invalid_date)
        if (percentage < 0 or percentage > 1) and percentage!=-1:
            logger.error("[Discount] Invalid percentage")
            raise DiscountAndConstraintsError("Invalid percentage", DiscountAndConstraintsErrorTypes.invalid_percentage)
        self.__discount_id = discount_id
        self.__store_id = store_id
        self.__discount_description = discount_description
        self.__starting_date = starting_date
        self.__ending_date = ending_date
        self.__percentage = percentage
        self.__predicate = predicate
        logger.info("[Discount] Discount with id: " + str(discount_id) + " created successfully!")

    @property
    def discount_id(self):
        return self.__discount_id
    
    @property 
    def store_id(self):
        return self.__store_id
    
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
    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        pass

    @abstractmethod
    def get_discount_info_as_dict(self) -> dict:
        pass

    def change_discount_percentage(self, new_percentage: float) -> None:
        if new_percentage < 0 or new_percentage > 1:
            logger.error("[Discount] Invalid percentage")
            raise DiscountAndConstraintsError("Invalid percentage", DiscountAndConstraintsErrorTypes.invalid_percentage)
        logger.info("[Discount] Discount percentage changed to: " + str(new_percentage))
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
    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, predicate: Optional[Constraint], category_id: int, applied_to_subcategories: bool):
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, predicate)
        self.__category_id = category_id
        self.__applied_to_subcategories = applied_to_subcategories
        logger.info("[CategoryDiscount] Category discount with id: " + str(discount_id) + " created successfully!")

    @property
    def category_id(self) -> int:
        return self.__category_id
    
    @property
    def applied_to_subcategories(self) -> bool:
        return self.__applied_to_subcategories
    

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForConstraintDTO
        * This function is responsible for calculating the discount based on the basket information, the discount is only applied to the products that fall under the category.
        * Returns: float of the amount the discount will deduce from the total price.
        """
        if self.predicate is not None and not self.predicate.is_satisfied(basket_information):
            logger.info("[CategoryDiscount] Predicate not satisfied")
            return 0.0
        if self.starting_date > datetime.now() or self.ending_date < datetime.now():
            logger.info("[CategoryDiscount] Discount expired!")
            return 0.0
        
        discount_reduction = 0.0
        for category in basket_information.categories:
            if category.category_id == self.__category_id:
                products_of_category = set(category.products)
                if self.__applied_to_subcategories:
                    for subcategory in category.sub_categories:
                        products_of_category.update(set(subcategory.products))
                    
                for product in products_of_category:
                    discount_reduction += product.price * product.amount * self.percentage
        logger.info("[CategoryDiscount] Discount calculated to be: " + str(discount_reduction))
        return discount_reduction
    
    def get_discount_info_as_dict(self) -> dict:
        is_applied = "Yes" if self.applied_to_subcategories else "No"
        
        return {
            "discount_type": "categoryDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "percentage": self.percentage,
            "predicate": self.predicate.get_constraint_info_as_string() if self.predicate is not None else "None",
            "category_id": self.category_id,
            "applied_to_subcategories": is_applied
        }


# --------------- Store Discount ---------------#
class StoreDiscount(Discount):
    """
    * This class is responsible for creating a discount that is applied to a specific store.
    """
    def __init__(self, discount_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, predicate: Optional[Constraint], store_id: int):
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, predicate)
        logger.info("[StoreDiscount] Store discount with id: " + str(discount_id) + " created successfully!")

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForConstraintDTO
        * This function is responsible for calculating the discount based on the basket information, the discount is only applied to the products that fall under the store.
        * Returns: float of the amount the discount will deduce from the total price.
        """
        if self.predicate is not None and not self.predicate.is_satisfied(basket_information):
            logger.info("[StoreDiscount] Predicate not satisfied")
            return 0.0
        
        if self.starting_date > datetime.now() or self.ending_date < datetime.now():
            logger.info("[StoreDiscount] Discount expired!")
            return 0.0
        
        discount_reduction = 0.0
        if self.store_id == basket_information.store_id:
            for product in basket_information.products:
                if product.store_id == self.store_id:
                    discount_reduction += product.price * product.amount * self.percentage
        logger.info("[StoreDiscount] Discount calculated to be: " + str(discount_reduction))
        return discount_reduction
    
    def get_discount_info_as_dict(self) -> dict:

        return {
            "discount_type": "storeDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "percentage": self.percentage,
            "predicate": self.predicate.get_constraint_info_as_string() if self.predicate is not None else "None"
        }

# --------------- Product Discount ---------------#
class ProductDiscount(Discount):
    # class responsible for returning the total price of the product discount.
    def __init__(self, discount_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, predicate: Optional[Constraint], product_id: int, store_id: int):
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, predicate)
        self.__product_id = product_id
        logger.info("[ProductDiscount] Product discount with id: " + str(discount_id) + " created successfully!")

    @property
    def product_id(self) -> int:
        return self.__product_id
    
    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForConstraintDTO
        * This function is responsible for calculating the discount based on the basket information, the discount is only applied to the products that fall under the product.
        * Returns: float of the amount the discount will deduce from the total price.
        """
        if self.predicate is not None and not self.predicate.is_satisfied(basket_information):
            logger.info("[ProductDiscount] Predicate not satisfied")
            return 0.0
        if self.starting_date > datetime.now() or self.ending_date < datetime.now():
            logger.info("[ProductDiscount] Discount expired!")
            return 0.0
        
        if self.store_id != basket_information.store_id:
            logger.info("[ProductDiscount] Discount not applicable due to store mismatch")
            return 0.0

        discount_reduction = 0.0
        for product in basket_information.products:
            if product.product_id == self.__product_id and product.store_id == self.store_id:
                discount_reduction += product.price * product.amount * self.percentage
        logger.info("[ProductDiscount] Discount calculated to be: " + str(discount_reduction))
        return discount_reduction
    
    def get_discount_info_as_dict(self) -> dict:

        return {
            "discount_type": "productDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "product_id": self.product_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "percentage": self.percentage,
            "predicate": self.predicate.get_constraint_info_as_string() if self.predicate is not None else "None"
        }


# --------------- And Discount ---------------#
class AndDiscount(Discount):
    """
    * This class is responsible for creating a discount composite that is applied when both discounts are applicable.
    """
    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, discount1: Discount, discount2: Discount):
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, None)
        self.__discount1 = discount1
        self.__discount2 = discount2
        logger.info("[AndDiscount] And discount created successfully!")

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForConstraintDTO
        * This function is responsible for calculating the discount based on the basket information. It is only applied when both discounts have satisfied predicates and returns the sum of the discounts
        """
        if self.__discount1.predicate is not None and self.__discount2.predicate is not None:
            if self.__discount1.predicate.is_satisfied(basket_information) and self.__discount2.predicate.is_satisfied(basket_information):
                logger.info("[AndDiscount] Both predicates satisfied, applying discounts")
                return self.__discount1.calculate_discount(basket_information) + self.__discount2.calculate_discount(basket_information)
            else:
                return 0.0
        else:
            if self.__discount1.predicate is not None and self.__discount2.predicate is None:
                if self.__discount1.predicate.is_satisfied(basket_information):
                    logger.info("[AndDiscount] Discount predicates satisfied, applying discounts")
                    return self.__discount1.calculate_discount(basket_information) + self.__discount2.calculate_discount(basket_information)
                else:
                    return 0.0
            elif self.__discount1.predicate is None and self.__discount2.predicate is not None:
                if self.__discount2.predicate.is_satisfied(basket_information):
                    logger.info("[AndDiscount] Discount predicates satisfied, applying discounts")
                    return self.__discount1.calculate_discount(basket_information) + self.__discount2.calculate_discount(basket_information)
                else:
                    return 0.0
            else:
                logger.info("[AndDiscount] Both discounts applicable, applying discounts")
                return self.__discount1.calculate_discount(basket_information) + self.__discount2.calculate_discount(basket_information)
    
    def change_predicate(self, new_predicate: Constraint) -> None:
        pass # we don't want to change the predicate of the composite discount

    def get_discount_info_as_dict(self) -> dict:

        dict_of_disc1 = self.__discount1.get_discount_info_as_dict()
        dict_of_disc2 = self.__discount2.get_discount_info_as_dict() 

        return {
            "discount_type": "andDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "discount_id1": dict_of_disc1,
            "discount_id2": dict_of_disc2
        }
    

# --------------- Or Discount ---------------#
class OrDiscount(Discount):
    """
    * This class is responsible for creating a discount composite that is applied when at least one of the discounts is applicable.
    """
    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, discount1: Discount, discount2: Discount): # add decision rule
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, None)
        self.__discount1 = discount1
        self.__discount2 = discount2

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForConstraintDTO
        * This function is responsible for calculating the discount based on the basket information. It is only applied when at least one of the discounts have satisfied predicates and returns the sum of the discounts
        * NOTE: for simplicity, we assume that if both discounts are applicable, we would use both, but if only one is applicable, we would use only that one.
        """
        if self.__discount1.predicate is None and self.__discount2.predicate is None:
            logger.info("[OrDiscount] Both discounts applicable, applying discounts")
            return self.__discount1.calculate_discount(basket_information) + self.__discount2.calculate_discount(basket_information)
        elif self.__discount1.predicate is None and self.__discount2.predicate is not None:
            if self.__discount2.predicate.is_satisfied(basket_information):
                logger.info("[OrDiscount] Both discounts applicable, applying discounts")
                return self.__discount1.calculate_discount(basket_information) + self.__discount2.calculate_discount(basket_information)
            else:
                logger.info("[OrDiscount] Discount 1 applicable, applying discount 1")
                return self.__discount1.calculate_discount(basket_information)
        elif self.__discount1.predicate is not None and self.__discount2.predicate is None:
            if self.__discount1.predicate.is_satisfied(basket_information):
                logger.info("[OrDiscount] Both discounts applicable, applying discounts")
                return self.__discount1.calculate_discount(basket_information) + self.__discount2.calculate_discount(basket_information)
            else:
                logger.info("[OrDiscount] Discount 2 applicable, applying discount 2")
                return self.__discount2.calculate_discount(basket_information)
        else:
            if self.__discount1.predicate.is_satisfied(basket_information) and self.__discount2.predicate.is_satisfied(basket_information):
                logger.info("[OrDiscount] Both discounts applicable, applying discounts")
                return self.__discount1.calculate_discount(basket_information) + self.__discount2.calculate_discount(basket_information)
            elif self.__discount1.predicate.is_satisfied(basket_information):
                logger.info("[OrDiscount] Discount 1 applicable, applying discount 1")
                return self.__discount1.calculate_discount(basket_information)
            elif self.__discount2.predicate.is_satisfied(basket_information):
                logger.info("[OrDiscount] Discount 2 applicable, applying discount 2")
                return self.__discount2.calculate_discount(basket_information)
            else:
                return 0.0
            
        
    def change_predicate(self, new_predicate: Constraint) -> None:
        pass # we don't want to change the predicate of the composite discount


    def get_discount_info_as_dict(self) -> dict:
        dict_of_disc1 = self.__discount1.get_discount_info_as_dict()
        dict_of_disc2 = self.__discount2.get_discount_info_as_dict() 

        return {
            "discount_type": "orDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "discount_id1": dict_of_disc1,
            "discount_id2": dict_of_disc2
        }

# --------------- Xor Discount ---------------#
class XorDiscount(Discount):
    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, discount1: Discount, discount2: Discount): # add decision rule
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, None)
        self.__discount1 = discount1
        self.__discount2 = discount2
        logger.info("[XorDiscount] Xor discount created successfully!")

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForConstraintDTO
        * This function is responsible for calculating the discount based on the basket information.
        * Returns: float of the amount the discount will deduce from the total price.
        """
        if self.__discount1.predicate is not None and self.__discount2.predicate is not None:    
            if self.__discount1.predicate.is_satisfied(basket_information):
                logger.info("[XorDiscount] Discount 1 applicable, applying discount 1")
                return self.__discount1.calculate_discount(basket_information)
            elif self.__discount2.predicate.is_satisfied(basket_information):
                logger.info("[XorDiscount] Discount 2 applicable, applying discount 2")
                return self.__discount2.calculate_discount(basket_information)
            else:
                return 0.0
        elif self.__discount1.predicate is not None and self.__discount2.predicate is None:
            if self.__discount1.predicate.is_satisfied(basket_information):
                logger.info("[XorDiscount] Discount 1 applicable, applying discount 1")
                return self.__discount1.calculate_discount(basket_information)
            else:
                logger.info("[XorDiscount] discount 2 applicable, applying discount 2")
                return self.__discount2.calculate_discount(basket_information)
        else:
            logger.info("[XorDiscount] Both discounts applicable, applying discount 1")
            return self.__discount1.calculate_discount(basket_information) 
        
    
    def change_predicate(self, new_predicate: Constraint) -> None:
        pass # we don't want to change the predicate of the composite discount

    def get_discount_info_as_dict(self) -> dict:

        dict_of_disc1 = self.__discount1.get_discount_info_as_dict()
        dict_of_disc2 = self.__discount2.get_discount_info_as_dict() 
        return {
            "discount_type": "xorDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "discount_id1": dict_of_disc1,
            "discount_id2": dict_of_disc2
        }

# --------------- Max Discount classes ---------------#
class MaxDiscount(Discount):
    # class responsible for returning the total price of the maximum discount.
    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, ListDiscount: list[Discount]):
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, None)
        self.__ListDiscount = ListDiscount
        logger.info("[maxDiscount] Max discount created successfully!")

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket in BasketDTO, user in UserDTO
        * This function is responsible for calculating the discount based on the basket and user.
        * Returns: float
        """
        logger.info("[maxDiscount] Calculating max discount")
        return max([discount.calculate_discount(basket_information) for discount in self.__ListDiscount])
    
    
    def change_predicate(self, new_predicate: Constraint) -> None:
        pass # we don't want to change the predicate of the composite discount

    def get_discount_info_as_dict(self) -> dict:
        discounts_info = dict()
        for discount in self.__ListDiscount:
            discounts_info[discount.discount_id] = discount.get_discount_info_as_dict()

        return {
            "discount_type": "maxDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "discounts_info": discounts_info
        }


# --------------- Additive Discount classes ---------------#
class AdditiveDiscount(Discount):
    # class responsible for returning the total price of the maximum discount.
    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, ListDiscount: list[Discount]):
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, None)
        self.__ListDiscount = ListDiscount
        logger.info("[additiveDiscount] Additive discount created successfully!")

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket in BasketDTO, user in UserDTO
        * This function is responsible for calculating the discount based on the basket and user.
        * Returns: float
        """
        logger.info("[additiveDiscount] Calculating additive discount")
        return sum([discount.calculate_discount(basket_information) for discount in self.__ListDiscount])
    
    
    def change_predicate(self, new_predicate: Constraint) -> None:
        pass # we don't want to change the predicate of the composite discount
    
    def get_discount_info_as_dict(self) -> dict:
        date_format = "%Y-%m-%d" 

        discounts_info = dict()
        for discount in self.__ListDiscount:
            discounts_info[discount.discount_id] = discount.get_discount_info_as_dict()
        return {
            "discount_type": "additiveDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(date_format)),
            "end_date": str(self.ending_date.strftime(date_format)),
            "discounts_info": discounts_info
        }