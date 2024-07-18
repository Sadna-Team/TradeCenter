from datetime import datetime, timedelta
import pytest
from backend.business.purchase.purchase import BidPurchase, ImmediateSubPurchase, PurchaseStatus, ImmediatePurchase, \
    PurchaseFacade
from backend.business.DTOs import PurchaseProductDTO
from typing import List, Dict, Tuple
from backend.error_types import *
from backend.database import db

app = None

default_ongoing_purchase_id: int = 0
default_accepted_purchase_id: int = 1
default_completed_purchase_id: int = 2
default_ongoing_subpurchase_id: int = 3
default_accepted_subpurchase_id: int = 4
default_completed_subpurchase_id: int = 5
default_bid_purchase_id: int = 6
default_date: datetime = datetime.now()
default_user_id: int = 0
default_store_id: int = 0
default_products_list: List[PurchaseProductDTO] = [PurchaseProductDTO(0, "carrot", "good condition", 20, 10),
                                                   PurchaseProductDTO(1, "apple", "red apples", 30, 20),
                                                   PurchaseProductDTO(2, "banana", "very yellow wow", 40, 30)]
default_price: float = sum([dto.price for dto in default_products_list])
default_discounted_price: float = default_price * 0.95
default_shoppping_cart: Dict[int, Tuple[List[PurchaseProductDTO], float, float]] = {
    default_store_id: (default_products_list, default_price, default_discounted_price)}


@pytest.fixture(scope='session', autouse=True)
def app():
    # Setup: Create the Flask app
    """app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_secret_key'  # Set a test secret key
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
    auth = Authentication()
    auth.clean_data()
    auth.set_jwt(jwt, bcrypt)"""
    global app

    from backend.app_factory import create_app_instance
    app = create_app_instance(mode='testing')

    # Push application context for testing
    app_context = app.app_context()
    app_context.push()

    # Make the app context available in tests
    yield app

    PurchaseFacade().clean_data()

    # app_context.pop()


@pytest.fixture(scope='function', autouse=True)
def clean():
    PurchaseFacade().clean_data()
    yield


@pytest.fixture
def accepted_subpurchase():
    return ImmediateSubPurchase(default_accepted_subpurchase_id, default_store_id, default_user_id,
                                default_date, default_price, default_discounted_price,
                                PurchaseStatus.accepted, default_products_list)


@pytest.fixture
def completed_subpurchase():
    return ImmediateSubPurchase(default_completed_subpurchase_id, default_store_id, default_user_id,
                                default_date, default_price, default_discounted_price,
                                PurchaseStatus.completed, default_products_list)


@pytest.fixture
def bid_purchase():
    return BidPurchase(default_user_id, default_price, default_store_id, default_products_list[0].product_id)


@pytest.fixture
def ongoing_subpurchase():
    return ImmediateSubPurchase(default_ongoing_subpurchase_id, default_store_id, default_user_id,
                                default_date, default_price, default_discounted_price,
                                PurchaseStatus.onGoing, default_products_list)


@pytest.fixture
def ongoing_purchase():
    from backend.business.purchase.purchase import create_immediate_purchase
    return create_immediate_purchase(default_user_id, default_price, default_shoppping_cart, default_discounted_price)
    # return ImmediatePurchase(default_accepted_purchase_id, default_user_id, default_price,
    #                          default_shoppping_cart, default_discounted_price)


@pytest.fixture
def accepted_purchase(ongoing_purchase):
    ongoing_purchase.accept()
    return ongoing_purchase


@pytest.fixture
def completed_purchase(accepted_purchase):
    accepted_purchase.complete()
    return accepted_purchase


@pytest.fixture
def accepted_bid_purchase(bid_purchase):
    bid_purchase.approve()
    bid_purchase.accept()
    return bid_purchase


@pytest.fixture
def completed_bid_purchase(accepted_bid_purchase):
    accepted_bid_purchase.complete()
    return accepted_bid_purchase


@pytest.fixture
def purchase_facade():
    pf = PurchaseFacade()
    return pf


# Now use pytest test functions instead of unittest.TestCase


# Test the ImmediateSubPurchase class:
def test_accept_subpurchase(ongoing_subpurchase):
    ongoing_subpurchase.accept()
    assert ongoing_subpurchase.status == PurchaseStatus.accepted


def test_accept_subpurchase_failed(completed_subpurchase, accepted_subpurchase):
    with pytest.raises(PurchaseError) as e:
        completed_subpurchase.accept()
    assert e.value.purchase_error_type == PurchaseErrorTypes.purchase_not_ongoing

    with pytest.raises(PurchaseError) as e:
        accepted_subpurchase.accept()
    assert e.value.purchase_error_type == PurchaseErrorTypes.purchase_not_ongoing


def test_complete_subpurchase(accepted_subpurchase):
    accepted_subpurchase.complete()
    assert accepted_subpurchase.status == PurchaseStatus.completed


def test_complete_subpurchase_failed(completed_subpurchase, ongoing_subpurchase):
    with pytest.raises(PurchaseError) as e:
        completed_subpurchase.complete()
    assert e.value.purchase_error_type == PurchaseErrorTypes.purchase_not_accepted

    with pytest.raises(PurchaseError) as e:
        ongoing_subpurchase.complete()
    assert e.value.purchase_error_type == PurchaseErrorTypes.purchase_not_accepted


# Test the ImmediatePurchase class:
def test_accept_purchase(ongoing_purchase):
    ongoing_purchase.accept()
    assert ongoing_purchase.status == PurchaseStatus.accepted
    for subpurchase in ongoing_purchase.immediate_sub_purchases:
        assert subpurchase.status == PurchaseStatus.accepted


def test_accept_purchase_failed(accepted_purchase, completed_purchase):
    with pytest.raises(PurchaseError) as e:
        accepted_purchase.accept()
    assert e.value.purchase_error_type == PurchaseErrorTypes.purchase_not_ongoing

    with pytest.raises(PurchaseError) as e:
        completed_purchase.accept()
    assert e.value.purchase_error_type == PurchaseErrorTypes.purchase_not_ongoing


def test_complete_purchase(accepted_purchase):
    accepted_purchase.complete()
    assert accepted_purchase.status == PurchaseStatus.completed
    for subpurchase in accepted_purchase.immediate_sub_purchases:
        assert subpurchase.status == PurchaseStatus.completed


def test_complete_purchase_failed(ongoing_purchase, completed_purchase):
    with pytest.raises(PurchaseError) as e:
        ongoing_purchase.complete()
    assert e.value.purchase_error_type == PurchaseErrorTypes.purchase_not_accepted

    with pytest.raises(PurchaseError) as e:
        completed_purchase.complete()
    assert e.value.purchase_error_type == PurchaseErrorTypes.purchase_not_accepted


def create_purchase_default(p_facade):
    return p_facade.create_immediate_purchase(default_user_id, default_price, default_discounted_price,
                                              default_shoppping_cart)


def create_purchase_default2(p_facade):
    p_facade.create_immediate_purchase(default_user_id + 1, default_price, default_discounted_price,
                                       default_shoppping_cart)


def create_bid_purchase_default(p_facade):
    return p_facade.create_bid_purchase(default_user_id, default_price, default_store_id,
                                        default_products_list[0].product_id)


def test_create_immediate_purchase(purchase_facade):
    purchase_facade.clean_data()
    num = len(db.session.query(ImmediatePurchase).all())
    create_purchase_default(purchase_facade)
    # purchase_facade._purchases: no attribute '_purchases', test by checking how many purchases in the session
    assert len(db.session.query(ImmediatePurchase).all()) == num + 1
    #assert len(purchase_facade._purchases) == 1
    create_purchase_default(purchase_facade)
    assert len(db.session.query(ImmediatePurchase).all()) == num + 2
    #assert len(purchase_facade._purchases) == 2


def test_create_immediate_purchase_failed_invalid_price(purchase_facade):
    with pytest.raises(PurchaseError) as e:
        purchase_facade.create_immediate_purchase(default_user_id, -1, default_discounted_price,
                                                  default_shoppping_cart)
    assert e.value.purchase_error_type == PurchaseErrorTypes.invalid_total_price

    with pytest.raises(PurchaseError) as e:
        purchase_facade.create_immediate_purchase(default_user_id, default_price, -1,
                                                  default_shoppping_cart)
    assert e.value.purchase_error_type == PurchaseErrorTypes.invalid_total_price


# deprecated
"""def test_get_new_purchase_id(purchase_facade):
    assert purchase_facade._PurchaseFacade__get_new_purchase_id() == 0
    assert purchase_facade._PurchaseFacade__get_new_purchase_id() == 1"""


def test_get_purchases_of_user(purchase_facade):
    create_purchase_default(purchase_facade)
    create_purchase_default(purchase_facade)
    assert len(purchase_facade.get_purchases_of_user(default_user_id)) == 2
    create_purchase_default2(purchase_facade)
    assert len(purchase_facade.get_purchases_of_user(default_user_id)) == 2


def test_get_purchases_of_user_empty(purchase_facade):
    assert len(purchase_facade.get_purchases_of_user(default_user_id)) == 0
    create_purchase_default2(purchase_facade)
    assert len(purchase_facade.get_purchases_of_user(default_user_id)) == 0


def test_get_purchases_of_store(purchase_facade):
    create_purchase_default(purchase_facade)
    create_purchase_default2(purchase_facade)
    assert len(purchase_facade.get_purchases_of_store(default_store_id)) == 2
    create_purchase_default2(purchase_facade)
    assert len(purchase_facade.get_purchases_of_store(default_store_id)) == 3


def test_get_purchases_of_store_empty(purchase_facade):
    assert len(purchase_facade.get_purchases_of_store(default_store_id)) == 0
    create_purchase_default(purchase_facade)
    assert len(purchase_facade.get_purchases_of_store(default_store_id + 1)) == 0


def test_accept_purchase_facade(purchase_facade):
    p_id = create_purchase_default(purchase_facade)
    purchase_facade.accept_purchase(p_id, datetime.now() + timedelta(days=1))
    assert db.session.query(ImmediatePurchase).get(p_id).status == PurchaseStatus.accepted
    # assert purchase_facade._purchases[0].status == PurchaseStatus.accepted


def test_accept_purchase_facade_purchase_doesnt_exist(purchase_facade):
    with pytest.raises(PurchaseError) as e:
        purchase_facade.accept_purchase(0, datetime.now() + timedelta(days=1))
    assert e.value.purchase_error_type == PurchaseErrorTypes.invalid_purchase_id


def test_accept_purchase_facade_purchase_already_accepted(purchase_facade):
    p_id = create_purchase_default(purchase_facade)
    purchase_facade.accept_purchase(p_id, datetime.now() + timedelta(days=1))
    with pytest.raises(PurchaseError) as e:
        purchase_facade.accept_purchase(p_id, datetime.now() + timedelta(days=1))
    assert e.value.purchase_error_type == PurchaseErrorTypes.purchase_not_ongoing


def test_complete_purchase_facade(purchase_facade):
    p_id = create_purchase_default(purchase_facade)
    purchase_facade.accept_purchase(p_id, datetime.now() + timedelta(days=1))
    purchase_facade.complete_purchase(p_id)
    assert db.session.query(ImmediatePurchase).get(p_id).status == PurchaseStatus.completed
    # assert purchase_facade._purchases[0].status == PurchaseStatus.completed


def test_complete_purchase_facade_purchase_doesnt_exist(purchase_facade):
    with pytest.raises(PurchaseError) as e:
        purchase_facade.complete_purchase(0)
    assert e.value.purchase_error_type == PurchaseErrorTypes.invalid_purchase_id


def test_complete_purchase_facade_purchase_not_accepted(purchase_facade):
    p_id = create_purchase_default(purchase_facade)
    with pytest.raises(PurchaseError) as e:
        purchase_facade.complete_purchase(p_id)
    assert e.value.purchase_error_type == PurchaseErrorTypes.purchase_not_accepted


def test_complete_purchase_facade_purchase_already_completed(purchase_facade):
    p_id = create_purchase_default(purchase_facade)
    purchase_facade.accept_purchase(p_id, datetime.now() + timedelta(days=1))
    purchase_facade.complete_purchase(p_id)
    with pytest.raises(PurchaseError) as e:
        purchase_facade.complete_purchase(p_id)
    assert e.value.purchase_error_type == PurchaseErrorTypes.purchase_not_accepted


def test_reject_purchase_facade(purchase_facade):
    p_id = create_purchase_default(purchase_facade)
    purchase_facade.reject_purchase(p_id)
    assert db.session.query(ImmediatePurchase).get(p_id) is None
    #assert len(purchase_facade._purchases) == 0


def test_reject_purchase_facade_purchase_doesnt_exist(purchase_facade):
    with pytest.raises(PurchaseError) as e:
        purchase_facade.reject_purchase(50000000)
    assert e.value.purchase_error_type == PurchaseErrorTypes.invalid_purchase_id


def test_reject_purchase_facade_purchase_already_accepted(purchase_facade):
    p_id = create_purchase_default(purchase_facade)
    purchase_facade.accept_purchase(p_id, datetime.now() + timedelta(days=1))
    with pytest.raises(PurchaseError) as e:
        purchase_facade.reject_purchase(p_id)
    assert e.value.purchase_error_type == PurchaseErrorTypes.purchase_already_accepted_or_completed


def test_get_purchase_by_id(purchase_facade):
    p_id = create_purchase_default(purchase_facade)
    assert purchase_facade._PurchaseFacade__get_purchase_by_id(p_id) is not None


def test_get_purchase_by_id_doesnt_exist(purchase_facade):
    with pytest.raises(PurchaseError) as e:
        purchase_facade._PurchaseFacade__get_purchase_by_id(0)
    assert e.value.purchase_error_type == PurchaseErrorTypes.invalid_purchase_id


#bid tests: 

def test_store_owner_manager_accept_offer(bid_purchase):
    bid_purchase.store_owner_manager_accept_offer(default_user_id)
    assert default_user_id in bid_purchase.list_of_store_owners_managers_that_accepted_offer


def test_store_owner_manager_accept_offer_failed(bid_purchase):
    bid_purchase.store_owner_manager_accept_offer(default_user_id)
    with pytest.raises(PurchaseError) as e:
        bid_purchase.store_owner_manager_accept_offer(default_user_id)
    assert e.value.purchase_error_type == PurchaseErrorTypes.store_owner_manager_already_accepted_offer


def test_store_reject_offer(bid_purchase):
    user_id = bid_purchase.store_reject_offer(default_user_id)
    assert bid_purchase.status == PurchaseStatus.offer_rejected
    assert user_id == default_user_id


def test_store_accept_offer(bid_purchase):
    bid_purchase.store_owner_manager_accept_offer(default_user_id)
    assert bid_purchase.store_accept_offer([default_user_id]) == True
    assert bid_purchase.status == PurchaseStatus.approved


def test_store_counter_offer(bid_purchase):
    bid_purchase.store_counter_offer(default_user_id, default_price + 10)
    assert bid_purchase.proposed_price == default_price + 10
    assert bid_purchase.is_offer_to_store == False


def test_store_counter_offer_failed(bid_purchase):
    with pytest.raises(PurchaseError) as e:
        bid_purchase.store_counter_offer(default_user_id, - 10)
    assert e.value.purchase_error_type == PurchaseErrorTypes.invalid_proposed_price


def test_user_accept_counter_offer(bid_purchase):
    bid_purchase.store_counter_offer(default_user_id, default_price + 10)
    bid_purchase.user_accept_counter_offer(default_user_id)
    assert bid_purchase.is_offer_to_store == True


def test_user_accept_counter_offer_failed(bid_purchase):
    bid_purchase.store_counter_offer(default_user_id, default_price + 10)
    with pytest.raises(PurchaseError) as e:
        bid_purchase.user_accept_counter_offer(default_user_id + 1)
    assert e.value.purchase_error_type == PurchaseErrorTypes.invalid_user_id


def test_user_reject_counter_offer(bid_purchase):
    bid_purchase.store_counter_offer(default_user_id, default_price + 10)
    bid_purchase.user_reject_counter_offer(default_user_id)
    assert bid_purchase.status == PurchaseStatus.offer_rejected


def test_user_reject_counter_offer_failed(bid_purchase):
    bid_purchase.store_counter_offer(default_user_id, default_price + 10)
    with pytest.raises(PurchaseError) as e:
        bid_purchase.user_reject_counter_offer(default_user_id + 1)
    assert e.value.purchase_error_type == PurchaseErrorTypes.invalid_user_id


def test_user_counter_offer(bid_purchase):
    bid_purchase.store_counter_offer(default_user_id, default_price + 10)
    bid_purchase.user_counter_offer(default_user_id, default_price + 15)
    assert bid_purchase.proposed_price == default_price + 15
    assert bid_purchase.is_offer_to_store == True
    assert bid_purchase.list_of_store_owners_managers_that_accepted_offer == []


def test_accept_bid_purchase(bid_purchase):
    bid_purchase.approve()
    bid_purchase.accept()
    assert bid_purchase.status == PurchaseStatus.accepted
    assert bid_purchase.total_price == default_price
    assert bid_purchase.total_price_after_discounts == default_price
    assert bid_purchase.date_of_purchase is not None


def test_complete_bid_purchase(accepted_bid_purchase):
    accepted_bid_purchase.complete()
    assert accepted_bid_purchase.status == PurchaseStatus.completed


#PurchaseFacade tests:

def test_create_bid_purchase(purchase_facade):
    num = len(db.session.query(BidPurchase).all())
    create_bid_purchase_default(purchase_facade)
    assert len(db.session.query(BidPurchase).all()) == num + 1


def test_store_owner_manager_accept_offer_facade(purchase_facade):
    p_id = create_bid_purchase_default(purchase_facade)
    purchase_facade.store_owner_manager_accept_offer(p_id, default_user_id)
    assert default_user_id in db.session.query(BidPurchase).get(p_id).list_of_store_owners_managers_that_accepted_offer


def test_store_reject_offer_facade(purchase_facade):
    p_id = create_bid_purchase_default(purchase_facade)
    user_id = purchase_facade.store_reject_offer(p_id, default_user_id)
    assert db.session.query(BidPurchase).get(p_id).status == PurchaseStatus.offer_rejected
    assert user_id == default_user_id


def test_store_accept_offer_facade(purchase_facade):
    p_id = create_bid_purchase_default(purchase_facade)
    purchase_facade.store_owner_manager_accept_offer(p_id, default_user_id)
    assert purchase_facade.store_accept_offer(p_id, [default_user_id])
    assert db.session.query(BidPurchase).get(p_id).status == PurchaseStatus.approved


def test_store_counter_offer_facade(purchase_facade):
    p_id = create_bid_purchase_default(purchase_facade)
    purchase_facade.store_counter_offer(p_id, default_user_id, default_price + 10)
    assert db.session.query(BidPurchase).get(p_id).proposed_price == default_price + 10


def test_user_accept_counter_offer_facade(purchase_facade):
    p_id = create_bid_purchase_default(purchase_facade)
    purchase_facade.store_counter_offer(p_id, default_user_id, default_price + 10)
    purchase_facade.user_accept_counter_offer(p_id, default_user_id)
    assert db.session.query(BidPurchase).get(p_id).is_offer_to_store == True


def test_user_reject_counter_offer_facade(purchase_facade):
    p_id = create_bid_purchase_default(purchase_facade)
    purchase_facade.store_counter_offer(p_id, default_user_id, default_price + 10)
    purchase_facade.user_reject_counter_offer(p_id, default_user_id)
    assert db.session.query(BidPurchase).get(p_id).status == PurchaseStatus.offer_rejected


def test_user_counter_offer_facade(purchase_facade):
    p_id = create_bid_purchase_default(purchase_facade)
    purchase_facade.store_counter_offer(p_id, default_user_id, default_price + 10)
    purchase_facade.user_counter_offer(p_id, default_user_id, default_price + 15)
    assert db.session.query(BidPurchase).get(p_id).proposed_price == default_price + 15
    assert db.session.query(BidPurchase).get(p_id).is_offer_to_store
    assert db.session.query(BidPurchase).get(p_id).list_of_store_owners_managers_that_accepted_offer == []


def test_get_bid_purchases_of_user(purchase_facade):
    create_bid_purchase_default(purchase_facade)
    bid_purchases = purchase_facade.get_bid_purchases_of_user(default_user_id)
    assert len(bid_purchases) == 1


def test_get_bid_purchases_of_store(purchase_facade):
    create_bid_purchase_default(purchase_facade)
    bid_purchases = purchase_facade.get_bid_purchases_of_store(default_store_id)
    assert len(bid_purchases) == 1


def test_view_all_bids_of_system(purchase_facade):
    create_bid_purchase_default(purchase_facade)
    bids = purchase_facade.view_all_bids_of_system()
    assert len(bids) > 0

def clean_data():
    PurchaseFacade().clean_data()
