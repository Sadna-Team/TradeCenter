import pytest
from backend.business.store.discount import *
from backend.business.store.constraints import *
from backend.business.DTOs import CategoryForDiscountDTO, BasketInformationForDiscountDTO, ProductForDiscountDTO, UserInformationForDiscountDTO, AddressDTO
from typing import List, Dict, Tuple
from datetime import date, datetime
from datetime import time


#Address default vars:     
default_address_id: int = 0
default_city: str = "city"
default_country: str = "country"
default_street: str = "street"
default_zip_code: str = "zip_code"
default_house_number: str = "house_number"

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
default_min_amount: int = 5
default_product_id: int = 0
default_store_id: int = 0

default_AmountProductConstraint: Constraint = AmountProductConstraint(default_min_amount, default_product_id, default_store_id)
#-----------------------------------

#CategoryDiscount default vars:
default_category_id: int = 0
default_applied_to_subcategories: bool = False

default_category_discount1: CategoryDiscount = CategoryDiscount(default_discount_id, default_discount_description, default_starting_date, default_ending_date, default_percentage, default_predicate, default_category_id, default_applied_to_subcategories)
default_category_discount2: CategoryDiscount = CategoryDiscount(default_discount_id, default_discount_description, default_starting_date, default_ending_date, default_percentage, default_predicate, 1, not default_applied_to_subcategories)
default_category_discount3: CategoryDiscount = CategoryDiscount(default_discount_id, default_discount_description, default_starting_date, default_ending_date, default_percentage, default_AmountProductConstraint, default_category_id, default_applied_to_subcategories)

#StoreDiscount default vars:
default_store_discount1: StoreDiscount = StoreDiscount(default_discount_id, default_discount_description, default_starting_date, default_ending_date, default_percentage2, default_predicate, default_store_id)

#ProductDiscount default vars:
default_product_discount1: ProductDiscount = ProductDiscount(default_discount_id, default_discount_description, default_starting_date, default_ending_date, default_percentage3, default_predicate, default_product_id, default_store_id)

#and discount default args:
default_discount_id2: int = 2
default_discount_id3: int = 3
default_discount_id4: int = 4
default_discount_id5: int = 5
default_discount_id6: int = 6
default_discount_id7: int = 7
default_discount_id8: int = 8
default_discount_id9: int = 9
default_discount_id10: int = 10
default_discount_id11: int = 11
default_discount_description2: str = "description"
default_starting_date2: datetime = datetime.now()
default_ending_date2: datetime = datetime(2025, 1, 1)
default_percentage6: float = 0.0

#AndDiscount default vars:
default_and_discount1: AndDiscount = AndDiscount(default_discount_id2, default_discount_description2, default_starting_date2, default_ending_date2, default_percentage6, default_category_discount1, default_category_discount2) #good
default_and_discount2: AndDiscount = AndDiscount(default_discount_id3, default_discount_description2, default_starting_date2, default_ending_date2, default_percentage6, default_category_discount1, default_category_discount3) #bad
default_and_discount3: AndDiscount = AndDiscount(default_discount_id4, default_discount_description2, default_starting_date2, default_ending_date2, default_percentage6,default_store_discount1, default_product_discount1) #good

#OrDiscount default vars:
default_or_discount1: OrDiscount = OrDiscount(default_discount_id5, default_discount_description2, default_starting_date2, default_ending_date2, default_percentage6, default_category_discount1, default_category_discount2) #good
default_or_discount2: OrDiscount = OrDiscount(default_discount_id6, default_discount_description2, default_starting_date2, default_ending_date2, default_percentage6, default_category_discount1, default_category_discount3) #good
default_or_discount3: OrDiscount = OrDiscount(default_discount_id7, default_discount_description2, default_starting_date2, default_ending_date2, default_percentage6, default_store_discount1, default_product_discount1) #good

#XorDiscount default vars:
default_xor_discount1: XorDiscount = XorDiscount(default_discount_id8, default_discount_description2, default_starting_date2, default_ending_date2, default_percentage6, default_category_discount1, default_category_discount2) #bad
default_xor_discount2: XorDiscount = XorDiscount(default_discount_id9, default_discount_description2, default_starting_date2, default_ending_date2, default_percentage6, default_category_discount1, default_category_discount3) #good

#maxDiscount default vars:
default_max_discount1: MaxDiscount = MaxDiscount(default_discount_id10, default_discount_description2, default_starting_date2, default_ending_date2, default_percentage6, [default_product_discount1, default_store_discount1])

#additiveDiscount default vars:
default_additive_discount1: AdditiveDiscount = AdditiveDiscount(default_discount_id11, default_discount_description2, default_starting_date2, default_ending_date2, default_percentage6,[default_product_discount1, default_store_discount1])




#DTOs:
#UserInformationForDiscountDTO
default_user_id1: int = 0
default_user_id2: int = 1
default_birthdate1: date = date(1990, 1, 1)
default_birthdate2: date = date(2009, 1, 1)

default_user_address: AddressDTO = AddressDTO(default_address_id, default_city, default_country, default_street, default_zip_code, default_house_number)
default_bad_user_address: AddressDTO = AddressDTO(1, "bad_city", "bad_country", default_street, default_zip_code, default_house_number)


user_information_dto1=  UserInformationForDiscountDTO(default_user_id1, default_birthdate1, default_user_address)

user_information_dto2=  UserInformationForDiscountDTO(default_user_id2, default_birthdate2, default_bad_user_address)



#ProductForDiscountDTO
default_product_price: float = 10
default_product_weight: float = 10
default_product_amount: int = 2

#ProductForDiscountDTO2
default_product_price2: float = 20
default_product_weight2: float = 20
default_product_amount2: int = 1


productForDiscountDTO = ProductForDiscountDTO(default_product_id, default_store_id, default_product_price, default_product_weight, default_product_amount)
productForDiscountDTO2 = ProductForDiscountDTO(1, default_store_id, default_product_price2, default_product_weight2, default_product_amount2)
#CategoryDTO
default_category_name: str = "category_name"
default_parent_category_id: int = 2
default_sub_categories: List[CategoryForDiscountDTO] = []
default_products: List[ProductForDiscountDTO] = [productForDiscountDTO]



categoryDTO= CategoryForDiscountDTO(default_category_id, default_category_name, default_parent_category_id, default_sub_categories, default_products)
categoryDTO2= CategoryForDiscountDTO(1, default_category_name, default_parent_category_id, [categoryDTO], [productForDiscountDTO2])


#BasketInformationForDiscountDTO
default_total_price_of_basket: float = 100  
default_time_of_purchase: datetime = datetime(2020, 1, 1)

basketInformationForDiscountDTO1= BasketInformationForDiscountDTO(default_store_id, default_products, default_total_price_of_basket, default_time_of_purchase, user_information_dto1, [categoryDTO])

basketInformationForDiscountDTO2= BasketInformationForDiscountDTO(default_store_id, default_products, default_total_price_of_basket, default_time_of_purchase, user_information_dto2, [categoryDTO, categoryDTO2])



#magic:
default_zero: float = 0.0

#Discount tests:

def test_change_discount_percentage():
    default_category_discount2.change_discount_percentage(0.2)
    assert default_category_discount2.percentage == 0.2
    
def test_is_simple_discount():
    assert default_category_discount1.is_simple_discount() == True
    
def test_is_conditional_discount():
    assert default_category_discount3.is_simple_discount() == False
    
#CategoryDiscount tests:

def test_calculate_category_discount():
    discount = default_zero
    for product in basketInformationForDiscountDTO1.products:
        if product in categoryDTO.products:
            discount += product.price * default_category_discount1.percentage * product.amount
        
    assert default_category_discount1.calculate_discount(basketInformationForDiscountDTO1) == discount
    
def test_calculate_category_discount2():
    discount = default_zero
    for category in basketInformationForDiscountDTO2.categories:
        if category.category_id == 1:
            products = set(category.products)
            for subCategory in category.sub_categories:
                products.update(set(subCategory.products))
        
            for product in products:
                discount += product.price * default_category_discount2.percentage * product.amount
            
    assert default_category_discount2.calculate_discount(basketInformationForDiscountDTO2) == discount
    
    
def test_discount_calculation_with_constraint():
    assert default_category_discount3.calculate_discount(basketInformationForDiscountDTO1) == default_zero
    
#StoreDiscount tests:
def test_calculate_store_discount():
    discount = default_zero
    for product in basketInformationForDiscountDTO1.products:
        discount += product.price * default_store_discount1.percentage * product.amount
    assert default_store_discount1.calculate_discount(basketInformationForDiscountDTO1) == discount
    

#ProductDiscount tests:

def test_calculate_product_discount():
    discount= default_zero
    for product in basketInformationForDiscountDTO1.products:
        if product in categoryDTO.products:
            discount += product.price * default_product_discount1.percentage * product.amount
    
    assert default_product_discount1.calculate_discount(basketInformationForDiscountDTO1) == discount
    
  
    
#AndDiscount tests:
def test_calculate_and_discount1():
    discount = default_category_discount1.calculate_discount(basketInformationForDiscountDTO1) + default_category_discount2.calculate_discount(basketInformationForDiscountDTO1)
    
    assert default_and_discount1.calculate_discount(basketInformationForDiscountDTO1) == discount
    
def test_calculate_and_discount3():
    discount = default_zero
    for product in basketInformationForDiscountDTO1.products:
        discount += product.price * default_store_discount1.percentage * product.amount
        discount += product.price * default_product_discount1.percentage * product.amount

    assert default_and_discount3.calculate_discount(basketInformationForDiscountDTO1) == discount
    
#OrDiscount tests:
def test_calculate_or_discount1():
    discount = default_zero
    for product in basketInformationForDiscountDTO1.products:
        if product in categoryDTO.products:
            discount += product.price * default_category_discount1.percentage * product.amount
        else:
            discount += product.price * default_category_discount2.percentage * product.amount
    
    assert default_or_discount1.calculate_discount(basketInformationForDiscountDTO1) == discount
    
def test_calculate_or_discount2():
    discount = default_zero
    for product in basketInformationForDiscountDTO1.products:
        if product in categoryDTO.products:
            discount += product.price * default_category_discount1.percentage * product.amount
        else:
            discount += product.price * default_category_discount3.percentage * product.amount
    
    assert default_or_discount2.calculate_discount(basketInformationForDiscountDTO1) == discount
    
def test_calculate_or_discount3():
    discount = default_zero
    for product in basketInformationForDiscountDTO1.products:
        discount += product.price * default_store_discount1.percentage * product.amount
        discount += product.price * default_product_discount1.percentage * product.amount
    assert default_or_discount3.calculate_discount(basketInformationForDiscountDTO1) == discount
    
    
#XorDiscount tests:

def test_calculate_xor_discount1():
    discount = default_zero
    products = set()
    for category in basketInformationForDiscountDTO1.categories:
        if category.category_id == 0:
            products.update(set(category.products))
            for subCategory in category.sub_categories:
                products.update(set(subCategory.products))

    for product in products:
        discount += product.price * default_category_discount1.percentage * product.amount
       
    assert default_xor_discount1.calculate_discount(basketInformationForDiscountDTO1) == discount
        
        
def test_calculate_xor_discount2():
    discount = default_zero
    for product in basketInformationForDiscountDTO1.products:
        if product in categoryDTO.products:
            discount += product.price * default_category_discount1.percentage * product.amount
        else:
            discount += product.price * default_category_discount3.percentage * product.amount
    
    assert default_xor_discount2.calculate_discount(basketInformationForDiscountDTO1) == discount
    
#maxDiscount tests:
def test_calculate_max_discount1():
    discount1 = default_zero
    discount2 = default_zero
    for product in basketInformationForDiscountDTO1.products:
        discount1 += product.price * default_store_discount1.percentage * product.amount
        discount2 += product.price * default_product_discount1.percentage * product.amount
        
    assert default_max_discount1.calculate_discount(basketInformationForDiscountDTO1) == max(discount1, discount2)
    
#additiveDiscount tests:
def test_calculate_additive_discount1():
    discount = default_zero
    for product in basketInformationForDiscountDTO1.products:
        discount += product.price * default_store_discount1.percentage * product.amount
        discount += product.price * default_product_discount1.percentage * product.amount
    assert default_additive_discount1.calculate_discount(basketInformationForDiscountDTO1) == discount
    





