# --------------- imports ---------------#
from abc import ABC, abstractmethod
from typing import List
from datetime import time #maybe timezone constraints :O


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
    def __init__(self, location: str):
        self.__location = location

    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        return basketInformation.location == self.__location
    
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
    
# --------------- price constraint class ---------------#
class PriceConstraint(Constraint):
    def __init__(self, min_price: float, max_price: float,):
        self.__min_price = min_price #if min_price is 0, then there is no lower limit
        self.__max_price = max_price #if max_price is -1, then there is no upper limit

    def is_satisfied(self, basketInformation: SOMETHING) -> bool:
        if self.__max_price == -1:
            return self.__min_price <= basketInformation.price
        return self.__min_price <= basketInformation.price <= self.__max_price
    
    @property
    def min_price(self):
        return self.__min_price
    
    @property
    def max_price(self):
        return self.__max_price

# --------------- amount of product constraint class ---------------#


