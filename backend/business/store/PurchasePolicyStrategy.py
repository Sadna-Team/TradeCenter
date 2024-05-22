from abc import ABC, abstractmethod


# --------------- PurchasePolicyStrategy class ---------------#
class PurchasePolicyStrategy(ABC):
    # interface responsible for representing discounts in general. discountId unique verifier.
    def __init__(self, purchase_policy_id: int, store_id: int):
        self._purchase_policy_id = purchase_policy_id
        self._store_id = store_id

    @property
    def purchase_policy_id(self):
        return self._purchase_policy_id

    @abstractmethod
    def check_constraint(self, basket) -> bool:
        return True  # in the meantime


class LocationPurchasePolicy(PurchasePolicyStrategy):
    # not implemented at this version
    @abstractmethod
    def check_constraint(self, basket) -> bool:
        return super().check_constraint(basket)


class AgePurchasePolicy(PurchasePolicyStrategy):
    # not implemented at this version
    @abstractmethod
    def check_constraint(self, basket) -> bool:
        return super().check_constraint(basket)


class MaxBulkPurchasePolicy(PurchasePolicyStrategy):
    # not implemented at this version
    @abstractmethod
    def check_constraint(self, basket) -> bool:
        return super().check_constraint(basket)
