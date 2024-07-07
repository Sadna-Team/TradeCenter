import pytest
from backend.business.store.constraints import *
from backend.business.DTOs import CategoryForConstraintDTO, BasketInformationForConstraintDTO, ProductForConstraintDTO, UserInformationForConstraintDTO
from typing import List, Dict, Tuple
from datetime import date, datetime
from datetime import time



#AgeConstraint default vars:
default_age_limit: int = 18

#Address default vars:     
default_address: str = "address"
default_city: str = "city"
default_state: str = "state"
default_country: str = "country"
default_zip_code: str = "zip_code"


#locationConstraint default vars:
default_location: AddressDTO = AddressDTO(default_address, default_city, default_state, default_country,default_zip_code)

#timeConstraint default vars:
default_start_time: time = time(0, 0, 0)
default_end_time: time = time(23, 59, 59)


#general default vars:
default_min_price: float = 0
default_max_price: float = 100
default_store_id: int = 0
default_product_id: int = 0
default_category_id: int = 0
default_min_amount: int = 0
default_max_amount: int = 20

default_min_weight: float = 0
default_max_weight: float = 100


#Constraints:
default_AgeConstraint: Constraint = AgeConstraint(default_age_limit)
default_LocationConstraint: Constraint = LocationConstraint(default_location)
default_TimeConstraint: Constraint = TimeConstraint(default_start_time, default_end_time)  
default_day_of_month_constraint: Constraint = DayOfMonthConstraint(1, 31)
default_day_of_week_constraint = DayOfWeekConstraint(0, 6)
default_season_constraint = SeasonConstraint("winter")
default_season_constraint_wrong = SeasonConstraint("summer")
default_holidays_of_country_constraint = HolidaysOfCountryConstraint("IL")



default_PriceBasketConstraint: Constraint = PriceBasketConstraint(default_min_price, default_max_price, default_store_id)
default_PriceProductConstraint: Constraint = PriceProductConstraint(default_min_price, default_max_price, default_product_id, default_store_id)
default_PriceCategoryConstraint: Constraint = PriceCategoryConstraint(default_min_price, default_max_price, default_category_id)
default_AmountBasketConstraint: Constraint = AmountBasketConstraint(default_min_amount,default_max_amount, default_store_id)
default_AmountProductConstraint: Constraint = AmountProductConstraint(default_min_amount, default_max_amount, default_product_id, default_store_id)
default_AmountCategoryConstraint: Constraint = AmountCategoryConstraint(default_min_amount,default_max_amount, default_category_id)
default_WeightBasketConstraint: Constraint = WeightBasketConstraint(default_min_weight, default_max_weight, default_store_id)
default_WeightProductConstraint: Constraint = WeightProductConstraint(default_min_weight, default_max_weight, default_product_id, default_store_id)
default_WeightCategoryConstraint: Constraint = WeightCategoryConstraint(default_min_weight, default_max_weight, default_category_id)


default_and_constraint: Constraint = AndConstraint(default_AgeConstraint, default_LocationConstraint)
default_or_constraint: Constraint = OrConstraint(default_AgeConstraint, default_LocationConstraint)
default_xor_constraint: Constraint = XorConstraint(default_AgeConstraint, default_PriceBasketConstraint)
default_implies_constraint: Constraint = ImpliesConstraint(default_AgeConstraint, default_LocationConstraint)


#DTOs:
#UserInformationForDiscountDTO
default_user_id1: int = 0
default_user_id2: int = 1
default_user_id3: int = 2
default_birthdate1: date = date(1990, 1, 1)
default_birthdate2: date = date(2009, 1, 1)
default_user_address: AddressDTO = AddressDTO(default_address, default_city, default_state, default_country, default_zip_code)
default_bad_user_address: AddressDTO = AddressDTO("bad_address", "bad_city", "bade_state", "bad_country", default_zip_code)


user_information_dto1=  UserInformationForConstraintDTO(default_user_id1, default_birthdate1, default_user_address)

user_information_dto2=  UserInformationForConstraintDTO(default_user_id2, default_birthdate2, default_bad_user_address)

guest_information_dto = UserInformationForConstraintDTO(default_user_id3,None, default_user_address)



#ProductForDiscountDTO
default_product_price: float = 10
default_product_weight: float = 10
default_product_amount: int = 10

productForDiscountDTO = ProductForConstraintDTO(default_product_id, default_store_id, default_product_price, default_product_weight, default_product_amount)

#CategoryDTO
default_category_name: str = "category_name"
default_parent_category_id: int = 2
default_sub_categories: List[CategoryForConstraintDTO] = []
default_products: List[ProductForConstraintDTO] = [productForDiscountDTO]

categoryDTO= CategoryForConstraintDTO(default_category_id, default_category_name, default_parent_category_id, default_sub_categories, default_products)

#BasketInformationForDiscountDTO
default_total_price_of_basket: float = 100  
default_time_of_purchase: datetime = datetime(2020, 1, 1)
default_time_of_purchase_holiday: datetime = datetime(2022, 9, 26)



basketInformationForDiscountDTO1= BasketInformationForConstraintDTO(default_store_id, default_products, default_total_price_of_basket, default_time_of_purchase, user_information_dto1, [categoryDTO])

basketInformationForDiscountDTO2= BasketInformationForConstraintDTO(default_store_id, default_products, default_total_price_of_basket, default_time_of_purchase, user_information_dto2, [categoryDTO])

basketInformationForDiscountDTO3 = BasketInformationForConstraintDTO(default_store_id, default_products, default_total_price_of_basket, default_time_of_purchase, guest_information_dto, [categoryDTO])

basketInformationForDiscountDTO4= BasketInformationForConstraintDTO(default_store_id, default_products, default_total_price_of_basket, default_time_of_purchase_holiday, user_information_dto1, [categoryDTO])

#AgeConstraint tests:
def test_AgeConstraint_is_satisfied():
    assert default_AgeConstraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
def test_AgeConstraint_is_not_satisfied():
    assert default_AgeConstraint.is_satisfied(basketInformationForDiscountDTO2) == False

def test_AgeConstraint_is_not_satisfied_guest():
    assert default_AgeConstraint.is_satisfied(basketInformationForDiscountDTO3) == False
    
    
#LocationConstraint tests:
def test_LocationConstraint_is_satisfied():
    assert default_LocationConstraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
def test_LocationConstraint_is_not_satisfied():
    assert default_LocationConstraint.is_satisfied(basketInformationForDiscountDTO2) == False
    
#TimeConstraint tests:
def test_TimeConstraint_is_satisfied():
    assert default_TimeConstraint.is_satisfied(basketInformationForDiscountDTO1) == True
    

#THESE 4 TESTS CAN SOMETIMES NOT WORK BUT ITS OKAY! (depends on the time of the test)


#DayOfMonthConstraint tests:
def test_DayOfMonthConstraint_is_satisfied():
    assert default_day_of_month_constraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
    
#DayOfWeekConstraint tests:
def test_DayOfWeekConstraint_is_satisfied():
    assert default_day_of_week_constraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
    
#SeasonConstraint tests:
def test_SeasonConstraint_is_satisfied():
    assert default_season_constraint.is_satisfied(basketInformationForDiscountDTO1) == True 
    assert default_season_constraint_wrong.is_satisfied(basketInformationForDiscountDTO1) == False 
    

#HolidaysOfCountryConstraint tests:
def test_HolidaysOfCountryConstraint_is_satisfied1():
    assert default_holidays_of_country_constraint.is_satisfied(basketInformationForDiscountDTO1) == False
    
def test_HolidaysOfCountryConstraint_is_satisfied2():
    assert default_holidays_of_country_constraint.is_satisfied(basketInformationForDiscountDTO4) == True
    
    
#PriceBasketConstraint tests:
def test_PriceBasketConstraint_is_satisfied():
    assert default_PriceBasketConstraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
    
#PriceProductConstraint tests:
def test_PriceProductConstraint_is_satisfied():
    assert default_PriceProductConstraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
    
#PriceCategoryConstraint tests:
def test_PriceCategoryConstraint_is_satisfied():
    assert default_PriceCategoryConstraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
#AmountBasketConstraint tests:
def test_AmountBasketConstraint_is_satisfied():
    assert default_AmountBasketConstraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
    
#AmountProductConstraint tests:
def test_AmountProductConstraint_is_satisfied():
    assert default_AmountProductConstraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
#AmountCategoryConstraint tests:
def test_AmountCategoryConstraint_is_satisfied():
    assert default_AmountCategoryConstraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
    
#WeightBasketConstraint tests:
def test_WeightBasketConstraint_is_satisfied():
    assert default_WeightBasketConstraint.is_satisfied(basketInformationForDiscountDTO1) == True
    

#WeightProductConstraint tests:
def test_WeightProductConstraint_is_satisfied():
    assert default_WeightProductConstraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
    
#WeightCategoryConstraint tests:
def test_WeightCategoryConstraint_is_satisfied():
    assert default_WeightCategoryConstraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
#AndConstraint tests:
def test_AndConstraint_is_satisfied():
    assert default_and_constraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
    
def test_AndConstraint_is_not_satisfied():
    assert default_and_constraint.is_satisfied(basketInformationForDiscountDTO2) == False


#OrConstraint tests:
def test_OrConstraint_is_satisfied():
    assert default_or_constraint.is_satisfied(basketInformationForDiscountDTO1) == True
    
#XorConstraint tests:
def test_XorConstraint_is_satisfied():
    assert default_xor_constraint.is_satisfied(basketInformationForDiscountDTO2) == True
    
    
#ImpliesConstraint tests:
def test_ImpliesConstraint_is_satisfied():
    assert default_implies_constraint.is_satisfied(basketInformationForDiscountDTO1) == True
