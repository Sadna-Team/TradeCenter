# test_roles.py
import pytest
from backend.business.roles.roles import RolesFacade, StoreOwner, StoreManager
from backend.error_types import *


@pytest.fixture(scope='module')
def app():
    from backend import create_app
    app = create_app('testing')
    from backend import app as app2
    app2.app = app
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def roles_facade(app):
    facade = RolesFacade()
    facade.clean_data()
    yield facade


def test_add_store(roles_facade):
    roles_facade.add_store(1, 2)
    assert 1 in roles_facade._RolesFacade__stores_to_roles
    assert 2 in roles_facade._RolesFacade__stores_to_roles[1]
    assert isinstance(roles_facade._RolesFacade__stores_to_roles[1][2], StoreOwner)


def test_add_store_existing(roles_facade):
    roles_facade.add_store(1, 1)
    with pytest.raises(RoleError) as e:
        roles_facade.add_store(1, 2)
    assert e.value.role_error_type == RoleErrorTypes.store_already_exists


def test_close_store(roles_facade):
    roles_facade.add_store(1, 2)
    roles_facade.remove_store(1, 2)
    assert 1 not in roles_facade._RolesFacade__stores_to_roles
    assert 1 not in roles_facade._RolesFacade__stores_to_role_tree


def test_close_store_nonexistent(roles_facade):
    with pytest.raises(StoreError) as e:
        roles_facade.remove_store(1, 1)
    assert e.value.store_error_type == StoreErrorTypes.store_not_found


def test_nominate_owner(roles_facade):
    roles_facade.add_store(1, 2)
    nomination_id = roles_facade.nominate_owner(1, 2, 3)
    assert nomination_id in roles_facade._RolesFacade__systems_nominations
    assert isinstance(roles_facade._RolesFacade__systems_nominations[nomination_id].role, StoreOwner)


def test_nominate_manager(roles_facade):
    roles_facade.add_store(1, 2)
    nomination_id = roles_facade.nominate_manager(1, 2, 3)
    assert nomination_id in roles_facade._RolesFacade__systems_nominations
    assert isinstance(roles_facade._RolesFacade__systems_nominations[nomination_id].role, StoreManager)


def test_accept_nomination(roles_facade):
    roles_facade.add_store(1, 2)
    nomination_id = roles_facade.nominate_manager(1, 2, 3)
    roles_facade.accept_nomination(nomination_id, 3)
    assert 3 in roles_facade._RolesFacade__stores_to_roles[1]
    assert isinstance(roles_facade._RolesFacade__stores_to_roles[1][3], StoreManager)


def test_decline_nomination(roles_facade):
    roles_facade.add_store(1, 2)
    nomination_id = roles_facade.nominate_manager(1, 2, 3)
    roles_facade.decline_nomination(nomination_id, 3)
    assert nomination_id not in roles_facade._RolesFacade__systems_nominations


def test_set_manager_permissions(roles_facade):
    roles_facade.add_store(1, 2)
    nomination_id = roles_facade.nominate_manager(1, 2, 3)
    roles_facade.accept_nomination(nomination_id, 3)  # Assuming the first nomination id is 0
    roles_facade.set_manager_permissions(1, 2, 3, True, True, True, True, True, True, True)
    assert roles_facade._RolesFacade__stores_to_roles[1][3].permissions.add_product is True


def test_remove_role(roles_facade):
    roles_facade.add_store(1, 2)
    roles_facade.nominate_manager(1, 2, 3)
    roles_facade.accept_nomination(0, 3)  # Assuming the first nomination id is 0
    roles_facade.remove_role(1, 2, 3)
    assert 3 not in roles_facade._RolesFacade__stores_to_roles[1]


def test_remove_role_nonexistent_store(roles_facade):
    with pytest.raises(StoreError) as e:
        roles_facade.remove_role(1, 1, 2)
    assert e.value.store_error_type == StoreErrorTypes.store_not_found


def test_is_system_manager(roles_facade):
    roles_facade.add_system_manager(0, 1)
    assert roles_facade.is_system_manager(1) is True


def test_add_system_manager(roles_facade):
    roles_facade.add_system_manager(0, 1)
    assert 1 in roles_facade._RolesFacade__system_managers


def test_remove_system_manager(roles_facade):
    roles_facade.add_system_manager(0, 1)
    roles_facade.remove_system_manager(0, 1)
    assert 1 not in roles_facade._RolesFacade__system_managers


def test_add_admin(roles_facade):
    roles_facade.add_admin(1)
    assert roles_facade.is_system_manager(1) is True
