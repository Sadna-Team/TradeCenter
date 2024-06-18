# --------------- imports ---------------#
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime, time

from backend.business.DTOs import AddressDTO, BasketInformationForConstraintDTO, CategoryForConstraintDTO #maybe timezone constraints :O

# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')

# ---------------------------------------------------

# --------------- Constraint Interface ---------------#
class Constraint(ABC):
    @abstractmethod
    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        pass

# ------------------------------------ Leaf Classes of Composite: ------------------------------------ #

# --------------- age constraint class ---------------#
class AgeConstraint(Constraint):
    def __init__(self, age_limit: int):
        self.__age_limit = age_limit
        logger.info("[AgeConstraint]: Age constraint created with age limit: " + str(age_limit))

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[AgeConstraint]: Checking if user is older than " + str(self.__age_limit) + " years old")
        today = datetime.today()
        if basket_information.user_info.birthdate is None:
            logger.info("[AgeConstraint]: User birthdate is not provided")
            return False
        birth_date = basket_information.user_info.birthdate
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


        return age >= self.__age_limit
    
    @property
    def age_limit(self):
        return self.__age_limit


# --------------- location constraint class ---------------# 
class LocationConstraint(Constraint):
    def __init__(self, location: AddressDTO):
        self.__location = location
        logger.info("[LocationConstraint]: Location constraint created with location: " + str(location))

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[LocationConstraint]: Checking if user location fulfills the constraint")
        user_location = basket_information.user_info.address
        country = user_location.country
        city = user_location.city
        return self.__location.country == country and self.__location.city == city
    
    @property
    def location(self):
        return self.__location
    

# --------------- time constraint class ---------------#
class TimeConstraint(Constraint):
    def __init__(self, start_time: time, end_time: time):
        self.__start_time = start_time
        self.__end_time = end_time
        logger.info("[TimeConstraint]: Time constraint created with start time: " + str(start_time) + " and end time: " + str(end_time))

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[TimeConstraint]: Checking if the time of purchase is within the time constraint")
        time_of_purchase = basket_information.time_of_purchase.time()

        return self.__start_time <= time_of_purchase <= self.__end_time
    
    @property
    def start_time(self):
        return self.__start_time
    
    @property
    def end_time(self):
        return self.__end_time
    
# --------------- price basket constraint class ---------------#
class PriceBasketConstraint(Constraint):
    def __init__(self, min_price: float, max_price: float, store_id: int):
        self.__min_price = min_price #if min_price is 0, then there is no lower limit
        self.__max_price = max_price #if max_price is -1, then there is no upper limit
        self.__store_id = store_id
        logger.info("[PriceBasketConstraint]: Price basket constraint created!")


    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        if basket_information.store_id != self.__store_id:
            logger.warning("[PriceBasketConstraint]: Store id does not match the store id of the basket")
            return False
        
        if self.__max_price == -1:
            logger.info("[PriceBasketConstraint]: Checking if the total price of the basket is atleast" + str(self.__min_price) + " dollars")
            return self.__min_price <= basket_information.total_price_of_basket
        logger.info("[PriceBasketConstraint]: Checking if the total price of the basket is between " + str(self.__min_price) + " and " + str(self.__max_price) + " dollars")
        return self.__min_price <= basket_information.total_price_of_basket <= self.__max_price
    
    @property
    def min_price(self):
        return self.__min_price
    
    @property
    def max_price(self):
        return self.__max_price
    
    @property
    def store_id(self):
        return self.__store_id

# --------------- price product constraint class  ---------------#
class PriceProductConstraint(Constraint):
    def __init__(self, min_price: float, max_price: float, product_id: int, store_id: int):
        self.__min_price = min_price #if min_price is 0, then there is no lower limit
        self.__max_price = max_price #if max_price is -1, then there is no upper limit
        self.__product_id = product_id
        self.__store_id = store_id
        logger.info("[PriceProductConstraint]: Price product constraint created!")


    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[PriceProductConstraint]: Checking if the price of the product fulfills the constraint")
        if basket_information.store_id != self.__store_id:
            return False
        
        for product in basket_information.products:
            if product.product_id == self.__product_id:
                if self.__max_price == -1:
                    return self.__min_price <= product.price * product.amount
                return self.__min_price <= product.price * product.amount <= self.__max_price
        raise ValueError("Product not found in basket")
        
    @property
    def min_price(self):
        return self.__min_price
    
    @property
    def max_price(self):
        return self.__max_price
    
    @property
    def product_id(self):
        return self.__product_id
    
    @property
    def store_id(self):
        return self.__store_id


# --------------- price category constraint class  ---------------#
class PriceCategoryConstraint(Constraint):
    def __init__(self, min_price: float, max_price: float, category_id: int):
        self.__min_price = min_price #if min_price is 0, then there is no lower limit
        self.__max_price = max_price #if max_price is -1, then there is no upper limit
        self.__category_id = category_id 
        logger.info("[PriceCategoryConstraint]: Price category constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        categories= basket_information.categories
        for category in categories:
            if category.category_id == self.__category_id:
                products = set(category.products)
                for sub_categories in category.sub_categories:
                    products.update(set(sub_categories.products))
                category_total_price: float = 0.0
                for product in products:
                    category_total_price += product.price * product.amount

                if self.__max_price == -1:
                    logger.info("[PriceCategoryConstraint]: Checking if the price of the products of the categpry i atleast" + str(self.__min_price) + " dollars")
                    return self.__min_price <= category_total_price
                logger.info("[PriceCategoryConstraint]: Checking if the price of the products of the categpry is between " + str(self.__min_price) + " and " + str(self.__max_price) + " dollars")
                return self.__min_price <= category_total_price <= self.__max_price
        
        logger.error("[PriceCategoryConstraint]: Category not found in basket")
        raise ValueError("Category not found in basket")
    
    @property
    def min_price(self):
        return self.__min_price
    
    @property
    def max_price(self):
        return self.__max_price
    
    @property
    def category_id(self):
        return self.__category_id
    


# --------------- amount basket constraint class  ---------------#
class AmountBasketConstraint(Constraint):
    def __init__(self, min_amount: int, store_id: int):
        self.__min_amount = min_amount #if min_amount is 0, then there is no lower limit
        self.__store_id = store_id
        logger.info("[AmountBasketConstraint]: Amount basket constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        amount_in_basket = 0
        for product in basket_information.products:
            amount_in_basket += product.amount
        
        if basket_information.store_id != self.__store_id:
            logger.warning("[AmountBasketConstraint]: Store id does not match the store id of the basket")
            return False
        
        logger.info("[AmountBasketConstraint]: Checking if the amount of products in the basket fulfills the constraint")
        return self.__min_amount <= amount_in_basket
    
    @property
    def min_amount(self):
        return self.__min_amount
    
    @property
    def store_id(self):
        return self.__store_id


# --------------- amount product constraint class  ---------------#
class AmountProductConstraint(Constraint):
    def __init__(self, min_amount: int, product_id: int, store_id: int):
        self.__min_amount = min_amount #if min_amount is 0, then there is no lower limit
        self.__product_id = product_id
        self.__store_id = store_id
        logger.info("[AmountProductConstraint]: Amount product constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        if basket_information.store_id != self.__store_id:
            logger.warning("[AmountProductConstraint]: Store id does not match the store id of the basket")
            return False
        
        for product in basket_information.products:
            if product.product_id == self.__product_id:
                logger.info("[AmountProductConstraint]: Checking if the amount of the product fulfills the constraint")
                return self.__min_amount <= product.amount
            
        logger.error("[AmountProductConstraint]: Product not found in basket")
        raise ValueError("Product not found in basket")
        
    @property
    def min_amount(self):
        return self.__min_amount
    
    @property
    def product_id(self):
        return self.__product_id
    
    @property
    def store_id(self):
        return self.__store_id
    
# --------------- amount category constraint class  ---------------#
class AmountCategoryConstraint(Constraint):
    def __init__(self, min_amount: int, category_id: int):
        self.__min_amount = min_amount #if min_amount is 0, then there is no lower limit
        self.__category_id = category_id
        logger.info("[AmountCategoryConstraint]: Amount category constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        categories = basket_information.categories
        for c in categories:
            if c.category_id == self.__category_id:
                products = c.products
                for sub_categories in c.sub_categories:
                    products += sub_categories.products
                category_total_amount: int = 0
                for product in products:
                    category_total_amount += product.amount

                logger.info("[AmountCategoryConstraint]: Checking if the amount of products in the category fulfills the constraint")
                return self.__min_amount <= category_total_amount
            
        logger.error("[AmountCategoryConstraint]: Category not found in basket")
        raise ValueError("Category not found in basket")
    
    @property
    def min_amount(self):
        return self.__min_amount
    
    @property
    def category_id(self):
        return self.__category_id
    

# --------------- weight basket constraint class  ---------------#
class WeightBasketConstraint(Constraint):
    def __init__(self, min_weight: float, max_weight: float, store_id: int):
        self.__min_weight = min_weight #if min_weight is 0, then there is no lower limit
        self.__max_weight = max_weight #if max_weight is -1, then there is no upper limit
        self.__store_id = store_id
        logger.info("[WeightBasketConstraint]: Weight basket constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        if basket_information.store_id != self.__store_id:
            logger.warning("[WeightBasketConstraint]: Store id does not match the store id of the basket")
            return False
        
        weight_of_basket = 0.0
        for product in basket_information.products:
            weight_of_basket += product.weight
        
        if self.__max_weight == -1:
            logger.info("[WeightBasketConstraint]: Checking if the total weight of the basket is atleast" + str(self.__min_weight) + " kg")
            return self.__min_weight <= weight_of_basket
        logger.info("[WeightBasketConstraint]: Checking if the total weight of the basket is between " + str(self.__min_weight) + " and " + str(self.__max_weight) + " kg")
        return self.__min_weight <= weight_of_basket <= self.__max_weight

    @property
    def min_weight(self):
        return self.__min_weight
    
    @property
    def max_weight(self):
        return self.__max_weight
    
    @property
    def store_id(self):
        return self.__store_id
    

# --------------- weight product constraint class  ---------------#
class WeightProductConstraint(Constraint):
    def __init__(self, min_weight: float, max_weight: float, product_id: int, store_id: int):
        self.__min_weight = min_weight #if min_weight is 0, then there is no lower limit
        self.__max_weight = max_weight #if max_weight is -1, then there is no upper limit
        self.__product_id = product_id
        self.__store_id = store_id
        logger.info("[WeightProductConstraint]: Weight product constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        if basket_information.store_id != self.__store_id:
            logger.warning("[WeightProductConstraint]: Store id does not match the store id of the basket")
            return False
        
        for product in basket_information.products:
            if product.product_id == self.__product_id:
                if self.__max_weight == -1:
                    logger.info("[WeightProductConstraint]: Checking if the weight of the product is atleast" + str(self.__min_weight) + " kg")
                    return self.__min_weight <= product.weight
                logger.info("[WeightProductConstraint]: Checking if the weight of the product is between " + str(self.__min_weight) + " and " + str(self.__max_weight) + " kg")
                return self.__min_weight <= product.weight <= self.__max_weight
            
        logger.error("[WeightProductConstraint]: Product not found in basket")
        raise ValueError("Product not found in basket")
    
    @property
    def min_weight(self):
        return self.__min_weight
    
    @property
    def max_weight(self):
        return self.__max_weight
    
    @property
    def product_id(self):
        return self.__product_id
    
    @property
    def store_id(self):
        return self.__store_id
    

# --------------- weight category constraint class  ---------------#
class WeightCategoryConstraint(Constraint):
    def __init__(self, min_weight: float, max_weight: float, category_id: int):
        self.__min_weight = min_weight #if min_weight is 0, then there is no lower limit
        self.__max_weight = max_weight #if max_weight is -1, then there is no upper limit
        self.__category_id = category_id
        logger.info("[WeightCategoryConstraint]: Weight category constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        for curr_category in basket_information.categories:
            if curr_category.category_id == self.__category_id:
                products = curr_category.products
                for sub_categories in curr_category.sub_categories:
                    products += sub_categories.products
                category_total_weight: float = 0.0
                for product in products:
                    category_total_weight += product.weight

                if self.__max_weight == -1:
                    logger.info("[WeightCategoryConstraint]: Checking if the weight of the products of the categpry is atleast" + str(self.__min_weight) + " kg")
                    return self.__min_weight <= category_total_weight
                logger.info("[WeightCategoryConstraint]: Checking if the weight of the products of the categpry is between " + str(self.__min_weight) + " and " + str(self.__max_weight) + " kg")
                return self.__min_weight <= category_total_weight <= self.__max_weight
            
        logger.error("[WeightCategoryConstraint]: Category not found in basket")
        raise ValueError("Category not found in basket")

    @property
    def min_weight(self):
        return self.__min_weight
    
    @property
    def max_weight(self):
        return self.__max_weight
    
    @property
    def category_id(self):
        return self.__category_id
    


# ------------------------------------ Composite Classes of Composite: ------------------------------------ #
# --------------- And constraint class ---------------#
class AndConstraint(Constraint):
    def __init__(self, constraint1: Constraint, constraint2: Constraint):
        self.__constraint1 = constraint1
        self.__constraint2 = constraint2
        logger.info("[AndConstraint]: And constraint created with two constraints")


    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[AndConstraint]: Checking if both constraints are satisfied")
        return self.__constraint1.is_satisfied(basket_information) and self.__constraint2.is_satisfied(basket_information)
    
    @property
    def constraint1(self):
        return self.__constraint1
    
    @property
    def constraint2(self):
        return self.__constraint2
    

# --------------- Or constraint class ---------------#
class OrConstraint(Constraint):
    def __init__(self, constraint1: Constraint, constraint2: Constraint):
        self.__constraint1 = constraint1
        self.__constraint2 = constraint2
        logger.info("[OrConstraint]: Or constraint created with two constraints")


    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[OrConstraint]: Checking if at least one of the constraints is satisfied")
        return self.__constraint1.is_satisfied(basket_information) or self.__constraint2.is_satisfied(basket_information)
    
    @property
    def constraint1(self):
        return self.__constraint1
    
    @property
    def constraint2(self):
        return self.__constraint2
    

# --------------- Xor constraint class ---------------#
class XorConstraint(Constraint):
    def __init__(self, constraint1: Constraint, constraint2: Constraint):
        self.__constraint1 = constraint1
        self.__constraint2 = constraint2
        logger.info("[XorConstraint]: Xor constraint created with two constraints")


    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[XorConstraint]: Checking if exactly one of the constraints is satisfied")
        return self.__constraint1.is_satisfied(basket_information) ^ self.__constraint2.is_satisfied(basket_information)
    
    @property
    def constraint1(self):
        return self.__constraint1
    
    @property
    def constraint2(self):
        return self.__constraint2
    

# --------------- Implies constraint class ---------------#
# this class is used to represent the implication between two constraints, where if the first constraint is satisfied, then the second constraint must be satisfied as well
class ImpliesConstraint(Constraint):
    def __init__(self, constraint1: Constraint, constraint2: Constraint):
        self.__constraint1 = constraint1
        self.__constraint2 = constraint2
        logger.info("[ImpliesConstraint]: Implies constraint created with two constraints")


    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[ImpliesConstraint]: Checking if the first constraint implies the second constraint")
        return not self.__constraint1.is_satisfied(basket_information) or self.__constraint2.is_satisfied(basket_information)
    
    @property
    def constraint1(self):
        return self.__constraint1
    
    @property
    def constraint2(self):
        return self.__constraint2
    
