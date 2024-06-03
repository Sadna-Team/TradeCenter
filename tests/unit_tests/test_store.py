import datetime
import pytest
from backend.business.store.store import *
from typing import List, Dict, Tuple


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
    
    
def test_add_product(product, store):
    product_id = product.add_product(store)
    assert product_id == product.id
    assert product in store.products
    
def test_remove_product(product, store):
    product_id = product.add_product(store)
    product.remove_product(store)
    assert product not in store.products
    

#Category tests:

def test_add_parent_category(category):
    parent_category = Category(1, "parent")
    category.add_parent_category(parent_category)
    assert parent_category in category.parent_categories
    
def test_remove_parent_category(category):
    parent_category = Category(1, "parent")
    category.add_parent_category(parent_category)
    category.remove_parent_category(parent_category)
    assert parent_category not in category.parent_categories
    
def test_add_sub_category(category):
    sub_category = Category(1, "sub")
    category.add_sub_category(sub_category)
    assert sub_category in category.sub_categories
    
def test_remove_sub_category(category):
    sub_category = Category(1, "sub")
    category.add_sub_category(sub_category)
    category.remove_sub_category(sub_category)
    assert sub_category not in category.sub_categories
    
def test_is_parent_category(category):
    parent_category = Category(1, "parent")
    category.add_parent_category(parent_category)
    assert category.is_parent_category(parent_category)
    
def test_is_sub_category(category):
    sub_category = Category(1, "sub")
    category.add_sub_category(sub_category)
    assert category.is_sub_category(sub_category)
    
def test_has_parent_category(category):
    parent_category = Category(1, "parent")
    category.add_parent_category(parent_category)
    assert category.has_parent_category(parent_category)
    
def test_add_product_to_category(category, product):
    category.add_product_to_category(product)
    assert product in category.products
    
def test_remove_product_from_category(category, product):
    category.add_product_to_category(product)
    category.remove_product_from_category(product)
    assert product not in category.products
    

#Store tests:

def test_close_store(store):
    store.close_store()
    assert store.is_active == False
    
def test_add_product_to_store(store, product):
    store.add_product(product)
    assert product in store.products
    
def test_remove_product_from_store(store, product):
    store.add_product(product)
    store.remove_product(product)
    assert product not in store.products
    
def test_update_store_rating(store):
    rating = 5
    store.update_store_rating(rating)
    assert store.rating == rating
    
def test_update_product_rating(product):
    rating = 5
    product.update_product_rating(rating)
    assert product.rating == rating
    
#StoreFacade tests:

def test_add_category():
    category_name = "category"
    category_id = StoreFacade().add_category(category_name)
    assert category_id == 0
    assert category_name in StoreFacade().categories
    
def test_remove_category():
    category_name = "category"
    category_id = StoreFacade().add_category(category_name)
    StoreFacade().remove_category(category_id)
    assert category_name not in StoreFacade().categories
    
def test_assign_sub_category_to_parent_category():
    parent_category_id = StoreFacade().add_category("parent")
    sub_category_id = StoreFacade().add_category("sub")
    StoreFacade().assign_sub_category_to_category(sub_category_id, parent_category_id)
    assert sub_category_id in StoreFacade().categories[parent_category_id].sub_categories
    
def test_remove_sub_category_from_parent_category():
    parent_category_id = StoreFacade().add_category("parent")
    sub_category_id = StoreFacade().add_category("sub")
    StoreFacade().assign_sub_category_to_category(sub_category_id, parent_category_id)
    StoreFacade().delete_sub_category_from_category(sub_category_id, parent_category_id)
    assert sub_category_id not in StoreFacade().categories[parent_category_id].sub_categories
    


def test_assign_product_to_category():
    product_id = 0
    product = Product(product_id, default_store_id, default_product_name, default_product_weight, default_product_description, default_product_price)
    category_id = StoreFacade().add_category("category")
    StoreFacade().assign_product_to_category(product, category_id)
    assert product in StoreFacade().categories[category_id].products
    
def test_remove_a_product_from_category():
    product_id = 0
    product = Product(product_id, default_store_id, default_product_name, default_product_weight, default_product_description, default_product_price)
    category_id = StoreFacade().add_category("category")
    StoreFacade().assign_product_to_category(product, category_id)
    StoreFacade().remove_product_from_category(product, category_id)
    assert product not in StoreFacade().categories[category_id].products
    
    
def test_add_a_product_to_store():
    product_id = 0
    product = Product(product_id, default_store_id, default_product_name, default_product_weight, default_product_description, default_product_price)
    StoreFacade().add_product_to_store(default_store_id, product)
    assert product in StoreFacade().stores[default_store_id].products
    
def test_remove_a_product_from_store():
    product_id = 0
    product = Product(product_id, default_store_id, default_product_name, default_product_weight, default_product_description, default_product_price)
    StoreFacade().add_product_to_store(default_store_id, product)
    StoreFacade().remove_product_from_store(default_store_id, product_id)
    assert product not in StoreFacade().stores[default_store_id].products
    
    
def test_add_product_amount_to_store():
    StoreFacade().add_product_amount(default_store_id, default_product_id,10)
    assert StoreFacade().stores[default_store_id].get_product_by_id(default_product_id).amount == 10
    

def test_remove_product_amount_from_store():
    StoreFacade().add_product_amount(default_store_id, default_product_id,5)
    StoreFacade().remove_product_amount(default_store_id, default_product_id,5)
    assert StoreFacade().stores[default_store_id].get_product_by_id(default_product_id).amount == 10
    
    
    
def test_add_store():
    store_id = StoreFacade().add_store(default_location_id, default_store_name, default_store_founder_id)
    assert store_id == 0
    assert default_store_name in StoreFacade().stores
    
def test_remove_store():
    store_id = StoreFacade().add_store(default_location_id, default_store_name, default_store_founder_id)
    StoreFacade().remove_store(store_id)
    assert default_store_name not in StoreFacade().stores
    
    

def clean_data():
    StoreFacade().clean_data()