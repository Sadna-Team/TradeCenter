from . import c
from typing import List, Dict, Optional, Set, Tuple
from datetime import datetime
from abc import ABC, abstractmethod
import threading
from collections import defaultdict
from backend.error_types import *
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
import json
from ...database import db

import logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                     format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("User Logger")

# NOTE: This is a workaround to avoid circular imports
# from .. import NotificationDTO

# NOTE: Solution:
from backend.business.DTOs import NotificationDTO, UserDTO, PurchaseUserDTO
from .. import NotificationDTO

class ShoppingBasket(db.Model):
    __tablename__ = 'shopping_baskets'
    store_id = db.Column(db.Integer, nullable=False, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('shopping_carts.user_id'), nullable=False, primary_key=True)
    products = db.Column(db.String(100), nullable=False)  # JSON string to store product quantities
    shopping_cart = db.relationship("ShoppingCart", back_populates="shopping_baskets")
   
    def __init__(self, store_id: int, cart_id: int) -> None:
        self.store_id = store_id
        self.cart_id = cart_id
        self.products = json.dumps({})  # Store products as a JSON string

    def add_product(self, product_id: int, quantity: int) -> None:
        products = json.loads(self.products)
        products[product_id] = products.get(product_id, 0) + quantity
        self.products = json.dumps(products)

        db.session.commit()

    def get_dto(self) -> Dict[int, int]:
        return json.loads(self.products)

    def remove_product(self, product_id: int, quantity: int):
        products = json.loads(self.products)
        if product_id not in products:
            raise StoreError("Product not found", StoreErrorTypes.product_not_found)
        if products[product_id] < quantity:
            raise StoreError("Not enough quantity", StoreErrorTypes.product_not_available)
        products[product_id] -= quantity
        if products[product_id] == 0:
            del products[product_id]
        self.products = json.dumps(products)

        db.session.commit()

    def subtract_product(self, product_id: int, quantity: int):
        products = json.loads(self.products)
        if product_id not in products:
            raise StoreError("Product not found", StoreErrorTypes.product_not_found)
        if products[product_id] < quantity:
            raise StoreError("Not enough quantity", StoreErrorTypes.product_not_available)
        products[product_id] -= quantity
        self.products = json.dumps(products)

        db.session.commit()


class ShoppingCart(db.Model):
    __tablename__ = 'shopping_carts'
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    shopping_baskets = db.relationship("ShoppingBasket", back_populates="shopping_cart")

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    def add_product_to_basket(self, store_id: int, product_id: int, quantity: int) -> None:
        basket = next((b for b in self.shopping_baskets if b.store_id == store_id), None)
        if not basket:
            basket = ShoppingBasket(store_id, self.user_id)
            self.shopping_baskets.append(basket)
            db.session.add(basket)
        basket.add_product(product_id, quantity)

        db.session.commit()

    def get_dto(self) -> Dict[int, Dict[int, int]]:
        return {basket.store_id: basket.get_dto() for basket in self.shopping_baskets}

    def remove_product_from_basket(self, store_id: int, product_id: int, quantity: int) -> None:
        basket = next((b for b in self.shopping_baskets if b.store_id == store_id), None)
        if not basket:
            raise StoreError("Store not found", StoreErrorTypes.store_not_found)
        basket.remove_product(product_id, quantity)

        db.session.commit()

    def subtract_product_from_cart(self, store_id: int, product_id: int, quantity: int) -> None:
        basket = next((b for b in self.shopping_baskets if b.store_id == store_id), None)
        if not basket:
            raise StoreError("Store not found", StoreErrorTypes.store_not_found)
        basket.subtract_product(product_id, quantity)

        db.session.commit()


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000), nullable=False)
    date = db.Column(DateTime, nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    member = db.relationship('Member', back_populates='notifications')

    def __init__(self, notification_id: int, message: str, date: datetime) -> None:
        self.id = notification_id
        self.message = message
        self.date = date

    def get_notification_dto(self) -> NotificationDTO:
        return NotificationDTO(self.id, self.message, self.date)


class State(ABC):
    @abstractmethod
    def get_password(self):
        pass

    @abstractmethod
    def get_notifications(self) -> List[Notification]:
        pass

    @abstractmethod
    def add_notification(self, notification: Notification):
        pass

    @abstractmethod
    def clear_notifications(self):
        pass

    @abstractmethod
    def get_email(self):
        pass

    @abstractmethod
    def get_username(self):
        pass

    @abstractmethod
    def get_birthdate(self) -> Optional[datetime]:
        pass

    @abstractmethod
    def get_phone(self):
        pass

    @abstractmethod
    def is_suspended(self):
        pass

    @abstractmethod
    def set_suspense(self, value: bool, suspended_until:Optional[datetime]):
        pass


class Guest(State):
    def get_password(self):
        raise UserError("User is not registered", UserErrorTypes.user_not_registered)

    def get_notifications(self):
        raise UserError("User is not registered", UserErrorTypes.user_not_registered)

    def add_notification(self, notification: Notification):
        raise UserError("User is not registered", UserErrorTypes.user_not_registered)

    def clear_notifications(self):
        raise UserError("User is not registered", UserErrorTypes.user_not_registered)

    def get_email(self):
        raise UserError("User is not registered", UserErrorTypes.user_not_registered)

    def get_username(self):
        raise UserError("User is not registered", UserErrorTypes.user_not_registered)

    def get_birthdate(self) -> Optional[datetime]:
        raise UserError("User is not registered", UserErrorTypes.user_not_registered)

    def get_phone(self):
        raise UserError("User is not registered", UserErrorTypes.user_not_registered)
    
    def is_suspended(self):
        raise UserError("User is not registered", UserErrorTypes.user_not_registered)

    def set_suspense(self, value: bool, suspended_until:Optional[datetime]):
        raise UserError("User is not registered", UserErrorTypes.user_not_registered)


class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    is_suspended = db.Column(db.Boolean, default=False)
    suspended_until = db.Column(db.DateTime, nullable=True)
    notifications = db.relationship('Notification', back_populates='member')


    def __init__(self, id: int, email: str, username: str, password: str, year: str, month: str, day: str, phone: str) -> None:
        self.id = id
        self.email = email
        self.username = username
        self.password = password
        self.birthdate = datetime(int(year), int(month), int(day))
        self.phone = phone

    def set_suspense(self, value: bool, suspended_until: Optional[datetime]):
        self.is_suspended = value
        self.suspended_until = suspended_until
        db.session.commit()

    def get_password(self):
        return self.password

    def get_notifications(self):
        return self.notifications

    def add_notification(self, notification: Notification):
        self.notifications.append(notification)
        db.session.commit()

    def clear_notifications(self):
        self.notifications.clear()
        db.session.commit()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=True)
    member = db.relationship("Member", backref=backref("user", uselist=False))
    shopping_cart = db.relationship("ShoppingCart", backref=backref("user", uselist=False))

    def __init__(self, user_id: int, currency: str = 'USD') -> None:
        if currency not in c.currencies:
            raise UserError("Currency not supported", UserErrorTypes.currency_not_supported)

        self.id = user_id
        self.currency = currency
        self.member_id = None
        self.member = None
        self.shopping_cart = ShoppingCart(self.id)

    def is_member(self):
        return self.member is not None
    
    def add_notification(self, notification: Notification) -> None:
        if self.is_member():
            self.member.add_notification(notification)

        db.session.add(notification)
        db.session.commit()

    def get_notifications(self) -> List[Notification]:
        if self.is_member():
            return self.member.get_notifications()
        return []

    def clear_notifications(self) -> None:
        if self.is_member():
            self.member.clear_notifications()
        
        notifications = Notification.query.filter_by(member_id=self.member.id).all()
        for notification in notifications:
            db.session.delete(notification)
        db.session.commit()

    def add_product_to_basket(self, store_id: int, product_id: int, quantity: int) -> None:
        self.shopping_cart.add_product_to_basket(store_id, product_id, quantity)

    def get_shopping_cart(self) -> Dict[int, Dict[int, int]]:
        return self.shopping_cart.get_dto()

    def register(self, email: str, username: str, password: str, year: int, month: int, day: int, phone: str) -> None:
        if self.is_member():
            raise UserError("User is already registered", UserErrorTypes.user_already_registered)
        self.member_id = db.session.query(Member).count() + 1
        self.member = Member(self.member_id, email, username, password, year, month, day, phone)
        db.session.add(self.member)
        db.session.commit()

    def remove_product_from_basket(self, store_id: int, product_id: int, quantity: int):
        self.shopping_cart.remove_product_from_basket(store_id, product_id, quantity)

    def subtract_product_from_cart(self, store_id: int, product_id: int, quantity: int):
        self.shopping_cart.subtract_product_from_cart(store_id, product_id, quantity)

    def clear_basket(self):
        self.shopping_cart = ShoppingCart(self.id)
        db.session.commit()

    def get_password(self):
        if self.is_member():
            return self.member.get_password()
        raise UserError("User is not registered", UserErrorTypes.user_not_registered)

    def is_suspended(self):
        if self.is_member():
            return self.member.is_suspended
        return False
    
    def change_suspend(self, value: bool, suspended_until: Optional[datetime]):
        if self.is_member():
            self.member.set_suspense(value, suspended_until)
        raise UserError("User is not registered", UserErrorTypes.user_not_registered)

    def create_purchase_user_dto(self) -> PurchaseUserDTO:
        if self.is_member():
            return PurchaseUserDTO(self.id, self.member.birthdate)
        return PurchaseUserDTO(self.id)

    def get_user_dto(self, role: str = None) -> UserDTO:
        if not self.is_member():
            return UserDTO(self.id)
        return UserDTO(self.id, self.member.email, self.member.username,
                       self.member.birthdate.year, self.member.birthdate.month,
                       self.member.birthdate.day, self.member.phone, role)
    
    def set_cart(self, cart: Dict[int, Dict[int, int]]):
        self.shopping_cart = ShoppingCart(self.id)
        for store_id, products in cart.items():
            for product_id, quantity in products.items():
                self.add_product_to_basket(store_id, product_id, quantity)
        
        db.session.commit()


class UserFacade:
    # singleton
    __create_lock = threading.Lock()
    __register_lock = threading.Lock()
    __notification_lock = threading.Lock()
    __suspend_lock = threading.Lock()
    __id_serializer: int = 0
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserFacade, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True

    def clean_data(self):
        """
        For testing purposes only
        """
        UserFacade.__id_serializer = 0
        db.session.query(User).delete()
        db.session.commit()

    def get_suspended_users(self) -> Dict[int, Optional[datetime]]:
        # suspended_users = SuspendedUser.query.all()
        # return {su.user_id: su.suspension_end for su in suspended_users}
        users = User.query.all()
        with UserFacade.__suspend_lock:
            out = {user.id: user.member.suspended_until for user in users if user.is_suspended()}
        return out

    def suspended(self, user_id: int) -> bool:
        """
        If a user is a guest we continue, 
        otherwise we check if the user is registered and suspended
        * Return True if we can't continue
        """
        user = User.query.filter_by(id=user_id).first()
        with UserFacade.__suspend_lock:
            if not user:
                return False
            ans = self.user.is_suspended()
        return ans

    def suspend_user_permanently(self, user_id: int):
        """
        Suspend user permanently, only system manager can do this
        * user_id: the id of the user to suspend
        """
        user = User.query.filter_by(id=user_id).first()
        with UserFacade.__suspend_lock:
            if not user:
                raise UserError("User not found", UserErrorTypes.user_not_found)
            user.change_suspend(True, None)

    def suspend_user_temporarily(self, user_id: int, date_details: dict, time_details: dict):
        """
        Suspend user for a specific time, only system manager can do this
        * user_id: the id of the user to suspend
        * date_details: the date until the user is suspended (year, month, day)
        * time_details: the time until the user is suspended (hour, minute)
        """
        date = datetime(int(date_details["year"]), int(date_details["month"]), int(date_details["day"]), int(time_details["hour"]), int(time_details["minute"]))    

        user = User.query.filter_by(id=user_id).first()
        with UserFacade.__suspend_lock:
            if not user:
                raise UserError("User not found", UserErrorTypes.user_not_found)
            user.change_suspend(True, date)

    def unsuspend_user(self, user_id: int):
        """
        Unsuspend user, only system manager can do this
        * actor_id: the id of system manager
        * user_id: the id of the user to unsuspend
        """
        user = User.query.filter_by(id=user_id).first()
        with UserFacade.__suspend_lock:
            if not user:
                raise UserError("User not found", UserErrorTypes.user_not_found)
            user.change_suspend(False, None)

    def __get_user(self, user_id: int) -> User:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserError("User not found", UserErrorTypes.user_not_found)
        return user

    def get_userDTO(self, user_id: int, role: str = None) -> UserDTO:
        user = self.__get_user(user_id)
        return user.get_user_dto(role)

    def create_user(self, currency: str = "USD") -> int:
        with UserFacade.__create_lock:
            id = UserFacade.__id_serializer
            UserFacade.__id_serializer += 1
        user = User(id, currency)
        db.session.add(user)
        db.session.commit()
        return user.id
    
    def register_user(self, user_id, email: str, username: str, password: str,
                      year: int, month: int, day: int, phone: str) -> None:
        with UserFacade.__register_lock:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                raise UserError("User not found", UserErrorTypes.user_not_found)
            if user.is_member():
                raise UserError("User is already registered", UserErrorTypes.user_already_registered)
            user = User.query.filter_by(username=username).first()
            if user:
                raise UserError("Username already exists", UserErrorTypes.username_already_exists)
            
            user.register(email, username, password, year, month, day, phone)

    def get_user_id_from_username(self, username: str) -> int:
        user = User.query.filter_by(username=username).first()
        if not user:
            raise UserError("Username not found", UserErrorTypes.username_not_found)
        return user.id

    def get_notifications(self, user_id: int) -> List[NotificationDTO]:
        with UserFacade.__notification_lock:
            notifications = self.__get_user(user_id).get_notifications()
            out = []
            for notification in notifications:
                out.append(notification.get_notification_dto().to_json())
        self.clear_notifications(user_id)
        return out

    def get_userid(self, username: str) -> int:
        member = Member.query.filter_by(username=username).first()
        if not member:
            raise UserError("Username not found", UserErrorTypes.username_not_found)
        return member.id

    def clear_notifications(self, user_id: int) -> None:
        with UserFacade.__notification_lock:
            self.__get_user(user_id).clear_notifications()

    def notify_user(self, user_id: int, notification: NotificationDTO) -> None:
        with UserFacade.__notification_lock:
            self.__get_user(user_id).add_notification(
                Notification(notification.get_message(), notification.get_date()))

    def add_product_to_basket(self, user_id: int, store_id: int, product_id: int, quantity: int) -> None:
        with UserFacade.__suspend_lock:
            if self.suspended(user_id):
                raise UserError("User is suspended", UserErrorTypes.user_suspended)
        self.__get_user(user_id).add_product_to_basket(store_id, product_id, quantity)

    def get_shopping_cart(self, user_id: int) -> Dict[int, Dict[int, int]]:
        with UserFacade.__suspend_lock:
            if self.suspended(user_id):
                raise UserError("User is suspended", UserErrorTypes.user_suspended)
        return self.__get_user(user_id).get_shopping_cart()

    def remove_product_from_basket(self, user_id: int, store_id: int, product_id: int, quantity: int) -> None:
        with UserFacade.__suspend_lock:
            if self.suspended(user_id):
                raise UserError("User is suspended", UserErrorTypes.user_suspended)
        self.__get_user(user_id).remove_product_from_basket(store_id, product_id, quantity)

    def clear_basket(self, user_id: int) -> None:
        with UserFacade.__suspend_lock:
            if self.suspended(user_id):
                raise UserError("User is suspended", UserErrorTypes.user_suspended)
        self.__get_user(user_id).clear_basket()

    def get_password(self, username: str) -> Tuple[int, str]:
        member = Member.query.filter_by(username=username).first()
        if not member:
            raise UserError("Username not found", UserErrorTypes.username_not_found)
        return member.id, member.get_password()

    def remove_user(self, user_id: int):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserError("User not found", UserErrorTypes.user_not_found)
        db.session.delete(user)
        db.session.commit()

    def is_member(self, user_id: int) -> bool:
        return self.__get_user(user_id).is_member()

    def get_users_dto(self, roles: Dict[int, str]) -> Dict[int, UserDTO]:  # user_id -> role
        out = {}
        for user_id, role in roles.items():
            out[user_id] = self.__get_user(user_id).get_user_dto(role)
        return out

    def restore_basket(self, user_id: int, cart: Dict[int, Dict[int, int]]):
        self.__get_user(user_id).clear_basket()
        for store_id, products in cart.items():
            for product_id, quantity in products.items():
                self.add_product_to_basket(user_id, store_id, product_id, quantity)

    def set_user_shopping_cart(self, user_id: int, cart: Dict[int, Dict[int, int]]):
        user = self.__get_user(user_id)
        user.set_cart(cart)

    def get_all_members(self) -> List[UserDTO]:
        users = User.query.all()
        out = []
        for user in users:
            if user.is_member():
                out.append(user.get_user_dto())
        return out
