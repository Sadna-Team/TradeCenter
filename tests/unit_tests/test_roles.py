import unittest
from unittest.mock import MagicMock
from backend.business.roles.roles import RolesFacade, StoreOwner, StoreManager, Nomination, Permissions
from backend.error_types import *


import unittest
from unittest.mock import MagicMock
from backend.business.roles.roles import RolesFacade
from backend import create_app

class TestRolesFacade(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        from backend import app as app2
        app2.app = self.app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.facade = RolesFacade()
        self.facade.clean_data()

    def tearDown(self):
        self.app_context.pop()
    def test_add_store(self):
        self.facade.add_store(1, 2)
        self.assertIn(1, self.facade._RolesFacade__stores_to_roles)
        self.assertIn(2, self.facade._RolesFacade__stores_to_roles[1])
        self.assertIsInstance(self.facade._RolesFacade__stores_to_roles[1][2], StoreOwner)

    def test_add_store_existing(self):
        self.facade.add_store(1, 1)
        with self.assertRaises(RoleError) as e:
            self.facade.add_store(1, 2)
        assert e.exception.role_error_type == RoleErrorTypes.store_already_exists

    def test_close_store(self):
        self.facade.add_store(1, 2)
        self.facade.remove_store(1, 2)
        self.assertNotIn(1, self.facade._RolesFacade__stores_to_roles)
        self.assertNotIn(1, self.facade._RolesFacade__stores_to_role_tree)

    def test_close_store_nonexistent(self):
        with self.assertRaises(StoreError) as e:
            self.facade.remove_store(1, 1)
        assert e.exception.store_error_type == StoreErrorTypes.store_not_found
        
    def test_nominate_owner(self):
        self.facade.add_store(1, 2)
        nomination_id = self.facade.nominate_owner(1, 2, 3)
        self.assertIn(nomination_id, self.facade._RolesFacade__systems_nominations)
        self.assertIsInstance(self.facade._RolesFacade__systems_nominations[nomination_id].role, StoreOwner)

    def test_nominate_manager(self):
        self.facade.add_store(1, 2)
        nomination_id = self.facade.nominate_manager(1, 2, 3)
        self.assertIn(nomination_id, self.facade._RolesFacade__systems_nominations)
        self.assertIsInstance(self.facade._RolesFacade__systems_nominations[nomination_id].role, StoreManager)

    def test_accept_nomination(self):
        self.facade.add_store(1, 2)
        nomination_id = self.facade.nominate_manager(1, 2, 3)
        self.facade.accept_nomination(nomination_id, 3)
        self.assertIn(3, self.facade._RolesFacade__stores_to_roles[1])
        self.assertIsInstance(self.facade._RolesFacade__stores_to_roles[1][3], StoreManager)

    def test_decline_nomination(self):
        self.facade.add_store(1, 2)
        nomination_id = self.facade.nominate_manager(1, 2, 3)
        self.facade.decline_nomination(nomination_id, 3)
        self.assertNotIn(nomination_id, self.facade._RolesFacade__systems_nominations)

    def test_set_manager_permissions(self):
        self.facade.add_store(1, 2)
        nomination_id = self.facade.nominate_manager(1, 2, 3)
        self.facade.accept_nomination(nomination_id, 3)  # Assuming the first nomination id is 0
        self.facade.set_manager_permissions(1, 2, 3, True, True, True, True, True, True, True)
        self.assertTrue(self.facade._RolesFacade__stores_to_roles[1][3].permissions.add_product)

    def test_remove_role(self):
        self.facade.add_store(1, 2)
        self.facade.nominate_manager(1, 2,3)
        self.facade.accept_nomination(0, 3)  # Assuming the first nomination id is 0
        self.facade.remove_role(1, 2, 3)
        self.assertNotIn(3, self.facade._RolesFacade__stores_to_roles[1])

    def test_remove_role_nonexistent_store(self):
        with self.assertRaises(StoreError) as e:
            self.facade.remove_role(1, 1, 2)
        assert e.exception.store_error_type == StoreErrorTypes.store_not_found
        
    def test_is_system_manager(self):
        self.facade.add_system_manager(0, 1)
        self.assertTrue(self.facade.is_system_manager(1))

    def test_add_system_manager(self):
        self.facade.add_system_manager(0, 1)
        self.assertIn(1, self.facade._RolesFacade__system_managers)

    def test_remove_system_manager(self):
        self.facade.add_system_manager(0, 1)
        self.facade.remove_system_manager(0, 1)
        self.assertNotIn(1, self.facade._RolesFacade__system_managers)

    def test_add_admin(self):
        self.facade.add_admin(1)
        self.assertTrue(self.facade.is_system_manager(1))

if __name__ == '__main__':
    unittest.main()
