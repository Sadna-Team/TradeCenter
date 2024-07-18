from datetime import date, datetime, time
from typing import Dict

import pytest
from backend.business.store.constraints import AgeConstraint, AndConstraint, LocationConstraint
from backend.business.store.discount import StoreDiscount
from backend.business.store.new_store import Product, Category, StoreFacade, create_store
from backend.business.DTOs import AddressDTO, ProductDTO, PurchaseUserDTO, UserInformationForConstraintDTO
from backend.error_types import *
from backend.app_factory import create_app_instance

@pytest.fixture
def app():
    app = create_app_instance('testing')
    from backend.database import clear_database
    with app.app_context():
        clear_database()
        yield app

@pytest.fixture
def product():
    return Product(store_id=0, product_id=0, product_name='product', description='very good product', price=10.0, weight=30.0, amount=10)

@pytest.fixture
def tagged_product(product):
    product.add_tag('tag')
    return product

@pytest.fixture
def category():
    return Category(category_id=0, category_name='category')

@pytest.fixture
def category2():
    return Category(category_id=3, category_name='alcohol')


@pytest.fixture
def sub_category(category):
    return Category(category_id=1, category_name='sub_category')

@pytest.fixture
def subsub_category(sub_category):
    return Category(category_id=2, category_name='subsub_category')

@pytest.fixture
def store(app):
    address = AddressDTO('address', 'city', 'state', 'country', 'zip_code')
    return create_store(address=address, store_name='store', store_founder_id=0)

@pytest.fixture
def product_dto():
    return ProductDTO(product_id=0, name='product', description='very good product', price=10.0, tags=['tag'], weight=30.0, amount=10)

@pytest.fixture
def product_dto3():
    return ProductDTO(product_id=1, name='product2', description='very good product', price=10.0, tags=['tag'], weight=30.0, amount=10)

@pytest.fixture
def product_dto2():
    return ProductDTO(product_id=3, name='product3', description='alcohol!', price=10.0, tags=['tag'], weight=30.0, amount=10)


@pytest.fixture
def store_facade(app):
    StoreFacade().clean_data()
    return StoreFacade()

#Address default vars:     
default_address: str ="address"
default_city: str = "city"
default_state: str = "state"
default_country: str = "country"
default_zip_code: str = "zip_code"
default_location: AddressDTO = AddressDTO(default_address, default_city, default_state, default_country, default_zip_code)
user_information_dto1=  UserInformationForConstraintDTO(0, date(1990, 1, 1), default_location)
user_information_dto2=  UserInformationForConstraintDTO(1, date(2009, 1, 1), default_location)



#magic:
default_zero: float = 0.0
product_price_10: float =10.0
product_price_20 : float =20.0
product_per_005: float =0.05
product_per_02: float =0.2
product_per_017: float =0.17
product_per_05: float =0.5
product_per_01 : float =0.1





       
def test_add_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount',store_id, datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,None,None)
    assert len(store_facade.discounts) == 1
    assert store_facade.discounts[0].discount_description == 'discount'
    assert store_facade.discounts[0].starting_date == datetime(2020, 1, 1)
    assert store_facade.discounts[0].ending_date == datetime(2020, 1, 2)
    assert store_facade.discounts[0].percentage == 0.1
    assert isinstance(store_facade.discounts[0], StoreDiscount)
    assert store_facade.discounts[0].store_id == store_id
    
    
def test_add_discount_fail(store_facade):
    with pytest.raises(DiscountAndConstraintsError) as e:
        store_facade.add_discount('discount',99, datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,None,None)
    assert e.value.discount_error_type == DiscountAndConstraintsErrorTypes.discount_creation_error
    
def test_add_discount_fail_percentage_too_high(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    with pytest.raises(DiscountAndConstraintsError) as e:
        store_facade.add_discount('discount',store_id, datetime(2020, 1, 1), datetime(2020, 1, 2), 1.1,None,None,None)
    assert e.value.discount_error_type == DiscountAndConstraintsErrorTypes.invalid_percentage

def test_add_discount_fail_percentage_too_low(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    with pytest.raises(DiscountAndConstraintsError) as e:
        store_facade.add_discount('discount', store_id,datetime(2020, 1, 1), datetime(2020, 1, 2), -0.1,None,None,None)
    assert e.value.discount_error_type == DiscountAndConstraintsErrorTypes.invalid_percentage

        
def test_remove_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount', store_id,datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,None,None)
    assert len(store_facade.discounts) == 1
    store_facade.remove_discount(0)
    assert len(store_facade.discounts) == 0
    
def test_remove_discount_fail(store_facade):
    with pytest.raises(DiscountAndConstraintsError) as e:
        store_facade.remove_discount(0)
    assert e.value.discount_error_type == DiscountAndConstraintsErrorTypes.discount_not_found
        
    
def test_change_discount_description(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount',store_id, datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,None,None)
    store_facade.change_discount_description(0, 'new description')
    assert store_facade.discounts[0].discount_description == 'new description'
    
def test_change_discount_description_fail(store_facade):
    with pytest.raises(DiscountAndConstraintsError) as e:
        store_facade.change_discount_description(0, 'new description')
    assert e.value.discount_error_type == DiscountAndConstraintsErrorTypes.discount_not_found
        
def test_change_discount_percentage(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount',store_id, datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,None,None)
    store_facade.change_discount_percentage(0, 0.2)
    assert store_facade.discounts[0].percentage == 0.2
    
def test_change_discount_percentage_fail(store_facade):
    with pytest.raises(DiscountAndConstraintsError) as e:
        store_facade.change_discount_percentage(0, 20.0)
    assert e.value.discount_error_type == DiscountAndConstraintsErrorTypes.discount_not_found
        
     
def test_create_logical_composite_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount1',store_id, datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,None,None)
    store_facade.add_discount('discount2', store_id,datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,None,None)
    assert len(store_facade.discounts) == 2
    new_id=store_facade.create_logical_composite_discount('composite discount',store_id, datetime(2020, 1, 1), datetime(2020, 1, 2), -1, 0, 1, 1)
    assert len(store_facade.discounts) == 1
    assert store_facade.discounts[new_id].discount_description == 'composite discount'
    assert store_facade.discounts[new_id].starting_date == datetime(2020, 1, 1)
    assert store_facade.discounts[new_id].ending_date == datetime(2020, 1, 2)
    
    
    
def test_create_logical_composite_discount_fail(store_facade):
    with pytest.raises(DiscountAndConstraintsError) as e:
        store_facade.create_logical_composite_discount('composite discount',0, datetime(2020, 1, 1), datetime(2020, 1, 2), -1, 0, 1, 0)
    assert e.value.discount_error_type == DiscountAndConstraintsErrorTypes.discount_creation_error
 
  
def test_create_numerical_composite_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount1',store_id, datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,None,None)
    store_facade.add_discount('discount2', store_id,datetime(2020, 1, 1), datetime(2020, 1, 2), 0.4,None,None,None)
    assert len(store_facade.discounts) == 2
    new_id=store_facade.create_numerical_composite_discount('composite discount',store_id, datetime(2020, 1, 1), datetime(2020, 1, 2), -1, [0, 1], 1)
    assert len(store_facade.discounts) == 1
    assert store_facade.discounts[new_id].discount_description == 'composite discount'
    assert store_facade.discounts[new_id].starting_date == datetime(2020, 1, 1)
    assert store_facade.discounts[new_id].ending_date == datetime(2020, 1, 2)
    
def test_create_numerical_composite_discount_fail(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    with pytest.raises(DiscountAndConstraintsError) as e:
        store_facade.create_numerical_composite_discount('composite discount',store_id, datetime(2020, 1, 1), datetime(2020, 1, 2), -1, [0, 1], 0)       
    assert e.value.discount_error_type == DiscountAndConstraintsErrorTypes.invalid_type_of_composite_discount


def test_assign_predicate_to_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    discount_id1 = store_facade.add_discount('discount1',store_id, datetime(2020, 1, 1), datetime(2025, 1, 2), 0.1,None,None,None)
    #34 euro
    assert len(store_facade.discounts) == 1
    store_facade.assign_predicate_to_discount(discount_id1,('age',18))
    assert isinstance(store_facade.discounts[0].predicate, AgeConstraint)
    
    
def test_assign_predicate_to_discount2(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    discount_id1 = store_facade.add_discount('discount1',store_id, datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,None,None)
    locations: Dict = {'address': 'address', 'city': 'city', 'state': 'state', 'country': 'country', 'zip_code': 'zip_code'}
    store_facade.assign_predicate_to_discount(discount_id1,('and', ('location',locations) , ('time', 10, 0, 12, 0)))
    assert isinstance(store_facade.discounts[0].predicate, AndConstraint)
    
    
        
def test_get_total_price_before_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('product', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(0, 10)
    shopping_basket= {product_id:3}
    total_before_discount=shopping_basket[product_id]*product_price_10 #30
    shopping_cart= {store_id: shopping_basket}
    assert store_facade.get_total_price_before_discount(shopping_cart)==total_before_discount

   
def test_get_total_basket_price_before_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('product', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(0, 10)
    store_facade.add_discount('discount1',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), 0.5,None,None,None)
    shopping_basket= {product_id:3}
    total_before_discount=shopping_basket[product_id]*product_price_10 #30
    assert store_facade.get_total_basket_price_before_discount(store_id,shopping_basket)==total_before_discount

def test_get_total_price_after_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('product', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(0, 10)
    store_facade.add_discount('discount1', store_id,datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_05,None,None,None)
    shopping_basket= {product_id:3}
    total_before_discount=shopping_basket[product_id]*product_price_10 #30
    shopping_cart = {store_id: shopping_basket}
    assert store_facade.get_total_price_after_discount(shopping_cart, user_information_dto1)==total_before_discount-(total_before_discount*product_per_05) #15
   
    
def test_assign_predicate_to_discount_fail(store_facade):
    with pytest.raises(DiscountAndConstraintsError) as e:
        store_facade.assign_predicate_to_discount(0,('age',18))
    assert e.value.discount_error_type == DiscountAndConstraintsErrorTypes.discount_not_found


#specific unit tests that are requested in version 2:

#1. discount of 50% on all milk category products:
def test_apply_milk_category_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('product', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(product_id, 10)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id)
    store_facade.add_discount('discount1',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_05,category_id,None,False)
    shopping_basket= {product_id:3}
    total_price_of_basket= shopping_basket[product_id]*product_price_10
    assert store_facade.apply_discount(0, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==total_price_of_basket* product_per_05
    
#2. discount of 20% on all products in the store:
def test_apply_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('product', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(0, 10)
    store_facade.add_discount('discount1',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_05,None,None,None)
    shopping_basket= {product_id:3}
    total_price_of_basket= shopping_basket[product_id]*product_price_10
    assert store_facade.apply_discount(0, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==total_price_of_basket* product_per_05

#3. discount of 10% on tomatoes on a purchase that costs more than 200: (predicate)
def test_apply_tomatoes_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('tomatoes', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(0, 50)
    discount_id = store_facade.add_discount('discount1', store_id,datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_01,None,None,None)
    shopping_basket = {product_id:21}
    total_price_of_basket=shopping_basket[product_id]*product_price_10
    store_facade.assign_predicate_to_discount(discount_id, ('price_basket', 200.0, -1.0, store_id))
    assert store_facade.apply_discount(0, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==total_price_of_basket* product_per_01

#4. discount on milk products or bread products but not on both (XOR):
def test_apply_milk_or_bread_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', product_price_10, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('bread', 'very good product', product_price_10, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    category_id2 = store_facade.add_category('bread')
    store_facade.assign_product_to_category(category_id2, store_id,product_id2)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    #milk discount
    store_facade.add_discount('discount1',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_01,category_id,None,False)
    #bread discount
    store_facade.add_discount('discount2', store_id,datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_01,category_id2,None,False)
    shopping_basket= {product_id1:21, product_id2:21}
    total_price_of_basket=shopping_basket[product_id1]*product_price_10+shopping_basket[product_id2]*product_price_10
    
    new_id = store_facade.create_logical_composite_discount('composite discount',store_id, datetime(2020, 1, 1), datetime(2020, 1, 2), -1, 0, 1, 3)
    assert store_facade.apply_discount(new_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==(shopping_basket[product_id1]*product_price_10)* product_per_01 #21


#4.5 same test but with AND:
def test_apply_milk_and_bread_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', product_price_10, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('bread', 'very good product', product_price_10, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    category_id2 = store_facade.add_category('bread')
    store_facade.assign_product_to_category(category_id2, store_id,product_id2)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    #milk discount
    store_facade.add_discount('discount1',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_01,category_id,None,False)
    #bread discount
    store_facade.add_discount('discount2',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_01,category_id2,None,False)
    shopping_basket= {product_id1:21, product_id2:21}
    total_price_of_basket=shopping_basket[product_id1]*product_price_10+shopping_basket[product_id2]*product_price_10
    new_id = store_facade.create_logical_composite_discount('composite discount',store_id, datetime(2020, 1, 1), datetime(2020, 1, 2), -1, 0, 1, 1)
    assert store_facade.apply_discount(new_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)== total_price_of_basket* product_per_01 #42 

#4.5 same test but with OR:
def test_apply_milk_or_bread_discount2(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', product_price_10, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('bread', 'very good product', product_price_10, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    category_id2 = store_facade.add_category('bread')
    store_facade.assign_product_to_category(category_id2, store_id,product_id2)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    #milk discount
    store_facade.add_discount('discount1',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_01,category_id,None,False)
    #bread discount
    store_facade.add_discount('discount2', store_id,datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_01,category_id2,None,False)
    shopping_basket= {product_id1:21, product_id2:21}
    total_price_of_basket=shopping_basket[product_id1]*product_price_10+shopping_basket[product_id2]*product_price_10
    new_id = store_facade.create_logical_composite_discount('composite discount',store_id, datetime(2020, 1, 1), datetime(2020, 1, 2), -1, 0, 1, 2)
    assert store_facade.apply_discount(new_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)== total_price_of_basket* product_per_01 #42 
    
#5 there is a baked goods discount of 5% on bread or baguette products only if the cart contains at least 5 bread and at least 2 cakes:
def test_apply_baked_goods_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('bread', 'very good product', product_price_10, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('cake', 'very good product', product_price_10, ['tag'], 30.0)
    category_id = store_facade.add_category('baked goods')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    store_facade.assign_product_to_category(category_id, store_id,product_id2)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    #bread discount
    temp1 = store_facade.add_discount('bread_discount',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_005,None,product_id1,None)
    store_facade.assign_predicate_to_discount(temp1, ('amount_product', 5, -1,product_id1, store_id))
    #cake discount
    temp2 = store_facade.add_discount('cake_discount', store_id,datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_005,None,product_id2,None)
    store_facade.assign_predicate_to_discount(temp2, ('amount_product', 2, -1, product_id2, store_id))
    
    
    discount_id = store_facade.create_logical_composite_discount('bread_and_cake',store_id, datetime(2020, 1, 1), datetime(2050, 1, 2), -1, temp1, temp2, 1)
    shopping_basket= {product_id1:1, product_id2:1}
    total_price_of_basket=shopping_basket[product_id1]*product_price_10+shopping_basket[product_id2]*product_price_10
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==default_zero #0.0

    shopping_basket= {product_id1:1, product_id2:2}
    total_price_of_basket= shopping_basket[product_id1]*product_price_10+shopping_basket[product_id2]*product_price_10
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==default_zero #0.0

    
    shopping_basket= {product_id1:5, product_id2:1}
    total_price_of_basket=shopping_basket[product_id1]*product_price_10+shopping_basket[product_id2]*product_price_10
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==default_zero #0.0

    
    shopping_basket= {product_id1:5, product_id2:2}
    total_price_of_basket=shopping_basket[product_id1]*product_price_10+shopping_basket[product_id2]*product_price_10
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==total_price_of_basket*product_per_005 #3.5

#6. discount of 5% on milk products if the cart contains at least 3 cottege cheese products or at least 2 yugurts:
def test_apply_milk_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', product_price_10, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('cottage cheese', 'very good product', product_price_10, ['tag'], 30.0)
    product_id3 = store_facade.get_store_by_id(store_id).add_product('yogurt', 'very good product', product_price_10, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    store_facade.assign_product_to_category(category_id, store_id,product_id2)
    store_facade.assign_product_to_category(category_id, store_id,product_id3)
    
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id3, 50)
    #milk discount
    discount_id = store_facade.add_discount('milk_discount',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_005,category_id,None,False)
    store_facade.assign_predicate_to_discount(discount_id, ('or', ('amount_product', 2, -1, product_id3, store_id) ,('amount_product', 3,-1, product_id2, store_id)))
    
    shopping_basket= {product_id2:1, product_id3:1}
    total_price_of_basket=shopping_basket[product_id2]*product_price_10+shopping_basket[product_id3]*product_price_10
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==default_zero #0.0
    

    shopping_basket= {product_id2:1, product_id3:3}
    total_price_of_basket=shopping_basket[product_id2]*product_price_10+shopping_basket[product_id3]*product_price_10
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)== total_price_of_basket*product_per_005 #2
    
    
    shopping_basket= {product_id2:3, product_id3:1}
    total_price_of_basket=shopping_basket[product_id2]*product_price_10+shopping_basket[product_id3]*product_price_10
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==total_price_of_basket*product_per_005 #2

    
    shopping_basket= {product_id2:3, product_id3:3}
    total_price_of_basket=shopping_basket[product_id2]*product_price_10+shopping_basket[product_id3]*product_price_10
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==total_price_of_basket*product_per_005 #3.0
    
    
    
#7 if the cart total is more than 100 and the cart contains at least 3 pasts products, there is a 5% discount on milk product:
def test_apply_milk_discount2(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', product_price_10, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('pasta', 'very good product', product_price_10, ['tag'], 30.0)
    product_id3 = store_facade.get_store_by_id(store_id).add_product('fromage', 'une fromage tres jaune', product_price_20, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    store_facade.assign_product_to_category(category_id, store_id,product_id3)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id3, 50)
    #pasta discount
    discount_id = store_facade.add_discount('milk_discount',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_005,category_id,None,False)
    store_facade.assign_predicate_to_discount(discount_id, ('and', ('amount_product', 3,-1, product_id2, store_id), ('price_basket', 100.0, -1.0, store_id)))
    
    shopping_basket= {product_id1:1, product_id2:1, product_id3:1}
    total_price_of_basket=shopping_basket[product_id1]*product_price_10 + shopping_basket[product_id2]*product_price_10 + shopping_basket[product_id3]*product_price_20
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==default_zero #0.0
    
    
    shopping_basket= {product_id1:1, product_id2:3, product_id3:1}
    total_price_of_basket=shopping_basket[product_id1]*product_price_10 + shopping_basket[product_id2]*product_price_10 + shopping_basket[product_id3]*product_price_20
    
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==default_zero #0.0
    
    
    shopping_basket= {product_id1:10, product_id2:1, product_id3: 5}
    total_price_of_basket=shopping_basket[product_id1]*product_price_10 + shopping_basket[product_id2]*product_price_10 + shopping_basket[product_id3]*product_price_20
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==default_zero #0.0
    
    
    shopping_basket= {product_id1:10, product_id2:3,product_id3: 5}
    total_price_of_basket=230.0
    total_price_of_milk_products_in_basket=shopping_basket[product_id1]*product_price_10+ shopping_basket[product_id3]*product_price_20
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)== total_price_of_milk_products_in_basket*product_per_005 #10.0
    
    
    
#8. the discount that is given is the max between 5% of the pastas in the cart, and 20% of milk bottles in the cart:
def test_apply_max_discount(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', product_price_10, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('pasta', 'very good product', product_price_10, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    #pasta discount
    discount_id1 = store_facade.add_discount('pasta_discount',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_005,None,product_id2,None)
    #milk discount
    discount_id2 = store_facade.add_discount('milk_discount',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_02,category_id,None,False)
    
    
    discount_id = store_facade.create_numerical_composite_discount('max_discount',store_id, datetime(2020, 1, 1), datetime(2050, 1, 2), -1,[ discount_id1, discount_id2], 1)
    shopping_basket= {product_id1:1, product_id2:1}
    total_price_of_basket=shopping_basket[product_id1]*product_price_10 + shopping_basket[product_id2]*product_price_10 #20.0
    total_price_of_milk_in_basket=shopping_basket[product_id1]*product_price_10
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==total_price_of_milk_in_basket*product_per_02
    
    shopping_basket= {product_id1:1, product_id2:3}
    total_price_of_basket=shopping_basket[product_id1]*product_price_10 + shopping_basket[product_id2]*product_price_10 #40.0
    total_price_of_milk_in_basket=shopping_basket[product_id1]*product_price_10
    
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==total_price_of_milk_in_basket*product_per_02
    
    shopping_basket= {product_id1:10, product_id2:1}
    total_price_of_basket = shopping_basket[product_id1]*product_price_10 + shopping_basket[product_id2]*product_price_10 #120.0 
    total_price_of_milk_in_basket=shopping_basket[product_id1]*product_price_10
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)== total_price_of_milk_in_basket*product_per_02
    
    
    
#9. there is 5% discount on milk products and there is 20% discount on each store (so 25% discount on milk products):
def test_apply_additive_discount(store_facade):
    store_id= store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', product_price_10, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    #milk discount
    discount_id1 = store_facade.add_discount('milk_discount',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_005,category_id,None,False)
    #store discount
    discount_id2 = store_facade.add_discount('store_discount',store_id, datetime(2020, 1, 1), datetime(2030, 1, 2), product_per_02,None,None,None)
    
    discount_id = store_facade.create_numerical_composite_discount('additive_discount',store_id, datetime(2020, 1, 1), datetime(2050, 1, 2), -1,[ discount_id1, discount_id2], 2)
    shopping_basket= {product_id1:1}
    total_price_of_basket=shopping_basket[product_id1]*product_price_10 #10.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==total_price_of_basket*(product_per_005+ product_per_02)
    
    shopping_basket= {product_id1:3}
    total_price_of_basket=shopping_basket[product_id1]*product_price_10 #30.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==total_price_of_basket*(product_per_005+ product_per_02)
    
    
 #-----------------------------------------------------------------------------------------   


def test_create_product_dto(product):
    dto = product.create_product_dto()
    assert dto.product_id == product.product_id
    assert dto.name == product.product_name
    assert dto.description == product.description
    assert dto.price == product.price

def test_change_price(product):
    new_price = 20.0
    product.change_price(new_price)
    assert product.price == new_price

def test_change_price_fail(product):
    with pytest.raises(StoreError) as e:
        product.change_price(-1)
    assert e.value.store_error_type == StoreErrorTypes.invalid_price
        
def test_change_weight(product):
    new_weight = 20.0
    product.change_weight(new_weight)
    assert product.weight == new_weight
    
def test_change_weight_fail(product):
    with pytest.raises(StoreError) as e:
        product.change_weight(-1)
    assert e.value.store_error_type == StoreErrorTypes.invalid_weight
        



def test_add_tag(product):
    tag = 'tag'
    product.add_tag(tag)
    assert tag in product.tags

def test_add_tag_fail(product):
    tag = 'tag'
    product.add_tag(tag)
    with pytest.raises(StoreError) as e:
        product.add_tag(tag)
    assert e.value.store_error_type == StoreErrorTypes.tag_already_exists

def test_remove_tag(tagged_product):
    tag = 'tag'
    tagged_product.remove_tag(tag)
    assert tag not in tagged_product.tags

def test_remove_tag_fail(product):
    tag = 'tag'
    with pytest.raises(StoreError) as e:
        product.remove_tag(tag)
    assert e.value.store_error_type == StoreErrorTypes.tag_not_found

def test_has_tag(tagged_product):
    tag = 'tag'
    not_tag = 'not_tag'
    assert tagged_product.has_tag(tag)
    assert not tagged_product.has_tag(not_tag)

def test_add_parent_category(category):
    category.add_parent_category(3)
    assert 3 == category.parent_category_id

def test_add_parent_category_fail(category):
    category.add_parent_category(3)
    with pytest.raises(StoreError) as e:
        category.add_parent_category(4)
    assert e.value.store_error_type == StoreErrorTypes.parent_category_already_exists

def test_remove_parent_category(category):
    category.add_parent_category(3)
    category.remove_parent_category()
    assert category.parent_category_id == -1

def test_remove_parent_category_fail(category):
    with pytest.raises(StoreError) as e:
        category.remove_parent_category()
    assert e.value.store_error_type == StoreErrorTypes.parent_category_not_found

def test_add_sub_category(sub_category, category):
    category.add_sub_category(sub_category)
    assert sub_category in category.sub_categories

def test_add_sub_category_fail_duplicate(sub_category, category):
    category.add_sub_category(sub_category)
    with pytest.raises(StoreError) as e:
        category.add_sub_category(sub_category)
    assert e.value.store_error_type == StoreErrorTypes.sub_category_error

def test_add_sub_category_fail_parent(sub_category, category):
    sub_category.add_parent_category(3)
    with pytest.raises(StoreError) as e:
        category.add_sub_category(sub_category)
    assert e.value.store_error_type == StoreErrorTypes.parent_category_already_exists

def test_add_sub_category_fail_self(sub_category):
    with pytest.raises(StoreError) as e:
        sub_category.add_sub_category(sub_category)
    assert e.value.store_error_type == StoreErrorTypes.sub_category_error

def test_remove_sub_category(sub_category, category):
    category.add_sub_category(sub_category)
    category.remove_sub_category(sub_category)
    assert sub_category not in category.sub_categories

def test_remove_sub_category_fail_missing(sub_category, category):
    with pytest.raises(StoreError) as e:
        category.remove_sub_category(sub_category)
    assert e.value.store_error_type == StoreErrorTypes.sub_category_error

def test_is_parent_category(category, sub_category):
    category.add_sub_category(sub_category)
    assert sub_category.is_parent_category(category.category_id)

def test_is_parent_category_fail(category, sub_category):
        assert not sub_category.is_parent_category(category.category_id)

def test_is_sub_category(category, sub_category, subsub_category):
    category.add_sub_category(sub_category)
    sub_category.add_sub_category(subsub_category)
    assert category.is_sub_category(sub_category)
    assert sub_category.is_sub_category(subsub_category)
    assert category.is_sub_category(subsub_category)
    assert not subsub_category.is_sub_category(category)

def test_has_parent_category(category, sub_category):
    category.add_sub_category(sub_category)
    assert sub_category.has_parent_category()
    assert not category.has_parent_category()

def test_add_product_to_category(category):
    category.add_product_to_category(0, 0)
    assert (0,0) in category.category_products

def test_add_product_to_category_fail(category):
    category.add_product_to_category(0, 0)
    with pytest.raises(StoreError) as e:
        category.add_product_to_category(0, 0)
    assert e.value.store_error_type == StoreErrorTypes.product_already_exists

def test_remove_product_from_category(category):
    category.add_product_to_category(0, 0)
    category.remove_product_from_category(0, 0)
    assert (0,0) not in category.category_products

def test_remove_product_from_category_fail(category):
    with pytest.raises(StoreError) as e:
        category.remove_product_from_category(0, 0)
    assert e.value.store_error_type == StoreErrorTypes.product_not_found

def test_get_all_products_recursively(category, sub_category, subsub_category):
    category.add_product_to_category(0, 0)
    sub_category.add_product_to_category(1, 0)
    subsub_category.add_product_to_category(2, 0)
    category.add_sub_category(sub_category)
    sub_category.add_sub_category(subsub_category)
    products = category.get_all_products_recursively()
    assert (0,0) in products
    assert (1,0) in products
    assert (2,0) in products

def test_close_store(store):
    store.close_store(0)
    assert not store.is_active

def test_close_store_fail(store):
    with pytest.raises(StoreError) as e:
        store.close_store(1)
    assert e.value.store_error_type == StoreErrorTypes.user_not_founder_of_store

def test_add_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    assert len(store.store_products) == 1
    
def test_remove_product(store, product_dto):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    store.remove_product(product_id)
    assert len(store.store_products) == 0

def test_remove_product_fail(store):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    with pytest.raises(StoreError) as e:
        store.remove_product(product_id+1)
    assert e.value.store_error_type == StoreErrorTypes.product_not_found

def test_get_product_by_id(store, product_dto):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    product = store.get_product_by_id(product_id)
    assert product.product_id == product_id
    assert product.product_name == product_dto.name
    assert product.description == product_dto.description
    assert product.price == product_dto.price
    assert product.tags == product_dto.tags

def test_get_product_by_id_fail(store):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    with pytest.raises(StoreError) as e:
        store.get_product_by_id(product_id+5)
    assert e.value.store_error_type == StoreErrorTypes.product_not_found

def test_get_product_dto_by_id(store, product_dto):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    product_dto = store.get_product_dto_by_id(product_id)
    assert product_dto.product_id == product_id
    assert product_dto.name == product_dto.name
    assert product_dto.description == product_dto.description
    assert product_dto.price == product_dto.price
    assert product_dto.tags == product_dto.tags

def test_get_product_dto_by_id_fail(store):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    with pytest.raises(StoreError) as e:
        store.get_product_dto_by_id(product_id+1000)
    assert e.value.store_error_type == StoreErrorTypes.product_not_found

def test_get_total_price_of_basket_before_discount(store, product_dto):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    product_id2= store.add_product(product_dto.name, product_dto.description, product_dto.price + 10, product_dto.tags, product_dto.weight, product_dto.amount)
    assert store.get_total_price_of_basket_before_discount({product_id:1, product_id2:1}) == 30.0
    assert store.get_total_price_of_basket_before_discount({product_id:2}) == 20.0
    assert store.get_total_price_of_basket_before_discount({product_id:1, product_id2:2}) == 50.0

def test_get_total_price_of_basket_before_discount_fail(store):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    with pytest.raises(StoreError) as e:
        store.get_total_price_of_basket_before_discount({product_id+1000:1})
    assert e.value.store_error_type == StoreErrorTypes.product_not_found

def test_create_store_dto(store):
    dto = store.create_store_dto()
    assert dto.store_id == store.store_id
    assert dto.store_name == store.store_name
    assert dto.store_founder_id == store.store_founder_id
    assert dto.address == store.address
    assert dto.is_active == store.is_active

def test_get_store_information(store):
    dto = store.create_store_dto()
    assert dto.store_id == store.store_id
    assert dto.store_name == store.store_name
    assert dto.store_founder_id == store.store_founder_id
    assert dto.address == store.address
    assert dto.is_active == store.is_active

def test_restock_product(store, product_dto):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    store.restock_product(product_id, 10)
    assert store.has_amount_of_product(product_id, 10)

def test_restock_product_fail(store):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    with pytest.raises(StoreError) as e:
        store.restock_product(product_id+1000, 10)
    assert e.value.store_error_type== StoreErrorTypes.product_not_found

def test_remove_product_amount(store, product_dto):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    store.restock_product(product_id, 10)
    store.remove_product_amount(product_id, 5)
    assert store.has_amount_of_product(product_id, 5)

def test_remove_product_amount_fail_missing(store):
    product_id = store.add_product('product', 'description', 10.0, ['tag'], 30.0, 5)
    with pytest.raises(StoreError) as e:
        store.remove_product_amount(product_id+1000, 5)
    assert e.value.store_error_type== StoreErrorTypes.product_not_found

def test_remove_product_amount_fail_not_enough(store, product_dto):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store.restock_product(product_id, 5)
    with pytest.raises(StoreError) as e:
        store.remove_product_amount(product_id, 10)
    assert e.value.store_error_type== StoreErrorTypes.invalid_amount

def test_change_description_of_product(store, product_dto):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store.change_description_of_product(product_id, 'new description')
    assert store.get_product_by_id(product_id).description == 'new description'

def test_change_description_of_product_fail(store):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    with pytest.raises(StoreError) as e:
        store.change_description_of_product(product_id+1000, 'new description')
    assert e.value.store_error_type== StoreErrorTypes.product_not_found

def test_change_price_of_product(store, product_dto):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store.change_price_of_product(product_id, 20.0)
    assert store.get_product_by_id(product_id).price == 20.0

def test_change_price_of_product_fail(store):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    with pytest.raises(StoreError) as e:
        store.change_price_of_product(product_id+1000, 20.0)
    assert e.value.store_error_type== StoreErrorTypes.product_not_found

def test_add_tag_to_product(store, product_dto):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store.add_tag_to_product(product_id, 'tag2')
    assert 'tag2' in store.get_product_by_id(product_id).tags

def test_add_tag_to_product_fail(store):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    with pytest.raises(StoreError) as e:
        store.add_tag_to_product(product_id+1000, 'tag2')
    assert e.value.store_error_type== StoreErrorTypes.product_not_found

def test_remove_tag_from_product(store, product_dto):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store.add_tag_to_product(product_id, 'tag2')
    store.remove_tag_from_product(product_id, 'tag2')
    assert 'tag2' not in store.get_product_by_id(product_id).tags

def test_remove_tag_from_product_fail_missing_product(store):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    with pytest.raises(StoreError) as e:
        store.remove_tag_from_product(product_id, 'tag2')
    assert e.value.store_error_type == StoreErrorTypes.product_not_found

def test_remove_tag_from_product_fail_missing_tag(store, product_dto):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    with pytest.raises(StoreError) as e:
        store.remove_tag_from_product(product_id, 'idkrandomtagwhichdefoisntinproduct')
    assert e.value.store_error_type== StoreErrorTypes.tag_not_found

def test_get_tags_of_product(store, product_dto):
    product_id = store.add_product(product_dto.name, product_dto.description, product_dto.price, 'tag', product_dto.weight)
    store.add_tag_to_product(product_id, 'tag2')
    assert store.get_tags_of_product(product_id) == ['tag', 'tag2']

def test_get_tags_of_product_fail(store):
    with pytest.raises(StoreError) as e:
        store.get_tags_of_product(0)
    assert e.value.store_error_type== StoreErrorTypes.product_not_found

def test_has_amount_of_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store.restock_product(0, 5)
    assert store.has_amount_of_product(0, 5)
    assert not store.has_amount_of_product(0, 6)

def test_has_amount_of_product_fail(store):
    product_id = store.add_product('product', 'description', 10.0, ['tag'], 30.0)
    assert not store.has_amount_of_product(product_id, 5)
  

def test_get_category_by_id(store_facade, category):
    category_id = store_facade.add_category(category.category_name)
    assert store_facade.get_category_by_id(category_id).category_name == category.category_name

def test_get_category_by_id_fail(store_facade):
    category_id = store_facade.add_category(category.category_name)

    with pytest.raises(StoreError) as e:
        store_facade.get_category_by_id(category_id+1000)
    assert e.value.store_error_type== StoreErrorTypes.category_not_found

def test_add_category(store_facade, category):
    category_id = store_facade.add_category(category.category_name)
    assert store_facade.get_category_by_id(category_id).category_name == category.category_name

def test_remove_category(store_facade, category):
    category_id = store_facade.add_category(category.category_name)
    store_facade.remove_category(category_id)
    with pytest.raises(StoreError) as e:
        store_facade.get_category_by_id(category_id)
    assert e.value.store_error_type== StoreErrorTypes.category_not_found

def test_remove_category_fail(store_facade):
    category_id = store_facade.add_category(category.category_name)
    with pytest.raises(StoreError) as e:
        store_facade.remove_category(category_id+1000)
    assert e.value.store_error_type== StoreErrorTypes.category_not_found

def test_assign_sub_category_to_category(store_facade, category, sub_category):
    category_id = store_facade.add_category(category.category_name)
    sub = store_facade.add_category(sub_category.category_name)
    store_facade.assign_sub_category_to_category(sub, category_id)
    assert store_facade.get_category_by_id(category_id).sub_categories[0].category_name == sub_category.category_name

def test_assign_sub_category_to_category_fail(store_facade):
    category_id = store_facade.add_category(category.category_name)
    sub = store_facade.add_category(sub_category.category_name)
    
    with pytest.raises(StoreError) as e:
        store_facade.assign_sub_category_to_category(sub, category_id+1000)
    assert e.value.store_error_type== StoreErrorTypes.category_not_found

def test_delete_sub_category_from_category(store_facade, category, sub_category):
    category_id = store_facade.add_category(category.category_name)
    sub = store_facade.add_category(sub_category.category_name)
    store_facade.assign_sub_category_to_category(sub, category_id)
    store_facade.delete_sub_category_from_category(category_id, sub)
    assert len(store_facade.get_category_by_id(category_id).sub_categories) == 0

def test_delete_sub_category_from_category_fail(store_facade):
    category_id = store_facade.add_category(category.category_name)
    sub = store_facade.add_category(sub_category.category_name)
    with pytest.raises(StoreError) as e:
        store_facade.delete_sub_category_from_category(category_id, sub)
    assert e.value.store_error_type== StoreErrorTypes.category_not_found

def test_assign_product_to_category(store_facade, category, product_dto):
    category_id = store_facade.add_category(category.category_name)
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade._StoreFacade__get_store_by_id(store_id).add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store_facade.assign_product_to_category(category_id, store_id, product_id)
    with pytest.raises(StoreError) as e:
        store_facade.assign_product_to_category(category_id, store_id, product_id)
    assert e.value.store_error_type== StoreErrorTypes.product_already_exists

def test_assign_product_to_category_fail(store_facade):
    category_id = store_facade.add_category("category")
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade._StoreFacade__get_store_by_id(store_id).add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    with pytest.raises(StoreError) as e:
        store_facade.assign_product_to_category(category_id+1, store_id, product_id)
    assert e.value.store_error_type== StoreErrorTypes.category_not_found

def test_remove_product_from_category2(store_facade, category, product_dto):
    category_id = store_facade.add_category(category.category_name)
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade._StoreFacade__get_store_by_id(store_id).add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store_facade.assign_product_to_category(category_id, store_id, product_id)
    store_facade.remove_product_from_category(category_id, store_id, product_id)
    assert len(store_facade.get_category_by_id(category_id).category_products) == 0

def test_remove_product_from_category_fail2(store_facade, category):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade._StoreFacade__get_store_by_id(store_id).add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    with pytest.raises(StoreError) as e:
        store_facade.remove_product_from_category(category.category_id-1, store_id, product_id)
    assert e.value.store_error_type== StoreErrorTypes.category_not_found

def test_add_product_to_store(store_facade, product_dto):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, product_dto.price, product_dto.weight,product_dto.tags)

    assert len(store_facade._StoreFacade__get_store_by_id(store_id).store_products) == 1

def test_add_product_to_store_fail_store_id(store_facade, product_dto):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, product_dto.price, product_dto.weight,product_dto.tags)

    with pytest.raises(StoreError) as e:
        store_facade.add_product_to_store(store_id+1000, product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
    assert e.value.store_error_type== StoreErrorTypes.store_not_found
    
def test_add_product_to_store_fail_product_name(store_facade, product_dto):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    with pytest.raises(StoreError) as e:
        store_facade.add_product_to_store(store_id, '', product_dto.description, product_dto.price, product_dto.tags)
    assert e.value.store_error_type== StoreErrorTypes.invalid_product_name

def test_add_product_to_store_fail_price(store_facade, product_dto):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    with pytest.raises(StoreError) as e:
        store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, -1, 30.0, product_dto.tags)
    assert e.value.store_error_type== StoreErrorTypes.invalid_price

def test_remove_product_from_store(store_facade, product_dto):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, product_dto.price, product_dto.weight, product_dto.tags)
    store_facade.remove_product_from_store(store_id, product_id)
    assert len(store_facade._StoreFacade__get_store_by_id(store_id).store_products) == 0

def test_remove_product_from_store_fail(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, product_dto.price, product_dto.weight, product_dto.tags)
    with pytest.raises(StoreError) as e:
        store_facade.remove_product_from_store(store_id+1100, product_id)
    assert e.value.store_error_type== StoreErrorTypes.store_not_found

def test_add_product_amount(store_facade, product_dto):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, product_dto.price,product_dto.weight, product_dto.tags)
    store_facade.add_product_amount(store_id, product_id, 10)
    assert store_facade.get_store_by_id(store_id).has_amount_of_product(product_id, 10)

def test_add_product_amount_fail(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, product_dto.price, product_dto.weight,product_dto.tags)
    
    with pytest.raises(StoreError) as e:
        store_facade.add_product_amount(store_id+1, product_id, 10)
    assert e.value.store_error_type== StoreErrorTypes.store_not_found

def test_remove_product_amount2(store_facade, product_dto):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, product_dto.price, product_dto.weight,product_dto.tags)
    store_facade.add_product_amount(store_id, product_id, 10)
    store_facade.remove_product_amount(store_id, product_id, 5)
    assert store_facade.get_store_by_id(store_id).has_amount_of_product(product_id, 5)

def test_change_description_of_product2(store_facade, product_dto):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, product_dto.price,product_dto.weight, product_dto.tags)
    store_facade.change_description_of_product(store_id, product_id, 'new description')
    assert store_facade.get_store_by_id(store_id).get_product_by_id(product_id).description == 'new description'

def test_change_description_of_product_fail2(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, product_dto.price,product_dto.weight, product_dto.tags)
    with pytest.raises(StoreError) as e:
        store_facade.change_description_of_product(store_id+1000, product_id, 'new description')
    assert e.value.store_error_type== StoreErrorTypes.store_not_found

def test_change_price_of_product2(store_facade, product_dto):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, product_dto.price,product_dto.weight, product_dto.tags)
    store_facade.change_price_of_product(store_id, product_id, 20.0)
    assert store_facade._StoreFacade__get_store_by_id(store_id).get_product_by_id(product_id).price == 20.0

def test_change_price_of_product_fail2(store_facade):
    with pytest.raises(StoreError) as e:
        store_facade.change_price_of_product(0, 0, 20.0)
    assert e.value.store_error_type== StoreErrorTypes.store_not_found

def test_add_tag_to_product2(store_facade, product_dto):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, product_dto.price, product_dto.weight,product_dto.tags)
    store_facade.add_tag_to_product(store_id, product_id, 'tag2')
    assert 'tag2' in store_facade._StoreFacade__get_store_by_id(store_id).get_product_by_id(product_id).tags

def test_add_tag_to_product_fail2(store_facade):
    with pytest.raises(StoreError) as e:
        store_facade.add_tag_to_product(0, 0, 'tag2')
    assert e.value.store_error_type== StoreErrorTypes.store_not_found

def test_remove_tag_from_product2(store_facade, product_dto):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, product_dto.price, product_dto.weight,product_dto.tags)
    store_facade.add_tag_to_product(store_id, product_id, 'tag2')
    store_facade.remove_tag_from_product(store_id, product_id, 'tag2')
    assert 'tag2' not in store_facade._StoreFacade__get_store_by_id(store_id).get_product_by_id(product_id).tags

def test_remove_tag_from_product_fail(store_facade):
    with pytest.raises(StoreError) as e:
        store_facade.remove_tag_from_product(0, 0, 'tag2')
    assert e.value.store_error_type== StoreErrorTypes.store_not_found

def test_get_tags_of_product2(store_facade, product_dto):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.weight, product_dto.tags)
    store_facade.add_tag_to_product(0, 0, 'tag2')
    assert store_facade.get_tags_of_product(0, 0) == ['tag', 'tag2']

def test_get_tags_of_product_fail2(store_facade):
    with pytest.raises(StoreError) as e:
        store_facade.get_tags_of_product(0, 0)
    assert e.value.store_error_type== StoreErrorTypes.store_not_found

def test_add_store(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    assert store_facade._StoreFacade__get_store_by_id(0).store_name == 'store'

def test_close_store2(store_facade):
    id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.close_store(id, 0)
    assert not store_facade._StoreFacade__get_store_by_id(id).is_active

def test_close_store_fail2(store_facade):
    with pytest.raises(StoreError) as e:
        store_facade.close_store(0, 0)
    assert e.value.store_error_type== StoreErrorTypes.store_not_found

def test_get_store_by_id(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    assert store_facade._StoreFacade__get_store_by_id(0).store_name == 'store'

def test_get_store_by_id_fail(store_facade):
    with pytest.raises(StoreError) as e:
        store_facade._StoreFacade__get_store_by_id(0)
    assert e.value.store_error_type== StoreErrorTypes.store_not_found

def test_get_total_price_before_discount2(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_store(default_location, store_name='store2', store_founder_id=0)
    store_facade.add_product_to_store(0, 'product', 'description', 10.0, 21.0, ['tag'])
    store_facade.add_product_to_store(0, 'product2', 'description', 20.0, 21.0, ['tag'])
    store_facade.add_product_to_store(1, 'product', 'description', 10.0, 21.0, ['tag'])
    store_facade.add_product_to_store(1, 'product2', 'description', 20.0, 21.0, ['tag'])
    assert store_facade.get_total_price_before_discount({0: {0:1, 1:1}, 1: {0:1, 1:1}}) == 60.0

def test_get_total_price_before_discount_fail(store_facade):
    with pytest.raises(StoreError) as e:
        store_facade.get_total_price_before_discount({0: {0:1, 1:1}, 1: {0:1, 1:1}})
    assert e.value.store_error_type== StoreErrorTypes.store_not_found

def test_get_store_product_information(store_facade, product_dto, product_dto2):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.weight, product_dto.tags)
    store_facade.add_product_to_store(0, product_dto2.name, product_dto2.description, product_dto2.price, product_dto.weight, product_dto2.tags)
    out = store_facade.get_store_product_information(0, 0)
    out0, out1 = out[0], out[1]
    assert out0.product_id == 0
    assert out0.name == product_dto.name
    assert out0.description == product_dto.description
    assert out0.price == product_dto.price
    assert out0.tags == product_dto.tags
    assert out1.product_id == 1
    assert out1.name == product_dto2.name
    assert out1.description == product_dto2.description
    assert out1.price == product_dto2.price
    assert out1.tags == product_dto2.tags

def test_check_product_availability(store_facade, product_dto):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id = store_facade.add_product_to_store(store_id, product_dto.name, product_dto.description, product_dto.price, product_dto.weight,product_dto.tags)
    store_facade.add_product_amount(store_id, product_id, 10)
    assert store_facade.check_product_availability(store_id, product_id, 10)
    assert not store_facade.check_product_availability(store_id, product_id, 11)

def test_check_product_availability_fail(store_facade):
    with pytest.raises(StoreError) as e:
        store_facade.check_product_availability(0, 0, 1)
    assert e.value.store_error_type== StoreErrorTypes.store_not_found

def test_get_store_info(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    out = store_facade.get_store_info(0)
    assert out.store_id == 0
    assert out.store_name == 'store'
    assert out.store_founder_id == 0
    assert out.address == default_location
    assert out.is_active

def test_search_by_category(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_category('category')
    store_facade.add_category('sub_category')
    store_facade.add_category('subsub_category')
    store_facade.assign_sub_category_to_category(1, 0)
    store_facade.assign_sub_category_to_category(2, 1)
    store_facade.add_product_to_store(0, 'product', 'description', 10.0, 21.0, ['tag'])
    store_facade.assign_product_to_category(0, 0, 0)
    out = store_facade.search_by_category(0)
    assert out[0][0].product_id == 0

def test_search_by_category_fail(store_facade):
    with pytest.raises(StoreError) as e:
        store_facade.search_by_category(0)
    assert e.value.store_error_type== StoreErrorTypes.category_not_found

def test_search_by_tags(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, 'product', 'description', 10.0, 10.0, ['tag'])
    out = store_facade.search_by_tags(['tag'])
    assert out[0][0].product_id == 0

def test_search_by_name(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, 'product', 'description', 10.0, 10.0, ['tag'])
    out = store_facade.search_by_name('product')
    assert out[0][0].product_id == 0

def test_search_in_store_by_category(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_category('category')
    store_facade.add_category('sub_category')
    store_facade.add_category('subsub_category')
    store_facade.assign_sub_category_to_category(1, 0)
    store_facade.assign_sub_category_to_category(2, 1)
    store_facade.add_product_to_store(0, 'product', 'description', 10.0, 21.0, ['tag'])
    store_facade.assign_product_to_category(0, 0, 0)
    out = store_facade.search_by_category(0, 0)
    assert out[0][0].product_id == 0

def test_search_in_store_by_category_fail(store_facade):
    with pytest.raises(StoreError) as e:
        store_facade.search_by_category(0, 0)
    assert e.value.store_error_type== StoreErrorTypes.store_not_found

def test_search_in_store_by_tags(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, 'product', 'description', 10.0, 10.0, ['tag'])
    out = store_facade.search_by_tags(['tag'], 0)
    assert out[0][0].product_id == 0

def test_search_in_store_by_name(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, 'product', 'description', 10.0, 10.0, ['tag'])
    out = store_facade.search_by_name('product', 0)
    assert out[0][0].product_id == 0


def test_add_purchase_policy(store, category2):
    assert len(store.purchase_policy) == 0
    policy_id=store.add_purchase_policy('no_alcohol_bellow_18', category2.category_id, None)
    assert len(store.purchase_policy) == 1
    assert store.purchase_policy[0] == policy_id
    
    
def test_remove_purchase_policy(store,category2):
    policy_id=store.add_purchase_policy('no_alcohol_bellow_18', category2.category_id, None)
    assert len(store.purchase_policy) == 1
    store.remove_purchase_policy(policy_id)
    assert len(store.purchase_policy) == 0
    
    
    
    
#tests from the story:

#test 1: policy where a basket cannot have more than 5 kg of tomatoes:
def test_create_simple_purchase_policy_to_store(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('tomatoes', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(0, 50)
    policy_id=store_facade.add_purchase_policy_to_store(store_id, 'no_more_than_5_kg_tomatoes', None, product_id)
    shopping_basket = {product_id:21}
    total_price_of_basket=shopping_basket[product_id]*product_price_10
    store_facade.assign_predicate_to_purchase_policy(store_id,policy_id, ('weight_product', 0.0, 5.0,product_id, store_id))
    assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto1)==False
    
#test 2: policy where a user cant buy alcohol if he is under 18:
def test_create_simple_purchase_policy_to_store2(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('alcohol', 'very good product', product_price_10, ['tag'], 30.0)
    category_id3 = store_facade.add_category('alcohol')
    store_facade.assign_product_to_category(0, store_id,product_id)
    store_facade.get_store_by_id(store_id).restock_product(0, 50)
    policy_id=store_facade.add_purchase_policy_to_store(store_id, 'no_alcohol_bellow_18', category_id3)
    shopping_basket = {product_id:21}
    total_price_of_basket=shopping_basket[product_id]*product_price_10
    store_facade.assign_predicate_to_purchase_policy(store_id,policy_id, ('age', 18, -1, store_id))
    assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto2)==False

    
#test 3: policy where a user cant buy alcohol if the hour is past 23:00:
def test_create_simple_purchase_policy_to_store3(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('alcohol', 'very good product', product_price_10, ['tag'], 30.0)
    category_id3 = store_facade.add_category('alcohol')
    store_facade.assign_product_to_category(0, store_id,product_id)
    store_facade.get_store_by_id(store_id).restock_product(0, 50)
    policy_id=store_facade.add_purchase_policy_to_store(store_id, 'no_alcohol_after_23', category_id3)
    shopping_basket = {product_id:21}
    total_price_of_basket=shopping_basket[product_id]*product_price_10
    store_facade.assign_predicate_to_purchase_policy(store_id,policy_id, ('time', 6, 0, 23, 0, store_id))
    
    if datetime.now().hour<23 and datetime.now().hour>6:
        assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto2)==True
    else:
        assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto2)==False

    
#test 4: a policy where there cannot be any ice cream sales at the beggining of the month:
def test_create_simple_purchase_policy_to_store4(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('ice_cream', 'very good product', product_price_10, ['tag'], 30.0)
    category_id3 = store_facade.add_category('ice_cream')
    store_facade.assign_product_to_category(0, store_id,product_id)
    store_facade.get_store_by_id(store_id).restock_product(0, 50)
    policy_id=store_facade.add_purchase_policy_to_store(store_id, 'no_ice_cream_at_beginning_of_month', category_id3)
    shopping_basket = {product_id:21}
    total_price_of_basket=shopping_basket[product_id]*product_price_10
    store_facade.assign_predicate_to_purchase_policy(store_id,policy_id, ('day_of_month', 2, 31, store_id))
    assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto2)==True
    
    
#test 5: a "AND" policy where a basket cannot have more than 5 kg of tomatoes and a basket must have at least 2 corn:
def test_create_simple_purchase_policy_to_store5(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('tomatoes', 'very good product', product_price_10, ['tag'], 30.0)
    product_id2=store_facade.get_store_by_id(store_id).add_product('corn', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(product_id, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    policy_id1=store_facade.add_purchase_policy_to_store(store_id, 'no_more_than_5_kg_tomatoes',None, product_id)
    policy_id2=store_facade.add_purchase_policy_to_store(store_id, 'at_least_2_corn', None, product_id2)
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id1, ('weight_product', 0.0, 5.0, product_id, store_id ))
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id2, ('amount_product', 2, -1, product_id2, store_id))
    
    new_policy=store_facade.create_composite_purchase_policy_to_store(store_id,'and policy', policy_id1, policy_id2, 1)

    shopping_basket = {product_id:21, product_id2:6}
    
    total_price_of_basket=shopping_basket[product_id]*product_price_10+shopping_basket[product_id2]*product_price_10    
    assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto1)==False

    
#test 5.5: test 5 but it works now:
def test_create_simple_purchase_policy_to_store5_5(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('tomatoes', 'very good product', product_price_10, ['tag'], 1.0)
    product_id2=store_facade.get_store_by_id(store_id).add_product('corn', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(product_id, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    policy_id1=store_facade.add_purchase_policy_to_store(store_id, 'no_more_than_5_kg_tomatoes',None, product_id)
    policy_id2=store_facade.add_purchase_policy_to_store(store_id, 'at_least_2_corn', None, product_id2)
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id1, ('weight_product', 0.0, 5.0, product_id, store_id ))
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id2, ('amount_product', 2,-1, product_id2, store_id))
    
    new_policy=store_facade.create_composite_purchase_policy_to_store(store_id,'and policy', policy_id1, policy_id2, 1)

    shopping_basket = {product_id:4, product_id2:6}
    total_price_of_basket=shopping_basket[product_id]*product_price_10+shopping_basket[product_id2]*product_price_10    
    assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto1)==True

    
#test 6: a "OR" policy where a user cannot buy alcohol after 23:00 or when its a holiday:
def test_create_simple_purchase_policy_to_store6(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('alcohol', 'very good product', product_price_10, ['tag'], 30.0)
    category_id3 = store_facade.add_category('alcohol')
    store_facade.assign_product_to_category(0, store_id,product_id)
    store_facade.get_store_by_id(store_id).restock_product(0, 50)
    policy_id1=store_facade.add_purchase_policy_to_store(store_id, 'no_alcohol_after_23', category_id3)
    policy_id2=store_facade.add_purchase_policy_to_store(store_id, 'no_alcohol_on_holidays', category_id3)
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id1, ('time', 6, 0, 23, 0, store_id))
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id2, ('holidays_of_country', 'IL'))
    
    new_policy=store_facade.create_composite_purchase_policy_to_store(store_id,'or policy', policy_id1, policy_id2, 2)

    shopping_basket = {product_id:21}
    total_price_of_basket=shopping_basket[product_id]*product_price_10
    
    if datetime.now().hour>=23 or datetime.now().hour <= 6:
        assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto2)==False
    else:
        assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto2)==True
   
    
#test 7: a user can buy 5 kg of tomatoes only if (conditioning) there are eggplants in the basket:
def test_create_simple_purchase_policy_to_store7(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('tomatoes', 'very good product', product_price_10, ['tag'], 1.0)
    product_id2=store_facade.get_store_by_id(store_id).add_product('eggplants', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(product_id, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    policy_id1=store_facade.add_purchase_policy_to_store(store_id, 'no_more_than_5_kg_tomatoes',None, product_id)
    policy_id2=store_facade.add_purchase_policy_to_store(store_id, 'must_have_eggplants', None, product_id2)
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id1, ('weight_product', 0.0, 5.0, product_id, store_id ))
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id2, ('amount_product', 1, -1, product_id2, store_id))
    
    new_policy=store_facade.create_composite_purchase_policy_to_store(store_id,'condition policy', policy_id1, policy_id2, 3)

    shopping_basket = {product_id:5, product_id2:1}
    total_price_of_basket=shopping_basket[product_id]*product_price_10+shopping_basket[product_id2]*product_price_10    
    assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto1)==True
   
#test 7.5: a user can buy 5 kg of tomatoes only if (conditioning) there are eggplants in the basket:
def test_create_simple_purchase_policy_to_store75(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('tomatoes', 'very good product', product_price_10, ['tag'], 1.0)
    product_id2=store_facade.get_store_by_id(store_id).add_product('eggplants', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(product_id, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    policy_id1=store_facade.add_purchase_policy_to_store(store_id, 'no_more_than_5_kg_tomatoes',None, product_id)
    policy_id2=store_facade.add_purchase_policy_to_store(store_id, 'must_have_eggplants', None, product_id2)
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id1, ('weight_product', 0.0, 5.0, product_id, store_id ))
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id2, ('amount_product', 1, -1, product_id2, store_id))
    
    new_policy=store_facade.create_composite_purchase_policy_to_store(store_id,'condition policy', policy_id1, policy_id2, 3)

    shopping_basket = {product_id:5}
    total_price_of_basket=shopping_basket[product_id]*product_price_10    
    assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto1)==False
     
#test 8: a user can buy 5 kg of tomatoes only if (conditioning) there are at least 2 eggplants in the basket or its a holiday:
def test_create_simple_purchase_policy_to_store8(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('tomatoes', 'very good product', product_price_10, ['tag'], 1.0)
    product_id2=store_facade.get_store_by_id(store_id).add_product('eggplants', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(product_id, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    policy_id1=store_facade.add_purchase_policy_to_store(store_id, 'no_more_than_5_kg_tomatoes',None, product_id)
    policy_id2=store_facade.add_purchase_policy_to_store(store_id, 'must_have_2_eggplants_or_holiday', None, None)
        
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id1, ('weight_product', 0.0, 5.0, product_id, store_id ))
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id2, ('or' ,('amount_product', 2, -1, product_id2, store_id), ('holidays_of_country', 'IL')))
    
    new_policy=store_facade.create_composite_purchase_policy_to_store(store_id,'or policy', policy_id1, policy_id2, 1)

    shopping_basket = {product_id:5, product_id2:1}
    total_price_of_basket=shopping_basket[product_id]*product_price_10+shopping_basket[product_id2]*product_price_10    
    assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto1)==False
     
     
     
#test 9: a user can buy 5 kg of tomatoes only if (conditioning) there are at least 2 eggplants in the basket or its a holiday:
def test_create_simple_purchase_policy_to_store9(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('tomatoes', 'very good product', product_price_10, ['tag'], 1.0)
    product_id2=store_facade.get_store_by_id(store_id).add_product('eggplants', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(product_id, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    policy_id1=store_facade.add_purchase_policy_to_store(store_id, 'no_more_than_5_kg_tomatoes',None, product_id)
    policy_id2=store_facade.add_purchase_policy_to_store(store_id, 'must_have_2_eggplants_or_holiday', None, None)
        
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id1, ('weight_product', 0.0, 5.0, product_id, store_id ))
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id2, ('or' ,('amount_product', 2, -1, product_id2, store_id), ('holidays_of_country', 'IL')))
    
    new_policy=store_facade.create_composite_purchase_policy_to_store(store_id,'or policy', policy_id1, policy_id2, 1)

    shopping_basket = {product_id:5, product_id2:5}
    total_price_of_basket=shopping_basket[product_id]*product_price_10+shopping_basket[product_id2]*product_price_10    
    assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto1)==True
     

def test_create_composite_purchase_policy_to_store (store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('tomatoes', 'very good product', product_price_10, ['tag'], 1.0)
    product_id2=store_facade.get_store_by_id(store_id).add_product('eggplants', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(product_id, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    policy_id1=store_facade.add_purchase_policy_to_store(store_id, 'no_more_than_5_kg_tomatoes',None, product_id)
    policy_id2=store_facade.add_purchase_policy_to_store(store_id, 'must_have_2_eggplants_or_holiday', None, None)
        
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id1, ('weight_product', 0.0, 5.0, product_id, store_id ))
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id2, ('or' ,('amount_product', 2, -1, product_id2, store_id), ('holidays_of_country', 'IL')))
    
    new_policy=store_facade.create_composite_purchase_policy_to_store(store_id,'or policy', policy_id1, policy_id2, 1)

    shopping_basket = {product_id:5, product_id2:5}
    total_price_of_basket=shopping_basket[product_id]*product_price_10+shopping_basket[product_id2]*product_price_10    
    assert store_facade.validate_purchase_policy(store_id, total_price_of_basket,shopping_basket, user_information_dto1)==True



def test_validate_purchase_policies(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('tomatoes', 'very good product', product_price_10, ['tag'], 1.0)
    product_id2=store_facade.get_store_by_id(store_id).add_product('eggplants', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(product_id, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    policy_id1=store_facade.add_purchase_policy_to_store(store_id, 'no_more_than_5_kg_tomatoes',None, product_id)
    policy_id2=store_facade.add_purchase_policy_to_store(store_id, 'must_have_2_eggplants_or_holiday', None, None)
        
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id1, ('weight_product', 0.0, 5.0, product_id, store_id ))
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id2, ('or' ,('amount_product', 2, -1, product_id2, store_id), ('holidays_of_country', 'IL')))
    
    new_policy=store_facade.create_composite_purchase_policy_to_store(store_id,'or policy', policy_id1, policy_id2, 1)

    shopping_basket = {product_id:5, product_id2:1}
    total_price_of_basket=shopping_basket[product_id]*product_price_10+shopping_basket[product_id2]*product_price_10    
    assert store_facade.validate_purchase_policies({store_id:shopping_basket}, user_information_dto1)==False
    
def test_validate_purchase_policies2(store_facade):
    store_id = store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    product_id=store_facade.get_store_by_id(store_id).add_product('tomatoes', 'very good product', product_price_10, ['tag'], 1.0)
    product_id2=store_facade.get_store_by_id(store_id).add_product('eggplants', 'very good product', product_price_10, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(product_id, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    policy_id1=store_facade.add_purchase_policy_to_store(store_id, 'no_more_than_5_kg_tomatoes',None, product_id)
    policy_id2=store_facade.add_purchase_policy_to_store(store_id, 'must_have_2_eggplants_or_holiday', None, None)
        
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id1, ('weight_product', 0.0, 5.0, product_id, store_id ))
    store_facade.assign_predicate_to_purchase_policy(store_id, policy_id2, ('or' ,('amount_product', 2, -1, product_id2, store_id), ('holidays_of_country', 'IL')))
    
    new_policy=store_facade.create_composite_purchase_policy_to_store(store_id,'or policy', policy_id1, policy_id2, 1)

    shopping_basket = {product_id:5, product_id2:2}
    total_price_of_basket=shopping_basket[product_id]*product_price_10+shopping_basket[product_id2]*product_price_10    
    assert store_facade.validate_purchase_policies({store_id:shopping_basket}, user_information_dto1)==True



'''
def test_add_purchase_policy(store):
    store.add_purchase_policy("no_alcohol_and_tabbaco_bellow_18")
    assert len(store.purchase_policy) == 1
    assert store.purchase_policy[0] == "no_alcohol_and_tabbaco_bellow_18"

def test_add_purchase_policy_fail(store):
    with pytest.raises(StoreError) as e:
        store.add_purchase_policy("hello")
    assert e.value.store_error_type== StoreErrorTypes.invalid_purchase_policy_input

def test_remove_purchase_policy(store):
    store.add_purchase_policy("no_alcohol_and_tabbaco_bellow_18")
    store.remove_purchase_policy("no_alcohol_and_tabbaco_bellow_18")
    assert len(store.purchase_policy) == 0

def test_remove_purchase_policy_fail(store):
    with pytest.raises(StoreError) as e:
        store.remove_purchase_policy("no_alcohol_and_tabbaco_bellow_18")
    assert e.value.store_error_type== StoreErrorTypes.policy_not_found

def test_check_purchase_policy(store):
    store.add_purchase_policy("no_alcohol_and_tabbaco_bellow_18")
    store.add_purchase_policy("not_too_much_gun_powder")
    user_dto = PurchaseUserDTO(user_id=0, birthdate=datetime.now().replace(year=datetime.now().year - 21))
    alcohol_product = ProductDTO(product_id=0, name='alcohol', description='description', price=10.0, tags=['alcohol'], weight=10.0, amount=10)
    tabbaco_product = ProductDTO(product_id=1, name='tabbaco', description='description', price=10.0, tags=['tabbaco'], weight=10.0, amount=10)
    gun_powder_product = ProductDTO(product_id=2, name='gun_powder', description='description', price=10.0, tags=['gun_powder'], weight=10.0, amount=5)
    products = {alcohol_product: 1, tabbaco_product: 1, gun_powder_product: 8}
    assert store.check_purchase_policy(products, user_dto) is None

def test_check_purchase_policy_fail(store):
    store.add_purchase_policy("no_alcohol_and_tabbaco_bellow_18")
    store.add_purchase_policy("not_too_much_gun_powder")
    user_dto = PurchaseUserDTO(user_id=0, birthdate=datetime.now().replace(year=datetime.now().year - 17))
    alcohol_product = ProductDTO(product_id=0, name='alcohol', description='description', price=10.0, tags=['alcohol'], weight=10.0, amount=10)
    tabbaco_product = ProductDTO(product_id=1, name='tabbaco', description='description', price=10.0, tags=['tabbaco'], weight=10.0, amount=10)
    gun_powder_product = ProductDTO(product_id=2, name='gun_powder', description='description', price=10.0, tags=['gun_powder'], weight=10.0, amount=5)
    products = {alcohol_product: 1, tabbaco_product: 1, gun_powder_product: 8}
    with pytest.raises(StoreError) as e:
        store.check_purchase_policy(products, user_dto)
    assert e.value.store_error_type== StoreErrorTypes.policy_not_satisfied

def test_add_purchase_policy_to_store(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_purchase_policy_to_store(0, "no_alcohol_and_tabbaco_bellow_18")
    assert store_facade._StoreFacade__get_store_by_id(0).purchase_policy[0] == "no_alcohol_and_tabbaco_bellow_18"

def test_add_purchase_policy_to_store_fail(store_facade):
    with pytest.raises(StoreError) as e:
        store_facade.add_purchase_policy_to_store(0, "hello")
    assert e.value.store_error_type== StoreErrorTypes.invalid_purchase_policy_input

def test_remove_purchase_policy_from_store(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_purchase_policy_to_store(0, "no_alcohol_and_tabbaco_bellow_18")
    store_facade.remove_purchase_policy_from_store(0, "no_alcohol_and_tabbaco_bellow_18")
    assert len(store_facade._StoreFacade__get_store_by_id(0).purchase_policy) == 0

def test_remove_purchase_policy_from_store_fail(store_facade):
    with pytest.raises(StoreError) as e:
        store_facade.remove_purchase_policy_from_store(0, "no_alcohol_and_tabbaco_bellow_18")
    assert e.value.store_error_type== StoreErrorTypes.policy_not_found

def test_validate_purchase_policies(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_store(default_location, store_name='store2', store_founder_id=0)
    store_facade.add_purchase_policy_to_store(0, "no_alcohol_and_tabbaco_bellow_18")
    store_facade.add_purchase_policy_to_store(0, "not_too_much_gun_powder")
    store_facade.add_purchase_policy_to_store(1, "no_alcohol_and_tabbaco_bellow_18")
    store_facade.add_purchase_policy_to_store(1, "not_too_much_gun_powder")
    user_dto = PurchaseUserDTO(user_id=0, birthdate=datetime.now().replace(year=datetime.now().year - 21))
    store_facade.add_product_to_store(0, 'alcohol', 'description', 10.0, 10.0, ['alcohol'])
    store_facade.add_product_to_store(0, 'tabbaco', 'description', 10.0, 10.0, ['tabbaco'])
    store_facade.add_product_to_store(0, 'gun_powder', 'description', 10.0, 10.0, ['gun_powder'])
    store_facade.add_product_to_store(1, 'alcohol', 'description', 10.0, 10.0, ['alcohol'])
    store_facade.add_product_to_store(1, 'tabbaco', 'description', 10.0, 10.0, ['tabbaco'])
    store_facade.add_product_to_store(1, 'gun_powder', 'description', 10.0, 10.0, ['gun_powder'])
    products = {0: {0:1, 1:1, 2:4}, 1: {0:1, 1:1, 2:4}}
    assert store_facade.validate_purchase_policies(products, user_dto) is None

def test_validate_purchase_policies_fail(store_facade):
    store_facade.add_store(default_location, store_name='store', store_founder_id=0)
    store_facade.add_store(default_location, store_name='store2', store_founder_id=0)
    store_facade.add_purchase_policy_to_store(0, "no_alcohol_and_tabbaco_bellow_18")
    store_facade.add_purchase_policy_to_store(0, "not_too_much_gun_powder")
    store_facade.add_purchase_policy_to_store(1, "no_alcohol_and_tabbaco_bellow_18")
    store_facade.add_purchase_policy_to_store(1, "not_too_much_gun_powder")
    user_dto = PurchaseUserDTO(user_id=0, birthdate=datetime.now().replace(year=datetime.now().year - 17))
    store_facade.add_product_to_store(0, 'alcohol', 'description', 10.0, 10.0, ['alcohol'])
    store_facade.add_product_to_store(0, 'tabbaco', 'description', 10.0, 10.0, ['tabbaco'])
    store_facade.add_product_to_store(0, 'gun_powder', 'description', 10.0, 10.0, ['gun_powder'])
    store_facade.add_product_to_store(1, 'alcohol', 'description', 10.0, 10.0, ['alcohol'])
    store_facade.add_product_to_store(1, 'tabbaco', 'description', 10.0, 10.0, ['tabbaco'])
    store_facade.add_product_to_store(1, 'gun_powder', 'description', 10.0, 10.0, ['gun_powder'])
    products = {0: {0:1, 1:1, 2:4}, 1: {0:1, 1:1, 2:4}}
    with pytest.raises(StoreError) as e:
        store_facade.validate_purchase_policies(products, user_dto)
    assert e.value.store_error_type== StoreErrorTypes.policy_not_satisfied

'''

     
     
