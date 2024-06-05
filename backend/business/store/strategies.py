from abc import ABC, abstractmethod
from typing import List, Callable, Dict
from backend.business.DTOs import UserDTO, CategoryDTO, ProductDTO


class PurchaseComposite(ABC):
    @abstractmethod
    def pass_filter(self) -> bool:
        pass
class AndFilter(PurchaseComposite):
    def __init__(self, filters: List[PurchaseComposite]):
        self.__filters: List[PurchaseComposite] = filters
        self.__name = "AndFilter"

    def __str__(self) -> str:
        return self.__name + "[ " + str(self.__filters) + " ]"

    def pass_filter(self) -> bool:
        for filter in self.__filters:
            if not filter.pass_filter():
                return False
        return True

class OrFilter(PurchaseComposite):
    def __init__(self, filters: List[PurchaseComposite]):
        self.__filters: List[PurchaseComposite] = filters
        self.__name = "OrFilter"

    def __str__(self) -> str:
        return self.__name + "[ " + str(self.__filters) + " ]"

    def pass_filter(self) -> bool:
        for sub in self.__filters:
            ans = sub.pass_filter()
            if ans:
                return True
        return False
    
class XorFilter(PurchaseComposite):
    def __init__(self, filters: List[PurchaseComposite]):
        self.__filters: List[PurchaseComposite] = filters
        self.__name = "XorFilter"

    def __str__(self) -> str:
        return self.__name + "[ " + str(self.__filters) + " ]"

    def pass_filter(self) -> bool:
        count = 0
        for filter in self.__filters:
            if filter.pass_filter():
                count += 1
        return count == 1

class NotFilter(PurchaseComposite):
    def __init__(self, filter: PurchaseComposite):
        self.__filter: PurchaseComposite = filter
        self.__name = "NotFilter"

    def __str__(self) -> str:
        return self.__name + "[ " + str(self.__filter) + " ]"

    def pass_filter(self) -> bool:
        return not self.__filter.pass_filter()

class UserFilter(PurchaseComposite):
    def __init__(self, user: UserDTO, predicate: Callable[[UserDTO], bool]):
        self.__user: UserDTO = user
        self.__predicate: Callable[[UserDTO], bool] = predicate
        self.__name = "UserFilter"

    def __str__(self) -> str:
        return self.__name
    
    def pass_filter(self) -> bool:
        return self.__predicate(self.__user)
    
class ProductFilter(PurchaseComposite):
    def __init__(self, products: Dict[ProductDTO, int], predicate: Callable[[Dict[ProductDTO, int]], bool]):
        self.__product: Dict[ProductDTO, int] = products
        self.__predicate: Callable[[Dict[ProductDTO, int]], bool] = predicate
        self.__name = "ProductFilter"

    def __str__(self) -> str:
        return self.__name

    def pass_filter(self) -> bool:
        return self.__predicate(self.__product)
    
