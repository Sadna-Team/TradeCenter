from enum import Enum


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