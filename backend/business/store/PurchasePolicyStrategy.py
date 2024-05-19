from abc import ABC, abstractmethod
from datetime import datetime


#--------------- Discount class ---------------#
class PurchasePolicyStrategy(ABC):
    # interface responsible for representing discounts in general. discountId unique verifier.
    def __init__(self, purchasePolicyId: int):
        self.purchasePolicyId = purchasePolicyId
      

    @abstractmethod
    def checkConstraint(self) -> bool:
        pass


class locationPurchasePolicy(PurchasePolicyStrategy):
    # not implemented at this version
    pass


class agePurchasePolicy(PurchasePolicyStrategy):
    # not implemented at this version
    pass

class maxBulkPurchasePolicy(PurchasePolicyStrategy):
    # not implemented at this version
    pass

