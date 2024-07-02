from datetime import datetime
import pytest
from backend.business import MarketFacade, UserFacade, Authentication, PurchaseFacade
from backend.business.DTOs import BidPurchaseDTO
from backend.business.roles import RolesFacade
from typing import List, Optional
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from time import sleep
from backend.error_types import *


from backend.business.store.constraints import AgeConstraint

market_facade: Optional[MarketFacade] = None
user_facade: Optional[UserFacade] = None
purchase_facade: Optional[PurchaseFacade] = None
roles_facade: Optional[RolesFacade] = None

default_usernames = ['user1', 'user2', 'user3', 'user4', 'user5']
default_passwords = ['password1', 'password2', 'password3', 'password4', 'password5']
default_emails = ['email1', 'email2', 'email3', 'email4', 'email5']
default_years = [2010, 1991, 1992, 1993, 1994]
default_months = [1, 2, 3, 4, 5]
default_days = [1, 2, 3, 4, 5]
default_phones = ['0511111111', '0522222222', '0533333333', '0544444444', '0555555555']
default_currency = 'USD'

default_store_names = ['store1', 'store2', 'store3', 'store4', 'store5']

default_product_names = [['p11', 'p12', 'p13'],
                         ['p21', 'p22', 'p23'],
                         ['p31', 'p32', 'p33'],
                         ['p41', 'p42', 'p43'],
                         ['p51', 'p52', 'p53']]

default_product_descriptions = [['d11', 'd12', 'd13'],
                                ['d21', 'd22', 'd23'],
                                ['d31', 'd32', 'd33'],
                                ['d41', 'd42', 'd43'],
                                ['d51', 'd52', 'd53']]

default_product_prices = [[11, 12, 13],
                          [21, 22, 23],
                          [31, 32, 33],
                          [41, 42, 43],
                          [51, 52, 53]]

default_product_quantities = [[1, 2, 10],
                              [3, 1, 2],
                              [5, 4, 5],
                              [10, 10, 10],
                              [0, 0, 0]]

default_product_weights = [[0.1, 0.2, 0.3],
                           [0.4, 0.5, 0.6],
                           [0.7, 0.8, 0.9],
                           [1.0, 1.1, 1.2],
                           [1.3, 1.4, 1.5]]

default_tags = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', 'tag6', 'tag7', 'tag8', 'tag9', 'tag10']

default_product_tags = [[[default_tags[0], default_tags[1]],
                         [default_tags[2], default_tags[3]],
                         [default_tags[4], default_tags[5]]],
                        [[default_tags[6], default_tags[7]],
                         [default_tags[8], default_tags[9]],
                         [default_tags[0], default_tags[1]]],
                        [[default_tags[2], default_tags[3]],
                         [default_tags[4], default_tags[5]],
                         [default_tags[6], default_tags[7]]],
                        [[default_tags[8], default_tags[9]],
                         [default_tags[0], default_tags[1]],
                         [default_tags[2], default_tags[3]]],
                        [[default_tags[4], default_tags[5]],
                         [default_tags[6], default_tags[7]],
                         [default_tags[8], default_tags[9]]]]

default_payment_method = {'payment method': 'bogo'}

default_supply_method = "bogo"

default_address_checkout = {'address': 'randomstreet 34th', 'city': 'arkham', 'state': 'gotham', 'country': 'Wakanda', 'zip_code': '12345'}

default_store_address =  'elven street 420'
default_store_state = 'gothic'
default_store_city = 'Shiganshina'
default_store_country = 'paradis island'
default_store_zip_code = '139'

@pytest.fixture(scope='session', autouse=True)
def app():
    # Setup: Create the Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_secret_key'  # Set a test secret key
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
    auth = Authentication()
    auth.clean_data()
    auth.set_jwt(jwt, bcrypt)

    # Push application context for testing
    app_context = app.app_context()
    app_context.push()

    global market_facade
    global user_facade
    global purchase_facade
    global roles_facade

    market_facade = MarketFacade()
    user_facade = UserFacade()
    purchase_facade = PurchaseFacade()
    roles_facade = RolesFacade()

    # Make the app context available in tests
    yield app

    app_context.pop()


@pytest.fixture(scope='function', autouse=True)
def clean():
    yield
    market_facade.clean_data()


@pytest.fixture
def default_set_up():
    user_id1 = user_facade.create_user(default_currency)
    user_id2 = user_facade.create_user(default_currency)
    user_id3 = user_facade.create_user(default_currency)
    user_id4 = user_facade.create_user(default_currency)
    user_id5 = user_facade.create_user(default_currency)
    user_ids = [user_id1, user_id2, user_id3, user_id4, user_id5]

    user_facade.register_user(user_id1, default_emails[0], default_usernames[0], default_passwords[0], default_years[0],
                                default_months[0], default_days[0], default_phones[0])
    user_facade.register_user(user_id2, default_emails[1], default_usernames[1], default_passwords[1], default_years[1],
                                default_months[1], default_days[1], default_phones[1])
    user_facade.register_user(user_id3, default_emails[2], default_usernames[2], default_passwords[2], default_years[2],
                                default_months[2], default_days[2], default_phones[2])
    user_facade.register_user(user_id4, default_emails[3], default_usernames[3], default_passwords[3], default_years[3],
                                default_months[3], default_days[3], default_phones[3])
    user_facade.register_user(user_id5, default_emails[4], default_usernames[4], default_passwords[4], default_years[4],
                                default_months[4], default_days[4], default_phones[4])

    store_id1 = market_facade.add_store(user_id1, default_store_address, default_store_city, default_store_state, default_store_country, default_store_zip_code, default_store_names[0])
    store_id2 = market_facade.add_store(user_id2, default_store_address, default_store_city, default_store_state, default_store_country, default_store_zip_code, default_store_names[1])
    store_id3 = market_facade.add_store(user_id3, default_store_address, default_store_city, default_store_state, default_store_country, default_store_zip_code, default_store_names[2])
    store_id4 = market_facade.add_store(user_id4, default_store_address, default_store_city, default_store_state, default_store_country, default_store_zip_code, default_store_names[3])
    store_id5 = market_facade.add_store(user_id5, default_store_address, default_store_city, default_store_state, default_store_country, default_store_zip_code, default_store_names[4])

    store_ids = [store_id1, store_id2, store_id3, store_id4, store_id5]

    products: List[List[int]] = []
    for i in range(5):
        products.append([])
        for j in range(3):
            products[i].append(market_facade.add_product(user_ids[i],
                                                         store_ids[i],
                                                         default_product_names[i][j],
                                                         default_product_descriptions[i][j],
                                                         default_product_prices[i][j],
                                                         default_product_weights[i][j],
                                                         default_product_tags[i][j]))

    for i in range(5):
        for j in range(3):
            market_facade.add_product_amount(user_ids[i], store_ids[i], products[i][j],
                                             default_product_quantities[i][j])
            
    roles_facade.add_system_manager(0, user_id1)
    discount_id1 = market_facade.add_discount(user_id1, 'best you can find', datetime(2023, 10, 31), datetime(2050,10,31),0.3, store_id1, None, None, None)
    discount_id2 = market_facade.add_discount(user_id1, 'best you can find', datetime(2023, 10, 31), datetime(2050,10,31),0.2, store_id1, None, None, None)
    temp1 = market_facade.add_discount(user_id1, 'best you can find', datetime(2023, 10, 31), datetime(2050,10,31),0.1, store_id1, products[0][0], None, None)
    temp2 = market_facade.add_discount(user_id1, 'best you can find', datetime(2023, 10, 31), datetime(2050,10,31),0.3, store_id1, None, None, None)
    composite = market_facade.create_numerical_composite_discount(user_id1, 'max of the two', datetime(2024, 10, 31), datetime(2050,10,31), [temp1, temp2], 1)

    discount_ids = [discount_id1, discount_id2, composite]
    return user_ids, store_ids, products, discount_ids


@pytest.fixture
def default_user_cart(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    store_id2 = store_ids[1]
    product_id11 = products[0][0]
    product_id12 = products[0][1]
    product_id13 = products[0][2]
    product_id21 = products[1][0]
    market_facade.add_product_to_basket(user_id1, store_id1, product_id11, 1)
    market_facade.add_product_to_basket(user_id1, store_id1, product_id12, 2)
    market_facade.add_product_to_basket(user_id1, store_id1, product_id13, 3)
    market_facade.add_product_to_basket(user_id1, store_id2, product_id21, 1)
    return user_ids, store_ids, products


def test_add_product_to_basket(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    product_id12 = products[0][1]
    product_id13 = products[0][2]
    market_facade.add_product_to_basket(user_id1, store_id1, product_id11, 1)
    market_facade.add_product_to_basket(user_id1, store_id1, product_id12, 2)
    market_facade.add_product_to_basket(user_id1, store_id1, product_id13, 3)

    assert (market_facade.user_facade._UserFacade__get_user(user_id1)._User__shopping_cart
            ._ShoppingCart__shopping_baskets[store_id1]._ShoppingBasket__products[product_id11] == 1)
    assert (market_facade.user_facade._UserFacade__get_user(user_id1)._User__shopping_cart
            ._ShoppingCart__shopping_baskets[store_id1]._ShoppingBasket__products[product_id12] == 2)
    assert (market_facade.user_facade._UserFacade__get_user(user_id1)._User__shopping_cart
            ._ShoppingCart__shopping_baskets[store_id1]._ShoppingBasket__products[product_id13] == 3)




def test_checkout(default_user_cart):
    user_ids, store_ids, products = default_user_cart
    user_id1 = user_ids[0]
    user_id2 = user_ids[1]
    store_id1 = store_ids[0]
    store_id2 = store_ids[1]
    quantity_before = market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[
        products[0][0]].amount
    
    pur_id = market_facade.checkout(user_id1, default_payment_method, default_supply_method, default_address_checkout)

    assert not (market_facade.user_facade._UserFacade__get_user(user_id1)._User__shopping_cart
                ._ShoppingCart__shopping_baskets)
    assert len(purchase_facade.get_purchases_of_user(user_id1)) == 2  # two stores so two receipts
    assert len(purchase_facade.get_purchases_of_store(store_id1)) == 1
    assert len(purchase_facade.get_purchases_of_store(store_id2)) == 1
    quantity_after = market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[
        products[0][0]].amount
    assert quantity_before > quantity_after
    assert purchase_facade._PurchaseFacade__check_if_purchase_exists(pur_id)

    # user notification part
    assert len(market_facade.show_notifications(user_id1)) == 1
    assert len(market_facade.show_notifications(user_id2)) == 1
    # notifications cleared
    assert len(market_facade.show_notifications(user_id1)) == 0
    assert len(market_facade.show_notifications(user_id2)) == 0

    sleep(7)  # wait for bogo supply method to complete the purchase

    assert purchase_facade.check_if_purchase_completed(pur_id)


def test_checkout_failed_shopping_cart_empty(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    with pytest.raises(StoreError) as e:
        market_facade.checkout(user_id1, default_payment_method, default_supply_method, default_address_checkout)
    assert e.value.store_error_type == StoreErrorTypes.cart_is_empty


def test_checkout_failed_payment_method(default_user_cart):
    user_ids, store_ids, products = default_user_cart
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    quantity_before = market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[
        products[0][0]].amount
    with pytest.raises(ThirdPartyHandlerError) as e:
        market_facade.checkout(user_id1, {}, default_supply_method, default_address_checkout)
    assert e.value.third_party_handler_error_type == ThirdPartyHandlerErrorTypes.payment_not_specified
    
    assert (market_facade.user_facade._UserFacade__get_user(user_id1)._User__shopping_cart
            ._ShoppingCart__shopping_baskets)
    assert len(purchase_facade.get_purchases_of_user(user_id1)) == 0
    quantity_after = market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[
        products[0][0]].amount
    assert quantity_before == quantity_after


def test_checkout_failed_no_products(default_user_cart):
    user_ids, store_ids, products = default_user_cart
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    store_id5 = store_ids[4]
    market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products = {}
    with pytest.raises(StoreError) as e:
        market_facade.checkout(user_id1, default_payment_method, default_supply_method, default_address_checkout)
    assert e.value.store_error_type == StoreErrorTypes.product_not_found
    assert (market_facade.user_facade._UserFacade__get_user(user_id1)._User__shopping_cart
            ._ShoppingCart__shopping_baskets)
    assert len(purchase_facade.get_purchases_of_store(user_id1)) == 0

def test_nominate_store_owner(default_set_up):
    # User with user_id1 (The owner of store_id1 ) nominates user with user_id2 as store owner 
    user_ids, store_ids, _, __ = default_set_up
    user_id1 = user_ids[0]
    user_id2 = user_ids[1]
    user2_username = market_facade.user_facade.get_userDTO(user_id2).username
    store_id1 = store_ids[0]
    market_facade.nominate_store_owner(store_id1, user_id1, user2_username)
    assert market_facade.user_facade._UserFacade__get_user(user_id2).get_notifications().__len__() == 1

def test_nominate_store_owner_failed_user_not_owner(default_set_up):
    # User with user_id1 (The owner of store_id1 ) nominates user with user_id2 as store owner 
    user_ids, store_ids, _, __ = default_set_up
    user_id1 = user_ids[0]
    user_id2 = user_ids[1]
    user2_username = market_facade.user_facade.get_userDTO(user_id2).username
    store_id1 = store_ids[1]
    with pytest.raises(RoleError) as e:
        market_facade.nominate_store_owner(store_id1, user_id1, user2_username)
    assert e.value.role_error_type == RoleErrorTypes.nominator_not_member_of_store
    
def test_nominate_store_owner_failed_user_already_owner(default_set_up):
    user_ids, store_ids, products, _ = default_set_up
    user_id1 = user_ids[0]
    user1_username = market_facade.user_facade.get_userDTO(user_id1).username
    store_id1 = store_ids[1]
    with pytest.raises(RoleError) as e:
        market_facade.nominate_store_owner(store_id1, user_id1, user1_username)
    assert e.value.role_error_type == RoleErrorTypes.nominator_not_member_of_store
    
def test_nominate_store_manager(default_set_up):
    user_ids, store_ids, products, _ = default_set_up
    user_id1 = user_ids[0]
    user_id2 = user_ids[1]
    user2_username = market_facade.user_facade.get_userDTO(user_id2).username
    store_id1 = store_ids[0]
    market_facade.nominate_store_manager(store_id1, user_id1, user2_username)
    assert market_facade.user_facade._UserFacade__get_user(user_id2).get_notifications().__len__() == 1

def test_nominate_store_manager_failed_user_not_owner(default_set_up):
    user_ids, store_ids, products, _ = default_set_up
    user_id1 = user_ids[0]
    user_id2 = user_ids[1]
    user2_username = market_facade.user_facade.get_userDTO(user_id2).username
    store_id1 = store_ids[1]
    with pytest.raises(RoleError) as e:
        market_facade.nominate_store_manager(store_id1, user_id1, user2_username)
    assert e.value.role_error_type == RoleErrorTypes.nominator_not_member_of_store

def test_nominate_store_manager_failed_user_already_owner(default_set_up):
    user_ids, store_ids, products, _ = default_set_up
    user_id1 = user_ids[0]
    user1_username = market_facade.user_facade.get_userDTO(user_id1).username
    store_id1 = store_ids[1]
    with pytest.raises(RoleError) as e:
        market_facade.nominate_store_manager(store_id1, user_id1, user1_username)
    assert e.value.role_error_type == RoleErrorTypes.nominator_not_member_of_store

def test_accept_nomination():
    pass

def test_change_permissions():
    pass

def test_remove_role():
    pass

def test_add_system_manager():
    pass

def test_remove_system_manager():
    pass

def test_add_payment_method():
    pass

def test_edit_payment_method():
    pass

def test_remove_payment_method():
    pass

def test_add_supply_method():
    pass

def test_edit_supply_method():
    pass

def test_remove_supply_method():
    pass



#-----------------------------------------------------------


# more thorough tests in the unit tests of new_store.py !!!
def test_add_discount(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    discount_id1 = market_facade.add_discount(user_id1, 'best you can find', datetime(2023, 10, 31), datetime(2050,10,31), 0.3, store_id1, None, None, None)
    assert market_facade.store_facade.discounts.get(discount_id1).discount_description == 'best you can find'
    assert market_facade.store_facade.discounts.get(discount_id1).starting_date == datetime(2023, 10, 31)
    assert market_facade.store_facade.discounts.get(discount_id1).ending_date == datetime(2050,10,31)
    assert market_facade.store_facade.discounts.get(discount_id1).percentage == 0.3
    
    
def test_add_discount_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    with pytest.raises(UserError) as e:
        market_facade.add_discount(user_id1+1, 'best you can find', datetime(2023, 10, 31), datetime(2050,10,31), 0.3, store_id1, None, None, None)
    assert e.value.user_error_type == UserErrorTypes.user_not_system_manager   


def test_remove_discount(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    discount_id1 = discount_ids[0]
    market_facade.remove_discount(user_id1, discount_id1)
    assert discount_id1 not in market_facade.store_facade.discounts
    
def test_remove_discount_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    discount_id1 = discount_ids[0]
    with pytest.raises(UserError) as e:
        market_facade.remove_discount(user_id1+1, discount_id1)
    assert e.value.user_error_type == UserErrorTypes.user_not_system_manager
        

def test_create_logical_composite_discount(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    discount_id1 = discount_ids[0]
    discount_id2 = discount_ids[1]
    composite = market_facade.create_logical_composite_discount(user_id1, 'max of the two', datetime(2024, 10, 31), datetime(2050,10,31), discount_id1, discount_id2, 1)
    assert composite in market_facade.store_facade.discounts
    assert market_facade.store_facade.discounts.get(composite).discount_description == 'max of the two'
    assert market_facade.store_facade.discounts.get(composite).starting_date == datetime(2024, 10, 31)
    assert market_facade.store_facade.discounts.get(composite).ending_date == datetime(2050,10,31)
    assert market_facade.store_facade.discounts.get(composite).discount_id == composite
    assert market_facade.store_facade.discounts.get(composite).is_simple_discount()==True
    
def test_create_logical_composite_discount_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    discount_id1 = discount_ids[0]
    discount_id2 = discount_ids[1]
    with pytest.raises(UserError) as e:
        market_facade.create_logical_composite_discount(user_id1+1, 'max of the two', datetime(2024, 10, 31), datetime(2050,10,31), discount_id1, discount_id2, 1)
    assert e.value.user_error_type == UserErrorTypes.user_not_system_manager    

def test_create_numerical_composite_discount(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    discount_id1 = discount_ids[0]
    discount_id2 = discount_ids[1]
    composite = market_facade.create_numerical_composite_discount(user_id1, 'max of the two', datetime(2024, 10, 31), datetime(2050,10,31), [discount_id1, discount_id2], 1)
    assert composite in market_facade.store_facade.discounts
    assert market_facade.store_facade.discounts.get(composite).discount_description == 'max of the two'
    assert market_facade.store_facade.discounts.get(composite).starting_date == datetime(2024, 10, 31)
    assert market_facade.store_facade.discounts.get(composite).ending_date == datetime(2050,10,31)
    assert market_facade.store_facade.discounts.get(composite).discount_id == composite
    assert market_facade.store_facade.discounts.get(composite).is_simple_discount()==True
    
    
def test_create_numerical_composite_discount_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    discount_id1 = discount_ids[0]
    discount_id2 = discount_ids[1]
    with pytest.raises(UserError) as e:
        market_facade.create_numerical_composite_discount(user_id1+1, 'max of the two', datetime(2024, 10, 31), datetime(2050,10,31), [discount_id1, discount_id2], 1)
    assert e.value.user_error_type == UserErrorTypes.user_not_system_manager    

def test_assign_predicate_to_discount(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    discount_id1 = discount_ids[0]

    market_facade.assign_predicate_to_discount(user_id1, discount_id1,('age',21))
    assert isinstance(market_facade.store_facade.discounts.get(discount_id1).predicate, AgeConstraint)
    
    
def test_assign_predicate_to_discount_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id2 = user_ids[1]
    discount_id1 = discount_ids[0]
    with pytest.raises(UserError) as e:
        market_facade.assign_predicate_to_discount(user_id2, discount_id1,('age',21))
    assert e.value.user_error_type == UserErrorTypes.user_not_system_manager
    assert market_facade.store_facade.discounts.get(discount_id1).predicate == None


    

def test_change_discount_percentage(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    discount_id1 = discount_ids[0]
    market_facade.change_discount_percentage(user_id1, discount_id1, 0.5)
    assert market_facade.store_facade.discounts.get(discount_id1).percentage == 0.5
    
def test_change_discount_percentage_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    discount_id1 = discount_ids[0]
    with pytest.raises(UserError) as e:
        market_facade.change_discount_percentage(user_id1+1, discount_id1, 0.5)
    assert e.value.user_error_type == UserErrorTypes.user_not_system_manager 
    assert market_facade.store_facade.discounts.get(discount_id1).percentage != 0.5

def test_change_discount_description(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    discount_id1 = discount_ids[0]
    market_facade.change_discount_description(user_id1, discount_id1, 'new description')
    assert market_facade.store_facade.discounts.get(discount_id1).discount_description == 'new description'
    
def test_change_discount_description_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    discount_id1 = discount_ids[0]
    with pytest.raises(UserError) as e:
        market_facade.change_discount_description(user_id1+1, discount_id1, 'new description')
    assert e.value.user_error_type == UserErrorTypes.user_not_system_manager
    assert market_facade.store_facade.discounts.get(discount_id1).discount_description != 'new description'
    
#-----------------------------------------------------------

#tests for bid purchase:

      
def test_user_bid_offer(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    assert len(market_facade.store_facade.get_store_by_id(store_id1).purchase_policy)==0
    policy_id1 = market_facade.user_bid_offer(user_id1, 10, store_id1, product_id11)
    assert policy_id1 in market_facade.store_facade.get_store_by_id(store_id1).purchase_policy
    
      
def test_worker_accept_bid(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    policy_id1 = market_facade.user_bid_offer(user_id1, 10, store_id1, product_id11)
    market_facade.store_worker_accept_bid(store_id1, user_id1, policy_id1)
    assert policy_id1 not in market_facade.store_facade.get_store_by_id(store_id1).purchase_policy
    

def test_worker_decline_bid(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    policy_id1 = market_facade.user_bid_offer(user_id1, 10, store_id1, product_id11)
    market_facade.store_worker_decline_bid(store_id1, user_id1, policy_id1)
    assert policy_id1 not in market_facade.store_facade.get_store_by_id(store_id1).purchase_policy
    
     
def test_worker_counter_bid(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    policy_id1 = market_facade.user_bid_offer(user_id1, 10, store_id1, product_id11)
    market_facade.store_worker_counter_bid(store_id1, user_id1, policy_id1, 20)
    assert policy_id1 in market_facade.store_facade.get_store_by_id(store_id1).purchase_policy
    
      
def test_user_counter_bid_accept(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    policy_id1 = market_facade.user_bid_offer(user_id1, 10, store_id1, product_id11)
    market_facade.store_worker_counter_bid(store_id1, user_id1, policy_id1, 20)
    market_facade.user_counter_bid_accept(user_id1, policy_id1)
    assert policy_id1 not in market_facade.store_facade.get_store_by_id(store_id1).purchase_policy
    
      
def test_user_counter_bid_decline(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    policy_id1 = market_facade.user_bid_offer(user_id1, 10, store_id1, product_id11)
    market_facade.store_worker_counter_bid(store_id1, user_id1, policy_id1, 20)
    market_facade.user_counter_bid_decline(user_id1, policy_id1)
    assert policy_id1 not in market_facade.store_facade.get_store_by_id(store_id1).purchase_policy
    
       
def test_user_counter_bid(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    policy_id1 = market_facade.user_bid_offer(user_id1, 10, store_id1, product_id11)
    market_facade.store_worker_counter_bid(store_id1, user_id1, policy_id1, 20)
    market_facade.user_counter_bid(user_id1, policy_id1, 15)
    assert policy_id1 in market_facade.store_facade.get_store_by_id(store_id1).purchase_policy
    
     
def test_show_user_bids(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    policy_id1 = market_facade.user_bid_offer(user_id1, 10, store_id1, product_id11)
    assert market_facade.show_user_bids(0, user_id1) == [BidPurchaseDTO(policy_id1, 10, store_id1, product_id11)]
    
       
def test_show_store_bids(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    policy_id1 = market_facade.user_bid_offer(user_id1, 10, store_id1, product_id11)
    assert market_facade.show_store_bids(user_id1, store_id1) == [BidPurchaseDTO(policy_id1, 10, store_id1, product_id11)]
    
    
    


#-----------------------------------------------------------



def test_add_purchase_policy(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    assert len(market_facade.store_facade.get_store_by_id(store_id1).purchase_policy)==0
    policy_id1 = market_facade.add_purchase_policy(user_id1, store_id1, 'policy1', None, None)
    assert policy_id1 in market_facade.store_facade.get_store_by_id(store_id1).purchase_policy

def test_add_purchase_policy_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    with pytest.raises(UserError) as e:
        market_facade.add_purchase_policy(user_id1+1, store_id1, 'policy1', None, None)
    assert e.value.user_error_type == UserErrorTypes.user_does_not_have_necessary_permissions
    assert len(market_facade.store_facade.get_store_by_id(store_id1).purchase_policy)==0


def test_remove_purchase_policy(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    policy_id1 = market_facade.add_purchase_policy(user_id1, store_id1, 'policy1', None, None)
    market_facade.remove_purchase_policy(user_id1, store_id1, policy_id1)
    assert policy_id1 not in market_facade.store_facade._StoreFacade__get_store_by_id(store_id1).purchase_policy

def test_remove_purchase_policy_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    policy_id1 = market_facade.add_purchase_policy(user_id1, store_id1, 'policy1', None, None)
    with pytest.raises(UserError) as e:
        market_facade.remove_purchase_policy(user_id1+1, store_id1, policy_id1)
    assert e.value.user_error_type == UserErrorTypes.user_does_not_have_necessary_permissions
    assert policy_id1 in market_facade.store_facade._StoreFacade__get_store_by_id(store_id1).purchase_policy



def test_create_purchase_policy(default_set_up): 
    #test specific product policy
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    assert len(market_facade.store_facade.get_store_by_id(store_id1).purchase_policy) == 0
    policy_a =market_facade.add_purchase_policy(user_id1, store_id1, 'policy1', None, None)
    policy_b = market_facade.add_purchase_policy(user_id1, store_id1, 'policy2', None, None)
    policy_id1 = market_facade.create_composite_purchase_policy(user_id1, store_id1, 'or policy',policy_a ,policy_b , 2)
    assert policy_id1 in market_facade.store_facade.get_store_by_id(store_id1).purchase_policy
    
    
def test_create_purchase_policy_no_permission(default_set_up):
    #test specific product policy
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    with pytest.raises(UserError) as e:
        policy_a =market_facade.add_purchase_policy(user_id1, store_id1, 'policy1', None, None)
        policy_b = market_facade.add_purchase_policy(user_id1, store_id1, 'policy2', None, None)
        policy_id1 = market_facade.create_composite_purchase_policy(user_id1+1, store_id1, 'or policy',policy_a ,policy_b , 2)
        assert policy_id1 not in market_facade.store_facade.get_store_by_id(store_id1).purchase_policy
    assert e.value.user_error_type == UserErrorTypes.user_does_not_have_necessary_permissions
    
   

def test_assign_predicate_to_purchase_policy(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    policy_a =market_facade.add_purchase_policy(user_id1, store_id1, 'policy1', None, None)
    market_facade.assign_predicate_to_purchase_policy(user_id1,store_id1, policy_a,('age',21))
    assert isinstance(market_facade.store_facade.get_store_by_id(store_id1).get_policy_by_id(policy_a).predicate, AgeConstraint)
    
    

def test_add_product(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id14 = market_facade.add_product(user_id1, store_id1, 'p14', 'd14', 14, 0.4, [])
    assert product_id14 in market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products
    assert market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id14].product_name == 'p14'
    assert market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id14].description == 'd14'
    assert market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id14].price == 14
    assert market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id14].weight == 0.4

def test_remove_product(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id14 = market_facade.add_product(user_id1, store_id1, 'p14', 'd14', 14, 0.4, [])
    market_facade.remove_product(user_id1, store_id1, product_id14)
    assert product_id14 not in market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products
    

def test_add_product_amount(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id14 = market_facade.add_product(user_id1, store_id1, 'p14', 'd14', 14, 0.4, [])
    market_facade.add_product_amount(user_id1, store_id1, product_id14, 14)
    assert market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id14].amount == 14

def test_add_store(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id6 = market_facade.add_store(user_id1, 'address', 'fiji', 'fiji', 'fiji', '00000', 'store6')
    assert store_id6 in market_facade.store_facade._StoreFacade__stores
    assert market_facade.store_facade._StoreFacade__get_store_by_id(store_id6).store_name == 'store6'
    

def test_remove_store(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id6 = market_facade.add_store(user_id1, 'jujutsu high', 'tokyo', 'tokyo province', 'japan', '000', 'store6')
    market_facade.close_store(user_id1, store_id6)
    assert market_facade.store_facade.get_store_by_id(store_id6).is_active == False

def test_remove_store_bad_id(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    with pytest.raises(StoreError) as e:
        market_facade.close_store(user_id1, 6)
    assert e.value.store_error_type == StoreErrorTypes.store_not_found


def test_add_tag_to_product(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    market_facade.add_tag_to_product(user_id1, store_id1, product_id11, 'tag11')
    assert 'tag11' in market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id11].tags

def test_remove_tag_from_product(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    market_facade.add_tag_to_product(user_id1, store_id1, product_id11, 'tag11')
    assert 'tag11' in market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id11].tags
    market_facade.remove_tag_from_product(user_id1, store_id1, product_id11, 'tag11')
    assert 'tag11' not in market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id11].tags
    

def test_change_product_price(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    market_facade.change_product_price(user_id1, store_id1, product_id11, 14)
    assert market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id11].price == 14
    
def test_change_product_price_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    with pytest.raises(UserError) as e:
        market_facade.change_product_price(user_id1+1, store_id1, product_id11, 14)
    assert e.value.user_error_type == UserErrorTypes.user_does_not_have_necessary_permissions
    assert market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id11].price != 14

    

def test_change_product_description(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    market_facade.change_product_description(user_id1, store_id1, product_id11, 'd14')
    assert market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id11].description == 'd14'

def test_change_product_description_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    with pytest.raises(UserError) as e:
        market_facade.change_product_description(user_id1+1, store_id1, product_id11, 'd14')
    assert e.value.user_error_type == UserErrorTypes.user_does_not_have_necessary_permissions
    assert market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id11].description != 'd14'

def test_change_product_weight(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    market_facade.change_product_weight(user_id1, store_id1, product_id11, 0.5)
    assert market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id11].weight == 0.5
    
def test_change_product_weight_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    product_id11 = products[0][0]
    with pytest.raises(UserError) as e:
        market_facade.change_product_weight(user_id1+1, store_id1, product_id11, 0.5)
    assert e.value.user_error_type == UserErrorTypes.user_does_not_have_necessary_permissions
    assert market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[product_id11].weight != 0.5

def test_add_category(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    category_id=market_facade.add_category(user_id1, 'category1')
    assert category_id in market_facade.store_facade.categories
    
def test_add_category_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    with pytest.raises(UserError) as e:
        category_id=market_facade.add_category(user_id1+1, 'category1')
    assert e.value.user_error_type == UserErrorTypes.user_not_system_manager
    

def test_remove_category(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    category_id=market_facade.add_category(user_id1, 'category1')
    market_facade.remove_category(user_id1, category_id)
    assert category_id not in market_facade.store_facade.categories
    
def test_remove_category_no_permission(default_set_up):
    user_ids, store_ids, productsS, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    category_id=market_facade.add_category(user_id1, 'category1')
    with pytest.raises(UserError) as e:
        market_facade.remove_category(user_id1+1, category_id)   
    assert e.value.user_error_type == UserErrorTypes.user_not_system_manager
        

def test_add_sub_category_to_category(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    category_id=market_facade.add_category(user_id1, 'category1')
    sub_category_id = market_facade.add_category(user_id1, 'sub_category1')
    market_facade.add_sub_category_to_category(user_id1, sub_category_id, category_id)
    
    assert market_facade.store_facade.get_category_by_id(sub_category_id) in market_facade.store_facade.get_category_by_id(category_id).sub_categories
    

def test_add_sub_category_to_category_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    user_id2 = user_ids[1]
    category_id = market_facade.add_category(user_id1, 'category1')
    sub_category_id = market_facade.add_category(user_id1, 'sub_category1')
    sub_category_id 
    with pytest.raises(UserError) as e:
        market_facade.add_sub_category_to_category(user_id2, sub_category_id ,category_id)
    assert e.value.user_error_type == UserErrorTypes.user_not_system_manager
    

def test_remove_sub_category_from_category(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    category_id = market_facade.add_category(user_id1, 'category1')
    sub_category_id = market_facade.add_category(user_id1, 'sub_category1')
    market_facade.add_sub_category_to_category(user_id1, sub_category_id, category_id)
    assert market_facade.store_facade.get_category_by_id(sub_category_id) in market_facade.store_facade.get_category_by_id(category_id).sub_categories
    market_facade.remove_sub_category_from_category(user_id1, category_id, sub_category_id)
    assert market_facade.store_facade.get_category_by_id(sub_category_id) not in market_facade.store_facade.get_category_by_id(category_id).sub_categories

def test_assign_product_to_category(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    category_id=market_facade.add_category(user_id1, 'category1')
    product_id11 = products[0][0]
    market_facade.assign_product_to_category(user_id1, store_id1, product_id11, category_id)
    category_products_tuples =market_facade.store_facade.get_category_by_id(category_id).category_products
    product_ids = [product_id for store_id, product_id in category_products_tuples]
    assert product_id11 in product_ids
    
def test_assign_product_to_category_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    user_id2 = user_ids[1]
    store_id1 = store_ids[0]
    category_id=market_facade.add_category(user_id1, 'category1')
    product_id11 = products[0][0]
    with pytest.raises(UserError) as e:
        market_facade.assign_product_to_category(user_id2, store_id1, product_id11, category_id)
    assert e.value.user_error_type == UserErrorTypes.user_does_not_have_necessary_permissions
    category_products_tuples =market_facade.store_facade.get_category_by_id(category_id).category_products
    product_ids = [product_id for store_id, product_id in category_products_tuples]
    assert product_id11 not in product_ids
    
    

def test_remove_product_from_category(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    category_id=market_facade.add_category(user_id1, 'category1')
    product_id11 = products[0][0]
    market_facade.assign_product_to_category(user_id1, store_id1, product_id11, category_id)
    category_products_tuples =market_facade.store_facade.get_category_by_id(category_id).category_products
    product_ids = [product_id for store_id, product_id in category_products_tuples]
    assert product_id11 in product_ids
    market_facade.remove_product_from_category(user_id1, store_id1, product_id11, category_id)
    category_products_tuples =market_facade.store_facade.get_category_by_id(category_id).category_products
    product_ids = [product_id for store_id, product_id in category_products_tuples]
    assert product_id11 not in product_ids
    
def test_remove_product_from_category_no_permission(default_set_up):
    user_ids, store_ids, products, discount_ids = default_set_up
    user_id1 = user_ids[0]
    user_id2 = user_ids[1]
    store_id1 = store_ids[0]
    category_id=market_facade.add_category(user_id1, 'category1')
    product_id11 = products[0][0]
    market_facade.assign_product_to_category(user_id1, store_id1, product_id11, category_id)
    category_products_tuples =market_facade.store_facade.get_category_by_id(category_id).category_products
    product_ids = [product_id for store_id, product_id in category_products_tuples]
    assert product_id11 in product_ids
    with pytest.raises(UserError) as e:
        market_facade.remove_product_from_category(user_id2, store_id1, product_id11, category_id)
    assert e.value.user_error_type == UserErrorTypes.user_does_not_have_necessary_permissions
    category_products_tuples =market_facade.store_facade.get_category_by_id(category_id).category_products
    product_ids = [product_id for store_id, product_id in category_products_tuples]
    assert product_id11 in product_ids
    
    
    
