from abc import ABC, abstractmethod
from datetime import datetime


#--------------- PurchasePolicyStrategy class ---------------#
class PurchasePolicyStrategy(ABC):
    # interface responsible for representing discounts in general. discountId unique verifier.
    def __init__(self, purchasePolicyId: int, storeId: int):
        self.purchasePolicyId = purchasePolicyId
        self.storeId = storeId
      

    @abstractmethod
    def checkConstraint(self) -> bool:
        return True #in the meantime


class locationPurchasePolicy(PurchasePolicyStrategy):
    # not implemented at this version
    pass


class agePurchasePolicy(PurchasePolicyStrategy):
    # not implemented at this version
    pass

class maxBulkPurchasePolicy(PurchasePolicyStrategy):
    # not implemented at this version
    pass

