import pytest
from backend.business.store.PurchasePolicy import *
from backend.business.store.constraints import *
from backend.business.DTOs import CategoryForConstraintDTO, BasketInformationForConstraintDTO, ProductForConstraintDTO, UserInformationForConstraintDTO, AddressDTO
from typing import List, Dict, Tuple
from datetime import date, datetime
from datetime import time

from backend.business.store.discount import CategoryDiscount, ProductDiscount, StoreDiscount



#Address default vars:     
default_address: str = "address"
default_city: str = "city"
default_state: str = "state"
default_country: str = "country"
default_zip_code: str = "zip_code"

#Discount default vars:
default_discount_id: int = 0
default_discount_description: str = "description"
default_starting_date: datetime = datetime.now()
default_ending_date: datetime = datetime(2025, 1, 1)
default_percentage: float = 0.1
default_percentage2: float = 0.2
default_percentage3: float = 0.3
default_predicate: Optional[Constraint] = None

#-----------------------------------
    
#Constraints:
default_min_amount: int = 2
default_max_amount: int = -1
default_product_id: int = 0
default_store_id: int = 0
default_age_limit: int = 18

default_AgeConstraint: Constraint = AgeConstraint(default_age_limit)
default_AmountProductConstraint: Constraint = AmountProductConstraint(default_min_amount, default_max_amount, default_product_id, default_store_id)
default_day_of_month_constraint: Constraint = DayOfMonthConstraint(1, 31)
default_day_of_week_constraint = DayOfWeekConstraint(0, 6)
default_season_constraint = SeasonConstraint("winter")
default_season_constraint_wrong = SeasonConstraint("summer")
default_holidays_of_country_constraint = HolidaysOfCountryConstraint("IL")

#-----------------------------------

#CategoryDiscount default vars:
default_category_id: int = 0
default_category_2: int = 1
default_applied_to_subcategories: bool = False

default_category_discount1: CategoryDiscount = CategoryDiscount(default_discount_id, default_store_id, default_discount_description, default_starting_date, default_ending_date, default_percentage, default_predicate, default_category_id, default_applied_to_subcategories)
default_category_discount2: CategoryDiscount = CategoryDiscount(default_discount_id, default_store_id, default_discount_description, default_starting_date, default_ending_date, default_percentage, default_predicate, 1, not default_applied_to_subcategories)
default_category_discount3: CategoryDiscount = CategoryDiscount(default_discount_id, default_store_id, default_discount_description, default_starting_date, default_ending_date, default_percentage, default_AmountProductConstraint, default_category_id, default_applied_to_subcategories)

#StoreDiscount default vars:
default_store_discount1: StoreDiscount = StoreDiscount(default_discount_id, default_discount_description, default_starting_date, default_ending_date, default_percentage2, default_predicate, default_store_id)

#ProductDiscount default vars:
default_product_discount1: ProductDiscount = ProductDiscount(default_discount_id, default_discount_description, default_starting_date, default_ending_date, default_percentage3, default_predicate, default_product_id, default_store_id)




#policy default vars:
default_policy_id1: int = 0
default_policy_id2: int = 1
default_policy_id3: int = 2
default_policy_id4: int = 3
default_policy_id5: int = 4
default_policy_id6: int = 5
default_policy_id7: int = 6
default_policy_id8: int = 7
default_policy_id9: int = 8
default_policy_id10: int = 9
default_policy_id11: int = 10
default_policy_name: str = "policy_name"






#-----------------------------------------------------------------------------

#DTOs:
#UserInformationForDiscountDTO
default_user_id1: int = 0
default_user_id2: int = 1
default_birthdate1: date = date(1990, 1, 1)
default_birthdate2: date = date(2009, 1, 1)

default_user_address: AddressDTO = AddressDTO(default_address, default_city, default_state, default_country, default_zip_code)
default_bad_user_address: AddressDTO = AddressDTO("bad_address", "bad_city", "bad_state", "bad_country", default_zip_code)


user_information_dto1=  UserInformationForConstraintDTO(default_user_id1, default_birthdate1, default_user_address)

user_information_dto2=  UserInformationForConstraintDTO(default_user_id2, default_birthdate2, default_bad_user_address)



#ProductForDiscountDTO
default_product_price: float = 10
default_product_weight: float = 10
default_product_amount: int = 2

#ProductForDiscountDTO2
default_product_price2: float = 20
default_product_weight2: float = 20
default_product_amount2: int = 1


productForDiscountDTO = ProductForConstraintDTO(default_product_id, default_store_id, default_product_price, default_product_weight, default_product_amount)
productForDiscountDTO2 = ProductForConstraintDTO(1, default_store_id, default_product_price2, default_product_weight2, default_product_amount2)

#CategoryDTO
default_category_name: str = "category_name"
default_parent_category_id: int = 2
default_sub_categories: List[CategoryForConstraintDTO] = []
default_products: List[ProductForConstraintDTO] = [productForDiscountDTO]


categoryDTO= CategoryForConstraintDTO(default_category_id, default_category_name, default_parent_category_id, default_sub_categories, default_products)
categoryDTO2= CategoryForConstraintDTO(1, default_category_name, default_parent_category_id, [categoryDTO], [productForDiscountDTO2])


#BasketInformationForDiscountDTO
default_total_price_of_basket: float = 100  
default_time_of_purchase: datetime = datetime(2020, 1, 1)

basketInformationForDiscountDTO1= BasketInformationForConstraintDTO(default_store_id, default_products, default_total_price_of_basket, default_time_of_purchase, user_information_dto1, [categoryDTO])
basketInformationForDiscountDTO2= BasketInformationForConstraintDTO(default_store_id, default_products, default_total_price_of_basket, default_time_of_purchase, user_information_dto2, [categoryDTO, categoryDTO2])

#-----------------------------------------------------------------------------

#creating the policies:

#ProductSpecificPurchasePolicy
productSpecificPurchasePolicy1 = ProductSpecificPurchasePolicy(default_policy_id1, default_store_id, default_policy_name, default_product_id, default_predicate)
productSpecificPurchasePolicy2 = ProductSpecificPurchasePolicy(default_policy_id2, default_store_id, default_policy_name, 1, default_AmountProductConstraint)
productSpecificPurchasePolicy3 = ProductSpecificPurchasePolicy(default_policy_id3, default_store_id, default_policy_name, default_product_id, default_season_constraint)
productSpecificPurchasePolicy4 = ProductSpecificPurchasePolicy(default_policy_id4, default_store_id, default_policy_name, default_product_id, default_season_constraint_wrong)

#CategorySpecificPurchasePolicy
categorySpecificPurchasePolicy1 = CategorySpecificPurchasePolicy(default_policy_id3, default_store_id, default_policy_name, default_category_2, default_AgeConstraint)


#BasketSpecificPurchasePolicy
basketSpecificPurchasePolicy1 = BasketSpecificPurchasePolicy(default_policy_id5, default_store_id, default_policy_name, default_predicate)


#andPurchasePolicy
andPurchasePolicy1 = AndPurchasePolicy(default_policy_id6, default_store_id, default_policy_name, productSpecificPurchasePolicy3, productSpecificPurchasePolicy2, default_predicate) # good
andPurchasePolicy2 = AndPurchasePolicy(default_policy_id7, default_store_id, default_policy_name, productSpecificPurchasePolicy4, productSpecificPurchasePolicy2, default_predicate) # bad


#OrPurchasePolicy
orPurchasePolicy = OrPurchasePolicy(default_policy_id7, default_store_id, default_policy_name, productSpecificPurchasePolicy4, productSpecificPurchasePolicy2, default_predicate) # good


#conditioningPurchasePolicy
conditioningPurchasePolicy1 = ConditioningPurchasePolicy(default_policy_id8, default_store_id, default_policy_name, productSpecificPurchasePolicy2, productSpecificPurchasePolicy3, default_predicate) # good
conditioningPurchasePolicy2 = ConditioningPurchasePolicy(default_policy_id9, default_store_id, default_policy_name, productSpecificPurchasePolicy2, productSpecificPurchasePolicy4, default_predicate) # bad


#Purchase Policy tests:
#-----------------------------------------------------
#ProductSpecificPurchasePolicy tests:

def test_product_specific1():
    assert productSpecificPurchasePolicy1.check_constraint(basketInformationForDiscountDTO1) == True
    
def test_product_specific2():
    assert productSpecificPurchasePolicy2.check_constraint(basketInformationForDiscountDTO1) == True
    
def test_product_specific3():
    assert productSpecificPurchasePolicy3.check_constraint(basketInformationForDiscountDTO1) == True
    
def test_product_specific4():
    assert productSpecificPurchasePolicy4.check_constraint(basketInformationForDiscountDTO1) == False
    
    
#CategorySpecificPurchasePolicy tests:
def test_category_specific1():
    assert categorySpecificPurchasePolicy1.check_constraint(basketInformationForDiscountDTO1) == True
    
def test_category_specific2():
    assert categorySpecificPurchasePolicy1.check_constraint(basketInformationForDiscountDTO2) == False
    
#BasketSpecificPurchasePolicy tests:
def test_basket_specific1():
    assert basketSpecificPurchasePolicy1.check_constraint(basketInformationForDiscountDTO1) == True
    
#AndPurchasePolicy tests:
def test_and_purchase1():
    assert andPurchasePolicy1.check_constraint(basketInformationForDiscountDTO1) == True
    
def test_and_purchase2():
    assert andPurchasePolicy2.check_constraint(basketInformationForDiscountDTO1) == False

#OrPurchasePolicy tests:
def test_or_purchase1():
    assert orPurchasePolicy.check_constraint(basketInformationForDiscountDTO1) == True
    
#ConditioningPurchasePolicy tests:
def test_conditioning_purchase1():
    assert conditioningPurchasePolicy1.check_constraint(basketInformationForDiscountDTO1) == True
    
def test_conditioning_purchase2():
    assert conditioningPurchasePolicy2.check_constraint(basketInformationForDiscountDTO1) == False


