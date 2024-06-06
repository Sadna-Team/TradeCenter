import pytest
from backend.business import MarketFacade, UserFacade, Authentication, PurchaseFacade
from typing import List, Optional
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from time import sleep

market_facade: Optional[MarketFacade] = None
user_facade: Optional[UserFacade] = None
purchase_facade: Optional[PurchaseFacade] = None


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

default_address_checkout = {'street': 'street', 'city': 'city', 'country': 'country', 'zip': 'zip'}


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

    market_facade = MarketFacade()
    user_facade = UserFacade()
    purchase_facade = PurchaseFacade()

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

    user_facade.register_user(user_id1, default_usernames[0], default_passwords[0], default_emails[0], default_years[0],
                              default_months[0], default_days[0], default_phones[0])
    user_facade.register_user(user_id2, default_usernames[1], default_passwords[1], default_emails[1], default_years[1],
                              default_months[1], default_days[1], default_phones[1])
    user_facade.register_user(user_id3, default_usernames[2], default_passwords[2], default_emails[2], default_years[2],
                              default_months[2], default_days[2], default_phones[2])
    user_facade.register_user(user_id4, default_usernames[3], default_passwords[3], default_emails[3], default_years[3],
                              default_months[3], default_days[3], default_phones[3])
    user_facade.register_user(user_id5, default_usernames[4], default_passwords[4], default_emails[4], default_years[4],
                              default_months[4], default_days[4], default_phones[4])

    store_id1 = market_facade.add_store(user_id1, 0, default_store_names[0])
    store_id2 = market_facade.add_store(user_id2, 0, default_store_names[1])
    store_id3 = market_facade.add_store(user_id3, 0, default_store_names[2])
    store_id4 = market_facade.add_store(user_id4, 0, default_store_names[3])
    store_id5 = market_facade.add_store(user_id5, 0, default_store_names[4])

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

    return user_ids, store_ids, products


@pytest.fixture
def default_user_cart(default_set_up):
    user_ids, store_ids, products = default_set_up
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
    sleep(7)


def test_checkout_failed_shopping_cart_empty(default_set_up):
    user_ids, store_ids, products = default_set_up
    user_id1 = user_ids[0]
    with pytest.raises(ValueError):
        market_facade.checkout(user_id1, default_payment_method, default_supply_method, default_address_checkout)


def test_checkout_failed_payment_method(default_user_cart):
    user_ids, store_ids, products = default_user_cart
    user_id1 = user_ids[0]
    store_id1 = store_ids[0]
    quantity_before = market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products[
        products[0][0]].amount
    with pytest.raises(ValueError):
        market_facade.checkout(user_id1, {}, default_supply_method, default_address_checkout)

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
    market_facade.add_product_to_basket(user_id1, store_id5, products[4][0], 1)
    market_facade.store_facade._StoreFacade__get_store_by_id(store_id1)._Store__store_products = {}
    with pytest.raises(ValueError):
        market_facade.checkout(user_id1, default_payment_method, default_supply_method, default_address_checkout)

    assert (market_facade.user_facade._UserFacade__get_user(user_id1)._User__shopping_cart
            ._ShoppingCart__shopping_baskets)
    assert len(purchase_facade.get_purchases_of_store(user_id1)) == 0
