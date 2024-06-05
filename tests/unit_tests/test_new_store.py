from datetime import datetime
from dateutil import relativedelta
import pytest
from backend.business.store.new_store import Store, Product, Category, StoreFacade
from backend.business.DTOs import ProductDTO, UserDTO

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

def test_change_description(product):
    new_description = 'new description'
    product.change_description(new_description)
    assert product.description == new_description

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
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
    store.restock_product(0, 10)
    store.remove_product_amount(0, 5)
    assert store.has_amount_of_product(0, 5)
    assert not store.has_amount_of_product(0, 6)

def test_remove_product_amount_fail_missing(store):
    with pytest.raises(ValueError):
        store.remove_product_amount(0, 5)

def test_remove_product_amount_fail_not_enough(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, 0)
    store.restock_product(0, 5)
    with pytest.raises(ValueError):
        store.remove_product_amount(0, 10)

def test_change_description_of_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
    store.change_description_of_product(0, 'new description')
    assert store.get_product_by_id(0).description == 'new description'

def test_change_description_of_product_fail(store):
    with pytest.raises(ValueError):
        store.change_description_of_product(0, 'new description')

def test_change_price_of_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
    store.change_price_of_product(0, 20.0)
    assert store.get_product_by_id(0).price == 20.0

def test_change_price_of_product_fail(store):
    with pytest.raises(ValueError):
        store.change_price_of_product(0, 20.0)

def test_add_tag_to_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
    store.add_tag_to_product(0, 'tag2')
    assert 'tag2' in store.get_product_by_id(0).tags

def test_add_tag_to_product_fail(store):
    with pytest.raises(ValueError):
        store.add_tag_to_product(0, 'tag2')

def test_remove_tag_from_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
    store.add_tag_to_product(0, 'tag2')
    store.remove_tag_from_product(0, 'tag2')
    assert 'tag2' not in store.get_product_by_id(0).tags

def test_remove_tag_from_product_fail_missing_product(store):
    with pytest.raises(ValueError):
        store.remove_tag_from_product(0, 'tag2')

def test_remove_tag_from_product_fail_missing_tag(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight, product_dto.amount)
    with pytest.raises(ValueError):
        store.remove_tag_from_product(0, 'tag2')

def test_get_tags_of_product(store, product_dto):
    store.add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
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

def test_remove_product_from_category(store_facade, category, product_dto):
    store_facade.add_category(category.category_name)
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade._StoreFacade__get_store_by_id(0).add_product(product_dto.name, product_dto.description, product_dto.price, product_dto.tags, product_dto.weight)
    store_facade.assign_product_to_category(0, 0, 0)
    store_facade.remove_product_from_category(0, 0, 0)
    assert len(store_facade.get_category_by_id(0).category_products) == 0

def test_remove_product_from_category_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.remove_product_from_category(0, 0, 0)

def test_add_product_to_store(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
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
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
    store_facade.remove_product_from_store(0, 0)
    assert len(store_facade._StoreFacade__get_store_by_id(0).store_products) == 0

def test_remove_product_from_store_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.remove_product_from_store(0, 0)

def test_add_product_amount(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
    store_facade.add_product_amount(0, 0, 10)
    assert store_facade._StoreFacade__get_store_by_id(0).has_amount_of_product(0, 10)

def test_add_product_amount_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.add_product_amount(0, 0, 10)

def test_remove_product_amount(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
    store_facade.add_product_amount(0, 0, 10)
    store_facade.remove_product_amount(0, 0, 5)
    assert store_facade._StoreFacade__get_store_by_id(0).has_amount_of_product(0, 5)

def test_change_description_of_product(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
    store_facade.change_description_of_product(0, 0, 'new description')
    assert store_facade._StoreFacade__get_store_by_id(0).get_product_by_id(0).description == 'new description'

def test_change_description_of_product_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.change_description_of_product(0, 0, 'new description')

def test_change_price_of_product(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
    store_facade.change_price_of_product(0, 0, 20.0)
    assert store_facade._StoreFacade__get_store_by_id(0).get_product_by_id(0).price == 20.0

def test_change_price_of_product_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.change_price_of_product(0, 0, 20.0)

def test_add_tag_to_product(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
    store_facade.add_tag_to_product(0, 0, 'tag2')
    assert 'tag2' in store_facade._StoreFacade__get_store_by_id(0).get_product_by_id(0).tags

def test_add_tag_to_product_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.add_tag_to_product(0, 0, 'tag2')

def test_remove_tag_from_product(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
    store_facade.add_tag_to_product(0, 0, 'tag2')
    store_facade.remove_tag_from_product(0, 0, 'tag2')
    assert 'tag2' not in store_facade._StoreFacade__get_store_by_id(0).get_product_by_id(0).tags

def test_remove_tag_from_product_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.remove_tag_from_product(0, 0, 'tag2')

def test_get_tags_of_product(store_facade, product_dto):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.weight, product_dto.tags)
    store_facade.add_tag_to_product(0, 0, 'tag2')
    assert store_facade.get_tags_of_product(0, 0) == ['tag', 'tag2']

def test_get_tags_of_product_fail(store_facade):
    with pytest.raises(ValueError):
        store_facade.get_tags_of_product(0, 0)

def test_add_store(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    assert store_facade._StoreFacade__get_store_by_id(0).store_name == 'store'

def test_close_store(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.close_store(0, 0)
    assert not store_facade._StoreFacade__get_store_by_id(0).is_active

def test_close_store_fail(store_facade):
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
    store_facade.add_product_to_store(0, product_dto.name, product_dto.description, product_dto.price, product_dto.tags)
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
    user_dto = UserDTO(user_id=0, birthdate=datetime.now().replace(year=datetime.now().year - 21))
    alcohol_product = ProductDTO(product_id=0, name='alcohol', description='description', price=10.0, tags=['alcohol'], weight=10.0, amount=10)
    tabbaco_product = ProductDTO(product_id=1, name='tabbaco', description='description', price=10.0, tags=['tabbaco'], weight=10.0, amount=10)
    gun_powder_product = ProductDTO(product_id=2, name='gun_powder', description='description', price=10.0, tags=['gun_powder'], weight=10.0, amount=5)
    products = {alcohol_product: 1, tabbaco_product: 1, gun_powder_product: 8}
    assert store.check_purchase_policy(products, user_dto) == None

def test_check_purchase_policy_fail(store):
    store.add_purchase_policy("no_alcohol_and_tabbaco_bellow_18")
    store.add_purchase_policy("not_too_much_gun_powder")
    user_dto = UserDTO(user_id=0, birthdate=datetime.now().replace(year=datetime.now().year - 17))
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
    user_dto = UserDTO(user_id=0, birthdate=datetime.now().replace(year=datetime.now().year - 21))
    store_facade.add_product_to_store(0, 'alcohol', 'description', 10.0, 10.0, ['alcohol'], 10)
    store_facade.add_product_to_store(0, 'tabbaco', 'description', 10.0, 10.0, ['tabbaco'], 10)
    store_facade.add_product_to_store(0, 'gun_powder', 'description', 10.0, 10.0, ['gun_powder'], 5)
    store_facade.add_product_to_store(1, 'alcohol', 'description', 10.0, 10.0, ['alcohol'], 10)
    store_facade.add_product_to_store(1, 'tabbaco', 'description', 10.0, 10.0, ['tabbaco'], 10)
    store_facade.add_product_to_store(1, 'gun_powder', 'description', 10.0, 10.0, ['gun_powder'], 5)
    products = {0: {0:1, 1:1, 2:4}, 1: {0:1, 1:1, 2:4}}
    assert store_facade.validate_purchase_policies(products, user_dto) == None

def test_validate_purchase_policies_fail(store_facade):
    store_facade.add_store(location_id=0, store_name='store', store_founder_id=0)
    store_facade.add_store(location_id=0, store_name='store2', store_founder_id=0)
    store_facade.add_purchase_policy_to_store(0, "no_alcohol_and_tabbaco_bellow_18")
    store_facade.add_purchase_policy_to_store(0, "not_too_much_gun_powder")
    store_facade.add_purchase_policy_to_store(1, "no_alcohol_and_tabbaco_bellow_18")
    store_facade.add_purchase_policy_to_store(1, "not_too_much_gun_powder")
    user_dto = UserDTO(user_id=0, birthdate=datetime.now().replace(year=datetime.now().year - 17))
    store_facade.add_product_to_store(0, 'alcohol', 'description', 10.0, 10.0, ['alcohol'], 10)
    store_facade.add_product_to_store(0, 'tabbaco', 'description', 10.0, 10.0, ['tabbaco'], 10)
    store_facade.add_product_to_store(0, 'gun_powder', 'description', 10.0, 10.0, ['gun_powder'], 5)
    store_facade.add_product_to_store(1, 'alcohol', 'description', 10.0, 10.0, ['alcohol'], 10)
    store_facade.add_product_to_store(1, 'tabbaco', 'description', 10.0, 10.0, ['tabbaco'], 10)
    store_facade.add_product_to_store(1, 'gun_powder', 'description', 10.0, 10.0, ['gun_powder'], 5)
    products = {0: {0:1, 1:1, 2:4}, 1: {0:1, 1:1, 2:4}}
    with pytest.raises(ValueError):
        store_facade.validate_purchase_policies(products, user_dto)
