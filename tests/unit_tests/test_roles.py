import pytest
from backend.business.roles.roles import RolesFacade, StoreOwner, StoreManager, Nomination, Permissions
from backend.error_types import *
from backend.business.market import MarketFacade
from unittest.mock import patch, MagicMock


@pytest.fixture()
def roles_facade():


    from backend import create_app
    app = create_app('testing')
    from backend import app as app2
    app2.app = app
    with app.app_context():
        MarketFacade().clean_data()
        facade = RolesFacade()

        yield facade

def test_add_store(roles_facade):
    roles_facade.add_store(1, 2)
    store_role = roles_facade.get_role(1, 2)
    assert isinstance(store_role, StoreOwner)

def test_add_store_existing(roles_facade):
    roles_facade.add_store(1, 1)
    with pytest.raises(RoleError) as e:
        roles_facade.add_store(1, 2)
    assert e.value.role_error_type == RoleErrorTypes.store_already_exists

def test_remove_store(roles_facade):
    roles_facade.add_store(1, 2)
    roles_facade.remove_store(1, 2)
    assert roles_facade.get_role(1, 2) is None

def test_remove_store_nonexistent(roles_facade):
    with pytest.raises(StoreError) as e:
        roles_facade.remove_store(1, 1)
    assert e.value.store_error_type == StoreErrorTypes.store_not_found

def test_nominate_owner(roles_facade):
    roles_facade.add_store(1, 2)
    nomination_id = roles_facade.nominate_owner(1, 2, 3)
    nomination = roles_facade.get_nomination(nomination_id)
    assert nomination.role_type == 'store_owner'
def test_nominate_manager(roles_facade):
    roles_facade.add_store(1, 2)
    nomination_id = roles_facade.nominate_manager(1, 2, 3)
    nomination = roles_facade.get_nomination(nomination_id)
    assert nomination.role_type == 'store_manager'

def test_accept_nomination(roles_facade):
    roles_facade.add_store(1, 2)
    nomination_id = roles_facade.nominate_manager(1, 2, 3)
    roles_facade.accept_nomination(nomination_id, 3)
    store_role = roles_facade.get_role(1, 3)
    assert isinstance(store_role, StoreManager)

def test_decline_nomination(roles_facade):
    roles_facade.add_store(1, 2)
    nomination_id = roles_facade.nominate_manager(1, 2, 3)
    roles_facade.decline_nomination(nomination_id, 3)
    assert roles_facade.get_nomination(nomination_id) is None

def test_set_manager_permissions(roles_facade):
    roles_facade.add_store(1, 2)
    nomination_id = roles_facade.nominate_manager(1, 2, 3)
    roles_facade.accept_nomination(nomination_id, 3)
    roles_facade.set_manager_permissions(1, 2, 3, True, True, True, True, True, True, True)
    permissions = roles_facade.get_permissions(1, 3)
    assert permissions.add_product is True

def test_remove_role(roles_facade):
    with patch.object(roles_facade, '_RolesFacade__notifier', new=MagicMock()) as mock_notifier:
        # Mock the notifier methods
        mock_notifier.notify_removed_management_position.return_value = None
        mock_notifier.unsign_listener.return_value = None

        roles_facade.add_store(1, 2)
        nomination_id = roles_facade.nominate_manager(1, 2, 3)
        roles_facade.accept_nomination(nomination_id, 3)
        roles_facade.remove_role(1, 2, 3)
        assert roles_facade.get_role(1, 3) is None

        # Check that the notifier methods were called
        mock_notifier.notify_removed_management_position.assert_called()
        mock_notifier.unsign_listener.assert_called()

def test_remove_role_nonexistent_store(roles_facade):
    with pytest.raises(StoreError) as e:
        roles_facade.remove_role(1, 1, 2)
    assert e.value.store_error_type == StoreErrorTypes.store_not_found

def test_is_system_manager(roles_facade):
    roles_facade.add_system_manager(0, 1)
    assert roles_facade.is_system_manager(1) is True

def test_add_system_manager(roles_facade):
    roles_facade.add_system_manager(0, 1)
    assert roles_facade.is_system_manager(1) is True

def test_remove_system_manager(roles_facade):
    roles_facade.add_system_manager(0, 1)
    roles_facade.remove_system_manager(0, 1)
    assert roles_facade.is_system_manager(1) is False

# def test_add_admin(roles_facade):
#     roles_facade.add_admin(1)
#     assert roles_facade.is_system_manager(1) is True
