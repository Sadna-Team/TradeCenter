import unittest
from unittest.mock import MagicMock
from backend.business.notifier import Notifier

class TestNotifier(unittest.TestCase):
    def setUp(self):
        self.notifier = Notifier()

    def test_notify_new_purchase(self):
        self.notifier._user_facade.notify_user = MagicMock()
        self.notifier._listeners = {1: [1, 2]}
        self.notifier.notify_new_purchase(1, 1)
        self.assertEqual(self.notifier._user_facade.notify_user.call_count, 2)

    def test_notify_new_purchase_no_listeners(self):
        self.notifier._listeners = {}
        with self.assertRaises(ValueError):
            self.notifier.notify_new_purchase(1, 1)

    def test_notify_update_store_status(self):
        self.notifier._user_facade.notify_user = MagicMock()
        self.notifier._listeners = {1: [1, 2]}
        self.notifier.notify_update_store_status(1, "details", True)
        self.assertEqual(self.notifier._user_facade.notify_user.call_count, 2)

    def test_notify_update_store_status_open(self):
        self.notifier._user_facade.notify_user = MagicMock()
        self.notifier._listeners = {1: [1, 2]}
        self.notifier.notify_update_store_status(1, "details", False)
        self.assertEqual(self.notifier._user_facade.notify_user.call_count, 2)

    def test_notify_update_store_status_no_listeners(self):
        self.notifier._listeners = {}
        with self.assertRaises(ValueError):
            self.notifier.notify_update_store_status(1, "details", True)