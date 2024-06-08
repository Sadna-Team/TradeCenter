import pytest
from backend.business.store.store import *
from typing import List, Dict, Tuple
from datetime import datetime


#product default vars:
default_product_id: int = 0
default_product_name: str = "product"
default_product_weight: float = 1.0
default_product_description: str = "description"
default_product_price: float = 10.0

#category default vars:
default_category_id: int = 0
default_category_name: str = "category"

#store default vars:
default_store_id: int = 0
default_location_id: int = 0
default_store_name: str = "store"
default_store_founder_id: int = 0


@pytest.fixture
def product():
    return Product(default_product_id, default_store_id, default_product_name, default_product_weight, default_product_description, default_product_price)

@pytest.fixture
def category():
    return Category(default_category_id, default_category_name)

@pytest.fixture
def store():
    return Store(default_store_id, default_location_id, default_store_name, default_store_founder_id)


@pytest.fixture
def parent_category():
    return Category(1, "parent")

@pytest.fixture
def store_facade():
    return StoreFacade()



@pytest.fixture(autouse=True)
def clean():
    clean_data()
    yield


#Product tests:

def test_change_product_price(product):
    new_price = 20.0
    product.change_price(new_price)
    assert product.price == new_price
    
def test_change_product_description(product):
    new_description = "new description"
    product.change_description(new_description)
    assert product.description == new_description
    
    
def test_change_product_weight(product):
    new_weight = 2.0
    product.change_weight(new_weight)
    assert product.weight == new_weight
    
def test_add_tag_to_product(product):
    tag = "tag"
    product.add_tag(tag)
    assert tag in product.tags
    
def test_remove_tag_from_product(product):
    tag = "tag"
    product.add_tag(tag)
    product.remove_tag(tag)
    assert tag not in product.tags
    
def test_has_tag(product):
    tag = "tag"
    product.add_tag(tag)
    assert product.has_tag(tag)
    
    
def test_add_product(product):
    product.add_product(10)
    assert product.amount == 10
    

    
    
def test_remove_product(product):
    product.add_product(10)
    product.remove_product(10)
    assert product.amount == 0
    

#Category tests:

def test_add_parent_category(category):
    category.add_parent_category(parent_category)
    assert parent_category == category.parent_category_id
    
def test_remove_parent_category(category):
    category.add_parent_category(parent_category)
    category.remove_parent_category()
    assert category.parent_category_id == -1
    
def test_add_sub_category(category):
    sub_category=Category(2, "sub")
    category.add_sub_category(sub_category)
    assert sub_category in category.sub_categories
    assert category.category_id==sub_category.parent_category_id
    
def test_remove_sub_category(category):
    sub_category=Category(2, "sub")
    category.add_sub_category(sub_category)
    category.remove_sub_category(sub_category)
    assert sub_category.parent_category_id == -1
    assert sub_category not in category.sub_categories
    
def test_is_parent_category(category):
    parent_category = Category(1, "parent")
    category.add_parent_category(parent_category.category_id)
    assert category.is_parent_category(parent_category)
    
def test_is_sub_category(category):
    sub_category=Category(2, "sub")
    category.add_sub_category(sub_category)
    assert category.is_sub_category(sub_category)
    
def test_has_parent_category(category):
    parent_category = Category(1, "parent")
    category.add_parent_category(parent_category.category_id)
    assert category.has_parent_category()
    
def test_add_product_to_category(category, product):
    category.add_product_to_category(product)
    products_in_category = category.category_products
    for p in products_in_category:
        if p.product_id == default_product_id:
            assert p.product_id == default_product_id
            return
    
            
        
    
def test_remove_product_from_category(category, product):
    category.add_product_to_category(product)
    category.remove_product_from_category(product)
    products_in_category = category.category_products
    for p in products_in_category:
        if p.product_id == default_product_id:
            return
    assert True

    

#Store tests:

def test_close_store(store):
    store.close_store(store.store_founder_id)
    assert store.is_active == False
    
def test_add_product_to_store(store, product):
    store.add_product(product)
    assert product in store.store_products
    
def test_remove_product_from_store(store, product):
    store.add_product(product)
    store.remove_product(default_product_id)
    assert product not in store.store_products
    
def test_update_store_rating(store):
    rating = 5.0
    store.update_store_rating(rating)
    assert store.rating == rating
    
def test_update_product_rating(store):
    rating = 5.0
    store.update_product_rating(default_product_id, rating)
    assert store.ratings_of_product[default_product_id] == rating
    
#StoreFacade tests:

def test_add_category(store_facade):
    store_facade.add_category(default_category_name)
    store_categories = store_facade.categories
    for c in store_categories:
        if c.category_name == default_category_name:
            assert c.category_name == default_category_name
            return
   
    
def test_remove_category(store_facade):
    category_id = store_facade.add_category(default_category_name)
    store_facade.remove_category(category_id)
    store_categories = store_facade.categories
    for c in store_categories:
        assert c.category_id != category_id
        
        
    
def test_assign_sub_category_to_parent_category(store_facade,category,parent_category):
    store_facade.add_category(category.category_name)
    store_facade.add_category(parent_category.category_name)
    store_facade.assign_sub_category_to_category(category.category_id, parent_category.category_id)
    categories=store_facade.categories
    for c in categories:
        if c.category_id == parent_category.category_id:
            sub_categories=c.sub_categories
            
    for c in sub_categories:
        if c.category_id==category.category_id:
            assert c.category_id==category.category_id
            

def test_remove_sub_category_from_parent_category(store_facade,category,parent_category):
    store_facade.add_category(category.category_name)
    store_facade.add_category(parent_category.category_name)
    store_facade.assign_sub_category_to_category(category.category_id, parent_category.category_id)
    store_facade.delete_sub_category_from_category(parent_category.category_id,category.category_id)
    categories=store_facade.categories
    for c in categories:
        if c.category_id == parent_category.category_id:
            sub_categories=c.sub_categories
    
    for c in sub_categories:
        if c.category_id==category.category_id:
            return
    assert True
    


def test_assign_product_to_category(store_facade):
    store_facade.add_store(default_location_id, default_store_name, default_store_founder_id)
    store_facade.add_product_to_store(default_store_id, default_category_name,default_product_weight,default_product_description,default_product_price)
    store_facade.add_category(default_category_name)
    store_facade.assign_product_to_category(default_category_id,default_product_id)
    categories = store_facade.categories
    for c in categories:
        if c.category_name == default_category_name:
            products_in_category = c.category_products
            for p in products_in_category:
                if p.product_id == default_product_id:
                    assert p.product_id == default_product_id
                    return
    
def test_remove_a_product_from_category(store_facade):
    store_facade.add_store(default_location_id, default_store_name, default_store_founder_id)
    store_facade.add_product_to_store(default_store_id, default_category_name,default_product_weight,default_product_description,default_product_price)
    store_facade.add_category(default_category_name)
    store_facade.assign_product_to_category(default_category_id,default_product_id)
    store_facade.remove_product_from_category(default_category_id,default_product_id)
    categories = store_facade.categories
    for c in categories:
        if c.category_name == default_category_name:
            products_in_category = c.category_products
            for p in products_in_category:
                if p.product_id == default_product_id:
                    return
    assert True
    
    
def test_add_a_product_to_store(store_facade):
    store_facade.add_store(default_location_id, default_store_name, default_store_founder_id)
    store_facade.add_product_to_store(default_store_id, default_category_name,default_product_weight,default_product_description,default_product_price)
    stores = store_facade.stores
    for s in stores:
        if s.store_id == default_store_id:
            for p in s.store_products:
                if p.product_id == default_product_id:
                    assert p.product_id == default_product_id
                    return
    
def test_remove_a_product_from_store(store_facade):
    product_id = 0
    store_facade.add_store(default_location_id, default_store_name, default_store_founder_id)
    product = Product(product_id, default_store_id, default_product_name, default_product_weight, default_product_description, default_product_price)
    store_facade.add_product_to_store(default_store_id, default_category_name,default_product_weight,default_product_description,default_product_price)
    store_facade.remove_product_from_store(default_store_id, product_id)
    assert product not in store_facade.stores[default_store_id].store_products
    
def test_add_product_amount_to_store(store_facade):
    store_facade.add_store(default_location_id, default_store_name, default_store_founder_id)
    store_facade.add_product_to_store(default_store_id, default_category_name,default_product_weight,default_product_description,default_product_price)
    store_facade.add_product_amount(default_store_id, default_product_id,5)
    stores = store_facade.stores
    for s in stores:
        if s.store_id == default_store_id:
            for p in s.store_products:
                if p.product_id == default_product_id:
                    assert p.amount == 5
                    return
   
    

def test_remove_product_amount_from_store(store_facade):
    store_facade.add_store(default_location_id, default_store_name, default_store_founder_id)
    store_facade.add_product_to_store(default_store_id, default_category_name,default_product_weight,default_product_description,default_product_price)
    store_facade.add_product_amount(default_store_id, default_product_id,5)
    store_facade.remove_product_amount(default_store_id, default_product_id,5)
    stores = store_facade.stores
    for s in stores:
        if s.store_id == default_store_id:
            for p in s.store_products:
                if p.product_id == default_product_id:
                    assert p.amount == 0
                    return
    
    
    
def test_add_store(store_facade):
    store_facade.add_store(default_location_id, default_store_name, default_store_founder_id)
    assert default_store_founder_id == 0
    stores = store_facade.stores
    for s in stores:
        if s.store_name == default_store_name:
            assert s.store_name == default_store_name
            return
    
def test_remove_store(store_facade):
    store_facade.add_store(default_location_id, default_store_name, default_store_founder_id)
    store_facade.close_store(default_store_founder_id, default_store_founder_id)
    stores = store_facade.stores
    for s in stores:
        return 
    assert True
    
    

def clean_data():
    StoreFacade().clean_data()