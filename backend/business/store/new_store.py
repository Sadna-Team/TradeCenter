# ---------- Imports ------------#
from typing import Dict, Tuple, Set

from .constraints import *
from .discount import *
from .PurchasePolicy import *
from datetime import datetime
from backend.business.DTOs import ProductDTO, ProductForConstraintDTO, StoreDTO, PurchaseProductDTO, UserInformationForConstraintDTO, CategoryDTO
from backend.error_types import *
from backend.database import db

import threading
# -------------logging configuration----------------
import logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                     format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("New Store Logger")

# ---------------------------------------------------
NUMBER_OF_AVAILABLE_LOGICAL_DISCOUNT_TYPES = 3
NUMBER_OF_AVAILABLE_NUMERICAL_DISCOUNT_TYPES = 2
NUMBER_OF_AVAILALBE_PREDICATES = 4

# ---------------------product class---------------------#
class Product(db.Model):
    # id of product is productId. It is unique for each physical product
    __tablename__ = 'store_products'
    product_id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, primary_key=True)
    _product_name = db.Column(db.String(100))
    _description = db.Column(db.String(1000))
    _tags_demo = db.Column(db.String)
    _price = db.Column(db.Float)
    _weight = db.Column(db.Float)
    _amount = db.Column(db.Integer)

    __table_args__ = (
        db.PrimaryKeyConstraint('product_id', 'store_id'),
        db.ForeignKeyConstraint(['store_id'],
                                ['stores.store_id']),
    )

    """__table_args__ = (
        db.PrimaryKeyConstraint('product_id', 'store_id'),
    )"""

    product_locks = {}

    def __init__(self, store_id, product_id: int, product_name: str, description: str, price: float, weight: float,
                 amount: int = 0):
        self.product_id: int = product_id
        self.store_id = store_id

        if product_name is None or product_name == '':
            raise StoreError('Product name is not a valid string', StoreErrorTypes.invalid_product_name)

        self._product_name: str = product_name
        self._description: str = description
        self._tags_demo: str = ""  # initialized with no tags

        if price < 0:
            raise StoreError('Price is a negative value', StoreErrorTypes.invalid_price)

        self._price: float = price  # price is in dollars

        if weight < 0:
            raise StoreError('Weight is a negative value', StoreErrorTypes.invalid_weight)

        self._weight: float = weight  # weight is in kg

        if amount < 0:
            raise StoreError('Amount is a negative value', StoreErrorTypes.invalid_amount)

        self._amount: int = amount  # amount of the product in the store

        logger.info('[Product] successfully created product with id: ' + str(product_id))

    # ---------------------getters and setters---------------------
    @property
    def product_name(self) -> str:
        return self._product_name

    @property
    def description(self) -> str:
        return self._description

    @property
    def tags(self) -> List[str]:
        return self._tags

    @property
    def price(self) -> float:
        return self._price

    @property
    def weight(self) -> float:
        return self._weight

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def _tags(self) -> List[str]:
        if len(self._tags_demo) == 0:
            return []
        return self._tags_demo.split(',')

    @_tags.setter
    def _tags(self, tags: List[str]) -> None:
        if len(tags) == 0:
            self._tags_demo = ''
        else:
            self._tags_demo = ','.join(tags)

    def __add_tag(self, tag: str) -> None:
        real_tags = self._tags
        real_tags.append(tag)
        self._tags = real_tags

    def __remove_tag(self, tag: str) -> None:
        real_tags = self._tags
        real_tags.remove(tag)
        self._tags = real_tags

    # ---------------------methods--------------------------------
    def create_product_dto(self) -> ProductDTO:
        """
        * Parameters: none
        * This function creates a product DTO from the product
        * Returns: the product DTO
        """
        return ProductDTO(self.product_id, self._product_name, self._description, self._price, self._tags,
                          weight=self._weight, amount=self._amount)

    def acquire_lock(self):
        if self.product_id not in self.product_locks:
            self.product_locks[self.product_id] = threading.Lock()
        self.product_locks[self.product_id].acquire()

    def release_lock(self):
        if self.product_id in self.product_locks:
            self.product_locks[self.product_id].release()

    def change_name(self, new_name: str) -> None:
        """
        * Parameters: newName
        * This function changes the name of the product
        * Returns: none
        """
        if new_name is None or new_name == '':
            raise StoreError('New name is not a valid string', StoreErrorTypes.invalid_product_name)
        self.acquire_lock()
        self._product_name = new_name
        self.release_lock()
        logger.info('[Product] successfully changed name of product with id: ' + str(self.product_id))

    def change_price(self, new_price: float) -> None:
        """
        * Parameters: newPrice
        * This function changes the price of the product
        * Returns: True if the price is changed successfully
        """
        if new_price < 0:
            raise StoreError('New price is a negative value', StoreErrorTypes.invalid_price)
        self.acquire_lock()
        self._price = new_price
        self.release_lock()
        logger.info('[Product] successfully changed price of product with id: ' + str(self.product_id))

    def change_description(self, new_description: str) -> None:
        """
        * Parameters: new_description
        * This function changes the description of the product
        * Returns: none
        """
        if new_description is None:
            raise StoreError('New description is not a valid string', StoreErrorTypes.invalid_description)
        self.acquire_lock()
        self._description = new_description
        self.release_lock()
        logger.info(
            '[Product] successfully changed description of product with id: ' + str(self.product_id))

    def change_tags(self, new_tags: List[str]) -> None:
        """
        * Parameters: newTags
        * This function changes the tags of the product
        * Returns: none
        """
        self.acquire_lock()
        self._tags = new_tags
        self.release_lock()
        logger.info('[Product] successfully changed tags of product with id: ' + str(self.product_id))

    def change_amount(self, new_amount: int) -> None:
        """
        * Parameters: newAmount
        * This function changes the amount of the product
        * Returns: none
        """
        if new_amount < 0:
            raise StoreError('New amount is a negative value', StoreErrorTypes.invalid_amount)
        self.acquire_lock()
        self._amount = new_amount
        self.release_lock()
        logger.info('[Product] successfully changed amount of product with id: ' + str(self.product_id))

    def add_tag(self, tag: str) -> None:
        """
        * Parameters: tag
        * This function adds a tag to the product
        * Returns: true if successfully added tag
        """
        if tag is None:
            raise StoreError('Tag is not a valid string', StoreErrorTypes.invalid_tag)
        if tag in self._tags:
            raise StoreError('Tag is already in the list of tags', StoreErrorTypes.tag_already_exists)
        self.acquire_lock()
        self.__add_tag(tag)
        self.release_lock()
        logger.info('[Product] successfully added tag to product with id: ' + str(self.product_id))

    def remove_tag(self, tag: str) -> None:
        """
        * Parameters: tag
        * This function removes a tag from the product
        * Returns: none
        """
        if tag is None:
            raise StoreError('Tag is not a valid string', StoreErrorTypes.invalid_tag)
        if tag not in self._tags:
            raise StoreError('Tag is not in the list of tags', StoreErrorTypes.tag_not_found)
        self.acquire_lock()
        self.__remove_tag(tag)
        self.release_lock()
        logger.info(
            '[Product] successfully removed tag from product with id: ' + str(self.product_id))

    def has_tag(self, tag: str) -> bool:
        """
        * Parameters: tag
        * This function checks if the product has a given tag
        * Returns: true if the product has the given tag
        """
        return tag in self._tags

    def change_weight(self, new_weight: float) -> None:
        """
        * Parameters: newWeight
        * This function changes the weight of the product
        * Returns: none
        """
        logger.info('[Product] weight is being changed to: ' + str(new_weight))
        if new_weight < 0:
            raise StoreError('New weight is a negative value', StoreErrorTypes.invalid_weight)
        self.acquire_lock()
        self._weight = new_weight
        self.release_lock()
        logger.info('[Product] successfully changed weight of product with id: ' + str(self.product_id))

    def restock(self, amount) -> None:
        if amount < 0:
            raise StoreError('Amount is a negative value', StoreErrorTypes.invalid_amount)
        self.acquire_lock()
        self._amount += amount
        self.release_lock()

    def remove_amount(self, amount) -> None:
        if amount < 0:
            raise StoreError('Amount is a negative value', StoreErrorTypes.invalid_amount)
        if self._amount < amount:
            raise StoreError('Amount is greater than the available amount of the product',
                             StoreErrorTypes.invalid_amount)
        self.acquire_lock()
        self._amount -= amount
        self.release_lock()


# ---------------------category class---------------------#
class Category:
    # id of category is categoryId. It is unique for each category. Products are stored in either the category or found
    # in one of its subcategories
    # important to note: a category can only have one parent category, and a category can't have a subcategory that is
    # already a subcategory of a subcategory.

    def __init__(self, category_id: int, category_name: str):
        self.__category_id: int = category_id
        
        if category_name is None or category_name == '':
            raise StoreError('Category name is not a valid string', StoreErrorTypes.invalid_category_name)
        
        self.__category_name: str = category_name
        self.__parent_category_id: int = -1  # -1 means that the category does not have a parent category for now
        self.__category_products: List[Tuple[int, int]] = []
        self.__sub_categories: List['Category'] = []
        self.__category_lock = threading.Lock() # lock for category
        logger.info('[Category] successfully created category with id: ' + str(category_id))

    # ---------------------getters and setters---------------------
    @property
    def category_id(self) -> int:
        return self.__category_id

    @property
    def parent_category_id(self) -> int:
        return self.__parent_category_id

    @property
    def sub_categories(self) -> List['Category']:
        return self.__sub_categories

    @property
    def category_products(self) -> List[Tuple[int, int]]:
        return self.__category_products

    @property
    def category_name(self) -> str:
        return self.__category_name

    # ---------------------methods--------------------------------
    def acquire_lock(self):
        self.__category_lock.acquire()

    def release_lock(self):
        self.__category_lock.release()

    def add_parent_category(self, parent_category_id: int) -> None:
        """
        * Parameters: parentCategoryId
        * This function adds a parent category to the category
        * Returns: none
        """
        if self.__parent_category_id != -1:
            raise StoreError('Category already has a parent category', StoreErrorTypes.parent_category_already_exists)
        self.__parent_category_id = parent_category_id
        logger.info('[Category] successfully added parent category to category with id: ' + str(self.__category_id))


    def remove_parent_category(self) -> None:
        """
        * Parameters: none
        * This function removes the parent category of the category
        * Returns: none
        """
        if self.__parent_category_id == -1:
            raise StoreError('Category does not have a parent category', StoreErrorTypes.parent_category_not_found)
        self.__parent_category_id = -1
        logger.info(
            '[Category] successfully removed parent category from category with id: ' + str(self.__category_id))


    def add_sub_category(self, sub_category: 'Category') -> None:
        """
        * Parameters: sub_category
        * This function adds a sub category to the category and adds the current category as the parent category of the
        sub category
        * Returns: None
        """
        if sub_category is None:
            raise StoreError('Sub category is not a valid category', StoreErrorTypes.sub_category_error)
        elif self.is_sub_category(sub_category):
            raise StoreError('Sub category is already a sub category of the current category', StoreErrorTypes.sub_category_error)
        elif sub_category.has_parent_category():
            raise StoreError('Sub category already has a parent category', StoreErrorTypes.parent_category_already_exists)
        elif sub_category.__category_id == self.__category_id:
            raise StoreError('Sub category cannot be the same as the current category', StoreErrorTypes.sub_category_error)
        sub_category.add_parent_category(self.__category_id)
        self.__sub_categories.append(sub_category)
        logger.info('[Category] successfully added sub category to category with id: ' + str(self.__category_id))

    def remove_sub_category(self, sub_category: 'Category') -> None:
        """
        * Parameters: subCategory
        * This function removes a sub category from the category and removes the current category as the parent category
         of the sub category
        * Returns: None
        """
        if sub_category is None:
            raise StoreError('Sub category is not a valid category', StoreErrorTypes.sub_category_error)
        elif sub_category not in self.__sub_categories:
            raise StoreError('Sub category is not in the list of sub categories', StoreErrorTypes.sub_category_error)
        elif not sub_category.is_parent_category(self.__category_id):
            raise StoreError('Sub category is not a sub category of the current category', StoreErrorTypes.sub_category_error)
        sub_category.remove_parent_category()
        self.__sub_categories.remove(sub_category)
        logger.info(
            '[Category] successfully removed sub category from category with id: '
            + str(self.__category_id))

    def is_parent_category(self, category_id: int) -> bool:
        """
        * Parameters: category_id
        * This function checks that the given category is the parent category of the current category
        * Returns: True if the given category is the parent category of the current category, False otherwise
        """
        return self.__parent_category_id == category_id

    def is_sub_category(self, category: 'Category') -> bool:
        """
        * Parameters: category
        * This function checks that the given category is the sub category of the current category
        * Returns: True if the given category is the sub category of the current category, false otherwise
        """
        return category in self.__sub_categories or any(
            subCategory.is_sub_category(category) for subCategory in self.__sub_categories)

    def has_parent_category(self) -> bool:
        """
        * Parameters: none
        * This function checks that the current category has a parent category or not
        * Returns: True if the current category has a parent category, False otherwise
        """
        return self.__parent_category_id != -1

    def add_product_to_category(self, store_id: int, product_id: int) -> None:
        """
        * Parameters: store_id, product_id
        * This function adds a product to the category, 
        * Note: the product can only be added to the category if the product is not already in the list of products of the category, or the sub categories, or their subcategories etc.
        * Returns: None
        """
        with self.__category_lock:
            if (store_id, product_id) in self.get_all_products_recursively():
                raise StoreError('Product is already in the list of products', StoreErrorTypes.product_already_exists)
            self.__category_products.append((store_id, product_id))
        logger.info('[Category] successfully added product to category with id: ' + str(self.__category_id))

    def remove_product_from_category(self, store_id: int, product_id: int) -> None:
        """
        * Parameters: product_id
        * This function removes a product from the category
        * Returns: None
        """
        with self.__category_lock:
            if (store_id, product_id) not in self.__category_products:
                raise StoreError('Product is not in the list of products', StoreErrorTypes.product_not_found)
            self.__category_products.remove((store_id, product_id))
        logger.info('[Category] successfully removed product from category with id: ' + str(self.__category_id))

    def get_all_products_recursively(self) -> List[Tuple[int, int]]:
        """
        * Parameters: none
        * This function returns all the product_ids in the category and its sub categories recursively
        * Returns: all the products(store id, product id) in the category and its sub categories recursively
        """
        # Create a new list to avoid modifying the original list
        products = set(self.__category_products)

        for subCategory in self.__sub_categories:
            products.update(subCategory.get_all_products_recursively())
        return list(products)
    
    def get_all_subcategories_recursively(self) -> List[int]:
        """
        * Parameters: none
        * This function returns all the subcategories recursively
        * Returns: all the subcategories recursively
        """
        subcategories = set([self.__category_id])
        for subCategory in self.__sub_categories:
            subcategories.update(subCategory.get_all_subcategories_recursively())
        return list(subcategories)
    
    def get_category_dto(self) -> CategoryDTO:
        """
        * Parameters: none
        * This function returns the category DTO
        * Returns: the category DTO
        """
        return CategoryDTO(self.__category_id, self.__category_name, self.__parent_category_id, self.get_all_subcategories_recursively())

'''
    def get_all_product_names(self) -> str:
        """
        * Parameters: none
        * This function returns all the names of the products in the category as a big string
        * Returns: all the names of the products in the category as a big string
        """
        names = ""
        for product in self.get_all_products_recursively():
            names += product.product_name + " "
        return names
'''

'''
    def pred_no_alcohol_past_time(products: Dict[ProductDTO, int]) -> bool:
        """
            * Parameters: store_id, product_id, time
            * This function checks if the product is an alcohol product and if the time is after the time of the purchase
            * Returns: True if the product is an alcohol product and the time is after the time of the purchase, False otherwise
        """
        for product in products:
            if 'alcohol' in product.tags and datetime.now().hour > 22:
                logger.info('Alcohol product is not allowed after 22')
                return False
        return True

    def pred_has_tabacco(products: Dict[ProductDTO, int]) -> bool:
        """
        * Parameters: products
        * This function checks if the products contain alcohol
        * Returns: True if the products contain alcohol, False otherwise
        """
        for product in products:
            if 'alcohol' in product.tags:
                logger.info('Alcohol product in the basket')
                return True
        logger.info('No alcohol product in the basket')
        return False

    def pred_not_too_much_gun_powder(products: Dict[ProductDTO, int]) -> bool:
        """
        * Parameters: products
        * This function checks if the products contain too much gun powder
        * Returns: True if the products contain too much gun powder, False otherwise
        """
        for product in products:
            if 'gunpowder' in product.tags:
                logger.info('Amount of gunpowder product in the basket exceeds the limit of 100')
                return  product.weight * products[product] >= 100
        logger.info('Not too much gunpowder found in basket')
        return False

    def pred_has_tabbaco(products: Dict[ProductDTO, int]) -> bool:
        """
        * Parameters: products
        * This function checks if the products contain tabbaco
        * Returns: True if the products contain tabbaco, False otherwise
        """
        for product in products:
            if 'tabbaco' in product.tags:
                logger.info('Tabbaco product in the basket')
                return True
        logger.info('No tabbaco product in the basket')
        return False

    def pred_older_then_18(user: PurchaseUserDTO) -> bool:
        """
        * Parameters: products
        * This function checks if the products are older than 18
        * Returns: True if the products are older than 18, False otherwise
        """
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day
        if user.birthdate is None:
            logger.warning('User does not have a birthdate')
            return False
        delta = current_year - user.birthdate.year + (current_month - user.birthdate.month) / 12 + (current_day - user.birthdate.day) / 365
        return delta >= 18

    def pred_funny_name(products: Dict[ProductDTO, int]) -> bool:
        """
        * Parameters: products
        * This function checks if the products have a funny name
        * Returns: True if the products have a funny name, False otherwise
        """
        for product in products:
            if product.name == 'funny':
                return True
        return False

    def filter_no_alcohol_and_tabbaco_bellow_18(products: Dict[ProductDTO, int], user: PurchaseUserDTO) -> PurchaseComposite:
        """
        * Parameters: products, user
        * This function checks if the products contain alcohol and the user is older than 18
        * Returns: True if the products contain alcohol and the user is older than 18, False otherwise
        """
        user_old_enough = UserFilter(user, pred_older_then_18)
        no_alcohol = NotFilter(ProductFilter(products, pred_has_tabacco))
        no_tabbaco = NotFilter(ProductFilter(products, pred_has_tabbaco))
        total_filter = OrFilter([user_old_enough, AndFilter([no_alcohol, no_tabbaco])])
        return total_filter

    def filter_no_alcohol_past_time(products: Dict[ProductDTO, int], user: PurchaseUserDTO) -> PurchaseComposite:
        """
        * Parameters: products
        * This function checks if the products contain alcohol and the time is after 22
        * Returns: True if the products contain alcohol and the time is after 22, False otherwise
        """
        return ProductFilter(products, pred_no_alcohol_past_time)

    def filter_not_too_much_gun_powder(products: Dict[ProductDTO, int], user: PurchaseUserDTO) -> PurchaseComposite:
        """
        * Parameters: products
        * This function checks if the products contain too much gun powder
        * Returns: True if the products contain too much gun powder, False otherwise
        """
        return NotFilter(ProductFilter(products, pred_not_too_much_gun_powder))

    def filter_no_funny_name(products: Dict[ProductDTO, int], user: PurchaseUserDTO) -> PurchaseComposite:
        """
        * Parameters: products
        * This function checks if the products have a funny name
        * Returns: True if the products have a funny name, False otherwise
        """
        return NotFilter(ProductFilter(products, pred_funny_name))

    AVAILABLE_POLICIES = {
        "no_alcohol_past_time": filter_no_alcohol_past_time,
        "not_too_much_gun_powder": filter_not_too_much_gun_powder,
        "no_alcohol_and_tabbaco_bellow_18": filter_no_alcohol_and_tabbaco_bellow_18, 
        "no_funny_name": filter_no_funny_name
    }
'''

class Store(db.Model):
    # id of store is storeId. It is unique for each store
    __tablename__ = 'stores'

    store_id = db.Column(db.Integer, primary_key=True)#, autoincrement=True)
    _store_name = db.Column(db.String(100))
    _store_founder_id = db.Column(db.Integer)
    _is_active = db.Column(db.Boolean)
    _product_id_counter = db.Column(db.Integer)
    _founded_date = db.Column(db.DateTime)
    #_policy_id_counter = db.Column(db.Integer)

    _address = db.relationship('StoreAddress', uselist=False, backref='store')
    _store_products = db.relationship('Product', backref='store', lazy=True)

    checkout_locks = {}
    _product_id_locks = {}


    def __init__(self, store_name: str, store_founder_id: int):
        self._address: Optional[StoreAddress] = None
        self._store_name = store_name
        self._store_founder_id = store_founder_id
        self._is_active = True
        self._product_id_counter = 0  # product Id
        self._product_id_lock = threading.Lock() # lock for product id
        #self._purchase_policy: Dict[int, PurchasePolicy] = {} # purchase policy
        self._founded_date = datetime.now()
        #self._policy_id_counter = 0  # purchase policy Id

    # ---------------------getters and setters---------------------#

    def set_new_address(self, address: AddressDTO) -> None:
        self._address = StoreAddress(self.store_id, address.address, address.city, address.state, address.country,
                                     address.zip_code)

    @property
    def address(self):
        return self._address

    @property
    def store_name(self) -> str:
        return self._store_name

    @property
    def store_founder_id(self) -> int:
        return self._store_founder_id

    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def store_products(self) -> List[int]:
        # return a list of all the product ids in the store
        res = db.session.query(Product).filter(Product.store_id == self.store_id).all()
        # remove duplicates
        return list(set([product.product_id for product in res]))

    @property
    def founded_date(self) -> datetime:
        return self._founded_date

    @property
    def purchase_policy(self) -> List[int]:
        res = db.session.query(PurchasePolicy).filter(PurchasePolicy.store_id == self.store_id).all()
        return list(set([policy.policy_id for policy in res]))
    # ---------------------methods--------------------------------
    def close_store(self, user_id: int) -> None:
        """
        * Parameters: userId
        * This function closes the store
        * Returns: none
        """
        if user_id is None:
            raise StoreError('User id is not a valid integer', StoreErrorTypes.invalid_user_id)
        
        if not user_id == self._store_founder_id:
            raise StoreError('User is not the founder of the store', StoreErrorTypes.user_not_founder_of_store)
        if not self._is_active:
            raise StoreError('Store is already closed', StoreErrorTypes.store_not_active)
        self.acquire_lock()
        self._is_active = False
        self.release_lock()
        logger.info('[Store] successfully closed store with id: ' + str(self.store_id))
            

    def open_store(self, user_id: int) -> None:
        """
        * Parameters: userId
        * This function opens the store
        * Returns: none
        """
        if user_id is None:
            raise StoreError('User id is not a valid integer', StoreErrorTypes.invalid_user_id)
        if not user_id == self._store_founder_id:
            raise StoreError('User is not the founder of the store', StoreErrorTypes.user_not_founder_of_store)
        if self._is_active:
            raise StoreError('Store is already open', StoreErrorTypes.store_already_open)
        self.acquire_lock()
        self._is_active = True
        self.release_lock()
        logger.info('[Store] successfully opened store with id: ' + str(self.store_id))
        
    def acquire_lock(self):
        if self.store_id not in self.checkout_locks:
            self.checkout_locks[self.store_id] = threading.Lock()
        self.checkout_locks[self.store_id].acquire()

    def release_lock(self):
        if self.store_id in self.checkout_locks:
            self.checkout_locks[self.store_id].release()

    def __acquire_product_id_lock(self) -> None:
        if self.store_id not in self._product_id_locks:
            self._product_id_locks[self.store_id] = threading.Lock()

        self._product_id_locks[self.store_id].acquire()

    def __release_product_id_lock(self) -> None:
        if self.store_id in self._product_id_locks:
            self._product_id_locks[self.store_id].release()


    # We assume that the marketFacade verified that the user attempting to add the product is a store Owner
    def add_product(self, name: str, description: str, price: float, tags: List[str], weight: float, amount: int = 0) -> int:
        """
        * Parameters: name, description, price, tags, amount
        * This function adds a product to the store
        * Returns: none
        """
        self.__acquire_product_id_lock()
        product = Product(self.store_id, self._product_id_counter, name, description, price, weight, amount)
        for tag in tags:
            product.add_tag(tag)
        db.session.add(product)
        self._product_id_counter += 1
        self.__release_product_id_lock()
        logger.info('[Store] successfully added product to store with id: ' + str(self.store_id))
        return product.product_id

    # We assume that the marketFacade verified that the user attempting to remove the product is a store owner/purchased
    def remove_product(self, product_id: int) -> None:
        """
        * Parameters: productId
        * This function removes a product from the store
        * Returns: none
        """
        try:
            self.acquire_products_lock([product_id])
            db.session.query(Product).filter(Product.product_id == product_id).delete()
            Product.product_locks[product_id].release()
            logger.info('Successfully removed product from store with id: {self.__store_id}')
        except KeyError:
            raise StoreError('Product is not found', StoreErrorTypes.product_not_found)

    def get_product_by_id(self, product_id: int) -> Product:
        """
        * Parameters: productId
        * This function gets a product by its ID
        * Returns: the product with the given ID
        """
        try:
            return db.session.query(Product).filter(Product.product_id == product_id).one()
        except Exception:
            raise StoreError('Product is not found', StoreErrorTypes.product_not_found)

    def get_product_dto_by_id(self, product_id: int) -> ProductDTO:
        """
        * Parameters: productId
        * This function gets a product DTO by its ID
        * Returns: the product DTO with the given ID
        """
        return self.get_product_by_id(product_id).create_product_dto()
        
    def add_purchase_policy(self, policy_name: str, category_id: Optional[int], product_id: Optional[int]) -> int:
        """
        * Parameters: policyName, categoryId, productId
        * This function adds a purchase policy to the store
        * Returns: the purchase policy ID
        """
        policy_id: int = -1
        if policy_name is None or policy_name == '':
            raise StoreError('Policy name is not a valid string', StoreErrorTypes.invalid_policy_name)
        if category_id is None and product_id is None:
            basket_policy_to_add = BasketSpecificPurchasePolicy(self.store_id, policy_name)
            db.session.add(basket_policy_to_add)
            db.session.flush()
            #self._purchase_policy[self._policy_id_counter] = basket_policy_to_add
            policy_id = basket_policy_to_add.policy_id
            #self._policy_id_counter += 1

        elif category_id is not None and product_id is None:
            category_policy_to_add = CategorySpecificPurchasePolicy(self.store_id, policy_name, category_id)
            db.session.add(category_policy_to_add)
            #self._purchase_policy[self._policy_id_counter] = category_policy_to_add
            db.session.flush()
            policy_id = category_policy_to_add.policy_id
            #self._policy_id_counter += 1
        
        elif category_id is None and product_id is not None:
            if db.session.query(Product).filter(Product.product_id == product_id).count() == 0:
                logger.warning('[Store] Product is not found in the store with id: {self.__store_id}')
                raise StoreError('Product is not found', StoreErrorTypes.product_not_found)
            product_policy_to_add = ProductSpecificPurchasePolicy(self.store_id, policy_name, product_id)
            db.session.add(product_policy_to_add)
            db.session.flush()
            policy_id = product_policy_to_add.policy_id
            # self._purchase_policy[self._policy_id_counter] = product_policy_to_add
            # self._policy_id_counter += 1

        else:
            logger.warning('[Store] Invalid input when trying to add a purchase policy to store with id: {self.__store_id}')
            raise StoreError('Invalid purchase policy input', StoreErrorTypes.invalid_purchase_policy_input)

        if policy_id == -1:
            raise StoreError('Something unexpected happened when adding the purchase policy to the store with id: {self.__store_id}', StoreErrorTypes.unexpected_error)

        # db.session.add(self._purchase_policy[policy_id])
        db.session.commit()

        logger.info('[Store] successfully added purchase policy to store with id: {self.__store_id}')
        return policy_id

    def __get_purchase_policy_by_id(self, policy_id: int) -> PurchasePolicy:
        """
        * Parameters: policyId
        * This function gets a purchase policy by its ID
        * Returns: the purchase policy with the given ID
        """
        try:
            pur = db.session.query(PurchasePolicy).filter_by(purchase_policy_id=policy_id).one()
            if pur.store_id != self.store_id:
                raise StoreError('Purchase policy is not found', StoreErrorTypes.policy_not_found)
            return pur
        except Exception as e:
            logger.error('[Store] Purchase policy is not found in store with id: {self.__store_id}')
            raise StoreError('Purchase policy is not found', StoreErrorTypes.policy_not_found)

    def remove_purchase_policy(self, policy_id: int) -> None:
        """
        * Parameters: policyId
        * This function removes a purchase policy from the store
        * Returns: none
        """
        # if policy_id not in self._purchase_policy:
        #     raise StoreError('Purchase policy is not found', StoreErrorTypes.policy_not_found)
        # self._purchase_policy.pop(policy_id)
        self.__get_purchase_policy_by_id(policy_id) # check for existance
        
        db.session.query(PurchasePolicy).filter(PurchasePolicy.policy_id == policy_id).delete()
        db.session.commit()

        logger.info('[Store] successfully removed purchase policy from store with id: {self.__store_id}')
        
    def create_composite_purchase_policy(self, policy_name: str, policy_id_left: int, policy_id_right: int, type_of_composite: int) -> int:
        """
        * Parameters: policyName, policyIdLeft, policyIdRight, typeOfComposite
        * This function creates a composite purchase policy
        * Returns: the purchase policy ID
        * NOTE: in type_of_composite: 1 is AND, 2 is OR, 3 is Conditional
        """
        
        if policy_name is None or policy_name == '':
            logger.error('[Store] Policy name is not a valid string in store with id: {self.__store_id}')
            raise StoreError('Policy name is not a valid string', StoreErrorTypes.invalid_policy_name)
        
        new_policy_id: int = -1
        new_policy: PurchasePolicy = None
        # if policy_id_left not in self._purchase_policy or policy_id_right not in self._purchase_policy:
        #     logger.error('[Store] Purchase policy components of new composite policy are not found in store with id: {self.__store_id}')
        #     raise StoreError('Failed to create composite policy due to having atleast one of the policies missing', StoreErrorTypes.policy_not_satisfied)
        left_policy = self.__get_purchase_policy_by_id(policy_id_left)
        right_policy = self.__get_purchase_policy_by_id(policy_id_right)
        
        
        # left_policy = self._purchase_policy[policy_id_left]
        # right_policy = self._purchase_policy[policy_id_right]
        if type_of_composite == 1:
            and_composite_policy = AndPurchasePolicy(self.store_id, policy_name, left_policy, right_policy)
            # self._purchase_policy[self._policy_id_counter] = and_composite_policy
            new_policy_id = and_composite_policy.policy_id
            # self._policy_id_counter += 1
            
            # #we will now remove the two policies that were used to create the composite policy
            # self._purchase_policy.pop(policy_id_left)
            # self._purchase_policy.pop(policy_id_right)
            new_policy = and_composite_policy

        elif type_of_composite == 2:
            or_composite_policy = OrPurchasePolicy(self.store_id, policy_name, left_policy, right_policy)
            # self._purchase_policy[self._policy_id_counter] = or_composite_policy
            new_policy_id = or_composite_policy.policy_id
            # self._policy_id_counter += 1

            # #we will now remove the two policies that were used to create the composite policy
            # self._purchase_policy.pop(policy_id_left)
            # self._purchase_policy.pop(policy_id_right)
            new_policy = or_composite_policy

        elif type_of_composite == 3:
            conditional_composite_policy = ConditioningPurchasePolicy(self.store_id, policy_name, left_policy, right_policy)
            # self._purchase_policy[self._policy_id_counter] = conditional_composite_policy
            new_policy_id = conditional_composite_policy.policy_id
            # self._policy_id_counter += 1

            # #we will now remove the two policies that were used to create the composite policy
            # self._purchase_policy.pop(policy_id_left)
            # self._purchase_policy.pop(policy_id_right)
            new_policy = conditional_composite_policy
        else:
            raise StoreError('Invalid type of composite', StoreErrorTypes.invalid_purchase_policy_input)
        
        if new_policy_id == -1:
            raise StoreError('Failed to create composite policy in store with id: {self.__store_id}', StoreErrorTypes.unexpected_error)
        
        # remove left and right policies
        db.session.query(PurchasePolicy).filter(PurchasePolicy.policy_id == policy_id_left).delete()
        db.session.query(PurchasePolicy).filter(PurchasePolicy.policy_id == policy_id_right).delete()

        db.session.add(new_policy)
        db.session.commit()

        logger.info('[Store] successfully created composite purchase policy in store with id: {self.__store_id}')
        return new_policy_id

    def assign_predicate_to_purchase_policy(self, policy_id: int, predicate: Constraint):
        """
        * Parameters: policyId, predicate
        * This function assigns a predicate to a purchase policy
        * Returns: none
        """
        # if policy_id not in self._purchase_policy:
        #     raise StoreError('Purchase policy is not found', StoreErrorTypes.policy_not_found)
        pol = self.__get_purchase_policy_by_id(policy_id)
        pol.set_predicate(predicate)
        #self._purchase_policy[policy_id].set_predicate(predicate)

    def check_purchase_policies_of_store(self, basket: BasketInformationForConstraintDTO) -> bool:
        """
        * Parameters: basket
        * This function checks if the purchase policy is satisfied
        * Returns: true if the purchase policy is satisfied
        """
        if basket is None:
            raise PurchaseError('Basket is not a valid basket', PurchaseErrorTypes.invalid_basket)
        if basket.store_id != self.store_id:
            raise PurchaseError('Basket is not from the same store', PurchaseErrorTypes.basket_not_for_store)

        for policy in db.session.query(PurchasePolicy).filter(PurchasePolicy.store_id == self.store_id).all():
            if not policy.check_constraint(basket):
                return False
        return True
    
    def acquire_products_lock(self, product_ids: List[int]) -> None:
        """
        * Parameters: productIds
        * This function acquires the lock of the products
        * Returns: none
        """
        # sort the product ids to avoid deadlocks
        product_ids.sort()
        for product_id in product_ids:
            self.get_product_by_id(product_id).acquire_lock()

    def release_products_lock(self, product_ids: List[int]) -> None:
        """
        * Parameters: productIds
        * This function releases the lock of the products
        * Returns: none
        """
        # sort the product ids to avoid deadlocks
        product_ids.sort()
        for product_id in product_ids:
            self.get_product_by_id(product_id).release_lock()

    def get_total_price_of_basket_before_discount(self, basket: Dict[int, int]) -> float:
        """
        * Parameters: basket
        * This function calculates the total price of the basket
        * Returns: the total price of the basket
        """
        total_price = 0.0
        self.acquire_products_lock(list(basket.keys()))
        try:
            for product_id, amount in basket.items():
                product = self.get_product_by_id(product_id)
                if product is not None:
                    total_price += product.price * amount
                else:
                    self.release_products_lock(list(basket.keys()))
                    raise StoreError('Product is not found', StoreErrorTypes.product_not_found)
            self.release_products_lock(list(basket.keys()))
        except Exception as e:
            self.release_products_lock(list(basket.keys()))
            raise e
        return total_price

    def create_store_dto(self) -> StoreDTO:
        """
        * Parameters: none
        * This function creates a store DTO from the store
        * Returns: the store DTO
        """
        store_dto = StoreDTO(self.store_id, self._address.to_dto(), self._store_name, self._store_founder_id,
                             self._is_active, self._founded_date)
        product_dtos = [product.create_product_dto() for product in db.session.query(Product).filter(Product.store_id == self.store_id).all()]
        store_dto.products = product_dtos
        return store_dto

    def get_store_information(self) -> StoreDTO:
        """ 
        * Parameters: none
        * This function returns the store information as a string
        * Returns: the store information as a string
        """
        return self.create_store_dto()

    def restock_product(self, product_id: int, amount: int) -> None:
        """
        * Parameters: productId, amount
        * This function restocks a product in the store
        * Returns: none
        """
        if amount < 0:
            raise StoreError('Amount is not a valid integer', StoreErrorTypes.invalid_amount)
        
        
        prod = self.get_product_by_id(product_id)
        prod.restock(amount)
        logger.info('[Store] successfully restocked product with id: ' + str(product_id))

    def remove_product_amount(self, product_id: int, amount: int) -> None:
        """
        * Parameters: productId, amount
        * This function removes a product from the store
        * Returns: none
        """
        prod = self.get_product_by_id(product_id)
        if prod.amount < amount:
            raise StoreError('Amount is greater than the available amount of the product', StoreErrorTypes.invalid_amount)
        
        if amount < 0:
            raise StoreError('Amount is not a valid integer', StoreErrorTypes.invalid_amount)
        
        prod.remove_amount(amount)
        logger.info('Successfully removed product amount with id: {product_id}')

    def change_description_of_product(self, product_id: int, new_description: str) -> None:
        """
        * Parameters: productId, newDescription
        * This function changes the description of the product
        * Returns: none
        """
        product = self.get_product_by_id(product_id)
        if new_description is None:
            raise StoreError('Description is not a valid string', StoreErrorTypes.invalid_description)
        
        if product is not None:
            product.change_description(new_description)
            logger.info('Successfully changed description of product with id: {product_id}')
        else:
            raise StoreError('Product is not found', StoreErrorTypes.product_not_found)

    def change_price_of_product(self, product_id: int, new_price: float) -> None:
        """
        * Parameters: productId, newPrice
        * This function changes the price of the product
        * Returns: none
        """
        product = self.get_product_by_id(product_id)
        
        if new_price <0:
            raise StoreError('Price is not a valid float', StoreErrorTypes.invalid_price)
        
        if product is not None:
            product.change_price(new_price)
            logger.info('Successfully changed price of product with id: {product_id} to {new_price}')
        else:
            raise StoreError('Product is not found', StoreErrorTypes.product_not_found)

    def add_tag_to_product(self, product_id: int, tag: str) -> None:
        """
        * Parameters: productId, tag
        * This function adds a tag to the product
        * Returns: none
        """
        product = self.get_product_by_id(product_id)
        if product is not None:
            product.add_tag(tag)
            logger.info('Successfully added tag: {tag} to product with id: {product_id} in store with id: {self.__store_id}')
        else:
            raise StoreError('Product is not found', StoreErrorTypes.product_not_found)

    def remove_tag_from_product(self, product_id: int, tag: str) -> None:
        """
        * Parameters: productId, tag
        * This function removes a tag from the product
        * Returns: none
        """
        product = self.get_product_by_id(product_id)
        if product is not None:
            product.remove_tag(tag)
            logger.info('Successfully removed tag  {tag} from product with id: {product_id} in store with id: {self.__store_id}')
        else:
            raise StoreError('Product is not found', StoreErrorTypes.product_not_found)

         
    def get_policy_by_id(self, policy_id: int) -> PurchasePolicy:
        """
        * Parameters: policyId
        * This function gets a purchase policy by its ID
        * Returns: the purchase policy with the given ID
        """
        # try:
        #     return self._purchase_policy[policy_id]
        # except KeyError:
        #     raise StoreError("purchase policy is not found", StoreErrorTypes.policy_not_found)
        return self.__get_purchase_policy_by_id(policy_id)
        
    def view_all_purchase_policies(self) -> List[dict]:
        """
        * Parameters: none
        * This function gets all the purchase policies of the store
        * Returns: all the purchase policies of the store
        """
        policies = []
        for policy in db.session.query(PurchasePolicy).filter(PurchasePolicy.store_id == self.store_id).all():
            policies.append(policy.get_policy_info_as_dict())
        return policies

    def get_tags_of_product(self, product_id: int) -> List[str]:
        """
        * Parameters: productId
        * This function gets all the tags of a product
        * Returns: all the tags of the product
        """
        product = self.get_product_by_id(product_id)
        if product is not None:
            return product.tags
        else:
            raise StoreError('Product is not found', StoreErrorTypes.product_not_found)

    def has_amount_of_product(self, product_id: int, amount: int) -> bool:
        """
        * Parameters: productId, amount
        * This function checks if the store has the given amount of the product
        * Returns: true if the store has the given amount of the product
        """
        try:
            prod = self.get_product_by_id(product_id)
        except KeyError:
            return False
        prod.acquire_lock()
        try:
            ans = prod.amount >= amount
            prod.release_lock()
        except Exception as e:
            prod.release_lock()
            raise e
        return ans

    def change_weight_of_product(self, product_id: int, new_weight: float) -> None:
        """
        * Parameters: productId, newWeight
        * This function changes the weight of the product
        * Returns: none
        """
        product = self.get_product_by_id(product_id)
        product.change_weight(new_weight)

    
    def edit_product(self, product_id: int, name: str, description: str, price: float, tags: List[str], weight: float, amount: Optional[int]=None) -> None:
        """
        * Parameters: productId, name, description, price, tags, weight
        * This function edits a product in the store
        * Returns: none
        """
        product = self.get_product_by_id(product_id)
        product.change_name(name)
        product.change_description(description)
        product.change_price(price)
        product.change_weight(weight)
        product.change_tags(tags)
        if amount is not None:
            product.change_amount(amount)
        logger.info('[Store] successfully edited product in store with id: ' + str(self.store_id))
# ---------------------end of classes---------------------#

def create_store(address: AddressDTO, store_name: str, store_founder_id: int) -> Store:
    if store_name is None or store_name == '':
        raise StoreError('Store name is not a valid string', StoreErrorTypes.invalid_store_name)
    st = Store(store_name, store_founder_id)
    from backend.app_factory import get_app
    with get_app().app_context():
        db.session.add(st)
        db.session.flush()
        st.set_new_address(address)
        db.session.commit()
        db.session.refresh(st)
    logger.info('[Store] successfully created store with id: ' + str(st.store_id))
    return st

class StoreAddress(db.Model):
    __tablename__ = 'store_addresses'
    store_id = db.Column(db.Integer, primary_key=True)
    _address = db.Column(db.String(100))
    _city = db.Column(db.String(100))
    _state = db.Column(db.String(100))
    _country = db.Column(db.String(100))
    _zip_code = db.Column(db.String(100))

    __table_args__ = (
        db.PrimaryKeyConstraint('store_id'),
        db.ForeignKeyConstraint(['store_id'],
                                ['stores.store_id']),
    )

    def __init__(self, store_id: int, address: str, city: str, state: str, country: str, zip_code: str):
        self.store_id = store_id
        self._address = address
        self._city = city
        self._state = state
        self._country = country
        self._zip_code = zip_code

    def to_dict(self):
        return {
            'address': self._address,
            'city': self._city,
            'state': self._state,
            'country': self._country,
            'zip_code': self._zip_code
        }

    @property
    def address(self):
        return self._address

    @property
    def city(self):
        return self._city

    @property
    def state(self):
        return self._state

    @property
    def country(self):
        return self._country

    @property
    def zip_code(self):
        return self._zip_code

    def to_dto(self):
        return AddressDTO(self._address, self._city, self._state, self._country, self._zip_code)


# ---------------------storeFacade class---------------------#
class StoreFacade:
    # singleton
    __instance = None

    def __new__(cls):
        if StoreFacade.__instance is None:
            StoreFacade.__instance = super(StoreFacade, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.__categories: Dict[int, Category] = {}  # category_id: Category
            self.__category_id_counter = 0  # Counter for category IDs
            self.__category_id_lock = threading.Lock() # lock for category id
            self.__store_id_lock = threading.Lock() # lock for store id
            self.__tags: Set[str] = set() # all existing product tags for fast access
            logger.info('successfully created storeFacade')

    def clean_data(self):
        """
        For testing purposes only
        """
        self.__categories = {}
        self.__category_id_counter = 0
        self.__tags = {
                       'alcoholic', 'tobacco', 'food', 'utilities',
                        'clothing', 'electronics', 'furniture', 'toys', 'books',
                        'beauty', 'health', 'sports', 'outdoor', 'home decor',
                        'office supplies', 'pet supplies', 'jewelry', 'footwear', 
                        'automotive', 'gardening', 'tools', 'kitchenware', 'baby products',
                        'musical instruments', 'stationery', 'party supplies', 'craft supplies'}

    # ---------------------getters and setters---------------------
    @property
    def categories(self) -> List[int]:
        return list(self.__categories.keys())

    @property
    def stores(self) -> List[int]:
        res = db.session.query(Store).all()
        return list(set([store.store_id for store in res]))
    

    constraint_types = {
        'age': AgeConstraint,
        'location' : LocationConstraint,
        'time': TimeConstraint,
        'day_of_month': DayOfMonthConstraint,
        'day_of_week': DayOfWeekConstraint,
        'season': SeasonConstraint,
        'holidays_of_country': HolidaysOfCountryConstraint,
        'price_basket': PriceBasketConstraint,
        'price_product': PriceProductConstraint,
        'price_category': PriceCategoryConstraint,
        'weight_basket': WeightBasketConstraint,
        'weight_product': WeightProductConstraint,
        'weight_category': WeightCategoryConstraint,
        'amount_basket': AmountBasketConstraint,
        'amount_product': AmountProductConstraint,
        'amount_category': AmountCategoryConstraint,
        'and': AndConstraint,
        'or': OrConstraint,
        'xor': XorConstraint,
        'implies': ImpliesConstraint
    }

    # ---------------------methods--------------------------------
    def get_category_by_id(self, category_id: int) -> Category:
        """
        * Parameters: categoryId
        * This function gets a category by its ID
        * Returns: the category with the given ID
        """
        try:
            return self.__categories[category_id]
        except KeyError:
            raise StoreError('Category is not found', StoreErrorTypes.category_not_found)
        
    def add_category(self, category_name: str) -> int:
        """
        * Parameters: categoryName, parentCategoryId
        * This function adds a category to the store
        * Returns: none
        """
        if category_name is not None or category_name != '':
            with self.__category_id_lock:
                category = Category(self.__category_id_counter, category_name)
                self.__categories[self.__category_id_counter] = category
                self.__category_id_counter += 1
            logger.info(f'[StoreFacade] successfully added category: {category_name}')
            return category.category_id
        else:
            raise StoreError('Category name is not a valid string', StoreErrorTypes.invalid_category_name)

    def remove_category(self, category_id: int) -> None:
        """
        * Parameters: categoryId
        * This function removes a category from the store removing all connections of the category with other categories
        * Note: The subcategories of the category will be moved to the parent category of the category
        * Returns: none
        """
        category_to_remove = self.get_category_by_id(category_id)
        cond = category_to_remove.has_parent_category()
        parent_category = self.get_category_by_id(category_to_remove.parent_category_id) if cond else None
        
        if category_to_remove is None:
            raise StoreError('Category is not found', StoreErrorTypes.category_not_found)

        #removing the subCategories of the category
        for subCategory in category_to_remove.sub_categories:
            subCategory.remove_parent_category()
            if parent_category is not None:
                parent_category.add_sub_category(subCategory)  #adding the parent to the sub is performed in the method

        #removing the category from the parent category
        if parent_category is not None:
            parent_category.remove_sub_category(category_to_remove)
        self.__categories.pop(category_id)
        logger.info(f'Successfully removed category with id: {category_id}')

    def assign_sub_category_to_category(self, sub_category_id: int, category_id: int) -> None:
        """
        * Parameters: subCategoryId ,categoryId
        * This function assigns a subcategory to a category
        * Note: the parent category is assigned in the method addSubCategory of the category class
        * Returns: True if the subcategory is assigned successfully
        """
        if sub_category_id == category_id:
            raise StoreError('Category cannot be a subcategory of itself', StoreErrorTypes.sub_category_error)
            
        sub_category = self.get_category_by_id(sub_category_id)
        category = self.get_category_by_id(category_id)
        category.add_sub_category(sub_category)

    def delete_sub_category_from_category(self, category_id: int, sub_category_id: int) -> None:
        """
        * Parameters: categoryId, subCategoryId
        * This function deletes a subcategory from a category
        * Note: the parent category is removed in the method removeSubCategory of the category class
        * Returns: True if the subcategory is deleted successfully
        """
        if sub_category_id is None:
            raise StoreError('Sub category id is missing', StoreErrorTypes.sub_category_error)
        if category_id is None:
            raise StoreError('Category id is missing', StoreErrorTypes.category_not_found)
        
        category = self.get_category_by_id(category_id)
        sub_category = self.get_category_by_id(sub_category_id)
        category.remove_sub_category(sub_category)

    def assign_product_to_category(self, category_id: int, store_id: int, product_id: int) -> None:
        """
        * Parameters: category_id, store_id, product_id
        * This function assigns a product none to a category
        * Returns: none
        """
        category = self.get_category_by_id(category_id)
        category.add_product_to_category(store_id, product_id)

    def remove_product_from_category(self, category_id: int, store_id: int, product_id: int) -> None:
        """
        * Parameters: category_id, store_id, product_id
        * This function removes a product from a category
        * Note: the product can only be removed if it is stored in the category itself, not in
         subcategories
        * Returns: None
        """
        category = self.get_category_by_id(category_id)
        category.remove_product_from_category(store_id, product_id)

    def add_product_to_store(self, store_id: int, product_name: str, description: str, price: float, weight: float,
                             tags: Optional[List[str]]=[], amount: Optional[int] = 0) -> int:
        """
        * Parameters: productName, weight, description, tags, manufacturer, storeIds
        * This function adds a product to the store
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)

        if product_name is None or product_name == "":
            raise StoreError('Product name is missing', StoreErrorTypes.invalid_product_name)
        if description is None:
            raise StoreError('Description is missing', StoreErrorTypes.invalid_description)
        if price < 0:
            raise StoreError('Price is a negative value', StoreErrorTypes.invalid_price)
        if amount is not None and amount < 0:
            raise StoreError('Amount is a negative value', StoreErrorTypes.invalid_amount)
        
        if tags is None:
            tags = []
            
        if weight < 0 :
            raise StoreError('Weight is a negative value', StoreErrorTypes.invalid_weight)
        logger.info(f'Successfully added product: {product_name} to store with the id: {store_id}')
        if amount is None:
            amount = 0
        logger.info(f'attempting to add product: {product_name} to store with id: {store_id}')
        product_id = store.add_product(product_name, description, price, tags, weight, amount)
        logger.info(f'Successfully added product: {product_name} to store with the id: {store_id}')
        for tag in tags:
            self.__tags.add(tag)
        logger.info(f'Successfully added tags to product: {product_name} in store with the id: {store_id}')
        db.session.flush()

        return product_id


    def remove_product_from_store(self, store_id: int, product_id: int) -> None:
        """
        * Parameters: store_id, product_id
        * This function removes a product from the store
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.remove_product(product_id)
        db.session.flush()

    def add_product_amount(self, store_id: int, product_id: int, amount: int) -> None:
        """
        * Parameters: store_id, product_id, amount, condition
        * This function adds a product to the store
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.acquire_lock()
        try:
            store.restock_product(product_id, amount)
            store.release_lock()
        except Exception as e:
            store.release_lock()
            raise e
        db.session.flush()
        logger.info(f'Successfully added {amount} of product with id: {product_id} to store with id: {store_id}')

    def remove_product_amount(self, store_id: int, product_id: int, amount: int) -> None:
        """
        * Parameters: store_id, product_id, amount, condition
        * This function removes a product from the store
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.remove_product_amount(product_id, amount)
        db.session.flush()

    def change_description_of_product(self, store_id: int, product_id: int, new_description: str) -> None:
        """
        * Parameters: store_id, product_id, new_description
        * This function changes the description of the product
        * Returns: None
        """
        store = self.__get_store_by_id(store_id)
        store.change_description_of_product(product_id, new_description)
        db.session.flush()

    def change_price_of_product(self, store_id: int, product_id: int, new_price: float) -> None:
        """
        * Parameters: store_id, product_id, new_price
        * This function changes the price of the product
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.change_price_of_product(product_id, new_price)
        db.session.flush()

    def change_weight_of_product(self, store_id: int, product_id: int, new_weight: float) -> None:
        """
        * Parameters: store_id, product_id, new_weight
        * This function changes the weight of the product
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.change_weight_of_product(product_id, new_weight)
        db.session.flush()

    def add_tag_to_product(self, store_id: int, product_id: int, tag: str) -> None:
        """
        * Parameters: store_id, product_id, tag
        * This function adds a tag to the product
        * Returns: None
        """
        store = self.__get_store_by_id(store_id)
        store.add_tag_to_product(product_id, tag)
        self.__tags.add(tag)
        db.session.flush()

    def remove_tag_from_product(self, store_id: int, product_id: int, tag: str) -> None:
        """
        * Parameters: store_id, product_id, tag
        * This function removes a tag from the product
        * Returns: None
        """
        store = self.__get_store_by_id(store_id)
        if store is None:
            raise StoreError('Store is not found',StoreErrorTypes.store_not_found)
        store.remove_tag_from_product(product_id, tag)
        db.session.flush()

    def get_tags_of_product(self, store_id: int, product_id: int) -> List[str]:
        """
        * Parameters: product_id
        * This function gets all the tags of a product 
        * Returns: all the tags of the product 
        """
        store = self.__get_store_by_id(store_id)
        return store.get_tags_of_product(product_id)

    def add_store(self, address: AddressDTO, store_name: str, store_founder_id: int) -> int:
        """
        * Parameters: locationId, storeName, storeFounderId, isActive, storeProducts, purchasePolicies, foundedDate,
         ratingsOfProduct_Id
        * This function adds a store to the store
        * Returns: the id of the store
        """
        if store_name is None:
            raise StoreError('Store name is missing', StoreErrorTypes.invalid_store_name)
        if store_name == "":
            raise StoreError('Store name is an empty string', StoreErrorTypes.invalid_store_name)
        with self.__store_id_lock:
            store = create_store(address, store_name, store_founder_id)
            db.session.add(store)
            db.session.flush()

        logger.info(f'Successfully added store: {store_name}')
        return store.store_id

    def close_store(self, store_id: int, user_id: int) -> None:
        """
        * Parameters: storeId, userId
        * This function closes the store
        * Note: the store verifies whether the userId is the id of the founder, only the founder can close the store
        * Returns: None
        """
        store = self.__get_store_by_id(store_id)
        store.close_store(user_id)
        db.session.flush()

    def open_store(self, store_id: int, user_id: int) -> None:
        """
        * Parameters: storeId, userId
        * This function opens the store
        * Note: the store verifies whether the userId is the id of the founder, only the founder can open the store
        * Returns: None
        """
        store = self.__get_store_by_id(store_id)
        store.open_store(user_id)
        db.session.flush()

    def __store_exists(self, store_id: int) -> bool:
        logger.info('[StoreFacade] checking if store exists')
        return db.session.query(Store).filter(Store.store_id == store_id).first() is not None

    def __get_store_by_id(self, store_id: int) -> Store:
        """
        * Parameters: storeId
        * This function gets a store by its ID
        * Returns: the store with the given ID
        """
        if self.__store_exists(store_id):
            logger.info('[StoreFacade] successfully got store by id')
            return db.session.query(Store).filter(Store.store_id == store_id).first()
        raise StoreError('Store not found', StoreErrorTypes.store_not_found)
        
    #For Testing
    def get_store_by_id(self, store_id: int) -> Store:
        """
        * Parameters: storeId
        * This function gets a store by its ID
        * Returns: the store with the given ID
        """
        return self.__get_store_by_id(store_id)

    # we assume that the marketFacade verified that the user has necessary permissions to add a discount
    def add_discount(self, description: str, store_id: int, start_date: datetime, ending_date: datetime, percentage: float, category_id: Optional[int] = None,
                    product_id: Optional[int] = None, applied_to_sub: Optional[bool] = None) -> int:
        """
        * Parameters: description, startDate, endDate, percentage, categoryId, storeId, productId, appliedToSub
        * This function adds a discount to the store
        * NOTE: the discount starts off with no predicate! if the user wants to add a predicate they must use the assignPredicate function
        * Returns: the integer ID of the discount
        """
        logger.info('[StoreFacade] attempting to add discount to store')
        if not self.__store_exists(store_id):
            logger.warning('[StoreFacade] store the discount is applied to is not found')
            raise DiscountAndConstraintsError('Store is not found', DiscountAndConstraintsErrorTypes.discount_creation_error)
        
        if percentage < 0 or percentage > 1:
            logger.warning('[StoreFacade] percentage is not in the range of 0 to 1')
            raise DiscountAndConstraintsError('Percentage is not in the range of 0 to 1', DiscountAndConstraintsErrorTypes.invalid_percentage)
        
        id = -1

        if category_id is not None:
            if category_id not in self.__categories:
                logger.warning('[StoreFacade] category the discount is applied to is not found')
                raise DiscountAndConstraintsError('Category is not found', DiscountAndConstraintsErrorTypes.discount_creation_error)
            if applied_to_sub is None:
                logger.warning('[StoreFacade] applied to subcategories is missing')
                raise DiscountAndConstraintsError('Applied to subcategories is missing', DiscountAndConstraintsErrorTypes.discount_creation_error)
            logger.info('[StoreFacade] successfully added category discount to store')
            new_category_discount = CategoryDiscount(store_id, description, start_date, ending_date, percentage, None, category_id, applied_to_sub)
            db.session.add(new_category_discount)
            db.session.flush()
            id = new_category_discount.discount_id

        
        elif product_id is not None: 
            if product_id not in self.__get_store_by_id(store_id).store_products:
                logger.warning('[StoreFacade] product the discount is applied to is not found')
                raise DiscountAndConstraintsError('Product is not found', DiscountAndConstraintsErrorTypes.discount_creation_error)
            logger.info('[StoreFacade] successfully added product discount to store')
            new_product_discount = ProductDiscount(description, start_date, ending_date, percentage, None, product_id, store_id)
            db.session.add(new_product_discount)
            db.session.flush()
            id = new_product_discount.discount_id
        else:
            logger.info('[StoreFacade] successfully added store discount to store')
            new_store_discount = StoreDiscount(description, start_date, ending_date, percentage, None, store_id)
            db.session.add(new_store_discount)
            db.session.flush()
            id = new_store_discount.discount_id
        
        db.session.commit()
        return id
    

    def create_logical_composite_discount(self,description: str, store_id: int, start_date: datetime, ending_date: datetime, percentage: float,
                                           discount_id1: int, discount_id2: int, type_of_connection: int) -> int:
        """
        * Parameters: description, startDate, endDate, percentage, discountId1, discountId2, typeOfConnection
        * This function creates a logical composite discount
        *NOTE: type_of_connection: 1-> AND, 2-> OR, 3-> XOR
        * Returns: the integer ID of the discount
        """
        logger.info('[StoreFacade] attempting to create logical composite discount')
        if not self.__store_exists(store_id):
            logger.warning('[StoreFacade] store the discount is applied to is not found')
            raise DiscountAndConstraintsError('Store is not found', DiscountAndConstraintsErrorTypes.discount_creation_error)
        
        discount1 = db.session.query(Discount).filter(Discount.discount_id == discount_id1).first()
        discount2 = db.session.query(Discount).filter(Discount.discount_id == discount_id2).first()

        if discount1 is None or discount2 is None:
            logger.warning('[StoreFacade] one of the discounts is not found')
            raise DiscountAndConstraintsError('One of the discounts is not found', DiscountAndConstraintsErrorTypes.discount_not_found)
        
        if type_of_connection < 1 or type_of_connection > NUMBER_OF_AVAILABLE_LOGICAL_DISCOUNT_TYPES:
            logger.warning('[StoreFacade] type of connection is not valid')
            raise DiscountAndConstraintsError('Type of connection is not valid', DiscountAndConstraintsErrorTypes.invalid_type_of_composite_discount)
        
        id = -1

        if type_of_connection == 1:
            logger.info('[StoreFacade] successfully created AND discount')
            new_and_discount = AndDiscount(store_id, description, start_date, ending_date, percentage, discount1, discount2)
            #removing the sub discounts
            db.session.add(new_and_discount)
            db.session.flush()
            id = new_and_discount.discount_id

        elif type_of_connection == 2:
            logger.info('[StoreFacade] successfully created OR discount')
            new_or_discount = OrDiscount(store_id, description, start_date, ending_date, percentage, discount1, discount2)
            #removing the sub discounts
            db.session.add(new_or_discount)
            db.session.flush()
            id = new_or_discount.discount_id

        else:
            logger.info('[StoreFacade] successfully created XOR discount')
            new_xor_discount = XorDiscount(store_id, description, start_date, ending_date, percentage, discount1, discount2)
            #removing the sub discounts
            db.session.add(new_xor_discount)
            db.session.flush()
            id = new_xor_discount.discount_id

        db.session.commit()
        return id


    
    def create_numerical_composite_discount(self, description: str, store_id: int, start_date: datetime, ending_date: datetime, percentage: float,
                                            discount_ids: List[int], type_of_connection: int) -> int:
        """
        * Parameters: description, startDate, endDate, percentage, discountIds, typeOfConnection
        * This function creates a numerical composite discount
        * NOTE: type_of_connection: 1-> Max, 2-> Additive
        * Returns: the integer ID of the discount
        """
        logger.info('[StoreFacade] attempting to create numerical composite discount')
        
        if not self.__store_exists(store_id):
            logger.warning('[StoreFacade] store the discount is applied to is not found')
            raise DiscountAndConstraintsError('Store is not found', DiscountAndConstraintsErrorTypes.discount_creation_error)
        
        if type_of_connection < 1 or type_of_connection > NUMBER_OF_AVAILABLE_NUMERICAL_DISCOUNT_TYPES:
            logger.warning('[StoreFacade] type of connection is not valid')
            raise DiscountAndConstraintsError('Type of connection is not valid', DiscountAndConstraintsErrorTypes.invalid_type_of_composite_discount)
        
        if len(discount_ids) < 2:
            logger.warning('[StoreFacade] not enough discounts to create a composite discount')
            raise DiscountAndConstraintsError('Not enough discounts to create a composite discount', DiscountAndConstraintsErrorTypes.not_enough_discounts)
        
        discounts = []
        for discount_id in discount_ids:
            discount = db.session.query(Discount).filter(Discount.discount_id == discount_id).first()
            if discount is None:
                logger.warning('[StoreFacade] one of the discounts is not found')
                raise DiscountAndConstraintsError('One of the discounts is not found', DiscountAndConstraintsErrorTypes.discount_not_found)
            discounts.append(discount)
        
        id = 0

        if type_of_connection == 1:
            logger.info('[StoreFacade] successfully created Max discount')
            new_max_discount = MaxDiscount(store_id, description, start_date, ending_date, percentage, discounts)
            
            #removing the sub discounts
            for discount in discounts:
                db.session.delete(discount)
            db.session.add(new_max_discount)
            db.session.flush()
            id = new_max_discount.discount_id

        else:
            logger.info('[StoreFacade] successfully created Additive discount')
            new_additive_discount = AdditiveDiscount(store_id, description, start_date, ending_date, percentage, discounts)

            #removing the sub discounts
            for discount in discounts:
                db.session.delete(discount)
            db.session.add(new_additive_discount)
            db.session.flush()
            id = new_additive_discount.discount_id

        db.session.commit()
        return id
    
    def assign_predicate_helper(self, predicate_properties: Tuple) -> Optional[Constraint]:
        """
        * Parameters: predicate_properties
        * this function recursively creates a predicate for a discount
        * NOTE: the following are examples: (and,  
                                                (age, 18), 
                                                (or 
                                                    (location, {address: "bla", city: "bla", state: "bla", country: "bla", zip_code: "bla"}),
                                                    (time, 10, 00, 20, 00)
                                                ) 
                                            )
        * Returns: the predicated
        """
        if predicate_properties[0] not in self.constraint_types:
            logger.warning(f'[StoreFacade] invalid predicate type: {predicate_properties[0]}')
            raise DiscountAndConstraintsError(f'Invalid predicate type: {predicate_properties[0]}', DiscountAndConstraintsErrorTypes.predicate_creation_error)
        
        predicate_type = self.constraint_types[predicate_properties[0]]
    
        if not isinstance(predicate_type, Constraint):
            logger.warning(f'[StoreFacade] invalid predicate type: {predicate_type}')
            
        if predicate_type == AndConstraint or predicate_type == OrConstraint or predicate_type == XorConstraint or predicate_type == ImpliesConstraint:
            if len(predicate_properties) < 3 and not isinstance(predicate_properties[1], tuple) and not isinstance(predicate_properties[2], tuple):
                logger.warning('[StoreFacade] not enough sub predicates to create a composite predicate')
                raise DiscountAndConstraintsError('Not enough sub predicates to create a composite predicate', DiscountAndConstraintsErrorTypes.predicate_creation_error)
            predicate_left = self.assign_predicate_helper(predicate_properties[1])
            predicate_right = self.assign_predicate_helper(predicate_properties[2])
            return predicate_type(predicate_left, predicate_right)
        
        if predicate_type == AgeConstraint:
            if isinstance(predicate_properties[1], int):
                if predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] age is a negative value')
                    raise DiscountAndConstraintsError('Age is a negative value', DiscountAndConstraintsErrorTypes.invalid_age_limit)
                return predicate_type(predicate_properties[1])
            else:
                logger.warning('[StoreFacade] age is not an integer')
                raise DiscountAndConstraintsError('Age is not an integer', DiscountAndConstraintsErrorTypes.invalid_age_limit)
        elif predicate_type == LocationConstraint:
            if isinstance(predicate_properties[1], Dict):
                if 'address' not in predicate_properties[1] or 'city' not in predicate_properties[1] or 'state' not in predicate_properties[1] or 'country' not in predicate_properties[1] or 'zip_code' not in predicate_properties[1]:
                    logger.warning('[StoreFacade] location is missing fields')
                    raise DiscountAndConstraintsError('Location is missing fields', DiscountAndConstraintsErrorTypes.invalid_location)
                address = AddressDTO(predicate_properties[1]['address'], predicate_properties[1]['city'], predicate_properties[1]['state'], predicate_properties[1]['country'], predicate_properties[1]['zip_code'])
                return predicate_type(address)
            else:
                logger.warning('[StoreFacade] location is not a dictionary')
                raise DiscountAndConstraintsError('Location is not a dictionary', DiscountAndConstraintsErrorTypes.predicate_creation_error)
        elif predicate_type == TimeConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if predicate_properties[1] < 0 or predicate_properties[1] > 23 or predicate_properties[2] < 0 or predicate_properties[2] > 59 or predicate_properties[3] < 0 or predicate_properties[3] > 23 or predicate_properties[4] < 0 or predicate_properties[4] > 59:
                    logger.warning('[StoreFacade] time is not valid')
                    raise DiscountAndConstraintsError('Time is not valid', DiscountAndConstraintsErrorTypes.predicate_creation_error)
                starting_time = time(predicate_properties[1], predicate_properties[2],0)
                ending_time = time(predicate_properties[3], predicate_properties[4],0)
                if starting_time >= ending_time:
                    logger.warning('[StoreFacade] starting time is greater than ending time')
                    raise DiscountAndConstraintsError('Starting time is greater than ending time', DiscountAndConstraintsErrorTypes.invalid_time_constraint)
                return predicate_type(starting_time, ending_time)
            else:
                logger.warning('[StoreFacade] starting time or ending time is not a datetime.time')
                raise DiscountAndConstraintsError('Starting time or ending time is not a datetime.time', DiscountAndConstraintsErrorTypes.invalid_time_constraint)
        elif predicate_type == DayOfMonthConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int):
                if predicate_properties[1] < 1 or predicate_properties[1] > 31 or predicate_properties[2] < 1 or predicate_properties[2] > 31:
                    logger.warning('[StoreFacade] day of month is not valid')
                    raise DiscountAndConstraintsError('Day of month is not valid', DiscountAndConstraintsErrorTypes.invalid_day_of_month)
                return predicate_type(predicate_properties[1], predicate_properties[2])
            else:
                logger.warning('[StoreFacade] day of month is not an integer')
                raise DiscountAndConstraintsError('Day of month is not an integer', DiscountAndConstraintsErrorTypes.invalid_day_of_month)
        elif predicate_type == DayOfWeekConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int):
                if predicate_properties[1] < 1 or predicate_properties[1] > 7 or predicate_properties[2] < 1 or predicate_properties[2] > 7:
                    logger.warning('[StoreFacade] day of week is not valid')
                    raise DiscountAndConstraintsError('Day of week is not valid', DiscountAndConstraintsErrorTypes.invalid_day_of_week)
                return predicate_type(predicate_properties[1], predicate_properties[2])
            else:
                logger.warning('[StoreFacade] day of week is not an integer')
                raise DiscountAndConstraintsError('Day of week is not an integer', DiscountAndConstraintsErrorTypes.invalid_day_of_week)
        elif predicate_type == SeasonConstraint:
            if isinstance(predicate_properties[1], str):
                return predicate_type(predicate_properties[1])
            else:
                logger.warning('[StoreFacade] season is not an integer')
                raise DiscountAndConstraintsError('Season is not an integer', DiscountAndConstraintsErrorTypes.invalid_season)
        elif predicate_type == HolidaysOfCountryConstraint:
            if isinstance(predicate_properties[1], str):
                return predicate_type(predicate_properties[1])
            else:
                logger.warning('[StoreFacade] country is not a string')
                raise DiscountAndConstraintsError('Country is not a string', DiscountAndConstraintsErrorTypes.predicate_creation_error)
        elif predicate_type == PriceCategoryConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if (predicate_properties[1] != -1 and predicate_properties[2] > predicate_properties[1]) or predicate_properties[2] < 0:
                    logger.warning('[StoreFacade] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3])
            else:
                logger.warning('[StoreFacade] min price, max price or category id is not valid')
                raise DiscountAndConstraintsError('Min price, max price or category id is not valid', DiscountAndConstraintsErrorTypes.invalid_price)
        elif predicate_type == PriceProductConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3], predicate_properties[4])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3], predicate_properties[4])
            else:
                logger.warning('[StoreFacade] min price, max price, product id or store id is not valid')
                raise DiscountAndConstraintsError('Min price, max price, product id or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_price)
        elif predicate_type == PriceBasketConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min price is greater than max price')
                    raise DiscountAndConstraintsError('Min price is greater than max price', DiscountAndConstraintsErrorTypes.invalid_price)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3])
            else:
                logger.warning('[StoreFacade] min price, max price or store id is not valid')
                raise DiscountAndConstraintsError('Min price, max price or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_price)
        elif predicate_type == WeightCategoryConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3])
            else:
                logger.warning('[StoreFacade] min weight, max weight or category id is not valid')
                raise DiscountAndConstraintsError('Min weight, max weight or category id is not valid', DiscountAndConstraintsErrorTypes.invalid_weight)
        elif predicate_type == WeightProductConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3], predicate_properties[4])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3], predicate_properties[4])
            else:
                logger.warning('[StoreFacade] min weight, max weight, product id or store id is not valid')
                raise DiscountAndConstraintsError('Min weight, max weight, product id or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_weight)
        elif predicate_type == WeightBasketConstraint:
            if isinstance(predicate_properties[1], float) and isinstance(predicate_properties[2], float) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            elif isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if (predicate_properties[2] != -1 and predicate_properties[1] > predicate_properties[2]) or predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min weight is greater than max weight')
                    raise DiscountAndConstraintsError('Min weight is greater than max weight', DiscountAndConstraintsErrorTypes.invalid_weight)
                return predicate_type(float(predicate_properties[1]), float(predicate_properties[2]), predicate_properties[3])
            else:
                logger.warning('[StoreFacade] min weight, max weight or store id is not valid')
                raise DiscountAndConstraintsError('Min weight, max weight or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_weight)
        elif predicate_type == AmountCategoryConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min amount is a negative value')
                    raise DiscountAndConstraintsError('Min amount is a negative value', DiscountAndConstraintsErrorTypes.invalid_amount)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            else:
                logger.warning('[StoreFacade] min amount or category id is not valid')
                raise DiscountAndConstraintsError('Min amount or category id is not valid', DiscountAndConstraintsErrorTypes.invalid_amount)
        elif predicate_type == AmountProductConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int) and isinstance(predicate_properties[4], int):
                if predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min amount is a negative value')
                    raise DiscountAndConstraintsError('Min amount is a negative value', DiscountAndConstraintsErrorTypes.invalid_amount)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3], predicate_properties[4])
            else:
                logger.warning('[StoreFacade] min amount, product id or store id is not valid')
                raise DiscountAndConstraintsError('Min amount, product id or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_amount)
        elif predicate_type == AmountBasketConstraint:
            if isinstance(predicate_properties[1], int) and isinstance(predicate_properties[2], int) and isinstance(predicate_properties[3], int):
                if predicate_properties[1] < 0:
                    logger.warning('[StoreFacade] min amount is a negative value')
                    raise DiscountAndConstraintsError('Min amount is a negative value', DiscountAndConstraintsErrorTypes.invalid_amount)
                return predicate_type(predicate_properties[1], predicate_properties[2], predicate_properties[3])
            else:
                logger.warning('[StoreFacade] min amount or store id is not valid')
                raise DiscountAndConstraintsError('Min amount or store id is not valid', DiscountAndConstraintsErrorTypes.invalid_amount)
        return None


    def assign_predicate_to_discount(self, discount_id: int, predicate_builder: Tuple) -> None:
        """
        * Parameters: discountId, predicateBuilder
        * This function assigns a predicate to a discount
        * NOTE: for now subdiscounts are inaccessible to be changed
        * NOTE: address would be a dict of address, city, state, country, zip_code
        * NOTE: component_constraint would have two tuples in the second value.
        * Returns: none
        """     

        discount = db.session.query(Discount).filter(Discount.discount_id == discount_id).first()

        if discount is None:
            logger.error('[StoreFacade] discount is not found')
            raise DiscountAndConstraintsError('Discount is not found',DiscountAndConstraintsErrorTypes.discount_not_found)

        if predicate_builder is None:
            logger.error('[StoreFacade] predicate builder is missing')
            raise DiscountAndConstraintsError('Predicate builder is missing',DiscountAndConstraintsErrorTypes.missing_predicate_builder)
        
        predicate = self.assign_predicate_helper(predicate_builder)

        if predicate is None:
            logger.error('[StoreFacade] no valid predicate found')
            raise DiscountAndConstraintsError('No valid predicate found',DiscountAndConstraintsErrorTypes.no_predicate_found)
        
        discount.change_predicate(predicate)

    # we assume that the marketFacade verified that the user has necessary permissions to remove a discount
    def remove_discount(self, discount_id: int) -> None:
        """
        * Parameters: discountId
        * This function removes a discount from the store
        * NOTE: for now subdiscounts are inaccessible to be changed
        * Returns: none
        """
        discount = db.session.query(Discount).filter(Discount.discount_id == discount_id).first()
        if discount is not None:
            logger.info('[StoreFacade] successfully removed discount')
            db.session.delete(discount)
        else:
            logger.error('[StoreFacade] discount is not found')
            raise DiscountAndConstraintsError('Discount is not found',DiscountAndConstraintsErrorTypes.discount_not_found)
        db.session.commit()


    def change_discount_percentage(self, discount_id: int, new_percentage: float) -> None:
        """
        * Parameters: discountId, newPercentage
        * This function changes the percentage of the discount
        * NOTE: for now subdiscounts are inaccessible to be changed
        * Returns: none
        """
        discount = db.session.query(Discount).filter(Discount.discount_id == discount_id).first()
        if discount is None:
            logger.error('[StoreFacade] discount is not found')
            raise DiscountAndConstraintsError('Discount is not found',DiscountAndConstraintsErrorTypes.discount_not_found)
        logger.info('[StoreFacade] successfully changed discount percentage')
        if new_percentage < 0:
            logger.error('[StoreFacade] percentage is negative')
            raise DiscountAndConstraintsError('Percentage is negative',DiscountAndConstraintsErrorTypes.invalid_percentage)
        
        discount.change_discount_percentage(new_percentage)

    def change_discount_description(self, discount_id: int, new_description: str) -> None:
        """
        * Parameters: discountId, newDescription
        * This function changes the description of the discount
        * NOTE: for now subdiscounts are inaccessible to be changed
        * Returns: none
        """
        discount = db.session.query(Discount).filter(Discount.discount_id == discount_id).first()
        if discount is None:
            logger.error('[StoreFacade] discount is not found')
            raise DiscountAndConstraintsError('Discount is not found',DiscountAndConstraintsErrorTypes.discount_not_found)
        logger.info('[StoreFacade] successfully changed discount description')
        discount.change_discount_description(new_description)


    ''' def get_discount_by_store(self, store_id: int) -> List[Discount]:
        # TODO: implement this function
        return []

    def get_discount_by_product(self, product_id: int) -> List[Discount]:
        # TODO: implement this function
        return []

    def get_discount_by_category(self, category_id: int) -> List[Discount]:
        # TODO: implement this function
        return []

    def get_discount_by_discount_id(self, discount_id: int) -> Optional[Discount]:
        # TODO: implement this function
        return None
    '''
    def view_all_discount_information_of_store(self, store_id: int) -> List[dict]:
        """
        * Parameters: none
        * This function is used for converting all the discounts into a List of dictionaries for our frontend to manage the discounts
        * Returns: a list of dictionaries
        """
        discount_info = []
        for discount in db.session.query(Discount).all():
            if discount.store_id == store_id:
                discount_info.append(discount.get_discount_info_as_dict())
        return discount_info


    def get_category_as_dto_for_discount(self, category: Category, shopping_basket: Dict[int,int]) -> CategoryForConstraintDTO:
        """
        * Parameters: category
        * This function creates a category DTO for discounts
        * Returns: the category DTO
        """
        products_dto: List[ProductForConstraintDTO] = []
        for store_id, product_id  in category.category_products:
            if product_id in shopping_basket:
                if not self.__store_exists(store_id):
                    logger.warning('[StoreFacade] store is not found')
                    raise StoreError('Store is not found',StoreErrorTypes.store_not_found)
                if product_id not in self.__get_store_by_id(store_id).store_products:
                    logger.warning('[StoreFacade] product is not found in the store')
                    raise StoreError('Product is not found in the store',StoreErrorTypes.product_not_found)
                
                product = self.__get_store_by_id(store_id).get_product_by_id(product_id)
                
                productDTO = ProductForConstraintDTO(product_id, store_id, product.price, product.weight, shopping_basket[product_id])
                products_dto.append(productDTO)
        
        sub_categories_dto: List[CategoryForConstraintDTO] = []
        for sub_category in category.sub_categories:
            sub_category_dto = self.get_category_as_dto_for_discount(sub_category, shopping_basket)
            sub_categories_dto.append(sub_category_dto)
        
        logger.info('[StoreFacade] successfully created category DTO from category ' + category.category_name + ' for discounts')
        return CategoryForConstraintDTO(category.category_id, category.category_name, category.parent_category_id, sub_categories_dto, products_dto)

    def creating_basket_info_for_constraints(self, store_id: int, total_price_of_basket: float, shopping_basket: Dict[int, int], user_info: UserInformationForConstraintDTO) -> BasketInformationForConstraintDTO:
        """
        * Parameters: storeId, total_price_of_basket, shoppingBasket
        * This function creates the basket information for the constraints
        * Returns: the basket information for the constraints
        """
        
        if not self.__store_exists(store_id):
            logger.error('[StoreFacade] store is not found')
            raise StoreError('Store is not found',StoreErrorTypes.store_not_found)
        
        categories: List[CategoryForConstraintDTO] = []
        for category_id in self.__categories:
            curr_category = self.__categories[category_id]
            curr_category_dto = self.get_category_as_dto_for_discount(curr_category, shopping_basket)
            categories.append(curr_category_dto)
            
        
        products: List[ProductForConstraintDTO] = []
        for product_id in shopping_basket:
            if product_id not in self.__get_store_by_id(store_id).store_products:
                raise StoreError('Product is not found in the store',StoreErrorTypes.product_not_found)
            
            product = self.__get_store_by_id(store_id).get_product_by_id(product_id)
            productDTO = ProductForConstraintDTO(product_id, store_id, product.price, product.weight, shopping_basket[product_id])
            products.append(productDTO)
        
        time_of_purchase = datetime.now()

        return BasketInformationForConstraintDTO(store_id, products, total_price_of_basket, time_of_purchase, user_info, categories)

        
    def apply_discount(self, discount_id: int, store_id: int , total_price_of_basket: float, shopping_basket: Dict[int, int], user_info: UserInformationForConstraintDTO) -> float:
        """
        * Parameters: discountId, shoppingCart
        * This function applies the discount to the shopping basket
        * NOTE: if the discount_id = -1, then no discount is applied
        * Returns: the amount of money saved by the discount
        """
        if discount_id == -1:
            return 0.0
        
        discount = db.session.query(Discount).filter(Discount.discount_id == discount_id).first()
        if discount is None:
            logger.error('[StoreFacade] discount is not found')
            raise DiscountAndConstraintsError('Discount is not found',DiscountAndConstraintsErrorTypes.discount_not_found)
        
        if discount.store_id == store_id:
            basket_info: BasketInformationForConstraintDTO = self.creating_basket_info_for_constraints(store_id, total_price_of_basket, shopping_basket, user_info)

            logger.info('[StoreFacade] successfully applied discount')
            return discount.calculate_discount(basket_info)
        else:
            logger.info(f'[StoreFacade] discount {discount_id} not applied on store {store_id}!')
            return 0.0
    
    def get_total_price_before_discount(self, shopping_cart: Dict[int, Dict[int, int]]) -> float:
        """
        * Parameters: shoppingCart
        * This function calculates the total price of the shopping cart before applying any discounts
        * Returns: the total price of the shopping cart before applying any discounts
        """
        total_price = 0.0
        for store_id, products in shopping_cart.items():
            total_price += self.get_total_basket_price_before_discount(store_id, products)
        return total_price

    def get_total_basket_price_before_discount(self, store_id: int, shopping_cart: Dict[int, int]) -> float:
        """
        * Parameters: storeId, shoppingCart
        * This function calculates the total price of the shopping cart before applying any discounts
        * Returns: the total price of the shopping cart before applying any discounts
        """
        store = self.__get_store_by_id(store_id)
        return store.get_total_price_of_basket_before_discount(shopping_cart)


    def get_total_price_after_discount(self, shopping_cart: Dict[int, Dict[int, int]], user_info: UserInformationForConstraintDTO) -> float:
        """
        * Parameters: discountId, shoppingCart
        * This function calculates the total price of the shopping cart after applying the discount
        * Returns: the total price of the shopping cart after applying the discount
        """
        logger.info('[StoreFacade] attempting to get total price after discount')
        total_price = 0.0
        for store_id, products in shopping_cart.items():
            price_before_discount = self.get_total_basket_price_before_discount(store_id, products)
            discounts = db.session.query(Discount).filter(Discount.store_id == store_id).all()
            for discount in discounts:
                price_before_discount = price_before_discount - self.apply_discount(discount.discount_id, store_id, price_before_discount, products, user_info)
            total_price += price_before_discount
        logger.info('[StoreFacade] successfully calculated total price after discount to be ' + str(total_price))
        return total_price

#--------------------------------------------------
    
    def add_purchase_policy_to_store(self, store_id: int, policy_name: str, category_id: Optional[int] = None, product_id: Optional[int] = None) -> int: 
        """
        * Parameters: store_id, policy_name, category_id(default=None), product_id(default=None)
        * This function adds a purchase policy to the store
        * Returns: the integer ID of the purchase policy
        """
        store = self.__get_store_by_id(store_id)
        if category_id is not None: 
            if category_id not in self.__categories:
                raise StoreError("Category is not found", StoreErrorTypes.category_not_found)
        
        return store.add_purchase_policy(policy_name, category_id, product_id)

    def remove_purchase_policy_from_store(self, store_id: int, policy_id: int) -> None: 
        """
        * Parameters: store_id, policy_name
        * This function removes a purchase policy from the store
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.remove_purchase_policy(policy_id)

    def create_composite_purchase_policy_to_store(self, store_id: int, policy_name: str, policy_id_left: int, policy_id_right: int, type_of_connection: int) -> int:
        """
        * Parameters: store_id, policy_name, policy_id_left, policy_id_right, type_of_connection
        * This function creates a composite purchase policy
        * NOTE: type_of_connection: 1-> AND, 2-> OR, 3-> Conditional
        * Returns: the integer ID of the composite purchase policy
        """
        store = self.__get_store_by_id(store_id)
        return store.create_composite_purchase_policy(policy_name, policy_id_left, policy_id_right, type_of_connection)

    def assign_predicate_to_purchase_policy(self, store_id: int, policy_id: int, predicate_builder: Tuple) -> None:
        """
        * Parameters: store_id, policy_id, predicate
        * This function assigns a predicate to a purchase policy
        * Returns: none
        """
        if not self.__store_exists(store_id):
            logger.error('[StoreFacade] store is not found')
            raise StoreError('Store is not found',StoreErrorTypes.store_not_found)
        
        store = self.__get_store_by_id(store_id)

        if predicate_builder is None:
            logger.error('[StoreFacade] predicate builder is missing')
            raise DiscountAndConstraintsError('Predicate builder is missing',DiscountAndConstraintsErrorTypes.missing_predicate_builder)
        
        predicate = self.assign_predicate_helper(predicate_builder)

        if predicate is None:
            logger.error('[StoreFacade] no valid predicate found')
            raise DiscountAndConstraintsError('No valid predicate found',DiscountAndConstraintsErrorTypes.no_predicate_found)
        
        store.assign_predicate_to_purchase_policy(policy_id,predicate)
        

    def validate_purchase_policy(self, store_id: int, total_price_of_basket: float, shopping_basket: Dict[int, int], user_info: UserInformationForConstraintDTO) -> bool:
        """
        * Parameters: store_id, total_price_of_basket, shoppingBasket, user_info
        * This function validates the purchase policies of the stores
        * Returns: True if the purchase policies are satisfied
        """
        if not self.__store_exists(store_id):
            logger.error('[StoreFacade] store is not found')
            raise StoreError('Store is not found',StoreErrorTypes.store_not_found)
        
        store = self.__get_store_by_id(store_id)

        basket_info: BasketInformationForConstraintDTO = self.creating_basket_info_for_constraints(store_id, total_price_of_basket, shopping_basket, user_info)

        logger.info('[StoreFacade] successfully applied discount')
        return store.check_purchase_policies_of_store(basket_info)
            
    def view_all_purchase_policies_of_store(self, store_id: int) -> List[dict]:
        """
        * Parameters: store_id
        * This function returns all the purchase policies of the store
        * Returns: the list of purchase policies
        """
        store = self.__get_store_by_id(store_id)
        return store.view_all_purchase_policies()
    

    def validate_purchase_policies(self, shopping_cart: Dict[int, Dict[int, int]], user_info: UserInformationForConstraintDTO) -> bool:
        """
        * Parameters: store_id, total_price_of_basket, shoppingBasket, user_info
        * This function validates the purchase policies of the stores
        * Returns: True if the purchase policies are satisfied
        """
        total_price = 0.0
        for store_id, products in shopping_cart.items():
            price_of_purchase = self.get_total_basket_price_before_discount(store_id, products)
            if not self.validate_purchase_policy(store_id, price_of_purchase, products, user_info):
                return False
        return True    

#-------------------------------------------------------------

    def get_store_product_information(self, user_id: int, store_id: int) -> List[ProductDTO]:
        """
        * Parameters: storeId
        * This function returns the store information as a string
        * Returns: the store information as a string
        """
        store = self.__get_store_by_id(store_id)
        return store.create_store_dto().products

    def __acquire_store_locks(self, store_ids: List[int]) -> None:
        """
        * Parameters: storeIds
        * This function acquires locks for the given stores
        * Returns: none
        """
        # sort the store ids to avoid deadlock
        store_ids.sort()
        acquired = []
        try:
            for store_id in store_ids:
                store = self.__get_store_by_id(store_id)
                store.acquire_lock()
                acquired.append(store_id)
        except Exception as e:
            self.__release_store_locks(acquired)
            raise e

    def __release_store_locks(self, store_ids: List[int]) -> None:
        """
        * Parameters: storeIds
        * This function releases locks for the given stores
        * Returns: none
        """
        # sort the store ids to avoid deadlock
        store_ids.sort()
        for store_id in store_ids:
            store = self.__get_store_by_id(store_id)
            store.release_lock()

    def check_and_remove_shopping_cart(self, shopping_cart: Dict[int, Dict[int, int]]) -> None:
        """
        * Parameters: shoppingCart
        * This function checks if the store has the given amount of the products in the shopping cart and removes them
        * Returns: none
        """
        self.__acquire_store_locks(list(shopping_cart.keys()))
        try:
            for store_id, products in shopping_cart.items():
                store = self.__get_store_by_id(store_id)
                if not store.is_active:
                    raise StoreError('Store is not active', StoreErrorTypes.store_not_active)
                for product_id, amount in products.items():
                    if not store.has_amount_of_product(product_id, amount):
                        self.__release_store_locks(list(shopping_cart.keys()))
                        raise StoreError('Store does not have the given amount of the product', StoreErrorTypes.product_not_available)

            for store_id, products in shopping_cart.items():
                for product_id, amount in products.items():
                    self.remove_product_amount(store_id, product_id, amount)
            db.session.flush()
            self.__release_store_locks(list(shopping_cart.keys()))
        except Exception as e:
            self.__release_store_locks(list(shopping_cart.keys()))
            raise e

    def get_purchase_shopping_cart(self, user_info: UserInformationForConstraintDTO, shopping_cart: Dict[int, Dict[int, int]]) \
            -> Dict[int, Tuple[List[PurchaseProductDTO], float, float]]:
        purchase_shopping_cart: Dict[int, Tuple[List[PurchaseProductDTO], float, float]] = {}

        for store_id, products in shopping_cart.items():
            purchase_products: List[PurchaseProductDTO] = []
            store = self.__get_store_by_id(store_id)

            for product_id in products:
                product = store.get_product_by_id(product_id)
                amount = products[product_id]
                name = product.product_name
                description = product.description
                price = product.price
                purchase_products.append(PurchaseProductDTO(product_id, name, description, price, amount))

            basket_price_before_discount = store.get_total_price_of_basket_before_discount(products)
            temp_price = basket_price_before_discount
            for discount in db.session.query(Discount).filter(Discount.store_id == store_id).all():
                temp_price = temp_price - self.apply_discount(discount.discount_id, store_id, temp_price, products, user_info)
            basket_price_after_discount = temp_price
            purchase_shopping_cart[store_id] = (purchase_products,
                                                basket_price_before_discount,
                                                basket_price_after_discount)
        return purchase_shopping_cart

    # --------------------methods for market facade used by users team---------------------------#

    def check_product_availability(self, store_id: int, product_id: int, amount: int) -> bool:
        """
        * Parameters: store_id, product_id, amount
        * This function checks if the product is available in the store with the specified amount
        * Returns: True if the product is available, false otherwise
        """
        store = self.__get_store_by_id(store_id)
        return store.has_amount_of_product(product_id, amount)

    def get_store_info(self, store_id: int) -> StoreDTO:
        """
        * Parameters: store_id
        * This function gets the store information
        * Returns: the store information
        """
        store = self.__get_store_by_id(store_id)
        return store.create_store_dto()

    def search_by_category(self, category_id: int, store_id: Optional[int]=None) -> Dict[int, List[ProductDTO]]:
        """
        * Parameters: category_id, store_id(default=None)
        * This function searches for products by category
        * Returns: a dict from store_id to a list of productDTOs
        """
        products: Dict[int, List[ProductDTO]] = {}
        if store_id is not None:
            store = self.__get_store_by_id(store_id)
            for (curr_store_id, product_id) in self.get_category_by_id(category_id).get_all_products_recursively():
                if store_id == curr_store_id:
                    product = store.get_product_dto_by_id(product_id)
                    if store_id not in products:
                        products[store_id] = []
                    products[store_id].append(product)
        else:
            for (store_id, product_id) in self.get_category_by_id(category_id).get_all_products_recursively():
                if store_id not in products:
                    products[store_id] = []
                store = self.__get_store_by_id(store_id)
                product = store.get_product_dto_by_id(product_id)
                products[store_id].append(product)
        return products
        
    def search_by_tags(self, tags: List[str], store_id: Optional[int]=None) -> Dict[int, List[ProductDTO]]:
        """
        * Parameters: tags, store_id(default=None)
        * This function searches for products by tags
        * Returns: a dict from store_id to a list of productDTOs
        """
        products: Dict[int, List[ProductDTO]] = {}
        if store_id is not None:
            store = self.__get_store_by_id(store_id)
            for product_id in store.store_products:
                product = store.get_product_dto_by_id(product_id)
                if all(tag in product.tags for tag in tags):
                    if store_id not in products:
                        products[store_id] = []
                    products[store_id].append(product)
        else:
            for store in db.session.query(Store).all():
                for product_id in store.store_products:
                    product = store.get_product_dto_by_id(product_id)
                    if all(tag in product.tags for tag in tags):
                        if store.store_id not in products:
                            products[store.store_id] = []
                        products[store.store_id].append(product)
        return products

    def search_by_name(self, product_name: str, store_id: Optional[int]=None) -> Dict[int, List[ProductDTO]]:
        """
        * Parameters: product_name, store_id(default=None)
        * This function searches for products by name
        * Returns: a dict from store_id to a list of productDTOs
        """
        products: Dict[int, List[ProductDTO]] = {}
        if store_id is not None:
            store = self.__get_store_by_id(store_id)
            for product_id in store.store_products:
                product = store.get_product_dto_by_id(product_id)
                if product.name == product_name:
                    if store_id not in products:
                        products[store_id] = []
                    products[store_id].append(product)
        else:
            for store in db.session.query(Store).all():
                for product_id in store.store_products:
                    product = store.get_product_dto_by_id(product_id)
                    if product.name == product_name:
                        if store.store_id not in products:
                            products[store.store_id] = []
                        products[store.store_id].append(product)
        return products

    def get_stores(self, page: int, limit: int) -> Dict[int, StoreDTO]:
        start = (page - 1) * limit
        end = start + limit
        stores = {}
        store_keys = [store.store_id for store in db.session.query(Store).all()]
        store_keys.sort()
        store_keys = store_keys[start:end]
        for store_id in store_keys:
            store = self.__get_store_by_id(store_id)
            stores[store_id] = store.create_store_dto()

        return stores
    
    def get_all_tags(self) -> List[str]:
        """
        * This function gets all the tags in the system
        * Returns: a list of tags
        """
        return list(self.__tags)
    
    def get_all_store_names(self) -> Dict[int, str]:
        """
        * This function gets all the store names in the system
        * Returns: a dict from store_id to store_name
        """
        return {store.store_id: store.store_name for store in db.session.query(Store).all()}
    
    def get_all_categories(self) -> Dict[int, CategoryDTO]:
        """
        * This function gets all the category names in the system
        * Returns: a dict from category_id to category_name
        """
        return {category_id: category.get_category_dto() for category_id, category in self.__categories.items()}
    
    def edit_product_in_store(self, store_id: int, product_id: int, product_name: str, description: str, price: float, weight: float, tags: List[str],
                              amount: Optional[int]) -> None:
        """
        * Parameters: store_id, product_id, product_name, description, price, weight, tags
        * This function edits a product in the store
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.edit_product(product_id, product_name, description, price, tags, weight, amount)
        db.session.flush()

    def validate_cart(self, cart: Dict[int, Dict[int, int]]) -> None:
        """
        * Parameters: cart
        * This function validates the shopping cart
        * Returns: none
        """
        for store_id, products in cart.items():
            for product_id, amount in products.items():
                logger.info('[StoreFacade] checking product availability')
                logger.info(f'types are: {type(product_id)}, { type(amount)}, {type(store_id)}')
                existing_amount = self.__get_store_by_id(store_id).get_product_dto_by_id(product_id).amount
                if amount > existing_amount:
                    raise StoreError('Product amount is greater than the existing amount', StoreErrorTypes.product_not_available)
        
    def is_store_closed(self, store_id: int) -> bool:
        """
        * Parameters: storeId
        * This function checks if the store is closed
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        return not store.is_active

    def get_open_stores(self, user_id: int, store_ids: List[int]) -> List[int]:
        """
        * Parameters: storeIds
        * This function gets a list of stores and returns the open stores or the stores which are found by the user
        * Returns: a list of store ids which are open or found by the user
        """
        open_stores = []
        for store_id in store_ids:
            store = self.__get_store_by_id(store_id)
            if store.is_active or store.store_founder_id == user_id:
                open_stores.append(store_id)
        return open_stores
    
    def get_product_categories(self, store_id: int, product_id: int) -> Dict[int, CategoryDTO]:
        """
        * Parameters: storeId, productId
        * This function gets the categories of the product
        * Returns: a dict from category_id to category_name
        """
        categories = self.__categories
        product_categories = {}
        for category_id, category in categories.items():
            if (store_id, product_id) in category.category_products:
                product_categories[category_id] = category.get_category_dto()
        return product_categories
    
    def get_all_stores(self)-> Dict[int, StoreDTO]:
        """
        * Parameters: none
        * This function gets all the stores in the system
        * Returns: a dict from store_id to storeDTO
        """
        return {store.store_id: store.create_store_dto() for store in db.session.query(Store).all()}

    def get_store_id(self, store_name):
        for store in db.session.query(Store).all():
            if store.store_name == store_name:
                return store.store_id
        raise StoreError('Store not found', StoreErrorTypes.store_not_found)
