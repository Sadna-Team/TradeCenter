from enum import Enum
import datetime

class StoreFacade:
    # singleton
    __instance = None

    def __new__(cls):
        if StoreFacade.__instance is None:
            StoreFacade.__instance = object.__new__(cls)
        return StoreFacade.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # here you can add fields




# enumeration for product condition
class productCondition(Enum):
    NEW = 1
    USED = 2

productCondition = Enum('productCondition', ['NEW', 'USED'])


class product:
    # id of product is productId. It is unique for each physical product
    def __init__(self, productId: int, storeId: int, specificationId: int, expirationDate: datetime,
                condition: productCondition, price: float):
        self.__productId = productId
        self.__storeId = storeId
        self.__specificationId = specificationId
        self.__expirationDate = expirationDate
        self.__condition = condition
        self.__price = price

    #---------------------methods--------------------------------
    def isExpired(self) -> bool:
        ''' 
        * Parameters: none
        * This function checks whether the product is expired or not
        * Returns: True if the product is expired, False otherwise
        '''
        return self.__expirationDate < datetime.datetime.now()

    #---------------------getters and setters---------------------
    def get_productId(self) -> int:
        return self.__productId
    
    def set_productId(self, productId: int):
        self.__productId = productId

    def get_storeId(self) -> int:
        return self.__storeId
    
    def set_storeId(self, storeId: int):
        self.__storeId = storeId

    def get_specificationId(self) -> int:
        return self.__specificationId
    
    def set_specificationId(self, specificationId: int):
        self.__specificationId = specificationId

    def get_expirationDate(self) -> datetime:
        return self.__expirationDate
    
    def set_expirationDate(self, expirationDate: datetime):
        self.__expirationDate = expirationDate

    def get_condition(self) -> productCondition:
        return self.__condition
    
    def set_condition(self, condition: productCondition):
        self.__condition = condition

    def get_price(self) -> float:
        return self.__price
    
    def set_price(self, price: float):
        self.__price = price
    


    

    


