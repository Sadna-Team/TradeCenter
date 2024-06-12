from .. import UserFacade
from typing import Dict
from datetime import datetime
from .. import NotificationDTO
from threading import Lock
# from ...socketio import send_real_time_notification
from backend import socketio
from flask import jsonify
from backend.business.authentication.authentication import Authentication

# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')


# ---------------------------------------------------


def send_real_time_notification(user_id, notification: NotificationDTO):
    message = jsonify({'message': notification.to_json()})
    socketio.send(message, json=True, to=user_id, include_self=False)
    logger.info(f"sent message to user {user_id}")


class Notifier:
    # singleton
    __instance = None
    __create_lock = Lock()
    __sign_lock = Lock()
    __store_lock: Dict[int, Lock] = {}

    def __new__(cls):
        if Notifier.__instance is None:
            Notifier.__instance = object.__new__(cls)
        return Notifier.__instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._user_facade: UserFacade = UserFacade()  # Singleton
            self._authentication: Authentication = Authentication()  # Singleton
            self._listeners: Dict = {}  # Would it restart the listeners every time the server restarts?
            self._notification_id = 0

    def clean_data(self) -> None:
        """
        For testing purposes only
        """
        self._user_facade.clean_data()
        self._listeners.clear()
        self._notification_id = 0

    def _generate_notification_id(self) -> int:
        with self.__create_lock:
            self._notification_id += 1
            return self._notification_id

    def _notify_delayed(self, user_id: int, message: str) -> None:
        """
        * Parameters: user_id: int, message: str
        * This function sends a message to a single offline user.
        """
        notification = NotificationDTO(self._generate_notification_id(), message, datetime.now())
        self._user_facade.notify_user(user_id, notification)

    def _notify_real_time(self, user_id: int, message: str) -> None:
        """
        * Parameters: user_id: int, message: str
        * This function sends a message to a single online user.
        """
        notification = NotificationDTO(self._generate_notification_id(), message, datetime.now())
        send_real_time_notification(user_id, notification)

    def _notify_multiple(self, store_id: int, message: str) -> None:
        """
        * Parameters: store_id: int, message: str
        * This function sends a message to multiple users.
        """
        if store_id not in self._listeners:
            raise ValueError("No listeners for the store with ID:", store_id)

        for owner in self._listeners[store_id]:
            if self._authentication.is_logged_in(owner):
                self._notify_real_time(owner, message)
            else:
                self._notify_delayed(owner, message)

    # Notify on new purchase --- for store owner    
    def notify_new_purchase(self, store_id: int, purchase_id: int) -> None:
        """
        * Parameters: store_id: int, purchase_id: int
        * This function notifies the store owner(s) of a new purchase in the store.
        """
        msg = "New purchase in store: " + str(store_id) + "\n purchase ID: " + str(purchase_id)  # + "With the info:"
        self._notify_multiple(store_id, msg)

    # Notify on a new bid  --- for store owner
    def notify_new_bid(self, store_id: int, user_id: int) -> None:
        """
        * Parameters: store_id: int, user_id(Who created a bid purchase): int
        * This function notifies the store owner(s) of a new purchase in the store.
        """
        msg = f"User {user_id} has created a bid purchase"
        self._notify_multiple(store_id, msg)

    def notify_general_listeners(self, store_id: int, message: str) -> None:
        """
        * Parameters: store_id: int, message: str
        * This function notifies all the store listeners on a general message.
        """
        self._notify_multiple(store_id, message)

    # Notify on a store update (closed or opened) --- for store owner
    def notify_update_store_status(self, store_id: int, is_closed: bool, additional_details="") -> None:
        """
        * Parameters: store_id: int, isClosed: bool, additional details: str
        * isClosed is a boolean - *True* if the store is closed *False* if the store is opened.
        * This function notifies the store owner(s) on a change in the store status (closed or opened).
        """

        if is_closed:
            update = "closed"
        else:
            update = "opened"

        msg = "Store status updated for: " + str(
            store_id) + "\n Store is now: " + update + ".\nadditional details: " + additional_details
        self._notify_multiple(store_id, msg)

    # Notify on a removed management position --- for store owner
    def notify_removed_management_position(self, store_id: int, user_id: int) -> None:
        """
        * Parameters: store_id: int, user_id: int
        * This function notifies a store owner that he was removed from the management position.
        """

        if store_id not in self._listeners:
            raise ValueError("No listeners for the store with ID:", store_id)

        msg = "your position in store: " + str(store_id) + " has been terminated."
        if self._authentication.is_logged_in(user_id):
            self._notify_real_time(user_id, msg)
        else:
            self._notify_delayed(user_id, msg)

    # Notify on a new message --- for member
    def notify_general_message(self, user_id: int, message: str) -> None:
        """
        * Parameters: user_id: int, message: str
        * This function notifies a user on a new message.
        """
        if self._authentication.is_logged_in(user_id):
            self._notify_real_time(user_id, message)
        else:
            self._notify_delayed(user_id, message)

    # Notify and wait for 

    def sign_listener(self, user_id: int, store_id: int) -> None:
        """
        * Parameters: user_id: int, store_id: int
        * This function adds a new user (new manager or new owner) to the store listeners.
        * It would alert him to the events that are relevant to the store (new purchase, store update, removed
        management position)
        """
        with self.__sign_lock:
            if store_id not in self._listeners:
                self._listeners[store_id] = []
                self.__store_lock[store_id] = Lock()

        with self.__store_lock[store_id]:
            if user_id not in self._listeners[store_id]:
                self._listeners[store_id].append(user_id)
            else:
                raise ValueError("User is already a listener for the store with ID:", store_id)

    def unsign_listener(self, user_id: int, store_id: int) -> None:
        """
        * Parameters: user_id: int, store_id: int
        * This function removes a user (manager or owner) from the store listeners.
        """
        with self.__store_lock[store_id]:
            if store_id in self._listeners:
                self._listeners[store_id].remove(user_id)
                if not self._listeners[store_id]:
                    self._listeners.pop(store_id)
            else:
                raise ValueError("No listeners for the store with ID:", store_id)
