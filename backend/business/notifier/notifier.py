from .. import UserFacade
from typing import Dict
from datetime import datetime
from .. import NotificationDTO
from threading import Lock
from flask_socketio import join_room
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from backend.business.authentication.authentication import Authentication
from backend.error_types import *
from flask import current_app

# Database related imports
from sqlalchemy.exc import SQLAlchemyError
from backend.database import db

# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')


# ---------------------------------------------------

class Notifier:

    # singleton

    __instance = None
    __create_lock = Lock()
    __sign_lock = Lock()
    __store_lock: Dict[int, Lock] = {} #TODO #load_store_locks?


    def __new__(cls):
        if Notifier.__instance is None:
            Notifier.__instance = super(Notifier, cls).__new__(cls)
        return Notifier.__instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._user_facade: UserFacade = UserFacade()  # Singleton
            self._authentication: Authentication = Authentication()  # Singleton
            #self._listeners: Dict = {} # Would it restart the listeners every time the server restarts?
            self._notification_id = 0
            self.socketio_manager = None

    @property
    def _listeners(self):
        listeners = db.session.query(Listeners).all()
        result = {}
        for listener in listeners:
            result[listener.store_id] = [int(x) for x in listener.get_listeners.split(',')]
        return result
    
    @_listeners.setter
    def _listeners(self, listeners):
        #delete all listeners
        db.session.query(Listeners).delete()
        db.session.commit()

        for store_id in listeners.keys():
            for listener in listeners[store_id]:
                self.sign_listener(listener, store_id)


    def clean_data(self) -> None:
        """
        For testing purposes only
        """
        self._user_facade.clean_data()
        self._listeners.clear()
        self._notification_id = 0

    def set_socketio_manager(self, socketio_manager):
        self.socketio_manager = socketio_manager

    def send_real_time_notification(self, user_id, notification: NotificationDTO):
        message = jsonify({'message': notification.to_json()})
        # self.socketio_manager.send(notification.to_json(), json=True, to=user_id)
        self.socketio_manager.emit('message', notification.to_json(), room=user_id)
        # self.socketio_manager.send(message, json=True, to=user_id)
        logger.info(f"sent message to user {user_id}")

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
        self.send_real_time_notification(user_id, notification)

    def _notify_multiple(self, store_id: int, message: str, send_by = None) -> None:
        """
        * Parameters: store_id: int, message: str
        * This function sends a message to multiple users.
        """
        from backend.app_factory import create_app_instance
        app = create_app_instance()
        with app.app_context():
            all_listeners = db.session.query(Listeners).filter_by(store_id=store_id).all()
            if len(all_listeners) == 0:
                raise StoreError(f"No listenerss for the store with ID: {store_id}", StoreErrorTypes.no_listeners_for_store)
            for listeners in all_listeners:
                if listeners.get_listeners == '':
                    raise StoreError(f"No listenerss for the store with ID: {store_id}", StoreErrorTypes.no_listeners_for_store)

                for listener in listeners.get_listeners.split(','):
                    listener = int(listener)
                    logger.info(f"send message to user {listener}")
                    if self._authentication.is_logged_in(listener):
                        self._notify_real_time(listener, message)
                    else:
                        self._notify_delayed(listener, message)
            
        # if store_id not in self._listeners:
        #     raise StoreError(f"No listeners for the store with ID: {store_id}", StoreErrorTypes.no_listeners_for_store)

        # for owner in self._listeners[store_id]:
        #     if self._authentication.is_logged_in(owner):
        #         self._notify_real_time(owner, message)
        #     else:
        #         self._notify_delayed(owner, message)

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


    def notify_bid_cancelled_by_store_worker(self, store_id: int, user_id: int) -> None:
        """
        * Parameters: store_id: int, user_id(Who created a bid purchase): int
        * This function notifies the store owner(s) of a new purchase in the store.
        """
        msg = f"User {user_id} has cancelled a bid purchase"
        self._notify_multiple(store_id, msg, user_id)

    def notify_bid_cancelled_by_user(self, store_id: int, user_id: int) -> None:
        """
        * Parameters: store_id: int, user_id(Who created a bid purchase): int
        * This function notifies the store owner(s) of a new purchase in the store.
        """
        msg = f"User {user_id} has cancelled a bid purchase"
        self._notify_multiple(store_id, msg)

    def notify_bid_counter_offer(self, store_id: int, user_id: int) -> None:
        """
        * Parameters: store_id: int, user_id(Who created a bid purchase): int
        * This function notifies the store owner(s) of a new purchase in the store.
        """
        msg = f"User {user_id} has created a counter offer"
        self._notify_multiple(store_id, msg)

    def notify_bid_accepted(self, store_id: int, user_id: int) -> None:
        """
        * Parameters: store_id: int, user_id(Who created a bid purchase): int
        * This function notifies the store owner(s) of a new purchase in the store.
        """
        msg = f"User {user_id} has accepted a bid purchase"
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
            
            raise StoreError(f"No listeners for the store with ID: {store_id}", StoreErrorTypes.no_listeners_for_store)

        logger.info(f"send message to user {user_id} about being removed from store {store_id}")

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
        try:
            if self._authentication.is_logged_in(user_id):
                # logger.info(f"send message to user {user_id}")
                self._notify_real_time(user_id, message)
            else:
                self._notify_delayed(user_id, message)
        except Exception as e:
            logger.error(f"Failed to send message to user {user_id} with error: {e}")

    # Notify and wait for 

    def sign_listener(self, user_id: int, store_id: int) -> None:
        """
        * Parameters: user_id: int, store_id: int
        * This function adds a new user (new manager or new owner) to the store listeners.
        * It would alert him to the events that are relevant to the store (new purchase, store update, removed
        management position)
        """
        with current_app.app_context():
            store = db.session.query(Listeners).filter_by(store_id=store_id).all()
            if len(store) == 0:
                new_listener = Listeners(store_id, str(user_id))
                db.session.add(new_listener)
                db.session.commit()
                self.__store_lock[store_id] = Lock()
            else:
                db.session.query(Listeners).filter_by(store_id=store_id).first().add_listener_to_store(user_id)
                
        # with self.__sign_lock:
        #     if store_id not in self._listeners:
        #         self._listeners[store_id] = []
        #         self.__store_lock[store_id] = Lock()

        # with self.__store_lock[store_id]:
        #     if user_id not in self._listeners[store_id]:
        #         self._listeners[store_id].append(user_id)
        #     else:
        #         raise UserError(f"User is already a listener for the store with ID: {store_id}", UserErrorTypes.user_already_listener_for_store)

    def unsign_listener(self, user_id: int, store_id: int) -> None:
        """
        * Parameters: user_id: int, store_id: int
        * This function removes a user (manager or owner) from the store listeners.
        """
        with current_app.app_context():
            with self.__store_lock[store_id]:
                store = db.session.query(Listeners).filter_by(store_id=store_id).all()
                if len(store) == 0:
                    raise StoreError(f"No listeners for the store with ID: {store_id}", StoreErrorTypes.no_listeners_for_store)
                db.session.query(Listeners).filter_by(store_id=store_id).first().remove_listener_from_store(user_id)
            
        # with self.__store_lock[store_id]:
        #     if store_id in self._listeners:
        #         self._listeners[store_id].remove(user_id)
        #         if not self._listeners[store_id]:
        #             self._listeners.pop(store_id)
        #     else:
        #         raise StoreError(f"No listeners for the store with ID: {store_id}", StoreErrorTypes.no_listeners_for_store)
            

class Listeners(db.Model):
    __tablename__ = 'listeners'
    store_id = db.Column(db.Integer, primary_key=True)
    listeners = db.Column(db.String, nullable=False)

    def __init__(self, store_id: int, listeners: str):
        self.store_id = store_id
        self.listeners = listeners
        logger.info("[Listeners] created new listeners object for store_id: " + str(store_id) + " with listeners: " + listeners)

    def add_listener_to_store(self, listener: int) -> None: 
        if str(listener) in self.listeners.split(','):
            raise UserError(f"User is already a listener for the store with ID: {self.store_id}", UserErrorTypes.user_already_listener_for_store)
        
        self.listeners += ',' + str(listener)
        db.session.commit()
        logger.info("[Listeners] added listener: " + str(listener) + " to store_id: " + str(self.store_id))

    def remove_listener_from_store(self, listener: int) -> None:
        curr_listeners = self.listeners.split(',')
        if str(listener) not in curr_listeners:
            raise UserError(f"User is not a listener for the store with ID: {self.store_id}", UserErrorTypes.user_not_listener_for_store)
        self.listeners = ','.join([str(x) for x in curr_listeners if x != str(listener)])
        if self.listeners == '':
            db.session.query(Listeners).filter_by(store_id=self.store_id).delete()
        db.session.commit()
        logger.info("[Listeners] removed listener: " + str(listener) + " from store_id: " + str(self.store_id))

    @property
    def get_listeners(self):
        return self.listeners
