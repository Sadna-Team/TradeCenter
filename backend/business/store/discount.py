# --------------- imports ---------------#
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Optional, Tuple

from backend.business.DTOs import BasketInformationForConstraintDTO, CategoryDTO
from backend.business.store.constraints import *
from backend.error_types import *
from backend.database import db
import re


# -------------logging configuration----------------
import logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Discount Logger')
# ---------------------------------------------------
DATE_FORMAT = '%Y-%m-%d'

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

def discount_predicate_builder(self, predicate_properties: Tuple) -> Optional[Constraint]:
        """
        * Parameters: predicate_properties
        * this function recursively creates a predicate for a discount
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
            logger.warning(f'[DiscountBuilder] invalid predicate type: {predicate_properties[0]}')
            raise DiscountAndConstraintsError(f'Invalid predicate type: {predicate_properties[0]}', DiscountAndConstraintsErrorTypes.predicate_creation_error)
        
        predicate_type = self.constraint_types[predicate_properties[0]]
    
        if not isinstance(predicate_type, Constraint):
            logger.warning(f'[DiscountBuilder] invalid predicate type: {predicate_type}')
            
        if predicate_type == AndConstraint or predicate_type == OrConstraint or predicate_type == XorConstraint or predicate_type == ImpliesConstraint:
            if len(predicate_properties) < 3 and not isinstance(predicate_properties[1], tuple) and not isinstance(predicate_properties[2], tuple):
                logger.warning('[DiscountBuilder] not enough sub predicates to create a composite predicate')
                raise DiscountAndConstraintsError('Not enough sub predicates to create a composite predicate', DiscountAndConstraintsErrorTypes.predicate_creation_error)
            predicate_left = self.assign_predicate_helper(predicate_properties[1])
            predicate_right = self.assign_predicate_helper(predicate_properties[2])
            return predicate_type(predicate_left, predicate_right)
        
        if predicate_type == AgeConstraint:
            if isinstance(predicate_properties[1], int):
                if predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] age is a negative value')
                    raise DiscountAndConstraintsError('Age is a negative value', DiscountAndConstraintsErrorTypes.invalid_age_limit)
                return predicate_type(predicate_properties[1])
            else:
                logger.warning('[DiscountBuilder] age is not an integer')
                raise DiscountAndConstraintsError('Age is not an integer', DiscountAndConstraintsErrorTypes.invalid_age_limit)
        elif predicate_type == LocationConstraint:
            if isinstance(predicate_properties[1], Dict):
                if 'address' not in predicate_properties[1] or 'city' not in predicate_properties[1] or 'state' not in predicate_properties[1] or 'country' not in predicate_properties[1] or 'zip_code' not in predicate_properties[1]:
                    logger.warning('[DiscountBuilder] location is missing fields')
                    raise DiscountAndConstraintsError('Location is missing fields', DiscountAndConstraintsErrorTypes.invalid_location)
                address = AddressDTO(predicate_properties[1]['address'], predicate_properties[1]['city'], predicate_properties[1]['state'], predicate_properties[1]['country'], predicate_properties[1]['zip_code'])
                return predicate_type(address)
            else:
                logger.warning('[DiscountBuilder] location is not a dictionary')
                raise DiscountAndConstraintsError('Location is not a dictionary', DiscountAndConstraintsErrorTypes.predicate_creation_error)
        elif predicate_type == TimeConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if predicate_properties[1] < 0 or predicate_properties[1] > 23 or predicate_properties[2] < 0 or predicate_properties[2] > 59 or predicate_properties[3] < 0 or predicate_properties[3] > 23 or predicate_properties[4] < 0 or predicate_properties[4] > 59:
                    logger.warning('[DiscountBuilder] time is not valid')
                    raise DiscountAndConstraintsError('Time is not valid', DiscountAndConstraintsErrorTypes.predicate_creation_error)
                starting_time = time(predicate_properties[1], predicate_properties[2],0)
                ending_time = time(predicate_properties[3], predicate_properties[4],0)
                if starting_time >= ending_time:
                    logger.warning('[DiscountBuilder] starting time is greater than ending time')
                    raise DiscountAndConstraintsError('Starting time is greater than ending time', DiscountAndConstraintsErrorTypes.invalid_time_constraint)
                return predicate_type(starting_time, ending_time)
            else:
                logger.warning('[DiscountBuilder] starting time or ending time is not a datetime.time')
                raise DiscountAndConstraintsError('Starting time or ending time is not a datetime.time', DiscountAndConstraintsErrorTypes.invalid_time_constraint)
        elif predicate_type == DayOfMonthConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int):
                if predicate_properties[1] < 1 or predicate_properties[1] > 31 or predicate_properties[2] < 1 or predicate_properties[2] > 31:
                    logger.warning('[DiscountBuilder] day of month is not valid')
                    raise DiscountAndConstraintsError('Day of month is not valid', DiscountAndConstraintsErrorTypes.invalid_day_of_month)
                return predicate_type(predicate_properties[1], predicate_properties[2])
            else:
                logger.warning('[DiscountBuilder] day of month is not an integer')
                raise DiscountAndConstraintsError('Day of month is not an integer', DiscountAndConstraintsErrorTypes.invalid_day_of_month)
        elif predicate_type == DayOfWeekConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int):
                if predicate_properties[1] < 1 or predicate_properties[1] > 7 or predicate_properties[2] < 1 or predicate_properties[2] > 7:
                    logger.warning('[DiscountBuilder] day of week is not valid')
                    raise DiscountAndConstraintsError('Day of week is not valid', DiscountAndConstraintsErrorTypes.invalid_day_of_week)
                return predicate_type(predicate_properties[1], predicate_properties[2])
            else:
                logger.warning('[DiscountBuilder] day of week is not an integer')
                raise DiscountAndConstraintsError('Day of week is not an integer', DiscountAndConstraintsErrorTypes.invalid_day_of_week)
        elif predicate_type == SeasonConstraint:
            if isinstance(predicate_properties[1], str):
                return predicate_type(predicate_properties[1])
            else:
                logger.warning('[DiscountBuilder] season is not an integer')
                raise DiscountAndConstraintsError('Season is not an integer', DiscountAndConstraintsErrorTypes.invalid_season)
        elif predicate_type == HolidaysOfCountryConstraint:
            if isinstance(predicate_properties[1], str):
                return predicate_type(predicate_properties[1])
            else:
                logger.warning('[DiscountBuilder] country is not a string')
                raise DiscountAndConstraintsError('Country is not a string', DiscountAndConstraintsErrorTypes.predicate_creation_error)
        elif predicate_type == PriceCategoryConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if (predicate_properties[1] != -1 and predicate_properties[2] > predicate_properties[1]) or predicate_properties[2] < 0:
                    logger.warning('[DiscountBuilder] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3])
            else:
                logger.warning('[DiscountBuilder] min price, max price or category id is not valid')
                raise DiscountAndConstraintsError('Min price, max price or category id is not valid', DiscountAndConstraintsErrorTypes.invalid_price)
        elif predicate_type == PriceProductConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3], predicate_properties[4])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3], predicate_properties[4])
            else:
                logger.warning('[DiscountBuilder] min price, max price, product id or store id is not valid')
                raise DiscountAndConstraintsError('Min price, max price, product id or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_price)
        elif predicate_type == PriceBasketConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3])
            else:
                logger.warning('[DiscountBuilder] min price, max price or store id is not valid')
                raise DiscountAndConstraintsError('Min price, max price or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_price)
        elif predicate_type == WeightCategoryConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3])
            else:
                logger.warning('[DiscountBuilder] min weight, max weight or category id is not valid')
                raise DiscountAndConstraintsError('Min weight, max weight or category id is not valid', DiscountAndConstraintsErrorTypes.invalid_weight)
        elif predicate_type == WeightProductConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3], predicate_properties[4])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3], predicate_properties[4])
            else:
                logger.warning('[DiscountBuilder] min weight, max weight, product id or store id is not valid')
                raise DiscountAndConstraintsError('Min weight, max weight, product id or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_weight)
        elif predicate_type == WeightBasketConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3])
            else:
                logger.warning('[DiscountBuilder] min weight, max weight or store id is not valid')
                raise DiscountAndConstraintsError('Min weight, max weight or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_weight)
        elif predicate_type == AmountCategoryConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min amount is a negative value')
                    raise DiscountAndConstraintsError('Min amount is a negative value', DiscountAndConstraintsErrorTypes.invalid_amount)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            else:
                logger.warning('[DiscountBuilder] min amount or category id is not valid')
                raise DiscountAndConstraintsError('Min amount or category id is not valid', DiscountAndConstraintsErrorTypes.invalid_amount)
        elif predicate_type == AmountProductConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min amount is a negative value')
                    raise DiscountAndConstraintsError('Min amount is a negative value', DiscountAndConstraintsErrorTypes.invalid_amount)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3], predicate_properties[4])
            else:
                logger.warning('[DiscountBuilder] min amount, product id or store id is not valid')
                raise DiscountAndConstraintsError('Min amount, product id or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_amount)
        elif predicate_type == AmountBasketConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if predicate_properties[1] < 0:
                    logger.warning('[DiscountBuilder] min amount is a negative value')
                    raise DiscountAndConstraintsError('Min amount is a negative value', DiscountAndConstraintsErrorTypes.invalid_amount)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            else:
                logger.warning('[DiscountBuilder] min amount or store id is not valid')
                raise DiscountAndConstraintsError('Min amount or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_amount)
        return None


# --------------- Discount base ---------------#
class Discount(db.Model):
    __tablename__ = 'discounts'

    discount_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'), nullable=False)
    _discount_description = db.Column(db.String(100), nullable=True)
    _starting_date = db.Column(db.DateTime, nullable=False)
    _ending_date = db.Column(db.DateTime, nullable=False)
    _percentage = db.Column(db.Float, nullable=False)
    _predicate = db.Column(db.String(250), nullable=True)

    discount_type = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'discount',
        'polymorphic_on': 'discount_type'
    }

    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, predicate: Optional[Constraint]):
        if isinstance(starting_date,str):
            starting_date = datetime.strptime(starting_date, DATE_FORMAT)
        if isinstance(ending_date,str):
            ending_date = datetime.strptime(ending_date, DATE_FORMAT)
        if starting_date > ending_date:
            logger.error("[Discount] Invalid dates")
            raise DiscountAndConstraintsError("invalid dates", DiscountAndConstraintsErrorTypes.invalid_date)
        if (percentage < 0 or percentage > 1) and percentage!=-1:
            logger.error("[Discount] Invalid percentage")
            raise DiscountAndConstraintsError("Invalid percentage", DiscountAndConstraintsErrorTypes.invalid_percentage)
        self.discount_id = discount_id
        self._store_id = store_id
        self._discount_description = discount_description
        self._starting_date = starting_date
        self._ending_date = ending_date
        self._percentage = percentage
        self._predicate = predicate
        logger.info("[Discount] Discount with id: " + str(discount_id) + " created successfully!")

    @property
    def discount_id(self):
        return self.discount_id
    
    @property 
    def store_id(self):
        return self._store_id
    
    @property
    def discount_description(self):
        return self._discount_description
    
    @property
    def starting_date(self):
        return self._starting_date
    
    @property
    def ending_date(self):
        return self._ending_date
    
    @property
    def percentage(self):
        return self._percentage
    
    @property
    def predicate(self) -> Optional[Constraint]:
        if self._predicate is None or self._predicate is "":
            return None
        parsed = parse_constraint_string(self._predicate)
        predicate_builder = None
        if parsed[0] in ['and', 'or', 'xor', 'implies']:
            predicate_builder = build_nested_array(parsed)
            logger.info("[Discount] Predicate: " + str(predicate_builder))
            return discount_predicate_builder(predicate_builder)
        else: 
            predicate_builder = constraint_types[parsed[0]](*parsed[1:])
            logger.info("[Discount] Predicate: " + str(predicate_builder))
            return predicate_builder

    @abstractmethod
    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        pass

    @abstractmethod
    def get_discount_info_as_dict(self) -> dict:
        pass

    def change_discount_percentage(self, new_percentage: float) -> None:
        if new_percentage < 0 or new_percentage > 1:
            logger.error("[Discount] Invalid percentage")
            raise DiscountAndConstraintsError("Invalid percentage", DiscountAndConstraintsErrorTypes.invalid_percentage)
        logger.info("[Discount] Discount percentage changed to: " + str(new_percentage))
        self._percentage = new_percentage
        db.session.flush()        


    def change_discount_description(self, new_description: str) -> None:
        self._discount_description = new_description
        db.session.flush()

    def is_simple_discount(self) -> bool:
        if self.predicate is None:
            return True
        return False        
    
    def change_predicate(self, new_predicate: Constraint) -> None:
        self._predicate = new_predicate.get_constraint_string()
        db.session.flush()



# --------------- Category Discount ---------------#
class CategoryDiscount(Discount):
    __tablename__ = 'category_discounts'

    discount_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'), primary_key=True)
    _category_id = db.Column(db.Integer, nullable=False)
    _applied_to_subcategories = db.Column(db.Boolean, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'category_discount',
    }

    """
    * This class is responsible for creating a discount that is applied to a specific category.
    """
    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, predicate: Optional[Constraint], category_id: int, applied_to_subcategories: bool):
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, predicate)
        self._category_id = category_id
        self._applied_to_subcategories = applied_to_subcategories
        logger.info("[CategoryDiscount] Category discount with id: " + str(discount_id) + " created successfully!")

    @property
    def category_id(self) -> int:
        return self._category_id
    
    @property
    def applied_to_subcategories(self) -> bool:
        return self._applied_to_subcategories
    

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForConstraintDTO
        * This function is responsible for calculating the discount based on the basket information, the discount is only applied to the products that fall under the category.
        * Returns: float of the amount the discount will deduce from the total price.
        """
        if self.predicate is not None and not self.predicate.is_satisfied(basket_information):
            logger.info("[CategoryDiscount] Predicate not satisfied")
            return 0.0
        if self.starting_date > datetime.now() or self.ending_date < datetime.now():
            logger.info("[CategoryDiscount] Discount expired!")
            return 0.0
        
        discount_reduction = 0.0
        for category in basket_information.categories:
            if category.category_id == self._category_id:
                products_of_category = set(category.products)
                if self._applied_to_subcategories:
                    for subcategory in category.sub_categories:
                        products_of_category.update(set(subcategory.products))
                    
                for product in products_of_category:
                    discount_reduction += product.price * product.amount * self.percentage
        logger.info("[CategoryDiscount] Discount calculated to be: " + str(discount_reduction))
        return discount_reduction
    
    def get_discount_info_as_dict(self) -> dict:
        is_applied = "Yes" if self.applied_to_subcategories else "No"
        
        return {
            "discount_type": "categoryDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "percentage": self.percentage,
            "predicate": self.predicate.get_constraint_info_as_string() if self.predicate is not None else "None",
            "category_id": self.category_id,
            "applied_to_subcategories": is_applied
        }


# --------------- Store Discount ---------------#
class StoreDiscount(Discount):
    __tablename__ = 'store_discounts'

    discount_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'store_discount',
    }

    """
    * This class is responsible for creating a discount that is applied to a specific store.
    """
    def __init__(self, discount_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, predicate: Optional[Constraint], store_id: int):
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, predicate)
        logger.info("[StoreDiscount] Store discount with id: " + str(discount_id) + " created successfully!")

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForConstraintDTO
        * This function is responsible for calculating the discount based on the basket information, the discount is only applied to the products that fall under the store.
        * Returns: float of the amount the discount will deduce from the total price.
        """
        if self.predicate is not None and not self.predicate.is_satisfied(basket_information):
            logger.info("[StoreDiscount] Predicate not satisfied")
            return 0.0
        
        if self.starting_date > datetime.now() or self.ending_date < datetime.now():
            logger.info("[StoreDiscount] Discount expired!")
            return 0.0
        
        discount_reduction = 0.0
        if self.store_id == basket_information.store_id:
            for product in basket_information.products:
                if product.store_id == self.store_id:
                    discount_reduction += product.price * product.amount * self.percentage
        logger.info("[StoreDiscount] Discount calculated to be: " + str(discount_reduction))
        return discount_reduction
    
    def get_discount_info_as_dict(self) -> dict:

        return {
            "discount_type": "storeDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "percentage": self.percentage,
            "predicate": self.predicate.get_constraint_info_as_string() if self.predicate is not None else "None"
        }

# --------------- Product Discount ---------------#
class ProductDiscount(Discount):
    __tablename__ = 'product_discounts'

    discount_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'), primary_key=True)
    _product_id = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'product_discount',
    }

    # class responsible for returning the total price of the product discount.
    def __init__(self, discount_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, predicate: Optional[Constraint], product_id: int, store_id: int):
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, predicate)
        self._product_id = product_id
        logger.info("[ProductDiscount] Product discount with id: " + str(discount_id) + " created successfully!")

    @property
    def product_id(self) -> int:
        return self._product_id
    
    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForConstraintDTO
        * This function is responsible for calculating the discount based on the basket information, the discount is only applied to the products that fall under the product.
        * Returns: float of the amount the discount will deduce from the total price.
        """
        if self.predicate is not None and not self.predicate.is_satisfied(basket_information):
            logger.info("[ProductDiscount] Predicate not satisfied")
            return 0.0
        if self.starting_date > datetime.now() or self.ending_date < datetime.now():
            logger.info("[ProductDiscount] Discount expired!")
            return 0.0
        
        if self.store_id != basket_information.store_id:
            logger.info("[ProductDiscount] Discount not applicable due to store mismatch")
            return 0.0

        discount_reduction = 0.0
        for product in basket_information.products:
            if product.product_id == self._product_id and product.store_id == self.store_id:
                discount_reduction += product.price * product.amount * self.percentage
        logger.info("[ProductDiscount] Discount calculated to be: " + str(discount_reduction))
        return discount_reduction
    
    def get_discount_info_as_dict(self) -> dict:

        return {
            "discount_type": "productDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "product_id": self.product_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "percentage": self.percentage,
            "predicate": self.predicate.get_constraint_info_as_string() if self.predicate is not None else "None"
        }

discount_association = db.Table('discount_association',
    db.Column('parent_id', db.Integer, db.ForeignKey('discounts.discount_id'), primary_key=True),
    db.Column('child_id', db.Integer, db.ForeignKey('discounts.discount_id'), primary_key=True)
)


# --------------- And Discount ---------------#
class AndDiscount(Discount):
    __tablename__ = 'and_discounts'

    discount_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'), primary_key=True)
    _discount1_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'))
    _discount2_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'))

    __mapper_args__ = {
        'polymorphic_identity': 'and_discount',
    }

    """
    * This class is responsible for creating a discount composite that is applied when both discounts are applicable.
    """
    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, discount1: Discount, discount2: Discount):
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, None)
        self._discount1_id = discount1.discount_id
        self._discount2_id = discount2.discount_id
        logger.info("[AndDiscount] And discount created successfully!")

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForConstraintDTO
        * This function is responsible for calculating the discount based on the basket information. It is only applied when both discounts have satisfied predicates and returns the sum of the discounts
        """
        # get discount from db
        __discount1 = db.session.query(Discount).filter_by(discount_id=self._discount1_id).first()
        if __discount1 is None:
            logger.error("[AndDiscount] Discount 1 not found")
            return 0.0
        __discount2 = db.session.query(Discount).filter_by(discount_id=self._discount2_id).first()
        if __discount2 is None:
            logger.error("[AndDiscount] Discount 2 not found")
            return 0.0
        if __discount1.predicate is not None and __discount2.predicate is not None:
            if __discount1.predicate.is_satisfied(basket_information) and __discount2.predicate.is_satisfied(basket_information):
                logger.info("[AndDiscount] Both predicates satisfied, applying discounts")
                return __discount1.calculate_discount(basket_information) + __discount2.calculate_discount(basket_information)
            else:
                return 0.0
        else:
            if __discount1.predicate is not None and __discount2.predicate is None:
                if __discount1.predicate.is_satisfied(basket_information):
                    logger.info("[AndDiscount] Discount predicates satisfied, applying discounts")
                    return __discount1.calculate_discount(basket_information) + __discount2.calculate_discount(basket_information)
                else:
                    return 0.0
            elif __discount1.predicate is None and __discount2.predicate is not None:
                if self.__discount2.predicate.is_satisfied(basket_information):
                    logger.info("[AndDiscount] Discount predicates satisfied, applying discounts")
                    return __discount1.calculate_discount(basket_information) + __discount2.calculate_discount(basket_information)
                else:
                    return 0.0
            else:
                logger.info("[AndDiscount] Both discounts applicable, applying discounts")
                return __discount1.calculate_discount(basket_information) + __discount2.calculate_discount(basket_information)
    
    def change_predicate(self, new_predicate: Constraint) -> None:
        pass # we don't want to change the predicate of the composite discount

    def get_discount_info_as_dict(self) -> dict:
        __discount1 = db.session.query(Discount).filter_by(discount_id=self._discount1_id).first()
        if __discount1 is None:
            logger.error("[AndDiscount] Discount 1 not found")
            return {}
        __discount2 = db.session.query(Discount).filter_by(discount_id=self._discount2_id).first()
        if __discount2 is None:
            logger.error("[AndDiscount] Discount 2 not found")
            return {}
        dict_of_disc1 = __discount1.get_discount_info_as_dict()
        dict_of_disc2 = __discount2.get_discount_info_as_dict() 

        return {
            "discount_type": "andDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "discount_id1": dict_of_disc1,
            "discount_id2": dict_of_disc2
        }
    

# --------------- Or Discount ---------------#
class OrDiscount(Discount):
    __tablename__ = 'or_discounts'

    discount_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'), primary_key=True)
    _discount1_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'))
    _discount2_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'))

    __mapper_args__ = {
        'polymorphic_identity': 'or_discount',
    }

    """
    * This class is responsible for creating a discount composite that is applied when at least one of the discounts is applicable.
    """
    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, discount1: Discount, discount2: Discount): # add decision rule
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, None)
        self._discount1_id = discount1.discount_id
        self._discount2_id = discount2.discount_id

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForConstraintDTO
        * This function is responsible for calculating the discount based on the basket information. It is only applied when at least one of the discounts have satisfied predicates and returns the sum of the discounts
        * NOTE: for simplicity, we assume that if both discounts are applicable, we would use both, but if only one is applicable, we would use only that one.
        """
        __discount1 = db.session.query(Discount).filter_by(discount_id=self._discount1_id).first()
        if __discount1 is None:
            logger.error("[OrDiscount] Discount 1 not found")
            return 0.0
        
        __discount2 = db.session.query(Discount).filter_by(discount_id=self._discount2_id).first()
        if __discount2 is None:
            logger.error("[OrDiscount] Discount 2 not found")
            return 0.0
        if __discount1.predicate is None and __discount2.predicate is None:
            logger.info("[OrDiscount] Both discounts applicable, applying discounts")
            return __discount1.calculate_discount(basket_information) + __discount2.calculate_discount(basket_information)
        elif __discount1.predicate is None and __discount2.predicate is not None:
            if __discount2.predicate.is_satisfied(basket_information):
                logger.info("[OrDiscount] Both discounts applicable, applying discounts")
                return __discount1.calculate_discount(basket_information) + __discount2.calculate_discount(basket_information)
            else:
                logger.info("[OrDiscount] Discount 1 applicable, applying discount 1")
                return __discount1.calculate_discount(basket_information)
        elif __discount1.predicate is not None and __discount2.predicate is None:
            if self.__discount1.predicate.is_satisfied(basket_information):
                logger.info("[OrDiscount] Both discounts applicable, applying discounts")
                return __discount1.calculate_discount(basket_information) + __discount2.calculate_discount(basket_information)
            else:
                logger.info("[OrDiscount] Discount 2 applicable, applying discount 2")
                return __discount2.calculate_discount(basket_information)
        else:
            if __discount1.predicate.is_satisfied(basket_information) and __discount2.predicate.is_satisfied(basket_information):
                logger.info("[OrDiscount] Both discounts applicable, applying discounts")
                return __discount1.calculate_discount(basket_information) + __discount2.calculate_discount(basket_information)
            elif self.__discount1.predicate.is_satisfied(basket_information):
                logger.info("[OrDiscount] Discount 1 applicable, applying discount 1")
                return __discount1.calculate_discount(basket_information)
            elif __discount2.predicate.is_satisfied(basket_information):
                logger.info("[OrDiscount] Discount 2 applicable, applying discount 2")
                return __discount2.calculate_discount(basket_information)
            else:
                return 0.0
            
        
    def change_predicate(self, new_predicate: Constraint) -> None:
        pass # we don't want to change the predicate of the composite discount


    def get_discount_info_as_dict(self) -> dict:
        __discount1 = db.session.query(Discount).filter_by(discount_id=self._discount1_id).first()
        if __discount1 is None:
            logger.error("[OrDiscount] Discount 1 not found")
            return {}
        
        __discount2 = db.session.query(Discount).filter_by(discount_id=self._discount2_id).first()
        if __discount2 is None:
            logger.error("[OrDiscount] Discount 2 not found")
            return {}
        
        dict_of_disc1 = __discount1.get_discount_info_as_dict()
        dict_of_disc2 = __discount2.get_discount_info_as_dict() 

        return {
            "discount_type": "orDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "discount_id1": dict_of_disc1,
            "discount_id2": dict_of_disc2
        }

# --------------- Xor Discount ---------------#
class XorDiscount(Discount):
    __tablename__ = 'xor_discounts'

    discount_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'), primary_key=True)
    _discount1_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'))
    _discount2_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'))

    __mapper_args__ = {
        'polymorphic_identity': 'xor_discount',
    }
    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, discount1: Discount, discount2: Discount): # add decision rule
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, None)
        self._discount1_id = discount1.discount_id
        self._discount2_id = discount2.discount_id
        logger.info("[XorDiscount] Xor discount created successfully!")

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket_information in BasketInformationForConstraintDTO
        * This function is responsible for calculating the discount based on the basket information.
        * Returns: float of the amount the discount will deduce from the total price.
        """
        __discount1 = db.session.query(Discount).filter_by(discount_id=self._discount1_id).first()
        if __discount1 is None:
            logger.error("[XorDiscount] Discount 1 not found")
            return 0.0
        
        __discount2 = db.session.query(Discount).filter_by(discount_id=self._discount2_id).first()
        if __discount2 is None:
            logger.error("[XorDiscount] Discount 2 not found")
            return 0.0
        
        if __discount1.predicate is not None and __discount2.predicate is not None:    
            if __discount1.predicate.is_satisfied(basket_information):
                logger.info("[XorDiscount] Discount 1 applicable, applying discount 1")
                return __discount1.calculate_discount(basket_information)
            elif __discount2.predicate.is_satisfied(basket_information):
                logger.info("[XorDiscount] Discount 2 applicable, applying discount 2")
                return __discount2.calculate_discount(basket_information)
            else:
                return 0.0
        elif __discount1.predicate is not None and __discount2.predicate is None:
            if __discount1.predicate.is_satisfied(basket_information):
                logger.info("[XorDiscount] Discount 1 applicable, applying discount 1")
                return __discount1.calculate_discount(basket_information)
            else:
                logger.info("[XorDiscount] discount 2 applicable, applying discount 2")
                return __discount2.calculate_discount(basket_information)
        else:
            logger.info("[XorDiscount] Both discounts applicable, applying discount 1")
            return __discount1.calculate_discount(basket_information) 
        
    
    def change_predicate(self, new_predicate: Constraint) -> None:
        pass # we don't want to change the predicate of the composite discount

    def get_discount_info_as_dict(self) -> dict:
        __discount1 = db.session.query(Discount).filter_by(discount_id=self._discount1_id).first()
        if __discount1 is None:
            logger.error("[XorDiscount] Discount 1 not found")
            return {}
        
        __discount2 = db.session.query(Discount).filter_by(discount_id=self._discount2_id).first()
        if __discount2 is None:
            logger.error("[XorDiscount] Discount 2 not found")
            return {}
        
        dict_of_disc1 = __discount1.get_discount_info_as_dict()
        dict_of_disc2 = __discount2.get_discount_info_as_dict() 
        return {
            "discount_type": "xorDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "discount_id1": dict_of_disc1,
            "discount_id2": dict_of_disc2
        }

# --------------- Max Discount classes ---------------#
class MaxDiscount(Discount):
    __tablename__ = 'max_discounts'

    discount_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'), primary_key=True)
    _discounts = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'max_discount',
    }

    # class responsible for returning the total price of the maximum discount.
    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, ListDiscount: list[Discount]):
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, None)
        self._discounts = '#'.join([str(discount.discount_id) for discount in ListDiscount])
        logger.info("[maxDiscount] Max discount created successfully!")

    @property
    def __ListDiscount(self) -> list[Discount]:
        discount_ids = self._discounts.split('#')
        discounts = []
        for discount_id in discount_ids:
            discount = db.session.query(Discount).filter_by(discount_id=int(discount_id)).first()
            if discount is not None:
                discounts.append(discount)
        return discounts

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket in BasketDTO, user in UserDTO
        * This function is responsible for calculating the discount based on the basket and user.
        * Returns: float
        """
        logger.info("[maxDiscount] Calculating max discount")
        return max([discount.calculate_discount(basket_information) for discount in self.__ListDiscount])
    
    
    def change_predicate(self, new_predicate: Constraint) -> None:
        pass # we don't want to change the predicate of the composite discount

    def get_discount_info_as_dict(self) -> dict:
        discounts_info = dict()
        for discount in self.__ListDiscount:
            discounts_info[discount.discount_id] = discount.get_discount_info_as_dict()

        return {
            "discount_type": "maxDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(DATE_FORMAT)),
            "end_date": str(self.ending_date.strftime(DATE_FORMAT)),
            "discounts_info": discounts_info
        }


# --------------- Additive Discount classes ---------------#
class AdditiveDiscount(Discount):
    __tablename__ = 'additive_discounts'

    discount_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'), primary_key=True)
    _discounts = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'additive_discount',
    }

    # class responsible for returning the total price of the maximum discount.
    def __init__(self, discount_id: int, store_id: int, discount_description: str, starting_date: datetime, ending_date: datetime,
                 percentage: float, ListDiscount: list[Discount]):
        super().__init__(discount_id, store_id, discount_description, starting_date, ending_date, percentage, None)
        self._discounts = '#'.join([str(discount.discount_id) for discount in ListDiscount])
        logger.info("[additiveDiscount] Additive discount created successfully!")

    @property
    def __ListDiscount(self) -> list[Discount]:
        discount_ids = self._discounts.split('#')
        discounts = []
        for discount_id in discount_ids:
            discount = db.session.query(Discount).filter_by(discount_id=int(discount_id)).first()
            if discount is not None:
                discounts.append(discount)
        return discounts

    def calculate_discount(self, basket_information: BasketInformationForConstraintDTO) -> float:
        """
        * Parameters: basket in BasketDTO, user in UserDTO
        * This function is responsible for calculating the discount based on the basket and user.
        * Returns: float
        """
        logger.info("[additiveDiscount] Calculating additive discount")
        return sum([discount.calculate_discount(basket_information) for discount in self.__ListDiscount])
    
    
    def change_predicate(self, new_predicate: Constraint) -> None:
        pass # we don't want to change the predicate of the composite discount
    
    def get_discount_info_as_dict(self) -> dict:
        date_format = "%Y-%m-%d" 

        discounts_info = dict()
        for discount in self.__ListDiscount:
            discounts_info[discount.discount_id] = discount.get_discount_info_as_dict()
        return {
            "discount_type": "additiveDiscount",
            "discount_id": self.discount_id,
            "store_id": self.store_id,
            "description": self.discount_description,
            "start_date": str(self.starting_date.strftime(date_format)),
            "end_date": str(self.ending_date.strftime(date_format)),
            "discounts_info": discounts_info
        }