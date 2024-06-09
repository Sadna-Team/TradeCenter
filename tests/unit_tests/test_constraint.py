import pytest
from backend.business.store.constraints import *
from backend.business.DTOs import CategoryForDiscountDTO, BasketInformationForDiscountDTO, ProductForDiscountDTO, UserInformationForDiscountDTO
from typing import List, Dict, Tuple
from datetime import date, datetime
from datetime import time



#AgeConstraint default vars:
default_age_limit: int = 18

#Address default vars:     
default_address_id: int = 0
default_city: str = "city"
default_country: str = "country"
default_street: str = "street"
default_zip_code: str = "zip_code"
default_house_number: str = "house_number"


#locationConstraint default vars:
default_location: AddressDTO = AddressDTO(default_address_id, default_city, default_country, default_street, default_zip_code, default_house_number)

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

default_min_weight: float = 0
default_max_weight: float = 100


#Constraints:
default_AgeConstraint: Constraint = AgeConstraint(default_age_limit)
default_LocationConstraint: Constraint = LocationConstraint(default_location)
default_TimeConstraint: Constraint = TimeConstraint(default_start_time, default_end_time)  
default_PriceBasketConstraint: Constraint = PriceBasketConstraint(default_min_price, default_max_price, default_store_id)
default_PriceProductConstraint: Constraint = PriceProductConstraint(default_min_price, default_max_price, default_product_id, default_store_id)
default_PriceCategoryConstraint: Constraint = PriceCategoryConstraint(default_min_price, default_max_price, default_category_id)
default_AmountBasketConstraint: Constraint = AmountBasketConstraint(default_min_amount, default_store_id)
default_AmountProductConstraint: Constraint = AmountProductConstraint(default_min_amount, default_product_id, default_store_id)
default_AmountCategoryConstraint: Constraint = AmountCategoryConstraint(default_min_amount, default_category_id)
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
default_user_address: AddressDTO = AddressDTO(default_address_id, default_city, default_country, default_street, default_zip_code, default_house_number)
default_bad_user_address: AddressDTO = AddressDTO(1, "bad_city", "bad_country", default_street, default_zip_code, default_house_number)


user_information_dto1=  UserInformationForDiscountDTO(default_user_id1, default_birthdate1, default_user_address)

user_information_dto2=  UserInformationForDiscountDTO(default_user_id2, default_birthdate2, default_bad_user_address)

guest_information_dto = UserInformationForDiscountDTO(default_user_id3,None, default_user_address)



#ProductForDiscountDTO
default_product_price: float = 10
default_product_weight: float = 10
default_product_amount: int = 10

productForDiscountDTO = ProductForDiscountDTO(default_product_id, default_store_id, default_product_price, default_product_weight, default_product_amount)

#CategoryDTO
default_category_name: str = "category_name"
default_parent_category_id: int = 2
default_sub_categories: List[CategoryForDiscountDTO] = []
default_products: List[ProductForDiscountDTO] = [productForDiscountDTO]

categoryDTO= CategoryForDiscountDTO(default_category_id, default_category_name, default_parent_category_id, default_sub_categories, default_products)

#BasketInformationForDiscountDTO
default_total_price_of_basket: float = 100  
default_time_of_purchase: datetime = datetime(2020, 1, 1)

basketInformationForDiscountDTO1= BasketInformationForDiscountDTO(default_store_id, default_products, default_total_price_of_basket, default_time_of_purchase, user_information_dto1, [categoryDTO])

basketInformationForDiscountDTO2= BasketInformationForDiscountDTO(default_store_id, default_products, default_total_price_of_basket, default_time_of_purchase, user_information_dto2, [categoryDTO])

basketInformationForDiscountDTO3 = BasketInformationForDiscountDTO(default_store_id, default_products, default_total_price_of_basket, default_time_of_purchase, guest_information_dto, [categoryDTO])


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