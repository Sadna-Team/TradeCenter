from abc import ABC, abstractmethod


# -------------logging configuration----------------
import logging
from typing import Optional

from backend.business.DTOs import BasketInformationForConstraintDTO
from backend.business.store.constraints import Constraint
from backend.error_types import *


logger = logging.getLogger('myapp')

# ---------------------------------------------------

# --------------- PurchasePolicyStrategy class ---------------#
class PurchasePolicy(ABC):
    # interface responsible for representing discounts in general. discountId unique verifier.
    def __init__(self, purchase_policy_id: int, store_id: int, policy_name: str, predicate: Optional[Constraint] = None):
        if policy_name is None or policy_name == "":
            raise PurchaseError("invalid policy name", PurchaseErrorTypes.invalid_name)
        
        self._purchase_policy_id = purchase_policy_id
        self._store_id = store_id
        self._policy_name = policy_name
        self._predicate = predicate
        logger.info("[PurchasePolicy] Purchase Policy with id: " + str(purchase_policy_id) + " created successfully!")


    @property
    def purchase_policy_id(self):
        return self._purchase_policy_id
    
    @property
    def store_id(self):
        return self._store_id
    
    @property
    def policy_name(self):
        return self._policy_name
    
    @property
    def predicate(self):
        return self._predicate

    @abstractmethod
    def check_constraint(self, basket: BasketInformationForConstraintDTO) -> bool:
        pass

    @abstractmethod
    def set_predicate(self, predicate: Constraint):
        pass

    @abstractmethod
    def get_policy_info_as_dict(self) -> dict:
        pass
# --------------- ProductPolicy class ---------------#
class ProductSpecificPurchasePolicy(PurchasePolicy):
    def __init__(self, purchase_policy_id: int, store_id: int, policy_name: str, product_id: int, predicate: Optional[Constraint] = None):
        super().__init__(purchase_policy_id, store_id, policy_name, predicate)
        self._product_id = product_id
        logger.info("[ProductSpecificPurchasePolicy] Product Specific Purchase Policy with id: " + str(purchase_policy_id) + " created successfully!")

    @property
    def product_id(self):
        return self._product_id

    def check_constraint(self, basket: BasketInformationForConstraintDTO) -> bool:
        if self._predicate is None:
            return True

        #predicate not affecting the store        
        if self.store_id != basket.store_id:
            return True
        
        return self._predicate.is_satisfied(basket)
    
    def set_predicate(self, predicate: Constraint):
        self._predicate = predicate

    def get_policy_info_as_dict(self) -> dict:
        return {
            "policy_type": "productSpecificPolicy",
            "policy_id": self.purchase_policy_id,
            "policy_name": self.policy_name,
            "product_id": self.product_id,
            "store_id": self.store_id,
            "predicate": self.predicate.get_constraint_info_as_string() if self.predicate is not None else "None"
        }
    
# --------------- CategoryPolicy class ---------------#
class CategorySpecificPurchasePolicy(PurchasePolicy):
    def __init__(self, purchase_policy_id: int, store_id: int, policy_name: str, category_id: int, predicate: Optional[Constraint] = None):
        super().__init__(purchase_policy_id, store_id, policy_name, predicate)
        self._category_id = category_id
        logger.info("[CategorySpecificPurchasePolicy] Category Specific Purchase Policy with id: " + str(purchase_policy_id) + " created successfully!")

    @property
    def category_id(self):
        return self._category_id

    def check_constraint(self, basket: BasketInformationForConstraintDTO) -> bool:
        if self._predicate is None:
            return True
        
        if self.store_id != basket.store_id:
            return True

        #we assume that the category is not a subcategory of a category in the basket        
        for category in basket.categories:
            if category.category_id == self.category_id:
                return self._predicate.is_satisfied(basket)

        return True
    

    def set_predicate(self, predicate: Constraint):
        self._predicate = predicate
    
    def get_policy_info_as_dict(self) -> dict:
        return {
            "policy_type": "categorySpecificPolicy",
            "policy_id": self.purchase_policy_id,
            "policy_name": self.policy_name,
            "store_id": self.store_id,
            "category_id": self.category_id,
            "predicate": self.predicate.get_constraint_info_as_string() if self.predicate is not None else "None"
        }
    

# --------------- StorePolicy class ---------------#
class BasketSpecificPurchasePolicy(PurchasePolicy):
    def __init__(self, purchase_policy_id: int, store_id: int, policy_name: str, predicate: Optional[Constraint] = None):
        super().__init__(purchase_policy_id, store_id, policy_name, predicate)
        logger.info("[StoreSpecificPurchasePolicy] Store Specific Purchase Policy with id: " + str(purchase_policy_id) + " created successfully!")

    def check_constraint(self, basket: BasketInformationForConstraintDTO) -> bool:
        if self._predicate is None:
            return True
        
        if self.store_id != basket.store_id:
            return True
        
        return self._predicate.is_satisfied(basket)
    
    def set_predicate(self, predicate: Constraint):
        self._predicate = predicate


    def get_policy_info_as_dict(self) -> dict:
        return {
            "policy_type": "basketSpecificPolicy",
            "policy_id": self.purchase_policy_id,
            "policy_name": self.policy_name,
            "store_id": self.store_id,
            "predicate": self.predicate.get_constraint_info_as_string() if self.predicate is not None else "None"
        }
    

# --------------- CompositePolicy class ---------------#
class AndPurchasePolicy(PurchasePolicy):
    def __init__(self, purchase_policy_id: int, store_id: int, policy_name: str, policy_left: PurchasePolicy, policy_right: PurchasePolicy, predicate: Optional[Constraint] = None):
        super().__init__(purchase_policy_id, store_id, policy_name, None)
        self._policy_left = policy_left
        self._policy_right = policy_right
        logger.info("[AndPurchasePolicy] And Purchase Policy with id: " + str(purchase_policy_id) + " created successfully!")

    @property
    def policy_left(self):
        return self._policy_left
    
    @property
    def policy_right(self):
        return self._policy_right
    

    def check_constraint(self, basket: BasketInformationForConstraintDTO) -> bool:
        if self.store_id != basket.store_id:
            return True
        
        return self._policy_left.check_constraint(basket) and self._policy_right.check_constraint(basket)



    def set_predicate(self, predicate: Constraint):
        logger.info("[AndPurchasePolicy] Unable to set predicate for AndPurchasePolicy")
        pass 
    
    def get_policy_info_as_dict(self) -> dict:
        policy_left = self.policy_left.get_policy_info_as_dict()
        policy_right = self.policy_right.get_policy_info_as_dict()
        return {
            "policy_type": "andPolicy",
            "policy_id": self.purchase_policy_id,
            "policy_name": self.policy_name,
            "store_id": self.store_id,
            "policy_left": policy_left,
            "policy_right": policy_right,
        }

# --------------- CompositePolicy class ---------------#
class OrPurchasePolicy(PurchasePolicy):
    def __init__(self, purchase_policy_id: int, store_id: int, policy_name: str, policy_left: PurchasePolicy, policy_right: PurchasePolicy, predicate: Optional[Constraint] = None):
        super().__init__(purchase_policy_id, store_id, policy_name, None)
        self._policy_left = policy_left
        self._policy_right = policy_right
        logger.info("[OrPurchasePolicy] Or Purchase Policy with id: " + str(purchase_policy_id) + " created successfully!")

    @property
    def policy_left(self):
        return self._policy_left
    
    @property
    def policy_right(self):
        return self._policy_right
    

    def check_constraint(self, basket: BasketInformationForConstraintDTO) -> bool:
        if self.store_id != basket.store_id:
            return True
        
        return self._policy_left.check_constraint(basket) or self._policy_right.check_constraint(basket)


    def set_predicate(self, predicate: Constraint):
        logger.info("[OrPurchasePolicy] Unable to set predicate for OrPurchasePolicy")
        pass
    
    def get_policy_info_as_dict(self) -> dict:
        policy_left = self.policy_left.get_policy_info_as_dict()
        policy_right = self.policy_right.get_policy_info_as_dict()
        return {
            "policy_type": "orPolicy",
            "policy_id": self.purchase_policy_id,
            "policy_name": self.policy_name,
            "store_id": self.store_id,
            "policy_left": policy_left,
            "policy_right": policy_right,
        }

# --------------- CompositePolicy class ---------------#
class ConditioningPurchasePolicy(PurchasePolicy):
    def __init__(self, purchase_policy_id: int, store_id: int, policy_name: str, policy_left: PurchasePolicy, policy_right: PurchasePolicy, predicate: Optional[Constraint] = None):
        super().__init__(purchase_policy_id, store_id, policy_name, None)
        self._policy_left = policy_left
        self._policy_right = policy_right
        logger.info("[ConditioningPurchasePolicy] Conditioning Purchase Policy with id: " + str(purchase_policy_id) + " created successfully!")

    @property
    def policy_left(self):
        return self._policy_left
    
    @property
    def policy_right(self):
        return self._policy_right
    

    def check_constraint(self, basket: BasketInformationForConstraintDTO) -> bool:
        if self.store_id != basket.store_id:
            return True
        
        if self._policy_left.check_constraint(basket):
            return self._policy_right.check_constraint(basket)
        else:
            return True


    def set_predicate(self, predicate: Constraint):
        logger.info("[ConditioningPurchasePolicy] Unable to set predicate for ConditioningPurchasePolicy")
        pass

    def get_policy_info_as_dict(self) -> dict:
        policy_left = self.policy_left.get_policy_info_as_dict()
        policy_right = self.policy_right.get_policy_info_as_dict()
        return {
            "policy_type": "conditionalPolicy",
            "policy_id": self.purchase_policy_id,
            "policy_name": self.policy_name,
            "store_id": self.store_id,
            "policy_left": policy_left,
            "policy_right": policy_right,
        }
