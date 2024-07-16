import unittest
from unittest.mock import MagicMock
from backend.business.notifier import Notifier
from backend.error_types import *
from backend import create_app


class TestNotifier(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app("testing")
        from backend import app as app2
        app2.app = self.app
        self.notifier = Notifier()

    def tearDown(self) -> None:
        self.notifier.clean_data()

    def test_notify_new_purchase(self):
        self.notifier._user_facade.notify_user = MagicMock()
        self.notifier._listeners = {1: [1, 2]}
        self.notifier.notify_new_purchase(1, 1)
        self.assertEqual(self.notifier._user_facade.notify_user.call_count, 2)

    def test_notify_new_purchase_no_listeners(self):
        self.notifier._listeners = {}
        with self.assertRaises(StoreError) as e:
            self.notifier.notify_new_purchase(1, 1)
        assert e.exception.store_error_type == StoreErrorTypes.no_listeners_for_store

    def test_notify_update_store_status(self):
        self.notifier._user_facade.notify_user = MagicMock()
        self.notifier._listeners = {1: [1, 2]}
        self.notifier.notify_update_store_status(1, True, "details")
        self.assertEqual(self.notifier._user_facade.notify_user.call_count, 2)

    def test_notify_update_store_status_open(self):
        self.notifier._user_facade.notify_user = MagicMock()
        self.notifier._listeners = {1: [1, 2]}
        self.notifier.notify_update_store_status(1, False, "details")
        self.assertEqual(self.notifier._user_facade.notify_user.call_count, 2)

    def test_notify_update_store_status_no_listeners(self):
        self.notifier._listeners = {}
        with self.assertRaises(StoreError) as e:
            self.notifier.notify_update_store_status(1, True, "details")
        assert e.exception.store_error_type == StoreErrorTypes.no_listeners_for_store

    def test_notify_removed_management_position(self):
        self.notifier._user_facade.notify_user = MagicMock()
        self.notifier._listeners = {1: [1, 2]}
        self.notifier.notify_removed_management_position(1, 1)
        self.assertEqual(self.notifier._user_facade.notify_user.call_count, 1)

    def test_notify_removed_management_position_no_listeners(self):
        self.notifier._listeners = {}
        with self.assertRaises(StoreError) as e:
            self.notifier.notify_removed_management_position(1, 1)
        assert e.exception.store_error_type == StoreErrorTypes.no_listeners_for_store

    def test_general_message(self):
        self.notifier._user_facade.notify_user = MagicMock()
        self.notifier.notify_general_message(1, "message")
        self.notifier._user_facade.notify_user.assert_called_once()

    def test_generate_notification_id(self):
        self.assertEqual(self.notifier._generate_notification_id(), 1)
        self.assertEqual(self.notifier._generate_notification_id(), 2)
        self.assertEqual(self.notifier._generate_notification_id(), 3)
        self.assertEqual(self.notifier._generate_notification_id(), 4)
        self.assertEqual(self.notifier._generate_notification_id(), 5)
        self.assertEqual(self.notifier._generate_notification_id(), 6)
        self.assertEqual(self.notifier._generate_notification_id(), 7)
        self.assertEqual(self.notifier._generate_notification_id(), 8)
        self.assertEqual(self.notifier._generate_notification_id(), 9)
        self.assertEqual(self.notifier._generate_notification_id(), 10)

    def test_notify(self):
        self.notifier._user_facade.notify_user = MagicMock()
        self.notifier._notify_delayed(1, "message")
        self.notifier._user_facade.notify_user.assert_called_once()

    def test_sign_listener(self):
        self.notifier._listeners = {}
        self.notifier.sign_listener(1, 1)
        self.assertEqual(self.notifier._listeners, {1: [1]})

    def test_sign_listener_existing(self):
        self.notifier._listeners = {1: [1]}
        with self.assertRaises(UserError) as e:
            self.notifier.sign_listener(1, 1)
        assert e.exception.user_error_type == UserErrorTypes.user_already_listener_for_store

    def test_unsign_listener(self):
        self.notifier._listeners = {1: [1]}
        self.notifier.unsign_listener(1, 1)
        self.assertEqual(self.notifier._listeners, {})

    def test_unsign_listener_no_listeners(self):
        self.notifier._listeners = {}
        with self.assertRaises(StoreError) as e:
            self.notifier.unsign_listener(1, 1)
        assert e.exception.store_error_type == StoreErrorTypes.no_listeners_for_store
