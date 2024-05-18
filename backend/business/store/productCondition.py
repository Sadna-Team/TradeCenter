from enum import Enum

# enumeration for product condition
class productCondition(Enum):
    NEW = 1
    USED = 2

productCondition = Enum('productCondition', ['NEW', 'USED'])