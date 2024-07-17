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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    products = db.Column(db.String(1000), nullable=False)  # JSON string to store product quantities
    
    user = db.relationship("User", back_populates="baskets")
    # cart = db.relationship("ShoppingCart", back_populates='baskets')

    def __init__(self, store_id: int, user_id: int) -> None:
        self.store_id = store_id
        self.user_id = user_id
        self.products = json.dumps({})  # Store products as a JSON string

    def add_product(self, product_id: int, quantity: int) -> None:
        if quantity < 0:
            raise StoreError("Quantity can't be negative", StoreErrorTypes.invalid_amount)
        products = self.get_dto()
        products[product_id] = products.get(product_id, 0) + quantity
        self.products = json.dumps(products)

        db.session.commit()

    def get_dto(self) -> Dict[int, int]:
        dict = json.loads(self.products)
        ans = {}
        for key in dict:
            ans[int(key)] = int(dict[key])
        return ans

    def remove_product(self, product_id: int, quantity: int):
        if quantity < 0:
            raise StoreError("Quantity can't be negative", StoreErrorTypes.invalid_amount)
        products = self.get_dto()
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
        if quantity < 0:
            raise StoreError("Quantity can't be negative", StoreErrorTypes.invalid_amount)
        products = self.get_dto()
        if product_id not in products:
            raise StoreError("Product not found", StoreErrorTypes.product_not_found)
        if products[product_id] < quantity:
            raise StoreError("Not enough quantity", StoreErrorTypes.product_not_available)
        products[product_id] -= quantity
        self.products = json.dumps(products)

        db.session.commit()


class ShoppingCart():
    # __tablename__ = 'shopping_carts'
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, primary_key=True)
    # baskets = db.relationship("ShoppingBasket", back_populates='cart')

    # user = db.relationship("User", back_populates="shopping_cart", uselist=False)

    
    # __table_args__ = (
    #     db.PrimaryKeyConstraint('user_id'),
    #     db.ForeignKeyConstraint([''],
    #                             ['immediate_sub_purchases.purchase_id', 'immediate_sub_purchases.store_id']),
    # )

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    def add_product_to_basket(self, store_id: int, product_id: int, quantity: int) -> None:
        basket = next((b for b in self.baskets if b.store_id == store_id), None)
        if not basket:
            basket = ShoppingBasket(store_id, self.user_id)
            self.baskets.append(basket)
            db.session.add(basket)
        basket.add_product(product_id, quantity)

        db.session.commit()

    def get_dto(self) -> Dict[int, Dict[int, int]]:
        return {basket.store_id: basket.get_dto() for basket in self.baskets}

    def remove_product_from_basket(self, store_id: int, product_id: int, quantity: int) -> None:
        if quantity < 0: 
            raise StoreError("Quantity can't be negative", StoreErrorTypes.invalid_amount)
        basket = next((b for b in self.baskets if b.store_id == store_id), None)
        if not basket:
            raise StoreError("Store not found", StoreErrorTypes.store_not_found)
        basket.remove_product(product_id, quantity)

        db.session.commit()

    def subtract_product_from_cart(self, store_id: int, product_id: int, quantity: int) -> None:
        if quantity < 0:
            raise StoreError("Quantity can't be negative", StoreErrorTypes.invalid_amount)
        basket = next((b for b in self.baskets if b.store_id == store_id), None)
        if not basket:
            raise StoreError("Store not found", StoreErrorTypes.store_not_found)
        basket.subtract_product(product_id, quantity)

        db.session.commit()


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(5000), nullable=False)
    date = db.Column(DateTime, nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    member = db.relationship('Member', back_populates='notifications')

    def __init__(self, message: str, date: datetime) -> None:
        self.message = message
        self.date = date

    def get_notification_dto(self) -> NotificationDTO:
        return NotificationDTO(self.id, self.message, self.date)
    

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
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
    currency = db.Column(db.String(10), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=True)
    member = db.relationship("Member", backref=backref("user", uselist=False))
    baskets = db.relationship("ShoppingBasket", back_populates='user')

    def __init__(self, user_id: int, currency: str = 'USD') -> None:
        if currency not in c.currencies:
            raise UserError("Currency not supported", UserErrorTypes.currency_not_supported)

        self.id = user_id
        self.currency = currency
        self.member_id = None
        self.member = None
        # self.shopping_cart = ShoppingCart(self.id)

    def is_member(self):
        return self.member is not None
    
    def get_username(self):
        if self.is_member():
            return self.member.username
        return None

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


    def add_product_to_basket(self, store_id: int, product_id: int, quantity: int) -> None:
        if quantity < 0:
            raise StoreError("Quantity can't be negative", StoreErrorTypes.invalid_amount)
        # self.shopping_cart.add_product_to_basket(store_id, product_id, quantity)
        basket = next((b for b in self.baskets if b.store_id == store_id), None)
        if not basket:
            basket = ShoppingBasket(store_id, self.id)
            self.baskets.append(basket)
            db.session.add(basket)
        basket.add_product(product_id, quantity)

        db.session.commit()

    def get_shopping_cart(self) -> Dict[int, Dict[int, int]]:
        # return self.shopping_cart.get_dto()
        return {basket.store_id: basket.get_dto() for basket in self.baskets}

    def register(self, email: str, username: str, password: str, year: int, month: int, day: int, phone: str) -> None:
        if email == "" or username == "" or password == "":
            raise UserError("Empty fields", UserErrorTypes.empty_fields)
        if self.is_member():
            raise UserError("User is already registered", UserErrorTypes.user_already_registered)
        self.member_id = db.session.query(Member).count()
        self.member = Member(self.member_id, email, username, password, year, month, day, phone)
        db.session.add(self.member)
        db.session.commit()

    def remove_product_from_basket(self, store_id: int, product_id: int, quantity: int):
        if quantity < 0:
            raise StoreError("Quantity can't be negative", StoreErrorTypes.invalid_amount)
        # self.shopping_cart.remove_product_from_basket(store_id, product_id, quantity)
        basket = next((b for b in self.baskets if b.store_id == store_id), None)
        if not basket:
            raise StoreError("Store not found", StoreErrorTypes.store_not_found)
        basket.remove_product(product_id, quantity)

        db.session.commit()

    def subtract_product_from_cart(self, store_id: int, product_id: int, quantity: int):
        if quantity < 0:
            raise StoreError("Quantity can't be negative", StoreErrorTypes.invalid_amount)
        # self.shopping_cart.subtract_product_from_cart(store_id, product_id, quantity)
        basket = next((b for b in self.baskets if b.store_id == store_id), None)
        if not basket:
            raise StoreError("Store not found", StoreErrorTypes.store_not_found)
        basket.subtract_product(product_id, quantity)

        db.session.commit()

    def clear_basket(self):
        for basket in db.session.query(ShoppingBasket).filter_by(user_id=self.id).all():
            db.session.delete(basket)
        # cart = db.session.query(ShoppingCart).filter_by(user_id=self.id).first()
        # db.session.delete(cart)

        # self.cart = ShoppingCart(self.id)
        # db.session.add(self.cart)
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
        else:
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
        # self.shopping_cart = ShoppingCart(self.id)
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
            self.__id_serializer = db.session.query(User).count()

    def clean_data(self):
        """
        For testing purposes only
        """
        UserFacade.__id_serializer = 0
        db.session.query(User).delete()
        db.session.query(Member).delete()
        db.session.query(Notification).delete()
        db.session.query(ShoppingBasket).delete()
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
            ans = user.is_suspended()
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

    def get_user(self, user_id: int) -> User:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserError("User not found", UserErrorTypes.user_not_found)
        return user

    def get_userDTO(self, user_id: int, role: str = None) -> UserDTO:
        user = self.get_user(user_id)
        return user.get_user_dto(role)

    def create_user(self, currency: str = "USD") -> int:
        with UserFacade.__create_lock:
            id = UserFacade.__id_serializer
            UserFacade.__id_serializer += 1
        user = User(id, currency)
        logger.info(f"User {id} created")
        db.session.add(user)
        db.session.commit()
        logger.info(f"User {id} added to database")
        return user.id
    
    def register_user(self, user_id, email: str, username: str, password: str,
                      year: int, month: int, day: int, phone: str) -> None:
        with UserFacade.__register_lock:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                raise UserError("User not found", UserErrorTypes.user_not_found)
            if user.is_member():
                raise UserError("User is already registered", UserErrorTypes.user_already_registered)
            member = Member.query.filter_by(username=username).first()
            if member:
                raise UserError("Username already exists", UserErrorTypes.username_already_exists)
            
            user.register(email, username, password, year, month, day, phone)

    def get_user_id_from_username(self, username: str) -> int:
        member = Member.query.filter_by(username=username).first()
        if not member:
            raise UserError("Username not found", UserErrorTypes.username_not_found)
        return member.id

    def get_notifications(self, user_id: int) -> List[NotificationDTO]:
        with UserFacade.__notification_lock:
            notifications = self.get_user(user_id).get_notifications()
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
            self.get_user(user_id).clear_notifications()

    def notify_user(self, user_id: int, notification: NotificationDTO) -> None:
        with UserFacade.__notification_lock:
            self.get_user(user_id).add_notification(
                Notification(notification.get_message(), notification.get_date()))

    def add_product_to_basket(self, user_id: int, store_id: int, product_id: int, quantity: int) -> None:
        with UserFacade.__suspend_lock:
            if self.suspended(user_id):
                raise UserError("User is suspended", UserErrorTypes.user_suspended)
        self.get_user(user_id).add_product_to_basket(store_id, product_id, quantity)

    def get_shopping_cart(self, user_id: int) -> Dict[int, Dict[int, int]]:
        with UserFacade.__suspend_lock:
            if self.suspended(user_id):
                raise UserError("User is suspended", UserErrorTypes.user_suspended)
        return self.get_user(user_id).get_shopping_cart()

    def remove_product_from_basket(self, user_id: int, store_id: int, product_id: int, quantity: int) -> None:
        with UserFacade.__suspend_lock:
            if self.suspended(user_id):
                raise UserError("User is suspended", UserErrorTypes.user_suspended)
        self.get_user(user_id).remove_product_from_basket(store_id, product_id, quantity)

    def clear_basket(self, user_id: int) -> None:
        with UserFacade.__suspend_lock:
            if self.suspended(user_id):
                raise UserError("User is suspended", UserErrorTypes.user_suspended)
        self.get_user(user_id).clear_basket()

    def get_password(self, username: str) -> Tuple[int, str]:
        member = Member.query.filter_by(username=username).first()
        if not member:
            raise UserError("Username not found", UserErrorTypes.username_not_found)
        return member.id, member.get_password()

    def remove_user(self, user_id: int):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserError("User not found", UserErrorTypes.user_not_found)
        
        # cart = ShoppingCart.query.filter_by(user_id=user_id).first()
        # db.session.delete(cart)

        for basket in ShoppingBasket.query.filter_by(user_id=user_id).all():
            db.session.delete(basket)

        db.session.delete(user)
        db.session.commit()

    def logout_user(self, user_id: int):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UserError("User not found", UserErrorTypes.user_not_found)
        
        if not user.is_member():
            self.remove_user(user_id)

    def is_member(self, user_id: int) -> bool:
        return self.get_user(user_id).is_member()

    def get_users_dto(self, roles: Dict[int, str]) -> Dict[int, UserDTO]:  # user_id -> role
        out = {}
        for user_id, role in roles.items():
            out[user_id] = self.get_user(user_id).get_user_dto(role)
        return out

    def restore_basket(self, user_id: int, cart: Dict[int, Dict[int, int]]):
        self.get_user(user_id).clear_basket()
        for store_id, products in cart.items():
            for product_id, quantity in products.items():
                self.add_product_to_basket(user_id, store_id, product_id, quantity)

    def set_user_shopping_cart(self, user_id: int, cart: Dict[int, Dict[int, int]]):
        user = self.get_user(user_id)
        user.set_cart(cart)

    def get_all_members(self) -> List[UserDTO]:
        users = User.query.all()
        out = []
        for user in users:
            if user.is_member():
                out.append(user.get_user_dto())
        return out
