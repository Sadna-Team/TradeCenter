#--------------- imports ---------------#
from abc import ABC, abstractmethod
from datetime import datetime


#--------------- Discount class ---------------#
class DiscountStrategy(ABC):
    # interface responsible for representing discounts in general. discountId unique verifier.
    def __init__(self, discountId: int, discountDescription: str, startingDate: str, endingDate: str, percentage: float):
        self.discountId = discountId
        self.discountDescription = discountDescription
        self.startingDate = startingDate
        self.endingDate = endingDate
        self.percentage = percentage

    @abstractmethod
    def calculate_discount(self, price: float) -> float:
        pass


class categoryDiscount(DiscountStrategy):
    # not implemented at this version
    pass


class storeDiscount(DiscountStrategy):
    # not implemented at this version
    pass

class productDiscount(DiscountStrategy):
    def __init__(self, discountId: int, discountDescription: str, startingDate: str, endingDate: str, percentage: float, product_id: int):
        super().__init__(discountId, discountDescription, startingDate, endingDate, percentage)
        self.product_id = product_id

    @property
    def getDiscountId(self):
        return self.discountId
    
    @property
    def setDiscountId(self, discountId):
        self.discountId = discountId

    @property
    def getDiscountDescription(self):
        return self.discountDescription
    
    @property 
    def setDiscountDescription(self, discountDescription):
        self.discountDescription = discountDescription

    @property
    def getStartingDate(self):
        return self.startingDate
    
    @property
    def setStartingDate(self, startingDate):
        self.startingDate = startingDate

    @property
    def getEndingDate(self):
        return self.endingDate
    
    @property
    def setEndingDate(self, endingDate):
        self.endingDate = endingDate

    @property
    def getPercentage(self):
        return self.percentage
    
    @property
    def setPercentage(self, percentage):
        self.percentage = percentage

    @property
    def getProduct_id(self):
        return self.product_id
    
    @property
    def setProduct_id(self, product_id):
        self.product_id = product_id


    def calculate_discount(self, price: float) -> float:
        '''
        * Parameters: price in float
        * This function is responsible for verifying if the discount is valid and returning the price with the discount.
        * Returns: price after discount in float or without depending on if the discount is valid.
        '''
        if self.startingDate <= datetime.now() <= self.endingDate:
            return price - price * self.percentage
        return price
    