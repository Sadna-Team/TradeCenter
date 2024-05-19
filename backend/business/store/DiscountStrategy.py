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

    @abstractmethod 
    def changeDiscountPercentage(self, newpercentage: float) -> None:
        pass

    @abstractmethod
    def changeDiscountDescription(self, newDescription: str) -> None:
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
    def __setDiscountId(self, discountId):
        self.discountId = discountId

    @property
    def getDiscountDescription(self):
        return self.discountDescription
    
    @property 
    def __setDiscountDescription(self, discountDescription):
        self.discountDescription = discountDescription

    @property
    def getStartingDate(self):
        return self.startingDate
    
    @property
    def __setStartingDate(self, startingDate):
        self.startingDate = startingDate

    @property
    def getEndingDate(self):
        return self.endingDate
    
    @property
    def __setEndingDate(self, endingDate):
        self.endingDate = endingDate

    @property
    def getPercentage(self):
        return self.percentage
    
    @property
    def __setPercentage(self, percentage):
        self.percentage = percentage

    @property
    def getProduct_id(self):
        return self.product_id
    
    @property
    def __setProduct_id(self, product_id):
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
    
    def changeDiscountPercentage(self, newpercentage: float) -> bool:
        '''
        * Parameters: newpercentage in float
        * This function is responsible for changing the discount percentage.
        * Returns: None
        '''
        if newpercentage < 0 or newpercentage > 1:
            return False
        self.__setPercentage(newpercentage)
        return True


    def changeDiscountDescription(self, newDescription: str) -> bool:
        '''
        * Parameters: newDescription in str
        * This function is responsible for changing the discount description.
        * Returns: None
        '''
        self.__setDiscountDescription(newDescription)
        return True

