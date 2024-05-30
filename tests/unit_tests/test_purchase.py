import datetime
import pytest
from backend.business.purchase.purchase import ImmediateSubPurchase, PurchaseStatus, ImmediatePurchase, PurchaseFacade
from backend.business.DTOs import PurchaseProductDTO
from typing import List, Dict, Tuple

default_ongoing_purchase_id: int = 0
default_accepted_purchase_id: int = 1
default_completed_purchase_id: int = 2
default_ongoing_subpurchase_id: int = 3
default_accepted_subpurchase_id: int = 4
default_completed_subpurchase_id: int = 5
default_date: datetime = datetime.datetime.now()
default_user_id: int = 0
default_store_id: int = 0
default_products_list: List[PurchaseProductDTO] = [PurchaseProductDTO(0, "carrot", "good condition", 20, 10),
                                                   PurchaseProductDTO(1, "apple", "red apples", 30, 20),
                                                   PurchaseProductDTO(2, "banana", "very yellow wow", 40, 30)]
default_price: float = sum([dto.price for dto in default_products_list])
default_discounted_price: float = default_price * 0.95
default_shoppping_cart: Dict[int, Tuple[List[PurchaseProductDTO], float, float]] = {
    default_store_id: (default_products_list, default_price, default_discounted_price)}


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
def ongoing_subpurchase():
    return ImmediateSubPurchase(default_ongoing_subpurchase_id, default_store_id, default_user_id,
                                default_date, default_price, default_discounted_price,
                                PurchaseStatus.onGoing, default_products_list)


@pytest.fixture
def ongoing_purchase():
    return ImmediatePurchase(default_accepted_purchase_id, default_user_id, default_price,
                             default_shoppping_cart, default_discounted_price)


@pytest.fixture
def accepted_purchase(ongoing_purchase):
    ongoing_purchase.accept()
    return ongoing_purchase


@pytest.fixture
def completed_purchase(accepted_purchase):
    accepted_purchase.complete()
    return accepted_purchase


@pytest.fixture
def purchase_facade():
    pf = PurchaseFacade()
    return pf


@pytest.fixture(autouse=True)
def clean():
    clean_data()
    yield


# Now use pytest test functions instead of unittest.TestCase


# Test the ImmediateSubPurchase class:
def test_accept_subpurchase(ongoing_subpurchase):
    ongoing_subpurchase.accept()
    assert ongoing_subpurchase.status == PurchaseStatus.accepted


def test_accept_subpurchase_failed(completed_subpurchase, accepted_subpurchase):
    with pytest.raises(ValueError):
        completed_subpurchase.accept()

    with pytest.raises(ValueError):
        accepted_subpurchase.accept()


def test_complete_subpurchase(accepted_subpurchase):
    accepted_subpurchase.complete()
    assert accepted_subpurchase.status == PurchaseStatus.completed


def test_complete_subpurchase_failed(completed_subpurchase, ongoing_subpurchase):
    with pytest.raises(ValueError):
        completed_subpurchase.complete()

    with pytest.raises(ValueError):
        ongoing_subpurchase.complete()


# Test the ImmediatePurchase class:
def test_accept_purchase(ongoing_purchase):
    ongoing_purchase.accept()
    assert ongoing_purchase.status == PurchaseStatus.accepted
    for subpurchase in ongoing_purchase.immediate_sub_purchases:
        assert subpurchase.status == PurchaseStatus.accepted


def test_accept_purchase_failed(accepted_purchase, completed_purchase):
    with pytest.raises(ValueError):
        accepted_purchase.accept()

    with pytest.raises(ValueError):
        completed_purchase.accept()


def test_complete_purchase(accepted_purchase):
    accepted_purchase.complete()
    assert accepted_purchase.status == PurchaseStatus.completed
    for subpurchase in accepted_purchase.immediate_sub_purchases:
        assert subpurchase.status == PurchaseStatus.completed


def test_complete_purchase_failed(ongoing_purchase, completed_purchase):
    with pytest.raises(ValueError):
        ongoing_purchase.complete()

    with pytest.raises(ValueError):
        completed_purchase.complete()


def create_purchase_default(p_facade):
    p_facade.create_immediate_purchase(default_user_id, default_price, default_discounted_price,
                                       default_shoppping_cart)


def create_purchase_default2(p_facade):
    p_facade.create_immediate_purchase(default_user_id + 1, default_price, default_discounted_price,
                                       default_shoppping_cart)


def test_create_immediate_purchase(purchase_facade):
    create_purchase_default(purchase_facade)
    assert len(purchase_facade._purchases) == 1
    create_purchase_default(purchase_facade)
    assert len(purchase_facade._purchases) == 2


def test_create_immediate_purchase_failed_invalid_price(purchase_facade):
    with pytest.raises(ValueError):
        purchase_facade.create_immediate_purchase(default_user_id, -1, default_discounted_price,
                                                  default_shoppping_cart)

    with pytest.raises(ValueError):
        purchase_facade.create_immediate_purchase(default_user_id, default_price, -1,
                                                  default_shoppping_cart)


def test_get_new_purchase_id(purchase_facade):
    assert purchase_facade._PurchaseFacade__get_new_purchase_id() == 0
    assert purchase_facade._PurchaseFacade__get_new_purchase_id() == 1


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
    create_purchase_default(purchase_facade)
    purchase_facade.accept_purchase(0)
    assert purchase_facade._purchases[0].status == PurchaseStatus.accepted


def test_accept_purchase_facade_purchase_doesnt_exist(purchase_facade):
    with pytest.raises(ValueError):
        purchase_facade.accept_purchase(0)


def test_accept_purchase_facade_purchase_already_accepted(purchase_facade):
    create_purchase_default(purchase_facade)
    purchase_facade.accept_purchase(0)
    with pytest.raises(ValueError):
        purchase_facade.accept_purchase(0)


def test_complete_purchase_facade(purchase_facade):
    create_purchase_default(purchase_facade)
    purchase_facade.accept_purchase(0)
    purchase_facade.complete_purchase(0)
    assert purchase_facade._purchases[0].status == PurchaseStatus.completed


def test_complete_purchase_facade_purchase_doesnt_exist(purchase_facade):
    with pytest.raises(ValueError):
        purchase_facade.complete_purchase(0)


def test_complete_purchase_facade_purchase_not_accepted(purchase_facade):
    create_purchase_default(purchase_facade)
    with pytest.raises(ValueError):
        purchase_facade.complete_purchase(0)


def test_complete_purchase_facade_purchase_already_completed(purchase_facade):
    create_purchase_default(purchase_facade)
    purchase_facade.accept_purchase(0)
    purchase_facade.complete_purchase(0)
    with pytest.raises(ValueError):
        purchase_facade.complete_purchase(0)


def test_reject_purchase_facade(purchase_facade):
    create_purchase_default(purchase_facade)
    purchase_facade.reject_purchase(0)
    assert len(purchase_facade._purchases) == 0


def test_reject_purchase_facade_purchase_doesnt_exist(purchase_facade):
    with pytest.raises(ValueError):
        purchase_facade.reject_purchase(0)


def test_reject_purchase_facade_purchase_already_accepted(purchase_facade):
    create_purchase_default(purchase_facade)
    purchase_facade.accept_purchase(0)
    with pytest.raises(ValueError):
        purchase_facade.reject_purchase(0)


def test_get_purchase_by_id(purchase_facade):
    create_purchase_default(purchase_facade)
    assert purchase_facade._PurchaseFacade__get_purchase_by_id(0) == purchase_facade._purchases[0]


def test_get_purchase_by_id_doesnt_exist(purchase_facade):
    with pytest.raises(ValueError):
        purchase_facade._PurchaseFacade__get_purchase_by_id(0)


def clean_data():
    PurchaseFacade().clean_data()
