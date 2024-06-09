from datetime import date, datetime, time
from typing import Dict

import pytest
from backend.business.store.constraints import AgeConstraint, AndConstraint, LocationConstraint
from backend.business.store.discount import StoreDiscount
from backend.business.store.new_store import Store, Product, Category, StoreFacade
from backend.business.DTOs import AddressDTO, ProductDTO, PurchaseUserDTO, UserInformationForDiscountDTO
@pytest.fixture
def product():
    return Product(product_id=0, product_name='product', description='very good product', price=10.0, weight=30.0, amount=10)

@pytest.fixture
def tagged_product(product):
    product.add_tag('tag')
    return product

@pytest.fixture
def category():
    return Category(category_id=0, category_name='category')

@pytest.fixture
def sub_category(category):
    return Category(category_id=1, category_name='sub_category')

@pytest.fixture
def subsub_category(sub_category):
    return Category(category_id=2, category_name='subsub_category')

@pytest.fixture
def store():
    return Store(store_id=0, location_id=0, store_name='store', store_founder_id=0)

@pytest.fixture
def product_dto():
    return ProductDTO(product_id=0, name='product', description='very good product', price=10.0, tags=['tag'], weight=30.0, amount=10)

@pytest.fixture
def product_dto2():
    return ProductDTO(product_id=1, name='product2', description='very good product', price=10.0, tags=['tag'], weight=30.0, amount=10)

@pytest.fixture
def store_facade():
    StoreFacade().clean_data()
    return StoreFacade()

#Address default vars:     
default_address_id: int = 0
default_city: str = "city"
default_country: str = "country"
default_street: str = "street"
default_zip_code: str = "zip_code"
default_house_number: str = "house_number"
default_location: AddressDTO = AddressDTO(default_address_id, default_city, default_country, default_street, default_zip_code, default_house_number)
user_information_dto1=  UserInformationForDiscountDTO(0, date(1990, 1, 1), default_location)



       
def test_add_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount', datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,store_id,None,None)
    assert len(store_facade.discounts) == 1
    assert store_facade.discounts[0].discount_description == 'discount'
    assert store_facade.discounts[0].starting_date == datetime(2020, 1, 1)
    assert store_facade.discounts[0].ending_date == datetime(2020, 1, 2)
    assert store_facade.discounts[0].percentage == 0.1
    assert isinstance(store_facade.discounts[0], StoreDiscount)
    assert store_facade.discounts[0].store_id == store_id
    
    
def test_add_discount_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.add_discount('discount', datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,0,None,None)
        
def test_remove_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount', datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,store_id,None,None)
    assert len(store_facade.discounts) == 1
    store_facade.remove_discount(0)
    assert len(store_facade.discounts) == 0
    
def test_remove_discount_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.remove_discount(0)
        
    
def test_change_discount_description(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount', datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,store_id,None,None)
    store_facade.change_discount_description(0, 'new description')
    assert store_facade.discounts[0].discount_description == 'new description'
    
def test_change_discount_description_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.change_discount_description(0, 'new description')
        
def test_change_discount_percentage(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount', datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,store_id,None,None)
    store_facade.change_discount_percentage(0, 0.2)
    assert store_facade.discounts[0].percentage == 0.2
    
def test_change_discount_percentage_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.change_discount_percentage(0, 20.0)
        
     
def test_create_logical_composite_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount1', datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,store_id,None,None)
    store_facade.add_discount('discount2', datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,store_id,None,None)
    assert len(store_facade.discounts) == 2
    new_id=store_facade.create_logical_composite_discount('composite discount', datetime(2020, 1, 1), datetime(2020, 1, 2), -1, 0, 1, 1)
    assert len(store_facade.discounts) == 1
    assert store_facade.discounts[new_id].discount_description == 'composite discount'
    assert store_facade.discounts[new_id].starting_date == datetime(2020, 1, 1)
    assert store_facade.discounts[new_id].ending_date == datetime(2020, 1, 2)
    
    
    
def test_create_logical_composite_discount_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.create_logical_composite_discount('composite discount', datetime(2020, 1, 1), datetime(2020, 1, 2), -1, 0, 1, 0)
        
 
  
def test_create_numerical_composite_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount1', datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,store_id,None,None)
    store_facade.add_discount('discount2', datetime(2020, 1, 1), datetime(2020, 1, 2), 0.4,None,store_id,None,None)
    assert len(store_facade.discounts) == 2
    new_id=store_facade.create_numerical_composite_discount('composite discount', datetime(2020, 1, 1), datetime(2020, 1, 2), -1, [0, 1], 1)
    assert len(store_facade.discounts) == 1
    assert store_facade.discounts[new_id].discount_description == 'composite discount'
    assert store_facade.discounts[new_id].starting_date == datetime(2020, 1, 1)
    assert store_facade.discounts[new_id].ending_date == datetime(2020, 1, 2)
    
def test_create_numerical_composite_discount_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.create_numerical_composite_discount('composite discount', datetime(2020, 1, 1), datetime(2020, 1, 2), -1, [0, 1], 0)       



def test_assign_predicate_to_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount1', datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,store_id,None,None)
    store_facade.add_discount('discount2', datetime(2020, 1, 1), datetime(2020, 1, 2), 0.4,None,store_id,None,None)
    assert len(store_facade.discounts) == 2
    store_facade.assign_predicate_to_discount(0, [20], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None])
    assert isinstance(store_facade.discounts[0].predicate, AgeConstraint)
    
    
def test_assign_predicate_to_discount2(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_discount('discount1', datetime(2020, 1, 1), datetime(2020, 1, 2), 0.1,None,store_id,None,None)
    store_facade.add_discount('discount2', datetime(2020, 1, 1), datetime(2020, 1, 2), 0.4,None,store_id,None,None)
    assert len(store_facade.discounts) == 2
    locations: Dict = {'address_id': 1, 'address': 'address', 'city': 'city', 'state': 'state', 'country': 'country', 'postal_code': 'postal_code'}
    store_facade.assign_predicate_to_discount(0, [20,None],[None,locations] , [None,None], [None,None], [None,None], [None,None], [None,None], [None,None], [None,None], [None,None], [None,None], [None,None], [1])
    assert isinstance(store_facade.discounts[0].predicate, AndConstraint)
    
    
        
def test_get_total_price_before_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.get_store_by_id(store_id).add_product('product', 'very good product', 10.0, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(0, 10)
    shopping_basket= {0:3}
    shopping_cart= {store_id: shopping_basket}
    assert store_facade.get_total_price_before_discount(shopping_cart)==30.0

   
def test_get_total_basket_price_before_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.get_store_by_id(store_id).add_product('product', 'very good product', 10.0, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(0, 10)
    store_facade.add_discount('discount1', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.5,None,store_id,None,None)
    shopping_basket= {0:3}
    assert store_facade.get_total_basket_price_before_discount(store_id,shopping_basket)==30.0

def test_get_total_price_after_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.get_store_by_id(store_id).add_product('product', 'very good product', 10.0, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(0, 10)
    store_facade.add_discount('discount1', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.5,None,store_id,None,None)
    shopping_basket= {0:3}
    shopping_cart = {store_id: shopping_basket}
    assert store_facade.get_total_price_after_discount(shopping_cart, user_information_dto1)==15.0
   
    
def test_assign_predicate_to_discount_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.assign_predicate_to_discount(0, [20, 30], [{'city':'city1'}, {'city':'city2'}], [time(10, 0), time(12, 0)], [time(14, 0), time(16, 0)], [10.0, 20.0], [30.0, 40.0], [10.0, 20.0], [30.0, 40.0], [10, 20], [0, 1], [0, 1], [0, 1], [0, 1])
    

#specific unit tests that are requested in version 2:

#1. discount of 50% on all milk category products:
def test_apply_milk_category_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.get_store_by_id(store_id).add_product('product', 'very good product', 10.0, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(0, 10)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(0, 0,0)
    store_facade.add_discount('discount1', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.5,category_id,None,None,False)
    shopping_basket= {0:3}
    total_price_of_basket=30
    assert store_facade.apply_discount(0, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==15.0
    
#2. discount of 20% on all products in the store:
def test_apply_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.get_store_by_id(store_id).add_product('product', 'very good product', 10.0, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(0, 10)
    store_facade.add_discount('discount1', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.5,None,store_id,None,None)
    shopping_basket= {0:3}
    total_price_of_basket=30
    assert store_facade.apply_discount(0, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==15.0

#3. discount of 10% on tomatoes on a purchase that costs more than 200: (predicate)
def test_apply_tomatoes_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.get_store_by_id(store_id).add_product('tomatoes', 'very good product', 10.0, ['tag'], 30.0)
    store_facade.get_store_by_id(store_id).restock_product(0, 50)
    store_facade.add_discount('discount1', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.1,None,store_id,None,None)
    shopping_basket= {0:21}
    total_price_of_basket=210
    store_facade.assign_predicate_to_discount(0, [None], [None], [None], [None], [200.0], [-1], [None], [None], [None], [store_id], [None], [None], [None])
    assert store_facade.apply_discount(0, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==21.0

#4. discount on milk products or bread products but not on both (XOR):
def test_apply_milk_or_bread_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', 10.0, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('bread', 'very good product', 10.0, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    category_id2 = store_facade.add_category('bread')
    store_facade.assign_product_to_category(category_id2, store_id,product_id2)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    #milk discount
    store_facade.add_discount('discount1', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.1,category_id,None,None,False)
    #bread discount
    store_facade.add_discount('discount2', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.1,category_id2,None,None,False)
    shopping_basket= {product_id1:21, product_id2:21}
    total_price_of_basket=420
    new_id = store_facade.create_logical_composite_discount('composite discount', datetime(2020, 1, 1), datetime(2020, 1, 2), -1, 0, 1, 3)
    assert store_facade.apply_discount(new_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==21.0


#4.5 same test but with AND:
def test_apply_milk_and_bread_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', 10.0, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('bread', 'very good product', 10.0, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    category_id2 = store_facade.add_category('bread')
    store_facade.assign_product_to_category(category_id2, store_id,product_id2)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    #milk discount
    store_facade.add_discount('discount1', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.1,category_id,None,None,False)
    #bread discount
    store_facade.add_discount('discount2', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.1,category_id2,None,None,False)
    shopping_basket= {product_id1:21, product_id2:21}
    total_price_of_basket=420
    new_id = store_facade.create_logical_composite_discount('composite discount', datetime(2020, 1, 1), datetime(2020, 1, 2), -1, 0, 1, 1)
    assert store_facade.apply_discount(new_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==42.0

#4.5 same test but with OR:
def test_apply_milk_or_bread_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', 10.0, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('bread', 'very good product', 10.0, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    category_id2 = store_facade.add_category('bread')
    store_facade.assign_product_to_category(category_id2, store_id,product_id2)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    #milk discount
    store_facade.add_discount('discount1', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.1,category_id,None,None,False)
    #bread discount
    store_facade.add_discount('discount2', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.1,category_id2,None,None,False)
    shopping_basket= {product_id1:21, product_id2:21}
    total_price_of_basket=420
    new_id = store_facade.create_logical_composite_discount('composite discount', datetime(2020, 1, 1), datetime(2020, 1, 2), -1, 0, 1, 2)
    assert store_facade.apply_discount(new_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==42.0
    
#5 there is a baked goods discount of 5% on bread or baguette products only if the cart contains at least 5 bread and at least 2 cakes:
def test_apply_baked_goods_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('bread', 'very good product', 10.0, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('cake', 'very good product', 10.0, ['tag'], 30.0)
    category_id = store_facade.add_category('baked goods')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    store_facade.assign_product_to_category(category_id, store_id,product_id2)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    #bread discount
    temp1 = store_facade.add_discount('bread_discount', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.05,None,store_id,product_id1,None)
    store_facade.assign_predicate_to_discount(temp1, [None], [None], [None], [None], [None], [None], [None], [None], [5], [store_id], [product_id1], [None], [None])
    #cake discount
    temp2 = store_facade.add_discount('cake_discount', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.05,None,store_id,product_id2,None)
    store_facade.assign_predicate_to_discount(temp2, [None], [None], [None], [None], [None], [None], [None], [None], [2], [store_id], [product_id2], [None], [None])
    
    
    discount_id = store_facade.create_logical_composite_discount('bread_and_cake', datetime(2020, 1, 1), datetime(2050, 1, 2), -1, temp1, temp2, 1)
    shopping_basket= {product_id1:1, product_id2:1}
    total_price_of_basket=20.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==0.0

    shopping_basket= {product_id1:1, product_id2:2}
    total_price_of_basket=30.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==0.0

    
    shopping_basket= {product_id1:5, product_id2:1}
    total_price_of_basket=60.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==0.0

    
    shopping_basket= {product_id1:5, product_id2:2}
    total_price_of_basket=70
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==3.5

#6. discount of 5% on milk products if the cart contains at least 3 cottege cheese products or at least 2 yugurts:
def test_apply_milk_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', 10.0, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('cottage cheese', 'very good product', 10.0, ['tag'], 30.0)
    product_id3 = store_facade.get_store_by_id(store_id).add_product('yogurt', 'very good product', 10.0, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    store_facade.assign_product_to_category(category_id, store_id,product_id2)
    store_facade.assign_product_to_category(category_id, store_id,product_id3)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id3, 50)
    #cottage cheese discount
    temp1 = store_facade.add_discount('cottage_cheese_discount', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.05,None,store_id,product_id2,None)
    store_facade.assign_predicate_to_discount(temp1, [None], [None], [None], [None], [None], [None], [None], [None], [3], [store_id], [product_id2], [None], [None])
    #yogurt discount
    temp2 = store_facade.add_discount('yogurt_discount', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.05,None,store_id,product_id3,None)
    store_facade.assign_predicate_to_discount(temp2, [None], [None], [None], [None], [None], [None], [None], [None], [2], [store_id], [product_id3], [None], [None])
    
    
    discount_id = store_facade.create_logical_composite_discount('cottage_cheese_and_yogurt', datetime(2020, 1, 1), datetime(2050, 1, 2), -1, temp1, temp2, 2)
    shopping_basket= {product_id2:1, product_id3:1}
    total_price_of_basket=20.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==0.0
    
    
    shopping_basket= {product_id2:1, product_id3:3}
    total_price_of_basket=40.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==1.5
    
    
    shopping_basket= {product_id2:3, product_id3:1}
    total_price_of_basket=40.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==1.5
    
    shopping_basket= {product_id2:3, product_id3:3}
    total_price_of_basket=60.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==3.0
    
    
    
#7 if the cart total is more than 100 and the cart contains at least 3 pasts products, there is a 5% discount on milk product:
def test_apply_milk_discount2(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', 10.0, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('pasta', 'very good product', 10.0, ['tag'], 30.0)
    product_id3 = store_facade.get_store_by_id(store_id).add_product('fromage', 'une fromage tres jaune', 20.0, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    store_facade.assign_product_to_category(category_id, store_id,product_id3)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id3, 50)
    #pasta discount
    discount_id = store_facade.add_discount('milk_discount', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.05,category_id,None,None,False)
    store_facade.assign_predicate_to_discount(discount_id, [None,None], [None,None],[None,None], [None,None], [100.0,None],[-1,None], [None,None],[None,None], [None,3],[store_id,store_id],[None,product_id2],[None,None],[1])
    
    shopping_basket= {product_id1:1, product_id2:1, product_id3:1}
    total_price_of_basket=40.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==0.0
    
    
    shopping_basket= {product_id1:1, product_id2:3, product_id3:1}
    total_price_of_basket=60.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==0.0
    
    
    shopping_basket= {product_id1:10, product_id2:1, product_id3: 5}
    total_price_of_basket=210.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==0.0
    
    
    shopping_basket= {product_id1:10, product_id2:3,product_id3: 5}
    total_price_of_basket=230.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==10.0
    
    
#8. the discount that is given is the max between 5% of the pastas in the cart, and 17% of milk bottles in the cart:
def test_apply_max_discount(store_facade):
    store_id = store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', 10.0, ['tag'], 30.0)
    product_id2 = store_facade.get_store_by_id(store_id).add_product('pasta', 'very good product', 10.0, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    store_facade.get_store_by_id(store_id).restock_product(product_id2, 50)
    #pasta discount
    discount_id1 = store_facade.add_discount('pasta_discount', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.05,None,store_id,product_id2,None)
    #milk discount
    discount_id2 = store_facade.add_discount('milk_discount', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.17,category_id,None,None,False)
    
    
    discount_id = store_facade.create_numerical_composite_discount('max_discount', datetime(2020, 1, 1), datetime(2050, 1, 2), -1,[ discount_id1, discount_id2], 1)
    shopping_basket= {product_id1:1, product_id2:1}
    total_price_of_basket=20.0
    
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==(0.17*10.0)
    
    shopping_basket= {product_id1:1, product_id2:3}
    total_price_of_basket=40.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==(0.17*10.0)
    
    shopping_basket= {product_id1:10, product_id2:1}
    total_price_of_basket=120.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==(0.17*100.0)
    
    
    
#9. there is 5% discount on milk products and there is 20% discount on each store (so 25% discount on milk products):
def test_apply_additive_discount(store_facade):
    store_id= store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    product_id1 = store_facade.get_store_by_id(store_id).add_product('milk', 'very good product', 10.0, ['tag'], 30.0)
    category_id = store_facade.add_category('milk')
    store_facade.assign_product_to_category(category_id, store_id,product_id1)
    store_facade.get_store_by_id(store_id).restock_product(product_id1, 50)
    #milk discount
    discount_id1 = store_facade.add_discount('milk_discount', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.05,category_id,None,None,False)
    #store discount
    discount_id2 = store_facade.add_discount('store_discount', datetime(2020, 1, 1), datetime(2030, 1, 2), 0.2,None,store_id,None,None)
    
    discount_id = store_facade.create_numerical_composite_discount('additive_discount', datetime(2020, 1, 1), datetime(2050, 1, 2), -1,[ discount_id1, discount_id2], 2)
    shopping_basket= {product_id1:1}
    total_price_of_basket=10.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==2.5
    
    shopping_basket= {product_id1:3}
    total_price_of_basket=30.0
    assert store_facade.apply_discount(discount_id, store_id, total_price_of_basket, shopping_basket, user_information_dto1)==7.5
    
    
    


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
    with pytest.raises(ValueError):
        product.change_price(-1)
        
def test_change_weight(product):
    new_weight = 20.0
    product.change_weight(new_weight)
    assert product.weight == new_weight
    
def test_change_weight_fail(product):
    with pytest.raises(ValueError):
        product.change_weight(-1)
        



def test_add_tag(product):
    tag = 'tag'
    product.add_tag(tag)
    assert tag in product.tags

def test_add_tag_fail(product):
    tag = 'tag'
    product.add_tag(tag)
    with pytest.raises(ValueError):
        product.add_tag(tag)

def test_remove_tag(tagged_product):
    tag = 'tag'
    tagged_product.remove_tag(tag)
    assert tag not in tagged_product.tags

def test_remove_tag_fail(product):
    tag = 'tag'
    with pytest.raises(ValueError):
        product.remove_tag(tag)

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
    with pytest.raises(ValueError):
        category.add_parent_category(4)

def test_remove_parent_category(category):
    category.add_parent_category(3)
    category.remove_parent_category()
    assert category.parent_category_id == -1

def test_remove_parent_category_fail(category):
    with pytest.raises(ValueError):
        category.remove_parent_category()

def test_add_sub_category(sub_category, category):
    category.add_sub_category(sub_category)
    assert sub_category in category.sub_categories

def test_add_sub_category_fail_duplicate(sub_category, category):
    category.add_sub_category(sub_category)
    with pytest.raises(ValueError):
        category.add_sub_category(sub_category)

def test_add_sub_category_fail_parent(sub_category, category):
    sub_category.add_parent_category(3)
    with pytest.raises(ValueError):
        category.add_sub_category(sub_category)

def test_add_sub_category_fail_self(sub_category):
    with pytest.raises(ValueError):
        sub_category.add_sub_category(sub_category)

def test_remove_sub_category(sub_category, category):
    category.add_sub_category(sub_category)
    category.remove_sub_category(sub_category)
    assert sub_category not in category.sub_categories

def test_remove_sub_category_fail_missing(sub_category, category):
    with pytest.raises(ValueError):
        category.remove_sub_category(sub_category)

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
    with pytest.raises(ValueError):
        category.add_product_to_category(0, 0)

def test_remove_product_from_category(category):
    category.add_product_to_category(0, 0)
    category.remove_product_from_category(0, 0)
    assert (0,0) not in category.category_products

def test_remove_product_from_category_fail(category):
    with pytest.raises(ValueError):
        category.remove_product_from_category(0, 0)

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
    with pytest.raises(ValueError):
        store.close_store(1)

def test_add_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    assert len(store.store_products) == 1
    
def test_remove_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    store.remove_product(0)
    assert len(store.store_products) == 0

def test_remove_product_fail(store):
    with pytest.raises(ValueError):
        store.remove_product(0)

def test_get_product_by_id(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    product = store.get_product_by_id(0)
    assert product.product_id == 0
    assert product.product_name == product_dto.name
    assert product.description == product_dto.description
    assert product.price == product_dto.price
    assert product.tags == product_dto.tags

def test_get_product_by_id_fail(store):
    with pytest.raises(ValueError):
        store.get_product_by_id(0)

def test_get_product_dto_by_id(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    product_dto = store.get_product_dto_by_id(0)
    assert product_dto.product_id == 0
    assert product_dto.name == product_dto.name
    assert product_dto.description == product_dto.description
    assert product_dto.price == product_dto.price
    assert product_dto.tags == product_dto.tags

def test_get_product_dto_by_id_fail(store):
    with pytest.raises(ValueError):
        store.get_product_dto_by_id(0)

def test_get_total_price_of_basket_before_discount(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    store.add_product(product_dto.name, product_dto.description, product_dto.price + 10, product_dto.tags, product_dto.weight, product_dto.amount)
    assert store.get_total_price_of_basket_before_discount({0:1, 1:1}) == 30.0
    assert store.get_total_price_of_basket_before_discount({0:2}) == 20.0
    assert store.get_total_price_of_basket_before_discount({0:1, 1:2}) == 50.0

def test_get_total_price_of_basket_before_discount_fail(store):
    with pytest.raises(ValueError):
        store.get_total_price_of_basket_before_discount({0:1})

def test_create_store_dto(store):
    dto = store.create_store_dto()
    assert dto.store_id == store.store_id
    assert dto.store_name == store.store_name
    assert dto.store_founder_id == store.store_founder_id
    assert dto.location_id == store.location_id
    assert dto.is_active == store.is_active

def test_get_store_information(store):
    dto = store.create_store_dto()
    assert dto.store_id == store.store_id
    assert dto.store_name == store.store_name
    assert dto.store_founder_id == store.store_founder_id
    assert dto.location_id == store.location_id
    assert dto.is_active == store.is_active

def test_restock_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    store.restock_product(0, 10)
    assert store.has_amount_of_product(0, 10)

def test_restock_product_fail(store):
    with pytest.raises(ValueError):
        store.restock_product(0, 10)

def test_remove_product_amount(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    store.restock_product(0, 10)
    store.remove_product_amount(0, 5)
    assert store.has_amount_of_product(0, 5)

def test_remove_product_amount_fail_missing(store):
    with pytest.raises(ValueError):
        store.remove_product_amount(0, 5)

def test_remove_product_amount_fail_not_enough(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store.restock_product(0, 5)
    with pytest.raises(ValueError):
        store.remove_product_amount(0, 10)

def test_change_description_of_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store.change_description_of_product(0, 'new description')
    assert store.get_product_by_id(0).description == 'new description'

def test_change_description_of_product_fail(store):
    with pytest.raises(ValueError):
        store.change_description_of_product(0, 'new description')

def test_change_price_of_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store.change_price_of_product(0, 20.0)
    assert store.get_product_by_id(0).price == 20.0

def test_change_price_of_product_fail(store):
    with pytest.raises(ValueError):
        store.change_price_of_product(0, 20.0)

def test_add_tag_to_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store.add_tag_to_product(0, 'tag2')
    assert 'tag2' in store.get_product_by_id(0).tags

def test_add_tag_to_product_fail(store):
    with pytest.raises(ValueError):
        store.add_tag_to_product(0, 'tag2')

def test_remove_tag_from_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store.add_tag_to_product(0, 'tag2')
    store.remove_tag_from_product(0, 'tag2')
    assert 'tag2' not in store.get_product_by_id(0).tags

def test_remove_tag_from_product_fail_missing_product(store):
    with pytest.raises(ValueError):
        store.remove_tag_from_product(0, 'tag2')

def test_remove_tag_from_product_fail_missing_tag(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    with pytest.raises(ValueError):
        store.remove_tag_from_product(0, 'tag2')

def test_get_tags_of_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store.add_tag_to_product(0, 'tag2')
    assert store.get_tags_of_product(0) == ['tag', 'tag2']

def test_get_tags_of_product_fail(store):
    with pytest.raises(ValueError):
        store.get_tags_of_product(0)

def test_has_amount_of_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store.restock_product(0, 5)
    assert store.has_amount_of_product(0, 5)
    assert not store.has_amount_of_product(0, 6)

def test_has_amount_of_product_fail(store):
    assert not store.has_amount_of_product(0, 5)

def test_get_category_by_id(store_facade, category):
    store_facade.add_category(category.category_name)
    assert store_facade.get_category_by_id(0).category_name == category.category_name

def test_get_category_by_id_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.get_category_by_id(0)

def test_add_category(store_facade, category):
    store_facade.add_category(category.category_name)
    assert store_facade.get_category_by_id(0).category_name == category.category_name

def test_remove_category(store_facade, category):
    store_facade.add_category(category.category_name)
    store_facade.remove_category(0)
    with pytest.raises(ValueError):
        store_facade.get_category_by_id(0)

def test_remove_category_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.remove_category(0)

def test_assign_sub_category_to_category(store_facade, category, sub_category):
    store_facade.add_category(category.category_name)
    store_facade.add_category(sub_category.category_name)
    store_facade.assign_sub_category_to_category(1, 0)
    assert store_facade.get_category_by_id(0).sub_categories[0].category_name == sub_category.category_name

def test_assign_sub_category_to_category_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.assign_sub_category_to_category(1, 0)

def test_delete_sub_category_from_category(store_facade, category, sub_category):
    store_facade.add_category(category.category_name)
    store_facade.add_category(sub_category.category_name)
    store_facade.assign_sub_category_to_category(1, 0)
    store_facade.delete_sub_category_from_category(0, 1)
    assert len(store_facade.get_category_by_id(0).sub_categories) == 0

def test_delete_sub_category_from_category_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.delete_sub_category_from_category(0, 1)

def test_assign_product_to_category(store_facade, category, product_dto):
    store_facade.add_category(category.category_name)
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade._StoreFacade__get_store_by_id(0).add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store_facade.assign_product_to_category(0, 0, 0)

def test_assign_product_to_category_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.assign_product_to_category(0, 0, 0)

def test_remove_product_from_category2(store_facade, category, product_dto):
    store_facade.add_category(category.category_name)
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade._StoreFacade__get_store_by_id(0).add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store_facade.assign_product_to_category(0, 0, 0)
    store_facade.remove_product_from_category(0, 0, 0)
    assert len(store_facade.get_category_by_id(0).category_products) == 0

def test_remove_product_from_category_fail2(store_facade):
    with pytest.raises(ValueError):
        store_facade.remove_product_from_category(0, 0, 0)

def test_add_product_to_store(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.weight,product_dto.tags)

    assert len(store_facade._StoreFacade__get_store_by_id(0).store_products) == 1

def test_add_product_to_store_fail_store_id(store_facade, product_dto):
    with pytest.raises(ValueError):
        store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.tags)

def test_add_product_to_store_fail_product_name(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    with pytest.raises(ValueError):
        store_facade.add_product_to_store(0, '', product_dto.description, product_dto.price, product_dto.tags)

def test_add_product_to_store_fail_price(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    with pytest.raises(ValueError):
        store_facade.add_product_to_store(0, product_dto.name, product_dto.description, -1, 30.0, product_dto.tags)

def test_remove_product_from_store(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.weight, product_dto.tags)
    store_facade.remove_product_from_store(0, 0)
    assert len(store_facade._StoreFacade__get_store_by_id(0).store_products) == 0

def test_remove_product_from_store_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.remove_product_from_store(0, 0)

def test_add_product_amount(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price,product_dto.weight, product_dto.tags)
    store_facade.add_product_amount(0, 0, 10)
    assert store_facade._StoreFacade__get_store_by_id(0).has_amount_of_product(0, 10)

def test_add_product_amount_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.add_product_amount(0, 0, 10)

def test_remove_product_amount2(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.weight,product_dto.tags)
    store_facade.add_product_amount(0, 0, 10)
    store_facade.remove_product_amount(0, 0, 5)
    assert store_facade._StoreFacade__get_store_by_id(0).has_amount_of_product(0, 5)

def test_change_description_of_product2(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price,product_dto.weight, product_dto.tags)
    store_facade.change_description_of_product(0, 0, 'new description')
    assert store_facade._StoreFacade__get_store_by_id(0).get_product_by_id(0).description == 'new description'

def test_change_description_of_product_fail2(store_facade):
    with pytest.raises(ValueError):
        store_facade.change_description_of_product(0, 0, 'new description')

def test_change_price_of_product2(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price,product_dto.weight, product_dto.tags)
    store_facade.change_price_of_product(0, 0, 20.0)
    assert store_facade._StoreFacade__get_store_by_id(0).get_product_by_id(0).price == 20.0

def test_change_price_of_product_fail2(store_facade):
    with pytest.raises(ValueError):
        store_facade.change_price_of_product(0, 0, 20.0)

def test_add_tag_to_product2(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.weight,product_dto.tags)
    store_facade.add_tag_to_product(0, 0, 'tag2')
    assert 'tag2' in store_facade._StoreFacade__get_store_by_id(0).get_product_by_id(0).tags

def test_add_tag_to_product_fail2(store_facade):
    with pytest.raises(ValueError):
        store_facade.add_tag_to_product(0, 0, 'tag2')

def test_remove_tag_from_product2(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.weight,product_dto.tags)
    store_facade.add_tag_to_product(0, 0, 'tag2')
    store_facade.remove_tag_from_product(0, 0, 'tag2')
    assert 'tag2' not in store_facade._StoreFacade__get_store_by_id(0).get_product_by_id(0).tags

def test_remove_tag_from_product_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.remove_tag_from_product(0, 0, 'tag2')

def test_get_tags_of_product2(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.weight, product_dto.tags)
    store_facade.add_tag_to_product(0, 0, 'tag2')
    assert store_facade.get_tags_of_product(0, 0) == ['tag', 'tag2']

def test_get_tags_of_product_fail2(store_facade):
    with pytest.raises(ValueError):
        store_facade.get_tags_of_product(0, 0)

def test_add_store(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    assert store_facade._StoreFacade__get_store_by_id(0).store_name == 'store'

def test_close_store2(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.close_store(0, 0)
    assert not store_facade._StoreFacade__get_store_by_id(0).is_active

def test_close_store_fail2(store_facade):
    with pytest.raises(ValueError):
        store_facade.close_store(0, 0)

def test_get_store_by_id(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    assert store_facade._StoreFacade__get_store_by_id(0).store_name == 'store'

def test_get_store_by_id_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade._StoreFacade__get_store_by_id(0)

def test_get_total_price_before_discount(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_store(location_id=0, store_name='store2', store_founder_id=0)
    store_facade.add_product_to_store(0, 'product', 'description', 10.0, 21.0, ['tag'])
    store_facade.add_product_to_store(0, 'product2', 'description', 20.0, 21.0, ['tag'])
    store_facade.add_product_to_store(1, 'product', 'description', 10.0, 21.0, ['tag'])
    store_facade.add_product_to_store(1, 'product2', 'description', 20.0, 21.0, ['tag'])
    assert store_facade.get_total_price_before_discount({0: {0:1, 1:1}, 1: {0:1, 1:1}}) == 60.0

def test_get_total_price_before_discount_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.get_total_price_before_discount({0: {0:1, 1:1}, 1: {0:1, 1:1}})

def test_get_store_product_information(store_facade, product_dto, product_dto2):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
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
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.weight,product_dto.tags)
    store_facade.add_product_amount(0, 0, 10)
    assert store_facade.check_product_availability(0, 0, 10)
    assert not store_facade.check_product_availability(0, 0, 11)

def test_check_product_availability_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.check_product_availability(0, 0, 1)

def test_get_store_info(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    out = store_facade.get_store_info(0)
    assert out.store_id == 0
    assert out.store_name == 'store'
    assert out.store_founder_id == 0
    assert out.location_id == 0
    assert out.is_active

def test_search_by_category(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
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
    with pytest.raises(ValueError):
        store_facade.search_by_category(0)

def test_search_by_tags(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, 'product', 'description', 10.0, 10.0, ['tag'])
    out = store_facade.search_by_tags(['tag'])
    assert out[0][0].product_id == 0

def test_search_by_name(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, 'product', 'description', 10.0, 10.0, ['tag'])
    out = store_facade.search_by_name('product')
    assert out[0][0].product_id == 0

def test_search_in_store_by_category(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
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
    with pytest.raises(ValueError):
        store_facade.search_by_category(0, 0)

def test_search_in_store_by_tags(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, 'product', 'description', 10.0, 10.0, ['tag'])
    out = store_facade.search_by_tags(['tag'], 0)
    assert out[0][0].product_id == 0

def test_search_in_store_by_name(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, 'product', 'description', 10.0, 10.0, ['tag'])
    out = store_facade.search_by_name('product', 0)
    assert out[0][0].product_id == 0

def test_add_purchase_policy(store):
    store.add_purchase_policy("no_alcohol_and_tabbaco_bellow_18")
    assert len(store.purchase_policy) == 1
    assert store.purchase_policy[0] == "no_alcohol_and_tabbaco_bellow_18"

def test_add_purchase_policy_fail(store):
    with pytest.raises(ValueError):
        store.add_purchase_policy("hello")

def test_remove_purchase_policy(store):
    store.add_purchase_policy("no_alcohol_and_tabbaco_bellow_18")
    store.remove_purchase_policy("no_alcohol_and_tabbaco_bellow_18")
    assert len(store.purchase_policy) == 0

def test_remove_purchase_policy_fail(store):
    with pytest.raises(ValueError):
        store.remove_purchase_policy("no_alcohol_and_tabbaco_bellow_18")

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
    with pytest.raises(ValueError):
        store.check_purchase_policy(products, user_dto)

def test_add_purchase_policy_to_store(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_purchase_policy_to_store(0, "no_alcohol_and_tabbaco_bellow_18")
    assert store_facade._StoreFacade__get_store_by_id(0).purchase_policy[0] == "no_alcohol_and_tabbaco_bellow_18"

def test_add_purchase_policy_to_store_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.add_purchase_policy_to_store(0, "hello")

def test_remove_purchase_policy_from_store(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_purchase_policy_to_store(0, "no_alcohol_and_tabbaco_bellow_18")
    store_facade.remove_purchase_policy_from_store(0, "no_alcohol_and_tabbaco_bellow_18")
    assert len(store_facade._StoreFacade__get_store_by_id(0).purchase_policy) == 0

def test_remove_purchase_policy_from_store_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.remove_purchase_policy_from_store(0, "no_alcohol_and_tabbaco_bellow_18")

def test_validate_purchase_policies(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_store(location_id=0, store_name='store2', store_founder_id=0)
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
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_store(location_id=0, store_name='store2', store_founder_id=0)
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
    with pytest.raises(ValueError):
        store_facade.validate_purchase_policies(products, user_dto)


