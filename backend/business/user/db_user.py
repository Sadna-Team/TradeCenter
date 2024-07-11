from datetime import datetime
from typing import List, Optional, Dict
from backend.business.user.user import UserError, UserErrorTypes, User, PurchaseUserDTO, UserDTO
from backend.error_types import StoreError, StoreErrorTypes
from . import c
from flask_sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from flask_sqlalchemy.orm import relationship, backref, declarative_base
from flask_sqlalchemy.ext.declarative import declared_attr
from flask_sqlalchemy import create_engine
from flask_sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ShoppingBasket(Base):
    __tablename__ = 'shopping_baskets'
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, nullable=False)
    products = Column(String, nullable=False)  # JSON string to store product quantities

    def __init__(self, store_id: int) -> None:
        self.store_id = store_id
        self.products = {}  # Use dictionary for in-memory operations

    def add_product(self, product_id: int, quantity: int) -> None:
        self.products[product_id] = self.products.get(product_id, 0) + quantity

    def get_dto(self) -> Dict[int, int]:
        return self.products

    def remove_product(self, product_id: int, quantity: int):
        if product_id not in self.products:
            raise StoreError("Product not found", StoreErrorTypes.product_not_found)
        if self.products[product_id] < quantity:
            raise StoreError("Not enough quantity", StoreErrorTypes.product_not_available)
        self.products[product_id] -= quantity
        if self.products[product_id] == 0:
            del self.products[product_id]

    def subtract_product(self, product_id: int, quantity: int):
        if product_id not in self.products:
            raise StoreError("Product not found", StoreErrorTypes.product_not_found)
        if self.products[product_id] < quantity:
            raise StoreError("Not enough quantity", StoreErrorTypes.product_not_available)
        self.products[product_id] -= quantity

class ShoppingCart(Base):
    __tablename__ = 'shopping_carts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    shopping_baskets = relationship("ShoppingBasket", backref="shopping_cart")

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    def add_product_to_basket(self, store_id: int, product_id: int, quantity: int) -> None:
        basket = next((b for b in self.shopping_baskets if b.store_id == store_id), None)
        if not basket:
            basket = ShoppingBasket(store_id)
            self.shopping_baskets.append(basket)
        basket.add_product(product_id, quantity)

    def get_dto(self) -> Dict[int, Dict[int, int]]:
        return {basket.store_id: basket.get_dto() for basket in self.shopping_baskets}

    def remove_product_from_basket(self, store_id: int, product_id: int, quantity: int) -> None:
        basket = next((b for b in self.shopping_baskets if b.store_id == store_id), None)
        if not basket:
            raise StoreError("Store not found", StoreErrorTypes.store_not_found)
        basket.remove_product(product_id, quantity)

    def subtract_product_from_cart(self, store_id: int, product_id: int, quantity: int) -> None:
        basket = next((b for b in self.shopping_baskets if b.store_id == store_id), None)
        if not basket:
            raise StoreError("Store not found", StoreErrorTypes.store_not_found)
        basket.subtract_product(product_id, quantity)

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

    def __init__(self, message: str, date: datetime) -> None:
        self.message = message
        self.date = date

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    birthdate = Column(DateTime, nullable=False)
    phone = Column(String, nullable=False)
    is_suspended = Column(Boolean, default=False)
    suspended_until = Column(DateTime, nullable=True)
    notifications = relationship("Notification", backref="member")

    def __init__(self, email: str, username, password: str, year: str, month: str, day: str, phone: str) -> None:
        self.email = email
        self.username = username
        self.password = password
        self.birthdate = datetime(int(year), int(month), int(day))
        self.phone = phone
        self.notifications = []

    def set_suspense(self, value: bool, suspended_until: Optional[datetime]):
        self.is_suspended = value
        self.suspended_until = suspended_until
        
    def get_password(self):
        return self.password

    def get_notifications(self):
        return self.notifications

    def add_notification(self, notification: Notification):
        self.notifications.append(notification)

    def clear_notifications(self):
        self.notifications.clear()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    currency = Column(String, nullable=False)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=True)
    member = relationship("Member", backref=backref("user", uselist=False))
    shopping_cart_id = Column(Integer, ForeignKey('shopping_carts.id'))
    shopping_cart = relationship("ShoppingCart", backref=backref("user", uselist=False))

    def __init__(self, user_id: int, currency: str = 'USD') -> None:
        if currency not in c.currencies:
            raise UserError("Currency not supported", UserErrorTypes.currency_not_supported)

        self.id = user_id
        self.currency = currency
        self.member = None
        self.shopping_cart = ShoppingCart(user_id)

    def add_notification(self, notification: Notification) -> None:
        if self.member:
            self.member.add_notification(notification)

    def get_notifications(self) -> List[Notification]:
        if self.member:
            return self.member.get_notifications()
        return []

    def clear_notifications(self) -> None:
        if self.member:
            self.member.clear_notifications()

    def add_product_to_basket(self, store_id: int, product_id: int, quantity: int) -> None:
        self.shopping_cart.add_product_to_basket(store_id, product_id, quantity)

    def get_shopping_cart(self) -> Dict[int, Dict[int, int]]:
        return self.shopping_cart.get_dto()

    def register(self, email: str, username: str, password: str, year: int, month: int, day: int, phone: str) -> None:
        if self.member:
            raise UserError("User is already registered", UserErrorTypes.user_already_registered)
        self.member = Member(email, username, password, year, month, day, phone)

    def remove_product_from_basket(self, store_id: int, product_id: int, quantity: int):
        self.shopping_cart.remove_product_from_basket(store_id, product_id, quantity)

    def subtract_product_from_cart(self, store_id: int, product_id: int, quantity: int):
        self.shopping_cart.subtract_product_from_cart(store_id, product_id, quantity)

    def clear_basket(self):
        self.shopping_cart = ShoppingCart(self.id)

    def get_password(self):
        if self.member:
            return self.member.get_password()
        return None

    def is_member(self):
        return self.member is not None
    
    def is_suspended(self):
        if self.member:
            return self.member.is_suspended()
        return False
    
    def change_suspend(self, value: bool, suspended_until: Optional[datetime]):
        if self.member:
            self.member.set_suspense(value, suspended_until)

    def create_purchase_user_dto(self) -> PurchaseUserDTO:
        if self.member:
            return PurchaseUserDTO(self.id, self.member.get_birthdate())
        return PurchaseUserDTO(self.id)

    def get_user_dto(self, role: str = None) -> UserDTO:
        if not self.is_member():
            return UserDTO(self.id)
        return UserDTO(self.id, self.member.get_email(), self.member.get_username(),
                       self.member.get_birthdate().year, self.member.get_birthdate().month,
                       self.member.get_birthdate().day, self.member.get_phone(), role)
    
    def set_cart(self, cart: Dict[int, Dict[int, int]]):
        self.shopping_cart = ShoppingCart(self.id)
        for store_id, products in cart.items():
            for product_id, quantity in products.items():
                self.add_product_to_basket(store_id, product_id, quantity)

# SQLAlchemy setup
DATABASE_URL = "postgresql+psycopg2://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
