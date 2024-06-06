# --------------- imports ---------------#
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime, time

from backend.business.DTOs import AddressDTO, BasketInformationForDiscountDTO #maybe timezone constraints :O


# --------------- Constraint Interface ---------------#
class Constraint(ABC):
    @abstractmethod
    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
        pass

# ------------------------------------ Leaf Classes of Composite: ------------------------------------ #

# --------------- age constraint class ---------------#
class AgeConstraint(Constraint):
    def __init__(self, age_limit: int):
        self.__age_limit = age_limit

    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
        today = datetime.today()
        birth_date = basket_information.user_info.birthdate
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        return age >= self.__age_limit
    
    @property
    def age_limit(self):
        return self.__min_age


# --------------- location constraint class ---------------#
class LocationConstraint(Constraint):
    def __init__(self, location: AddressDTO):
        self.__location = location

    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
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

    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
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


    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
        if basket_information.store_id != self.__store_id:
            return False
        
        if self.__max_price == -1:
            return self.__min_price <= basket_information.total_price_of_basket
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


    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
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

    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
        for category in basket_information.categories:
            if category.category_id == self.__category_id:
                products = category.products
                for sub_categories in category.sub_categories:
                    products += sub_categories.products
                category_total_price: float = 0.0
                for product in products:
                    category_total_price += product.price * product.amount

                if self.__max_price == -1:
                    return self.__min_price <= category_total_price
                return self.__min_price <= category_total_price <= self.__max_price
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

    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
        amount_in_basket = 0
        for product in basket_information.products:
            amount_in_basket += product.amount
        
        if basket_information.store_id != self.__store_id:
            return False
        
        return self.__min_amount <= amount_in_basket
    
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

    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
        if basket_information.store_id != self.__store_id:
            return False
        
        for product in basket_information.products:
            if product.product_id == self.__product_id:
                return self.__min_amount <= product.amount
        raise ValueError("Product not found in basket")
        
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

    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
        for category in basket_information.categories:
            if category.category_id == self.__category_id:
                products = category.products
                for sub_categories in category.sub_categories:
                    products += sub_categories.products
                category_total_amount: int = 0
                for product in products:
                    category_total_amount += product.amount

                return self.__min_amount <= category_total_amount
            
        raise ValueError("Category not found in basket")
    
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

    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
        if basket_information.store_id != self.__store_id:
            return False
        
        weight_of_basket = 0.0
        for product in basket_information.products:
            weight_of_basket += product.weight
        
        if self.__max_weight == -1:
            return self.__min_weight <= weight_of_basket
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

    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
        if basket_information.store_id != self.__store_id:
            return False
        
        for product in basket_information.products:
            if product.product_id == self.__product_id:
                if self.__max_weight == -1:
                    return self.__min_weight <= product.weight
                return self.__min_weight <= product.weight <= self.__max_weight
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

    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
        for category in basket_information.categories:
            if category.category_id == self.__category_id:
                products = category.products
                for sub_categories in category.sub_categories:
                    products += sub_categories.products
                category_total_weight: float = 0.0
                for product in products:
                    category_total_weight += product.weight

                if self.__max_weight == -1:
                    return self.__min_weight <= category_total_weight
                return self.__min_weight <= category_total_weight <= self.__max_weight
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


    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
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


    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
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


    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
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


    def is_satisfied(self, basket_information: BasketInformationForDiscountDTO) -> bool:
        return not self.__constraint1.is_satisfied(basket_information) or self.__constraint2.is_satisfied(basket_information)
    
    @property
    def constraint1(self):
        return self.__constraint1
    
    @property
    def constraint2(self):
        return self.__constraint2
    
