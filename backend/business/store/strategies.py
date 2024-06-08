from abc import ABC, abstractmethod
from typing import List, Callable, Dict
from backend.business.DTOs import PurchaseUserDTO, CategoryDTO, ProductDTO

# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')

# ---------------------------------------------------


class PurchaseComposite(ABC):
    @abstractmethod
    def pass_filter(self) -> bool:
        pass
    
class AndFilter(PurchaseComposite):
    def __init__(self, filters: List[PurchaseComposite]):
        self.__filters: List[PurchaseComposite] = filters
        self.__name = "AndFilter"
        logger.info("[AndFilter] And Filter created successfully!")
        

    def __str__(self) -> str:
        return self.__name + "[ " + str(self.__filters) + " ]"

    def pass_filter(self) -> bool:
        for filter in self.__filters:
            if not filter.pass_filter():
                logger.info("[AndFilter] And Filter failed!")
                return False
        return True

class OrFilter(PurchaseComposite):
    def __init__(self, filters: List[PurchaseComposite]):
        self.__filters: List[PurchaseComposite] = filters
        self.__name = "OrFilter"
        logger.info("[OrFilter] Or Filter created successfully!")

    def __str__(self) -> str:
        return self.__name + "[ " + str(self.__filters) + " ]"

    def pass_filter(self) -> bool:
        for sub in self.__filters:
            ans = sub.pass_filter()
            if ans:
                return True
        logger.info("[OrFilter] Or Filter failed!")
        return False
    
class XorFilter(PurchaseComposite):
    def __init__(self, filters: List[PurchaseComposite]):
        self.__filters: List[PurchaseComposite] = filters
        self.__name = "XorFilter"
        logger.info("[XorFilter] Xor Filter created successfully!")

    def __str__(self) -> str:
        return self.__name + "[ " + str(self.__filters) + " ]"

    def pass_filter(self) -> bool:
        count = 0
        for filter in self.__filters:
            if filter.pass_filter():
                count += 1
        if count != 1:
            logger.info("[XorFilter] Xor Filter failed!")
        return count == 1

class NotFilter(PurchaseComposite):
    def __init__(self, filter: PurchaseComposite):
        self.__filter: PurchaseComposite = filter
        self.__name = "NotFilter"
        logger.info("[NotFilter] Not Filter created successfully!")

    def __str__(self) -> str:
        return self.__name + "[ " + str(self.__filter) + " ]"

    def pass_filter(self) -> bool:
        return not self.__filter.pass_filter()

class UserFilter(PurchaseComposite):
    def __init__(self, user: PurchaseUserDTO, predicate: Callable[[PurchaseUserDTO], bool]):
        self.__user: PurchaseUserDTO = user
        self.__predicate: Callable[[PurchaseUserDTO], bool] = predicate
        self.__name = "UserFilter"
        logger.info("[UserFilter] User Filter created successfully!")

    def __str__(self) -> str:
        return self.__name
    
    def pass_filter(self) -> bool:
        return self.__predicate(self.__user)
    
class ProductFilter(PurchaseComposite):
    def __init__(self, products: Dict[ProductDTO, int], predicate: Callable[[Dict[ProductDTO, int]], bool]):
        self.__product: Dict[ProductDTO, int] = products
        self.__predicate: Callable[[Dict[ProductDTO, int]], bool] = predicate
        self.__name = "ProductFilter"
        logger.info("[ProductFilter] Product Filter created successfully!")


    def __str__(self) -> str:
        return self.__name

    def pass_filter(self) -> bool:
        return self.__predicate(self.__product)
    
