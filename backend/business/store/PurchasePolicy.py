from abc import ABC, abstractmethod


# -------------logging configuration----------------
import logging
from typing import Optional, Tuple, Dict

from backend.business.DTOs import BasketInformationForConstraintDTO
from backend.business.store.constraints import *
from backend.error_types import *
from backend.database import db
import re


import logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                     format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Purchase Policy Logger")

# ---------------------------------------------------
constraint_types = {
        'age': AgeConstraint,
        'location' : LocationConstraint,
        'time': TimeConstraint,
        'day_of_month': DayOfMonthConstraint,
        'day_of_week': DayOfWeekConstraint,
        'season': SeasonConstraint,
        'holidays_of_country': HolidaysOfCountryConstraint,
        'price_basket': PriceBasketConstraint,
        'price_product': PriceProductConstraint,
        'price_category': PriceCategoryConstraint,
        'weight_basket': WeightBasketConstraint,
        'weight_product': WeightProductConstraint,
        'weight_category': WeightCategoryConstraint,
        'amount_basket': AmountBasketConstraint,
        'amount_product': AmountProductConstraint,
        'amount_category': AmountCategoryConstraint,
        'and': AndConstraint,
        'or': OrConstraint,
        'xor': XorConstraint,
        'implies': ImpliesConstraint
    }


def parse_constraint_string(constraint_str):
    split_regex = r'[\s,]+'

    def convert_to_number(s):
        try:
            if '.' in s:
                return float(s)
            else:
                return int(s)
        except ValueError:
            return s

    def parse(s):
        tokens = re.sub(r'[()]', '', s).strip().split()
        return [convert_to_number(token) for token in tokens]

    clean_str = re.sub(r'\s+', ' ', constraint_str).strip()
    return parse(clean_str)

simple_components = [
    'age', 'time', 'location', 'day_of_month', 'day_of_week', 'season', 
    'holidays_of_country', 'price_basket', 'price_product', 'price_category', 
    'amount_basket', 'amount_product', 'amount_category', 
    'weight_category', 'weight_basket', 'weight_product'
]
composite_components = ['and', 'or', 'xor', 'implies']

def build_nested_array(parsed_composite, index=0):
    properties = []
    constraint_type = ''
    i = index
    while i < len(parsed_composite):
        if parsed_composite[i] in composite_components:
            left, new_index = build_nested_array(parsed_composite, i + 1)
            right, new_index = build_nested_array(parsed_composite, new_index + 1)
            return ([parsed_composite[i], left, right], new_index)
        elif parsed_composite[i] in simple_components:
            if constraint_type == '':
                constraint_type = parsed_composite[i]
            else:
                return ([constraint_type] + properties, i - 1)
        else:
            properties.append(parsed_composite[i])
        i += 1
    return ([constraint_type] + properties, len(parsed_composite))

def policy_predicate_builder(self, predicate_properties: Tuple) -> Optional[Constraint]:
        """
        * Parameters: predicate_properties
        * this function recursively creates a predicate for a policy
        * NOTE: the following are examples: (and,  
                                                (age, 18), 
                                                (or 
                                                    (location, {address: "bla", city: "bla", state: "bla", country: "bla", zip_code: "bla"}),
                                                    (time, 10, 00, 20, 00)
                                                ) 
                                            )
        * Returns: the predicated
        """
        if predicate_properties[0] not in self.constraint_types:
            logger.warning(f'[PolicyBuilder] invalid predicate type: {predicate_properties[0]}')
            raise DiscountAndConstraintsError(f'Invalid predicate type: {predicate_properties[0]}', DiscountAndConstraintsErrorTypes.predicate_creation_error)
        
        predicate_type = self.constraint_types[predicate_properties[0]]
    
        if not isinstance(predicate_type, Constraint):
            logger.warning(f'[PolicyBuilder] invalid predicate type: {predicate_type}')
            
        if predicate_type == AndConstraint or predicate_type == OrConstraint or predicate_type == XorConstraint or predicate_type == ImpliesConstraint:
            if len(predicate_properties) < 3 and not isinstance(predicate_properties[1], tuple) and not isinstance(predicate_properties[2], tuple):
                logger.warning('[PolicyBuilder] not enough sub predicates to create a composite predicate')
                raise DiscountAndConstraintsError('Not enough sub predicates to create a composite predicate', DiscountAndConstraintsErrorTypes.predicate_creation_error)
            predicate_left = self.assign_predicate_helper(predicate_properties[1])
            predicate_right = self.assign_predicate_helper(predicate_properties[2])
            return predicate_type(predicate_left, predicate_right)
        
        if predicate_type == AgeConstraint:
            if isinstance(predicate_properties[1], int):
                if predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] age is a negative value')
                    raise DiscountAndConstraintsError('Age is a negative value', DiscountAndConstraintsErrorTypes.invalid_age_limit)
                return predicate_type(predicate_properties[1])
            else:
                logger.warning('[PolicyBuilder] age is not an integer')
                raise DiscountAndConstraintsError('Age is not an integer', DiscountAndConstraintsErrorTypes.invalid_age_limit)
        elif predicate_type == LocationConstraint:
            if isinstance(predicate_properties[1], Dict):
                if 'address' not in predicate_properties[1] or 'city' not in predicate_properties[1] or 'state' not in predicate_properties[1] or 'country' not in predicate_properties[1] or 'zip_code' not in predicate_properties[1]:
                    logger.warning('[PolicyBuilder] location is missing fields')
                    raise DiscountAndConstraintsError('Location is missing fields', DiscountAndConstraintsErrorTypes.invalid_location)
                address = AddressDTO(predicate_properties[1]['address'], predicate_properties[1]['city'], predicate_properties[1]['state'], predicate_properties[1]['country'], predicate_properties[1]['zip_code'])
                return predicate_type(address)
            else:
                logger.warning('[PolicyBuilder] location is not a dictionary')
                raise DiscountAndConstraintsError('Location is not a dictionary', DiscountAndConstraintsErrorTypes.predicate_creation_error)
        elif predicate_type == TimeConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if predicate_properties[1] < 0 or predicate_properties[1] > 23 or predicate_properties[2] < 0 or predicate_properties[2] > 59 or predicate_properties[3] < 0 or predicate_properties[3] > 23 or predicate_properties[4] < 0 or predicate_properties[4] > 59:
                    logger.warning('[PolicyBuilder] time is not valid')
                    raise DiscountAndConstraintsError('Time is not valid', DiscountAndConstraintsErrorTypes.predicate_creation_error)
                starting_time = time(predicate_properties[1], predicate_properties[2],0)
                ending_time = time(predicate_properties[3], predicate_properties[4],0)
                if starting_time >= ending_time:
                    logger.warning('[PolicyBuilder] starting time is greater than ending time')
                    raise DiscountAndConstraintsError('Starting time is greater than ending time', DiscountAndConstraintsErrorTypes.invalid_time_constraint)
                return predicate_type(starting_time, ending_time)
            else:
                logger.warning('[PolicyBuilder] starting time or ending time is not a datetime.time')
                raise DiscountAndConstraintsError('Starting time or ending time is not a datetime.time', DiscountAndConstraintsErrorTypes.invalid_time_constraint)
        elif predicate_type == DayOfMonthConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int):
                if predicate_properties[1] < 1 or predicate_properties[1] > 31 or predicate_properties[2] < 1 or predicate_properties[2] > 31:
                    logger.warning('[PolicyBuilder] day of month is not valid')
                    raise DiscountAndConstraintsError('Day of month is not valid', DiscountAndConstraintsErrorTypes.invalid_day_of_month)
                return predicate_type(predicate_properties[1], predicate_properties[2])
            else:
                logger.warning('[PolicyBuilder] day of month is not an integer')
                raise DiscountAndConstraintsError('Day of month is not an integer', DiscountAndConstraintsErrorTypes.invalid_day_of_month)
        elif predicate_type == DayOfWeekConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int):
                if predicate_properties[1] < 1 or predicate_properties[1] > 7 or predicate_properties[2] < 1 or predicate_properties[2] > 7:
                    logger.warning('[PolicyBuilder] day of week is not valid')
                    raise DiscountAndConstraintsError('Day of week is not valid', DiscountAndConstraintsErrorTypes.invalid_day_of_week)
                return predicate_type(predicate_properties[1], predicate_properties[2])
            else:
                logger.warning('[PolicyBuilder] day of week is not an integer')
                raise DiscountAndConstraintsError('Day of week is not an integer', DiscountAndConstraintsErrorTypes.invalid_day_of_week)
        elif predicate_type == SeasonConstraint:
            if isinstance(predicate_properties[1], str):
                return predicate_type(predicate_properties[1])
            else:
                logger.warning('[PolicyBuilder] season is not an integer')
                raise DiscountAndConstraintsError('Season is not an integer', DiscountAndConstraintsErrorTypes.invalid_season)
        elif predicate_type == HolidaysOfCountryConstraint:
            if isinstance(predicate_properties[1], str):
                return predicate_type(predicate_properties[1])
            else:
                logger.warning('[PolicyBuilder] country is not a string')
                raise DiscountAndConstraintsError('Country is not a string', DiscountAndConstraintsErrorTypes.predicate_creation_error)
        elif predicate_type == PriceCategoryConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if (predicate_properties[1] != -1 and predicate_properties[2] > predicate_properties[1]) or predicate_properties[2] < 0:
                    logger.warning('[PolicyBuilder] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3])
            else:
                logger.warning('[PolicyBuilder] min price, max price or category id is not valid')
                raise DiscountAndConstraintsError('Min price, max price or category id is not valid', DiscountAndConstraintsErrorTypes.invalid_price)
        elif predicate_type == PriceProductConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3], predicate_properties[4])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3], predicate_properties[4])
            else:
                logger.warning('[PolicyBuilder] min price, max price, product id or store id is not valid')
                raise DiscountAndConstraintsError('Min price, max price, product id or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_price)
        elif predicate_type == PriceBasketConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3])
            else:
                logger.warning('[PolicyBuilder] min price, max price or store id is not valid')
                raise DiscountAndConstraintsError('Min price, max price or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_price)
        elif predicate_type == WeightCategoryConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3])
            else:
                logger.warning('[PolicyBuilder] min weight, max weight or category id is not valid')
                raise DiscountAndConstraintsError('Min weight, max weight or category id is not valid', DiscountAndConstraintsErrorTypes.invalid_weight)
        elif predicate_type == WeightProductConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3], predicate_properties[4])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3], predicate_properties[4])
            else:
                logger.warning('[PolicyBuilder] min weight, max weight, product id or store id is not valid')
                raise DiscountAndConstraintsError('Min weight, max weight, product id or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_weight)
        elif predicate_type == WeightBasketConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3])
            else:
                logger.warning('[PolicyBuilder] min weight, max weight or store id is not valid')
                raise DiscountAndConstraintsError('Min weight, max weight or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_weight)
        elif predicate_type == AmountCategoryConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min amount is a negative value')
                    raise DiscountAndConstraintsError('Min amount is a negative value', DiscountAndConstraintsErrorTypes.invalid_amount)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            else:
                logger.warning('[PolicyBuilder] min amount or category id is not valid')
                raise DiscountAndConstraintsError('Min amount or category id is not valid', DiscountAndConstraintsErrorTypes.invalid_amount)
        elif predicate_type == AmountProductConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min amount is a negative value')
                    raise DiscountAndConstraintsError('Min amount is a negative value', DiscountAndConstraintsErrorTypes.invalid_amount)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3], predicate_properties[4])
            else:
                logger.warning('[PolicyBuilder] min amount, product id or store id is not valid')
                raise DiscountAndConstraintsError('Min amount, product id or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_amount)
        elif predicate_type == AmountBasketConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if predicate_properties[1] < 0:
                    logger.warning('[PolicyBuilder] min amount is a negative value')
                    raise DiscountAndConstraintsError('Min amount is a negative value', DiscountAndConstraintsErrorTypes.invalid_amount)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            else:
                logger.warning('[PolicyBuilder] min amount or store id is not valid')
                raise DiscountAndConstraintsError('Min amount or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_amount)
        return None

# --------------- PurchasePolicyStrategy class ---------------#
class PurchasePolicy(db.Model):
    __tablename__ = 'purchase_policies'

    purchase_policy_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_id = db.Column(db.Integer)
    _policy_name = db.Column(db.String(100), nullable=False)
    _predicate = db.Column(db.String(250), nullable=True)

    type = db.Column(db.String(50), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('purchase_policy_id'),
    )

    __mapper_args__ = {
        'polymorphic_identity': 'purchase_policy',
        'polymorphic_on': 'type'
    }

    # interface responsible for representing discounts in general. discountId unique verifier.
    def __init__(self, store_id: int, policy_name: str, predicate: Optional[Constraint] = None):
        if policy_name is None or policy_name == "":
            raise PurchaseError("invalid policy name", PurchaseErrorTypes.invalid_name)
        
        self.store_id = store_id
        self._policy_name = policy_name
        self._predicate = predicate
        logger.info("[PurchasePolicy] Purchase Policy with id: " + str(self.purchase_policy_id) + " created successfully!")

    
    @property
    def policy_name(self):
        return self._policy_name
    
    @property
    def policy_id(self):
        return self.purchase_policy_id
    
    @property
    def predicate(self):
        if self._predicate is None or self._predicate == "":
            return None
        parsed = parse_constraint_string(self._predicate)
        predicate_builder = None
        if parsed[0] in ['and', 'or', 'xor', 'implies']:
            predicate_builder = build_nested_array(parsed)
            logger.info(f'[PurchasePolicy] composite predicate {predicate_builder}')
            return self.policy_predicate_builder(predicate_builder)
        else:
            return constraint_types[parsed[0]](*parsed[1:])

    @abstractmethod
    def check_constraint(self, basket: BasketInformationForConstraintDTO) -> bool:
        pass
    
    def set_predicate(self, predicate: Constraint):
        if predicate is None:
            self._predicate = None
        else:
            self._predicate = predicate.get_constraint_string()
        db.session.commit()

    @abstractmethod
    def get_policy_info_as_dict(self) -> dict:
        pass
# --------------- ProductPolicy class ---------------#
class ProductSpecificPurchasePolicy(PurchasePolicy):
    __tablename__ = 'product_specific_policies'

    purchase_policy_id = db.Column(db.Integer, db.ForeignKey('purchase_policies.purchase_policy_id'), primary_key=True)
    _product_id = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'product_specific_policy'
    }

    __table_args__ = (
        db.PrimaryKeyConstraint('purchase_policy_id'),
    )

    def __init__(self, store_id: int, policy_name: str, product_id: int, predicate: Optional[str] = None):
        super().__init__(store_id, policy_name, predicate)
        self._product_id = product_id
        logger.info("[ProductSpecificPurchasePolicy] Product Specific Purchase Policy created successfully!")


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

    def get_policy_info_as_dict(self) -> dict:
        return {
            "policy_type": "productSpecificPolicy",
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "product_id": self.product_id,
            "store_id": self.store_id,
            "predicate": self.predicate.get_constraint_info_as_string() if self.predicate is not None else "None"
        }
    
# --------------- CategoryPolicy class ---------------#
class CategorySpecificPurchasePolicy(PurchasePolicy):
    __tablename__ = 'category_specific_policies'

    purchase_policy_id = db.Column(db.Integer, db.ForeignKey('purchase_policies.purchase_policy_id'), primary_key=True)
    _category_id = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'category_specific_policy',
    }

    def __init__(self, store_id: int, policy_name: str, category_id: int, predicate: Optional[Constraint] = None):
        super().__init__(store_id, policy_name, predicate)
        self._category_id = category_id
        logger.info("[CategorySpecificPurchasePolicy] Category Specific Purchase Policy created successfully!")

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
            if category.category_id == self._category_id:
                return self._predicate.is_satisfied(basket)

        return True
    
    def get_policy_info_as_dict(self) -> dict:
        return {
            "policy_type": "categorySpecificPolicy",
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "store_id": self.store_id,
            "category_id": self._category_id,
            "predicate": self.predicate.get_constraint_info_as_string() if self.predicate is not None else "None"
        }
    

# --------------- StorePolicy class ---------------#
class BasketSpecificPurchasePolicy(PurchasePolicy):
    __tablename__ = 'basket_specific_policies'

    purchase_policy_id = db.Column(db.Integer, db.ForeignKey('purchase_policies.purchase_policy_id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'basket_specific_policy',
    }

    def __init__(self, store_id: int, policy_name: str, predicate: Optional[Constraint] = None):
        super().__init__(store_id, policy_name, predicate)
        logger.info("[StoreSpecificPurchasePolicy] Store Specific Purchase Policy created successfully!")

    def check_constraint(self, basket: BasketInformationForConstraintDTO) -> bool:
        if self._predicate is None:
            return True
        
        if self.store_id != basket.store_id:
            return True
        
        return self._predicate.is_satisfied(basket)

    def get_policy_info_as_dict(self) -> dict:
        return {
            "policy_type": "basketSpecificPolicy",
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "store_id": self.store_id,
            "predicate": self.predicate.get_constraint_info_as_string() if self.predicate is not None else "None"
        }
    

# --------------- CompositePolicy class ---------------#
class AndPurchasePolicy(PurchasePolicy):
    __tablename__ = 'and_policies'

    purchase_policy_id = db.Column(db.Integer, db.ForeignKey('purchase_policies.purchase_policy_id'), primary_key=True)
    # policy_left_id = db.Column(db.Integer, db.ForeignKey('purchase_policies.purchase_policy_id'))
    # policy_right_id = db.Column(db.Integer, db.ForeignKey('purchase_policies.purchase_policy_id'))

    # policy_left = db.relationship("PurchasePolicy", foreign_keys=[policy_left_id], backref=db.backref('parent_left', remote_side=[purchase_policy_id]))
    # policy_right = db.relationship("PurchasePolicy", foreign_keys=[policy_right_id], backref=db.backref('parent_right', remote_side=[purchase_policy_id]))

    policy_left_id = db.Column(db.Integer, nullable=False)
    policy_right_id = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'and_policy',
    }

    def __init__(self, store_id: int, policy_name: str, policy_left: PurchasePolicy, policy_right: PurchasePolicy, predicate: Optional[Constraint] = None):
        super().__init__(store_id, policy_name, None)
        self.policy_left = policy_left
        self.policy_right = policy_right
        logger.info("[AndPurchasePolicy] And Purchase Policy created successfully!")
    

    def check_constraint(self, basket: BasketInformationForConstraintDTO) -> bool:
        if self.store_id != basket.store_id:
            return True
        
        
        return self.policy_left.check_constraint(basket) and self.policy_right.check_constraint(basket)


    def set_predicate(self, predicate: Constraint):
        logger.info("[AndPurchasePolicy] Unable to set predicate for AndPurchasePolicy")
        pass 
    
    def get_policy_info_as_dict(self) -> dict:
        policy_left = self.policy_left.get_policy_info_as_dict()
        policy_right = self.policy_right.get_policy_info_as_dict()
        return {
            "policy_type": "andPolicy",
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "store_id": self.store_id,
            "policy_left": policy_left,
            "policy_right": policy_right,
        }

# --------------- CompositePolicy class ---------------#
class OrPurchasePolicy(PurchasePolicy):
    __tablename__ = 'or_policies'

    purchase_policy_id = db.Column(db.Integer, db.ForeignKey('purchase_policies.purchase_policy_id'), primary_key=True)
    # policy_left_id = db.Column(db.Integer, db.ForeignKey('purchase_policies.purchase_policy_id'))
    # policy_right_id = db.Column(db.Integer, db.ForeignKey('purchase_policies.purchase_policy_id'))

    # policy_left = db.relationship("PurchasePolicy", foreign_keys=[policy_left_id], backref=db.backref('parent_left', remote_side=[purchase_policy_id]))
    # policy_right = db.relationship("PurchasePolicy", foreign_keys=[policy_right_id], backref=db.backref('parent_right', remote_side=[purchase_policy_id]))

    policy_left_id = db.Column(db.Integer, nullable=False)
    policy_right_id = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'or_policy',
    }

    def __init__(self, store_id: int, policy_name: str, policy_left: PurchasePolicy, policy_right: PurchasePolicy, predicate: Optional[Constraint] = None):
        super().__init__(store_id, policy_name, None)
        self.policy_left = policy_left
        self.policy_right = policy_right
        logger.info("[OrPurchasePolicy] Or Purchase Policy created successfully!")
    

    def check_constraint(self, basket: BasketInformationForConstraintDTO) -> bool:
        if self.store_id != basket.store_id:
            return True
        
        return self.policy_left.check_constraint(basket) or self.policy_right.check_constraint(basket)


    def set_predicate(self, predicate: Constraint):
        logger.info("[OrPurchasePolicy] Unable to set predicate for OrPurchasePolicy")
        pass
    
    def get_policy_info_as_dict(self) -> dict:
        policy_left = self.policy_left.get_policy_info_as_dict()
        policy_right = self.policy_right.get_policy_info_as_dict()
        return {
            "policy_type": "orPolicy",
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "store_id": self.store_id,
            "policy_left": policy_left,
            "policy_right": policy_right,
        }

# --------------- CompositePolicy class ---------------#
class ConditioningPurchasePolicy(PurchasePolicy):
    __tablename__ = 'conditioning_policies'

    purchase_policy_id = db.Column(db.Integer, db.ForeignKey('purchase_policies.purchase_policy_id'), primary_key=True)
    # policy_left_id = db.Column(db.Integer, db.ForeignKey('purchase_policies.purchase_policy_id'))
    # policy_right_id = db.Column(db.Integer, db.ForeignKey('purchase_policies.purchase_policy_id'))

    # policy_left = db.relationship("PurchasePolicy", foreign_keys=[policy_left_id], backref=db.backref('parent_left', remote_side=[purchase_policy_id]))
    # policy_right = db.relationship("PurchasePolicy", foreign_keys=[policy_right_id], backref=db.backref('parent_right', remote_side=[purchase_policy_id]))

    policy_left_id = db.Column(db.Integer, nullable=False)
    policy_right_id = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'conditioning_policy',
    }
    
    def __init__(self, store_id: int, policy_name: str, policy_left: PurchasePolicy, policy_right: PurchasePolicy, predicate: Optional[Constraint] = None):
        super().__init__(store_id, policy_name, None)
        self.policy_left = policy_left
        self.policy_right = policy_right
        logger.info("[ConditioningPurchasePolicy] Conditioning Purchase Policy created successfully!")
    

    def check_constraint(self, basket: BasketInformationForConstraintDTO) -> bool:
        if self.store_id != basket.store_id:
            return True
        
        if self.policy_left.check_constraint(basket):
            return self.policy_right.check_constraint(basket)
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
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "store_id": self.store_id,
            "policy_left": policy_left,
            "policy_right": policy_right,
        }