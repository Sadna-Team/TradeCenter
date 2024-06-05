# --------------- imports ---------------#
from abc import ABC, abstractmethod
from typing import List
from datetime import time

from backend.business.address import Address #maybe timezone constraints :O


# --------------- Constraint Interface ---------------#
class Constraint(ABC):
    @abstractmethod
    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        pass

# ------------------------------------ Leaf Classes of Composite: ------------------------------------ #

# --------------- age constraint class ---------------#
class AgeConstraint(Constraint):
    def __init__(self, age_limit: int):
        self.__age_limit = age_limit

    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        return basketInformation.age >= self.__age_limit
    
    @property
    def age_limit(self):
        return self.__min_age


# --------------- location constraint class ---------------#
class LocationConstraint(Constraint):
    def __init__(self, location: Address):
        self.__location = location

    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        return basketInformation.location == self.__location.country #basketInformation.location.country
    
    @property
    def location(self):
        return self.__location
    

# --------------- time constraint class ---------------#
class TimeConstraint(Constraint):
    def __init__(self, start_time: time, end_time: time):
        self.__start_time = start_time
        self.__end_time = end_time

    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        return self.__start_time <= basketInformation.time <= self.__end_time
    
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


    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        if basketInformation.store_id != self.__store_id:
            return False
        
        if self.__max_price == -1:
            return self.__min_price <= basketInformation.basket_price
        return self.__min_price <= basketInformation.basket_price <= self.__max_price
    
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


    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        if basketInformation.store_id != self.__store_id:
            return False
        
        #for 
        if self.__max_price == -1:
            return self.__min_price <= basketInformation.product_price
        return self.__min_price <= basketInformation.product_price <= self.__max_price
    
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

    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        if self.__max_price == -1:
            return self.__min_price <= basketInformation.category_price
        return self.__min_price <= basketInformation.category_price <= self.__max_price
    
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

    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        if basketInformation.store_id != self.__store_id:
            return False
        
        return self.__min_amount <= basketInformation.basket_amount
    
    @property
    def min_amount(self):
        return self.__min_amount
    
    @property
    def max_amount(self):
        return self.__max_amount
    
    @property
    def store_id(self):
        return self.__store_id


# --------------- amount product constraint class  ---------------#
class AmountProductConstraint(Constraint):
    def __init__(self, min_amount: int, product_id: int, store_id: int):
        self.__min_amount = min_amount #if min_amount is 0, then there is no lower limit
        self.__product_id = product_id
        self.__store_id = store_id

    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        if basketInformation.store_id != self.__store_id:
            return False
        
        return self.__min_amount <= basketInformation.product_amount
    
    @property
    def min_amount(self):
        return self.__min_amount
    
    @property
    def max_amount(self):
        return self.__max_amount
    
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

    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        return self.__min_amount <= basketInformation.category_amount
    
    @property
    def min_amount(self):
        return self.__min_amount
    
    @property
    def max_amount(self):
        return self.__max_amount
    
    @property
    def category_id(self):
        return self.__category_id
    

# --------------- weight basket constraint class  ---------------#
class WeightBasketConstraint(Constraint):
    def __init__(self, min_weight: float, max_weight: float, store_id: int):
        self.__min_weight = min_weight #if min_weight is 0, then there is no lower limit
        self.__max_weight = max_weight #if max_weight is -1, then there is no upper limit
        self.__store_id = store_id

    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        if basketInformation.store_id != self.__store_id:
            return False
        
        if self.__max_weight == -1:
            return self.__min_weight <= basketInformation.basket_weight
        return self.__min_weight <= basketInformation.basket_weight <= self.__max_weight
    
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

    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        if basketInformation.store_id != self.__store_id:
            return False
        
        if self.__max_weight == -1:
            return self.__min_weight <= basketInformation.product_weight
        return self.__min_weight <= basketInformation.product_weight <= self.__max_weight
    
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

    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        if self.__max_weight == -1:
            return self.__min_weight <= basketInformation.category_weight
        return self.__min_weight <= basketInformation.category_weight <= self.__max_weight
    
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


    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        return self.__constraint1.is_satisfied(basketInformation) and self.__constraint2.is_satisfied(basketInformation)
    
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


    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        return self.__constraint1.is_satisfied(basketInformation) or self.__constraint2.is_satisfied(basketInformation)
    
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


    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        return self.__constraint1.is_satisfied(basketInformation) ^ self.__constraint2.is_satisfied(basketInformation)
    
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


    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        return not self.__constraint1.is_satisfied(basketInformation) or self.__constraint2.is_satisfied(basketInformation)
    
    @property
    def constraint1(self):
        return self.__constraint1
    
    @property
    def constraint2(self):
        return self.__constraint2
    
