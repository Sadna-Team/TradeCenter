# --------------- imports ---------------#
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime, time
import holidays

from backend.business.DTOs import AddressDTO, BasketInformationForConstraintDTO, CategoryForConstraintDTO #maybe timezone constraints :O
from backend.error_types import *
 
# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')

# ---------------------------------------------------
seasons = {
    'spring': (21, 3, 20, 6),
    'summer': (21,6, 22, 9),
    'autumn': (23, 9, 20, 12),
    'winter': (21, 12, 20, 3)
}

# --------------- Constraint Interface ---------------#
class Constraint(ABC):
    @abstractmethod
    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        pass

    @abstractmethod
    def get_constraint_info_as_dict(self) -> dict:
        pass

    @abstractmethod
    def get_constraint_info_as_string(self) -> str:
        pass

    @abstractmethod
    def get_constraint_string(self) -> str:
        pass

# ------------------------------------ Leaf Classes of Composite: ------------------------------------ #

# --------------- age constraint class ---------------#
class AgeConstraint(Constraint):
    def __init__(self, age_limit: int):
        if age_limit < 0:
            raise DiscountAndConstraintsError("Age limit is not valid", DiscountAndConstraintsErrorTypes.invalid_age_limit)
        self.__age_limit = age_limit
        logger.info("[AgeConstraint]: Age constraint created with age limit: " + str(age_limit))

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[AgeConstraint]: Checking if user is older than " + str(self.__age_limit) + " years old")
        today = datetime.today()
        if basket_information.user_info.birthdate is None:
            logger.info("[AgeConstraint]: User birthdate is not provided")
            return False
        birth_date = basket_information.user_info.birthdate
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


        return age >= self.__age_limit
    
    @property
    def age_limit(self):
        return self.__age_limit

    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "age_constraint",
            "age_limit": self.__age_limit
            }
    
    def get_constraint_info_as_string(self) -> str:
        return "Age constraint with age limit: " + str(self.__age_limit)
    
    def get_constraint_string(self) -> str:
        return f"(age, {self.__age_limit})"

# --------------- location constraint class ---------------# 
class LocationConstraint(Constraint):
    def __init__(self, location: AddressDTO):
        if location is None:
            raise DiscountAndConstraintsError("Location is not valid", DiscountAndConstraintsErrorTypes.invalid_location)
        self.__location = location
        logger.info("[LocationConstraint]: Location constraint created with location: " + str(location))

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[LocationConstraint]: Checking if user location fulfills the constraint")
        user_location = basket_information.user_info.address
        country = user_location.country
        city = user_location.city
        return self.__location.country == country and self.__location.city == city
    
    @property
    def location(self):
        return self.__location
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "location_constraint",
            "address": self.__location.address,
            "city": self.__location.city,
            "state": self.__location.state,
            "country": self.__location.country,
            "zip_code": self.__location.zip_code
            }
    
    def get_constraint_info_as_string(self) -> str:
        return "Location constraint with location: " + "address: " + self.__location.address + ", city: " + self.__location.city + ", state: " + self.__location.state + ", country: " + self.__location.country + ", zip code: " + self.__location.zip_code
    
    def get_constraint_string(self) -> str:
        return f"(location, {self.__location.address}, {self.__location.city}, {self.__location.state}, {self.__location.country}, {self.__location.zip_code})"
# --------------- time constraint class ---------------#
class TimeConstraint(Constraint):
    def __init__(self, start_time: time, end_time: time):
        if start_time >= end_time:
            raise DiscountAndConstraintsError("Start time is greater than end time", DiscountAndConstraintsErrorTypes.invalid_time_constraint)
        self.__start_time = start_time
        self.__end_time = end_time
        logger.info("[TimeConstraint]: Time constraint created with start time: " + str(start_time) + " and end time: " + str(end_time))

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[TimeConstraint]: Checking if the time of purchase is within the time constraint")
        time_of_purchase = basket_information.time_of_purchase.time()

        return self.__start_time <= time_of_purchase <= self.__end_time
    
    @property
    def start_time(self):
        return self.__start_time
    
    @property
    def end_time(self):
        return self.__end_time
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "time_constraint",
            "start_time": self.__start_time,
            "end_time": self.__end_time
            }
    
    def get_constraint_info_as_string(self) -> str:
        return "Time constraint with start time: " + str(self.__start_time) + " and end time: " + str(self.__end_time)
    
    def get_constraint_string(self) -> str:
        return f"(time, {self.__start_time.hour}, {self.__start_time.minute}, {self.__end_time.hour}, {self.__end_time.minute})"
# --------------- day constraint class ---------------#
class DayOfMonthConstraint(Constraint):
    def __init__(self, start_day: int, end_day: int):
        if start_day < 1 or start_day > 31 or end_day < 1 or end_day > 31:
            raise DiscountAndConstraintsError("Day of month is not valid", DiscountAndConstraintsErrorTypes.invalid_day_of_month)
        
        if start_day > end_day:
            raise DiscountAndConstraintsError("Start day is greater than end day", DiscountAndConstraintsErrorTypes.invalid_day_of_month)
        
        self.__start_day = start_day
        self.__end_day = end_day
        logger.info("[DayOfMonthConstraint]: Day of month constraint created with start day: " + str(start_day) + " and end day: " + str(end_day))

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[DayOfMonthConstraint]: Checking if the day of the month fulfills the constraint")
        day_of_purchase = basket_information.time_of_purchase.day

        return self.__start_day <= day_of_purchase <= self.__end_day
    
    @property
    def start_day(self):
        return self.__start_day
    
    @property
    def end_day(self):
        return self.__end_day

    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "day_of_month_constraint",
            "start_day": self.__start_day,
            "end_day": self.__end_day
            }
    
    def get_constraint_info_as_string(self) -> str:
        return "Day of month constraint with start day: " + str(self.__start_day) + " and end day: " + str(self.__end_day)

    def get_constraint_string(self) -> str:
        return f"(day_of_month, {self.__start_day}, {self.__end_day})"

# --------------- day of week constraint class ---------------#
class DayOfWeekConstraint(Constraint):
    def __init__(self, start_day: int, end_day: int):
        if start_day < 0 or start_day > 6 or end_day < 0 or end_day > 6:
            raise DiscountAndConstraintsError("Day of week is not valid", DiscountAndConstraintsErrorTypes.invalid_day_of_week)
        
        if start_day > end_day:
            raise DiscountAndConstraintsError("Start day is greater than end day", DiscountAndConstraintsErrorTypes.invalid_day_of_week)
        
        self.__start_day = start_day
        self.__end_day = end_day
        logger.info("[DayOfWeekConstraint]: Day of week constraint created with start day: " + str(start_day) + " and end day: " + str(end_day))

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[DayOfWeekConstraint]: Checking if the day of the week fulfills the constraint")
        day_of_purchase = basket_information.time_of_purchase.weekday()

        return self.__start_day <= day_of_purchase <= self.__end_day
    
    @property
    def start_day(self):
        return self.__start_day
    
    @property
    def end_day(self):
        return self.__end_day
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "day_of_week_constraint",
            "start_day": self.__start_day,
            "end_day": self.__end_day
            }
    
    def get_constraint_info_as_string(self) -> str:
        return "Day of week constraint with start day: " + str(self.__start_day) + " and end day: " + str(self.__end_day)
    
    def get_constraint_string(self) -> str:
        return f"(day_of_week, {self.__start_day}, {self.__end_day})"
    



# --------------- season constraint class ---------------#
class SeasonConstraint(Constraint):
    def __init__(self, season: str):
        if season not in seasons.keys():
            raise DiscountAndConstraintsError("Season is not valid", DiscountAndConstraintsErrorTypes.invalid_season)
        self.__season = season
        self.__start_month = seasons[season][1]
        self.__start_day_of_month = seasons[season][0]
        self.__end_month = seasons[season][3]
        self.__end_day_of_month = seasons[season][2]
        logger.info("[SeasonConstraint]: Season constraint created with season: " + str(season))
        
    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[SeasonConstraint]: Checking if the season fulfills the constraint")
        month_of_purchase = basket_information.time_of_purchase.month
        day_of_purchase = basket_information.time_of_purchase.day
        if month_of_purchase == self.__start_month:
            return day_of_purchase >= self.__start_day_of_month
        if month_of_purchase == self.__end_month:
            return day_of_purchase <= self.__end_day_of_month
        if self.__start_month > self.__end_month:
            if month_of_purchase > self.__start_month or month_of_purchase < self.__end_month:
                return True
        else:
            if self.__start_month < month_of_purchase < self.__end_month:
                return True
        return False
        
    @property
    def start_month(self):
        return self.__start_month
    
    @property
    def start_day_of_month(self):
        return self.__start_day_of_month
    
    @property
    def end_month(self):
        return self.__end_month
    
    @property
    def end_day_of_month(self):
        return self.__end_day_of_month
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "season_constraint",
            "start_month": self.__start_month,
            "start_day_of_month": self.__start_day_of_month,
            "end_month": self.__end_month,
            "end_day_of_month": self.__end_day_of_month
            }
    
    def get_constraint_info_as_string(self) -> str:
        season = ""
        for key, value in seasons.items():
            if value == (self.__start_day_of_month, self.__start_month, self.__end_day_of_month, self.__end_month):
                season = key
        return "Season constraint of season: " + season
    
    def get_constraint_string(self) -> str:
        return f"(season, {self.__season})"


# --------------- holiday constraint class ---------------#
class HolidaysOfCountryConstraint(Constraint):
    def __init__(self, country_code: str):
        if country_code not in holidays.list_supported_countries().keys():
            raise PurchaseError("Country code is not valid", PurchaseErrorTypes.invalid_country_code)
        self.__country_code = country_code
        logger.info("[HolidaysOfCountryConstraint]: Holidays of country constraint created with country code: " + str(country_code))

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[HolidaysOfCountryConstraint]: Checking if the day of the purchase is a holiday in the country")
        day_of_purchase = basket_information.time_of_purchase.date()
        country_holidays = holidays.CountryHoliday(self.country_code,None, day_of_purchase.year)
        if country_holidays.get(day_of_purchase) is None:
            return False
        return True

    @property
    def country_code(self):
        return self.__country_code
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "holidays_of_country_constraint",
            "country_code": self.__country_code
            }
    
    def get_constraint_info_as_string(self) -> str:
        return "Holidays of country constraint with country code: " + str(self.__country_code)
    
    def get_constraint_string(self) -> str:
        return f"(holidays_of_country, {self.__country_code})"
    
# --------------- price basket constraint class ---------------#
class PriceBasketConstraint(Constraint):
    def __init__(self, min_price: float, max_price: float, store_id: int):
        if min_price < 0:
            raise DiscountAndConstraintsError("Min price is not valid", DiscountAndConstraintsErrorTypes.invalid_price)
        
        if max_price != -1.0 and max_price < min_price:
            raise DiscountAndConstraintsError("Max price is not valid", DiscountAndConstraintsErrorTypes.invalid_price)
        
        self.__min_price = min_price #if min_price is 0, then there is no lower limit
        self.__max_price = max_price #if max_price is -1, then there is no upper limit
        self.__store_id = store_id
        logger.info("[PriceBasketConstraint]: Price basket constraint created!")


    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        if basket_information.store_id != self.__store_id:
            logger.warning("[PriceBasketConstraint]: Store id does not match the store id of the basket")
            return False
        
        if self.__max_price == -1.0:
            logger.info("[PriceBasketConstraint]: Checking if the total price of the basket is atleast" + str(self.__min_price) + " dollars")
            return self.__min_price <= basket_information.total_price_of_basket
        logger.info("[PriceBasketConstraint]: Checking if the total price of the basket is between " + str(self.__min_price) + " and " + str(self.__max_price) + " dollars")
        return self.__min_price <= basket_information.total_price_of_basket <= self.__max_price
    
    @property
    def min_price(self):
        return self.__min_price
    
    @property
    def max_price(self):
        return self.__max_price
    
    @property
    def store_id(self):
        return self.__store_id
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "price_basket_constraint",
            "min_price": self.__min_price,
            "max_price": self.__max_price,
            "store_id": self.__store_id
            }
    
    def get_constraint_info_as_string(self) -> str:
        if self.__max_price == -1:
            return "Price basket constraint with min price: " + str(self.__min_price) + " in store: " + str(self.__store_id)
        return "Price basket constraint with min price: " + str(self.__min_price) + " and max price: " + str(self.__max_price) + " in store: " + str(self.__store_id)

    def get_constraint_string(self) -> str:
        return f"(price_basket, {self.__min_price}, {self.__max_price}, {self.__store_id})"
    
# --------------- price product constraint class  ---------------#
class PriceProductConstraint(Constraint):
    def __init__(self, min_price: float, max_price: float, product_id: int, store_id: int):
        if min_price < 0:
            raise DiscountAndConstraintsError("Min price is not valid", DiscountAndConstraintsErrorTypes.invalid_price)
        
        if max_price != -1.0 and max_price < min_price:
            raise DiscountAndConstraintsError("Max price is not valid", DiscountAndConstraintsErrorTypes.invalid_price)
        
        self.__min_price = min_price #if min_price is 0, then there is no lower limit
        self.__max_price = max_price #if max_price is -1, then there is no upper limit
        self.__product_id = product_id
        self.__store_id = store_id
        logger.info("[PriceProductConstraint]: Price product constraint created!")


    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[PriceProductConstraint]: Checking if the price of the product fulfills the constraint")
        if basket_information.store_id != self.__store_id:
            return False
        
        for product in basket_information.products:
            if product.product_id == self.__product_id:
                if self.__max_price == -1.0:
                    return self.__min_price <= product.price * product.amount
                return self.__min_price <= product.price * product.amount <= self.__max_price
                
        logger.warn("[WeightProductConstraint]: Product not found in basket")
        return False
        
    @property
    def min_price(self):
        return self.__min_price
    
    @property
    def max_price(self):
        return self.__max_price
    
    @property
    def product_id(self):
        return self.__product_id
    
    @property
    def store_id(self):
        return self.__store_id
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "price_product_constraint",
            "min_price": self.__min_price,
            "max_price": self.__max_price,
            "product_id": self.__product_id,
            "store_id": self.__store_id
            }
    
    def get_constraint_info_as_string(self) -> str:
        if self.__max_price == -1.0:
            return "Price product constraint with min price: " + str(self.__min_price) + " of product: " + str(self.__product_id) + " in store: " + str(self.__store_id)
        return "Price product constraint with min price: " + str(self.__min_price) + " and max price: " + str(self.__max_price) + " of product: " + str(self.__product_id) + " in store: " + str(self.__store_id)


    def get_constraint_string(self) -> str:
        return f"(price_product, {self.__min_price}, {self.__max_price}, {self.__product_id}, {self.__store_id})"
    
# --------------- price category constraint class  ---------------#
class PriceCategoryConstraint(Constraint):
    def __init__(self, min_price: float, max_price: float, category_id: int):
        if min_price < 0:
            raise DiscountAndConstraintsError("Min price is not valid", DiscountAndConstraintsErrorTypes.invalid_price)
        
        if max_price != -1.0 and max_price < min_price:
            raise DiscountAndConstraintsError("Max price is not valid", DiscountAndConstraintsErrorTypes.invalid_price)
        
        self.__min_price = min_price #if min_price is 0, then there is no lower limit
        self.__max_price = max_price #if max_price is -1, then there is no upper limit
        self.__category_id = category_id 
        logger.info("[PriceCategoryConstraint]: Price category constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        categories= basket_information.categories
        for category in categories:
            if category.category_id == self.__category_id:
                products = set(category.products)
                for sub_categories in category.sub_categories:
                    products.update(set(sub_categories.products))
                category_total_price: float = 0.0
                for product in products:
                    category_total_price += product.price * product.amount

                if self.__max_price == -1.0:
                    logger.info("[PriceCategoryConstraint]: Checking if the price of the products of the categpry i atleast" + str(self.__min_price) + " dollars")
                    return self.__min_price <= category_total_price
                logger.info("[PriceCategoryConstraint]: Checking if the price of the products of the categpry is between " + str(self.__min_price) + " and " + str(self.__max_price) + " dollars")
                return self.__min_price <= category_total_price <= self.__max_price
        
        logger.warn("[PriceCategoryConstraint]: Category not found in basket")
        return False    
    @property
    def min_price(self):
        return self.__min_price
    
    @property
    def max_price(self):
        return self.__max_price
    
    @property
    def category_id(self):
        return self.__category_id
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "price_category_constraint",
            "min_price": self.__min_price,
            "max_price": self.__max_price,
            "category_id": self.__category_id
            }
    
    def get_constraint_info_as_string(self) -> str:
        if self.__max_price == -1.0:
            return "Price category constraint with min price: " + str(self.__min_price) + " of category: " + str(self.__category_id)
        return "Price category constraint with min price: " + str(self.__min_price) + " and max price: " + str(self.__max_price) + " of category: " + str(self.__category_id)

    def get_constraint_string(self) -> str:
        return f"(price_category, {self.__min_price}, {self.__max_price}, {self.__category_id})"

# --------------- amount basket constraint class  ---------------#
class AmountBasketConstraint(Constraint):
    def __init__(self, min_amount: int, max_amount: int, store_id: int):
        if min_amount < 0:
            raise DiscountAndConstraintsError("Min amount is not valid", DiscountAndConstraintsErrorTypes.invalid_amount)
        
        if max_amount != -1 and max_amount < min_amount:
            raise DiscountAndConstraintsError("Max amount is not valid", DiscountAndConstraintsErrorTypes.invalid_amount)
        
        self.__min_amount = min_amount #if min_amount is 0, then there is no lower limit
        self.__max_amount = max_amount #if max_amount is -1, then there is no upper limit
        self.__store_id = store_id
        logger.info("[AmountBasketConstraint]: Amount basket constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        amount_in_basket = 0
        for product in basket_information.products:
            amount_in_basket += product.amount
        
        if basket_information.store_id != self.__store_id:
            logger.warning("[AmountBasketConstraint]: Store id does not match the store id of the basket")
            return False
        logger.info("[AmountBasketConstraint]: Checking if the amount of products in the basket fulfills the constraint")
        if self.__max_amount == -1:
            return self.__min_amount <= amount_in_basket
        else:
            return self.__min_amount <= amount_in_basket <= self.__max_amount
    
    @property
    def min_amount(self):
        return self.__min_amount
    
    @property
    def max_amount(self):
        return self.__max_amount
    
    @property
    def store_id(self):
        return self.__store_id
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "amount_basket_constraint",
            "min_amount": self.__min_amount,
            "max_amount": self.__max_amount,
            "store_id": self.__store_id
            }

    def get_constraint_info_as_string(self) -> str:
        if self.__max_amount == -1:
            return "Amount basket constraint with min amount: " + str(self.__min_amount) + " in store: " + str(self.__store_id)
        return "Amount basket constraint with min amount: " + str(self.__min_amount) + "and max amount" + str(self.__min_amount) +" in store: " + str(self.__store_id)

    def get_constraint_string(self) -> str:
        return f"(amount_basket, {self.__min_amount}, {self.__max_amount}, {self.__store_id})"
    
# --------------- amount product constraint class  ---------------#
class AmountProductConstraint(Constraint):
    def __init__(self, min_amount: int, max_amount: int, product_id: int, store_id: int):
        if min_amount < 0:
            raise DiscountAndConstraintsError("Min amount is not valid", DiscountAndConstraintsErrorTypes.invalid_amount)
        
        if max_amount != -1 and max_amount < min_amount:
            raise DiscountAndConstraintsError("Max amount is not valid", DiscountAndConstraintsErrorTypes.invalid_amount)
        
        self.__min_amount = min_amount #if min_amount is 0, then there is no lower limit
        self.__max_amount = max_amount #if max_amount is -1, then there is no upper limit
        self.__product_id = product_id
        self.__store_id = store_id
        logger.info("[AmountProductConstraint]: Amount product constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        if basket_information.store_id != self.__store_id:
            logger.warning("[AmountProductConstraint]: Store id does not match the store id of the basket")
            return False
        
        for product in basket_information.products:
            if product.product_id == self.__product_id:
                logger.info("[AmountProductConstraint]: Checking if the amount of the product fulfills the constraint")
                if self.__max_amount == -1:
                    return self.__min_amount <= product.amount
                else:
                    return self.__min_amount <= product.amount <= self.__max_amount
        
        logger.warn("[WeightProductConstraint]: Product not found in basket")
        return False
        
    @property
    def min_amount(self):
        return self.__min_amount
    
    @property
    def max_amount(self):
        return self.__max_amount
    
    @property
    def product_id(self):
        return self.__product_id
    
    @property
    def store_id(self):
        return self.__store_id
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "amount_product_constraint",
            "min_amount": self.__min_amount,
            "max_amount": self.__max_amount,
            "product_id": self.__product_id,
            "store_id": self.__store_id
            }
    
    def get_constraint_info_as_string(self) -> str:
        if self.__max_amount == -1:
            return "Amount product constraint with min amount: " + str(self.__min_amount) + " of product: " + str(self.__product_id) + " in store: " + str(self.__store_id)
        return "Amount product constraint with min amount: " + str(self.__min_amount) + " and max amount: " + str(self.__max_amount) + " of product: " + str(self.__product_id) + " in store: " + str(self.__store_id)

    def get_constraint_string(self) -> str:
        return f"(amount_product, {self.__min_amount}, {self.__max_amount}, {self.__product_id}, {self.__store_id})"
    
# --------------- amount category constraint class  ---------------#
class AmountCategoryConstraint(Constraint):
    def __init__(self, min_amount: int, max_amount: int, category_id: int):
        if min_amount < 0:
            raise DiscountAndConstraintsError("Min amount is not valid", DiscountAndConstraintsErrorTypes.invalid_amount)
        
        if max_amount != -1 and max_amount < min_amount:
            raise DiscountAndConstraintsError("Max amount is not valid", DiscountAndConstraintsErrorTypes.invalid_amount)
        
        self.__min_amount = min_amount #if min_amount is 0, then there is no lower limit
        self.__max_amount = max_amount #if max_amount is -1, then there is no upper limit
        self.__category_id = category_id
        logger.info("[AmountCategoryConstraint]: Amount category constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        categories = basket_information.categories
        for c in categories:
            if c.category_id == self.__category_id:
                products = c.products
                for sub_categories in c.sub_categories:
                    products += sub_categories.products
                category_total_amount: int = 0
                for product in products:
                    category_total_amount += product.amount


                logger.info("[AmountCategoryConstraint]: Checking if the amount of products in the category fulfills the constraint")
                if self.__max_amount == -1:
                    return self.__min_amount <= category_total_amount
                else:
                    return self.__min_amount <= category_total_amount <= self.__max_amount
            
        logger.warn("[AmountCategoryConstraint]: Category not found in basket")
        return False    
    @property
    def min_amount(self):
        return self.__min_amount
    
    @property
    def max_amount(self):    
        return self.__max_amount

    @property
    def category_id(self):
        return self.__category_id
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "amount_category_constraint",
            "min_amount": self.__min_amount,
            "max_amount": self.__max_amount,
            "category_id": self.__category_id
            }
    
    def get_constraint_info_as_string(self) -> str:
        if self.__max_amount == -1:
            return "Amount category constraint with min amount: " + str(self.__min_amount) + " of category: " + str(self.__category_id)
        return "Amount category constraint with min amount: " + str(self.__min_amount) + " and max amount: " + str(self.__max_amount) + " of category: " + str(self.__category_id)

    def get_constraint_string(self) -> str:
        return f"(amount_category, {self.__min_amount}, {self.__max_amount}, {self.__category_id})"
    
# --------------- weight basket constraint class  ---------------#
class WeightBasketConstraint(Constraint):
    def __init__(self, min_weight: float, max_weight: float, store_id: int):
        if min_weight < 0:
            raise DiscountAndConstraintsError("Min weight is not valid", DiscountAndConstraintsErrorTypes.invalid_weight)
        
        if max_weight != -1 and max_weight < max_weight:
            raise DiscountAndConstraintsError("Max weight is not valid", DiscountAndConstraintsErrorTypes.invalid_weight)
        
        self.__min_weight = min_weight #if min_weight is 0, then there is no lower limit
        self.__max_weight = max_weight #if max_weight is -1, then there is no upper limit
        self.__store_id = store_id
        logger.info("[WeightBasketConstraint]: Weight basket constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        if basket_information.store_id != self.__store_id:
            logger.warning("[WeightBasketConstraint]: Store id does not match the store id of the basket")
            return False
        
        weight_of_basket = 0.0
        for product in basket_information.products:
            weight_of_basket += product.weight
        
        if self.__max_weight == -1:
            logger.info("[WeightBasketConstraint]: Checking if the total weight of the basket is atleast" + str(self.__min_weight) + " kg")
            return self.__min_weight <= weight_of_basket
        logger.info("[WeightBasketConstraint]: Checking if the total weight of the basket is between " + str(self.__min_weight) + " and " + str(self.__max_weight) + " kg")
        return self.__min_weight <= weight_of_basket <= self.__max_weight

    @property
    def min_weight(self):
        return self.__min_weight
    
    @property
    def max_weight(self):
        return self.__max_weight
    
    @property
    def store_id(self):
        return self.__store_id
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "weight_basket_constraint",
            "min_weight": self.__min_weight,
            "max_weight": self.__max_weight,
            "store_id": self.__store_id
            }
    
    def get_constraint_info_as_string(self) -> str:
        if self.__max_weight == -1:
            return "Weight basket constraint with min weight: " + str(self.__min_weight) + " in store: " + str(self.__store_id)
        return "Weight basket constraint with min weight: " + str(self.__min_weight) + " and max weight: " + str(self.__max_weight) + " in store: " + str(self.__store_id)

    def get_constraint_string(self) -> str:
        return f"(weight_basket, {self.__min_weight}, {self.__max_weight}, {self.__store_id})"
    
# --------------- weight product constraint class  ---------------#
class WeightProductConstraint(Constraint):
    def __init__(self, min_weight: float, max_weight: float, product_id: int, store_id: int):
        if min_weight < 0:
            raise DiscountAndConstraintsError("Min weight is not valid", DiscountAndConstraintsErrorTypes.invalid_weight)
        
        if max_weight != -1 and max_weight < max_weight:
            raise DiscountAndConstraintsError("Max weight is not valid", DiscountAndConstraintsErrorTypes.invalid_weight)
        
        self.__min_weight = min_weight #if min_weight is 0, then there is no lower limit
        self.__max_weight = max_weight #if max_weight is -1, then there is no upper limit
        self.__product_id = product_id
        self.__store_id = store_id
        logger.info("[WeightProductConstraint]: Weight product constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        if basket_information.store_id != self.__store_id:
            logger.warning("[WeightProductConstraint]: Store id does not match the store id of the basket")
            return False
        
        for product in basket_information.products:
            if product.product_id == self.__product_id:
                if self.__max_weight == -1:
                    logger.info("[WeightProductConstraint]: Checking if the weight of the product is atleast" + str(self.__min_weight) + " kg")
                    return self.__min_weight <= product.weight
                logger.info("[WeightProductConstraint]: Checking if the weight of the product is between " + str(self.__min_weight) + " and " + str(self.__max_weight) + " kg")
                return self.__min_weight <= product.weight <= self.__max_weight
            
        logger.warn("[WeightProductConstraint]: Product not found in basket")
        return False
    
    @property
    def min_weight(self):
        return self.__min_weight
    
    @property
    def max_weight(self):
        return self.__max_weight
    
    @property
    def product_id(self):
        return self.__product_id
    
    @property
    def store_id(self):
        return self.__store_id
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "weight_product_constraint",
            "min_weight": self.__min_weight,
            "max_weight": self.__max_weight,
            "product_id": self.__product_id,
            "store_id": self.__store_id
            }
    
    def get_constraint_info_as_string(self) -> str:
        if self.__max_weight == -1:
            return "Weight product constraint with min weight: " + str(self.__min_weight) + " of product: " + str(self.__product_id) + " in store: " + str(self.__store_id)
        return "Weight product constraint with min weight: " + str(self.__min_weight) + " and max weight: " + str(self.__max_weight) + " of product: " + str(self.__product_id) + " in store: " + str(self.__store_id)
    
    def get_constraint_string(self) -> str:
        return f"(weight_product, {self.__min_weight}, {self.__max_weight}, {self.__product_id}, {self.__store_id})"
    
# --------------- weight category constraint class  ---------------#
class WeightCategoryConstraint(Constraint):
    def __init__(self, min_weight: float, max_weight: float, category_id: int):
        if min_weight < 0:
            raise DiscountAndConstraintsError("Min weight is not valid", DiscountAndConstraintsErrorTypes.invalid_weight)
        
        if max_weight != -1 and max_weight < max_weight:
            raise DiscountAndConstraintsError("Max weight is not valid", DiscountAndConstraintsErrorTypes.invalid_weight)
        
        self.__min_weight = min_weight #if min_weight is 0, then there is no lower limit
        self.__max_weight = max_weight #if max_weight is -1, then there is no upper limit
        self.__category_id = category_id
        logger.info("[WeightCategoryConstraint]: Weight category constraint created!")

    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        for curr_category in basket_information.categories:
            if curr_category.category_id == self.__category_id:
                products = curr_category.products
                for sub_categories in curr_category.sub_categories:
                    products += sub_categories.products
                category_total_weight: float = 0.0
                for product in products:
                    category_total_weight += product.weight

                if self.__max_weight == -1:
                    logger.info("[WeightCategoryConstraint]: Checking if the weight of the products of the categpry is atleast" + str(self.__min_weight) + " kg")
                    return self.__min_weight <= category_total_weight
                logger.info("[WeightCategoryConstraint]: Checking if the weight of the products of the categpry is between " + str(self.__min_weight) + " and " + str(self.__max_weight) + " kg")
                return self.__min_weight <= category_total_weight <= self.__max_weight
            
        logger.warn("[WeightCategoryConstraint]: Category not found in basket")
        return False
    
    @property
    def min_weight(self):
        return self.__min_weight
    
    @property
    def max_weight(self):
        return self.__max_weight
    
    @property
    def category_id(self):
        return self.__category_id
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "weight_category_constraint",
            "min_weight": self.__min_weight,
            "max_weight": self.__max_weight,
            "category_id": self.__category_id
            }
    
    def get_constraint_info_as_string(self) -> str:
        if self.__max_weight == -1:
            return "Weight category constraint with min weight: " + str(self.__min_weight) + " of category: " + str(self.__category_id)
        return "Weight category constraint with min weight: " + str(self.__min_weight) + " and max weight: " + str(self.__max_weight) + " of category: " + str(self.__category_id)


    def get_constraint_string(self) -> str:
        return f"(weight_category, {self.__min_weight}, {self.__max_weight}, {self.__category_id})"

# ------------------------------------ Composite Classes of Composite: ------------------------------------ #
# --------------- And constraint class ---------------#
class AndConstraint(Constraint):
    def __init__(self, constraint1: Constraint, constraint2: Constraint):
        self.__constraint1 = constraint1
        self.__constraint2 = constraint2
        logger.info("[AndConstraint]: And constraint created with two constraints")


    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[AndConstraint]: Checking if both constraints are satisfied")
        return self.__constraint1.is_satisfied(basket_information) and self.__constraint2.is_satisfied(basket_information)
    
    @property
    def constraint1(self):
        return self.__constraint1
    
    @property
    def constraint2(self):
        return self.__constraint2
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "and_constraint",
            "constraint1": self.__constraint1.get_constraint_info_as_dict(),
            "constraint2": self.__constraint2.get_constraint_info_as_dict()
            }
    
    def get_constraint_info_as_string(self) -> str:
        return self.__constraint1.get_constraint_info_as_string() + " and " + self.__constraint2.get_constraint_info_as_string()

    def get_constraint_string(self) -> str:
        return f"(and, {self.__constraint1.get_constraint_string()}, {self.__constraint2.get_constraint_string()})"
# --------------- Or constraint class ---------------#
class OrConstraint(Constraint):
    def __init__(self, constraint1: Constraint, constraint2: Constraint):
        self.__constraint1 = constraint1
        self.__constraint2 = constraint2
        logger.info("[OrConstraint]: Or constraint created with two constraints")


    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[OrConstraint]: Checking if at least one of the constraints is satisfied")
        return self.__constraint1.is_satisfied(basket_information) or self.__constraint2.is_satisfied(basket_information)
    
    @property
    def constraint1(self):
        return self.__constraint1
    
    @property
    def constraint2(self):
        return self.__constraint2
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "or_constraint",
            "constraint1": self.__constraint1.get_constraint_info_as_dict(),
            "constraint2": self.__constraint2.get_constraint_info_as_dict()
            }
    
    def get_constraint_info_as_string(self) -> str:
        return self.__constraint1.get_constraint_info_as_string() + " or " + self.__constraint2.get_constraint_info_as_string()
    
    def get_constraint_string(self) -> str:
        return f"(or, {self.__constraint1.get_constraint_string()}, {self.__constraint2.get_constraint_string()})"

# --------------- Xor constraint class ---------------#
class XorConstraint(Constraint):
    def __init__(self, constraint1: Constraint, constraint2: Constraint):
        self.__constraint1 = constraint1
        self.__constraint2 = constraint2
        logger.info("[XorConstraint]: Xor constraint created with two constraints")


    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[XorConstraint]: Checking if exactly one of the constraints is satisfied")
        return self.__constraint1.is_satisfied(basket_information) ^ self.__constraint2.is_satisfied(basket_information)
    
    @property
    def constraint1(self):
        return self.__constraint1
    
    @property
    def constraint2(self):
        return self.__constraint2
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "xor_constraint",
            "constraint1": self.__constraint1.get_constraint_info_as_dict(),
            "constraint2": self.__constraint2.get_constraint_info_as_dict()
            }
    
    def get_constraint_info_as_string(self) -> str:
        return self.__constraint1.get_constraint_info_as_string() + " xor " + self.__constraint2.get_constraint_info_as_string()

    def get_constraint_string(self) -> str:
        return f"(xor, {self.__constraint1.get_constraint_string()}, {self.__constraint2.get_constraint_string()})"
    
# --------------- Implies constraint class ---------------#
# this class is used to represent the implication between two constraints, where if the first constraint is satisfied, then the second constraint must be satisfied as well
class ImpliesConstraint(Constraint):
    def __init__(self, constraint1: Constraint, constraint2: Constraint):
        self.__constraint1 = constraint1
        self.__constraint2 = constraint2
        logger.info("[ImpliesConstraint]: Implies constraint created with two constraints")


    def is_satisfied(self, basket_information: BasketInformationForConstraintDTO) -> bool:
        logger.info("[ImpliesConstraint]: Checking if the first constraint implies the second constraint")
        return not self.__constraint1.is_satisfied(basket_information) or self.__constraint2.is_satisfied(basket_information)
    
    @property
    def constraint1(self):
        return self.__constraint1
    
    @property
    def constraint2(self):
        return self.__constraint2
    
    def get_constraint_info_as_dict(self) -> dict:
        return {
            "constraint_type": "implies_constraint",
            "constraint1": self.__constraint1.get_constraint_info_as_dict(),
            "constraint2": self.__constraint2.get_constraint_info_as_dict()
            }
    
    def get_constraint_info_as_string(self) -> str:
        return self.__constraint1.get_constraint_info_as_string() + " implies " + self.__constraint2.get_constraint_info_as_string()
    

    def get_constraint_string(self) -> str:
        return f"(implies, {self.__constraint1.get_constraint_string()}, {self.__constraint2.get_constraint_string()})"