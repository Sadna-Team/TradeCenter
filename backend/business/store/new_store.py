# ---------- Imports ------------#
from typing import List, Dict, Tuple, Optional, Callable
from .DiscountStrategy import DiscountStrategy
from .PurchasePolicyStrategy import PurchasePolicyStrategy
from datetime import datetime
from backend.business.DTOs import ProductDTO, StoreDTO, PurchaseProductDTO, PurchaseUserDTO
from backend.business.store.strategies import PurchaseComposite, AndFilter, OrFilter, XorFilter, UserFilter, ProductFilter, NotFilter
import threading
# -------------logging configuration----------------
import logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                     format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("New Store Logger")

# ---------------------------------------------------

# ---------------------product class---------------------#
class Product:
    # id of product is productId. It is unique for each physical product
    def __init__(self, product_id: int, product_name: str, description: str, price: float, weight: float, amount: int=0):
        self.__product_id: int = product_id
        self.__product_name: str = product_name
        self.__description: str = description
        self.__tags: List[str] = []  # initialized with no tags
        self.__price: float = price  # price is in dollars
        self.__weight: float = weight  # weight is in kg
        self.__amount: int = amount  # amount of the product in the store
        self.__product_lock = threading.Lock() # lock for product
        logger.info('[Product] successfully created product with id: ' + str(product_id))

    # ---------------------getters and setters---------------------
    @property
    def product_id(self) -> int:
        return self.__product_id

    @property
    def product_name(self) -> str:
        return self.__product_name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def tags(self) -> List[str]:
        return self.__tags

    @property
    def price(self) -> float:
        return self.__price

    @property
    def weight(self) -> float:
        return self.__weight
    
    @property
    def amount(self) -> int:
        return self.__amount
    
    # ---------------------methods--------------------------------
    def create_product_dto(self) -> ProductDTO:
        """
        * Parameters: none
        * This function creates a product DTO from the product
        * Returns: the product DTO
        """
        return ProductDTO(self.__product_id, self.__product_name, self.__description, self.__price, self.__tags, weight=self.__weight, amount=self.__amount)

    def aquire_lock(self):
        self.__product_lock.acquire()

    def release_lock(self):
        self.__product_lock.release()

    def change_price(self, new_price: float) -> None:
        """
        * Parameters: newPrice
        * This function changes the price of the product
        * Returns: True if the price is changed successfully
        """
        if new_price < 0:
            raise ValueError('New price is a negative value')
        with self.__product_lock:
            self.__price = new_price
        logger.info('[Product] successfully changed price of product with id: ' + str(self.__product_id))

    def change_description(self, new_description: str) -> None:
        """
        * Parameters: new_description
        * This function changes the description of the product 
        * Returns: none
        """
        if new_description is None:
            raise ValueError('New description is not a valid string')
        with self.__product_lock:
            self.__description = new_description
        logger.info(
            '[Product] successfully changed description of product with id: ' + str(self.__product_id))


    def add_tag(self, tag: str) -> None:
        """
        * Parameters: tag
        * This function adds a tag to the product 
        * Returns: true if successfully added tag
        """
        if tag is None:
            raise ValueError('Tag is not a valid string')
        if tag in self.__tags:
            raise ValueError('Tag is already in the list of tags')
        with self.__product_lock:
            self.__tags.append(tag)
        logger.info('[Product] successfully added tag to product with id: ' + str(self.__product_id))


    def remove_tag(self, tag: str) -> None:
        """
        * Parameters: tag
        * This function removes a tag from the product 
        * Returns: none
        """
        if tag is None:
            raise ValueError('Tag is not a valid string')
        if tag not in self.__tags:
            raise ValueError('Tag is not in the list of tags')
        with self.__product_lock:
            self.__tags.remove(tag)
        logger.info(
            '[Product] successfully removed tag from product with id: ' + str(self.__product_id))



    def has_tag(self, tag: str) -> bool:
        """
        * Parameters: tag
        * This function checks if the product has a given tag
        * Returns: true if the product has the given tag
        """
        with self.__product_lock:
            return tag in self.__tags

    def change_weight(self, new_weight: float) -> None:
        """
        * Parameters: newWeight
        * This function changes the weight of the product
        * Returns: none
        """
        if new_weight < 0:
            raise ValueError('New weight is a negative value')
        with self.__product_lock:
            self.__weight = new_weight
        logger.info('[Product] successfully changed weight of product with id: ' + str(self.__product_id))


    def restock(self, amount) -> None:
        if amount < 0:
            raise ValueError('Amount is a negative value')
        with self.__product_lock:
            self.__amount += amount

    def remove_amount(self, amount) -> None:
        if self.__amount < amount:
            raise ValueError('Amount is greater than the available amount of the product')
        with self.__product_lock:
            self.__amount -= amount

# ---------------------category class---------------------#
class Category:
    # id of category is categoryId. It is unique for each category. Products are stored in either the category or found
    # in one of its subcategories
    # important to note: a category can only have one parent category, and a category can't have a subcategory that is
    # already a subcategory of a subcategory.

    def __init__(self, category_id: int, category_name: str):
        self.__category_id: int = category_id
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
    def aquire_lock(self):
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
            raise ValueError('Category already has a parent category')
        self.__parent_category_id = parent_category_id
        logger.info('[Category] successfully added parent category to category with id: ' + str(self.__category_id))


    def remove_parent_category(self) -> None:
        """
        * Parameters: none
        * This function removes the parent category of the category
        * Returns: none
        """
        if self.__parent_category_id == -1:
            raise ValueError('Category does not have a parent category')    
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
            raise ValueError('Sub category is not a valid category')
        elif self.is_sub_category(sub_category):
            raise ValueError('Sub category is already a sub category of the current category')
        elif sub_category.has_parent_category():
            raise ValueError('Sub category already has a parent category')
        elif sub_category.__category_id == self.__category_id:
            raise ValueError('Sub category cannot be the same as the current category')
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
            raise ValueError('Sub category is not a valid category')
        elif sub_category not in self.__sub_categories:
            raise ValueError('Sub category is not in the list of sub categories')
        elif not sub_category.is_parent_category(self.__category_id):
            raise ValueError('Sub category is not a sub category of the current category')
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
                raise ValueError('Product is already in the list of products')
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
                raise ValueError('Product is not in the list of products')
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


def pred_no_alcohol_past_time(products: Dict[ProductDTO, int]) -> bool:
    """
        * Parameters: store_id, product_id, time
        * This function checks if the product is an alcohol product and if the time is after the time of the purchase
        * Returns: True if the product is an alcohol product and the time is after the time of the purchase, False otherwise
    """
    for product in products:
        if 'alcohol' in product.tags and datetime.now().hour > 22:
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
            return True
    return False

def pred_not_too_much_gun_powder(products: Dict[ProductDTO, int]) -> bool:
    """
    * Parameters: products
    * This function checks if the products contain too much gun powder
    * Returns: True if the products contain too much gun powder, False otherwise
    """
    for product in products:
        if 'gunpowder' in product.tags:
            return  product.weight * products[product] >= 100
    return False

def pred_has_tabbaco(products: Dict[ProductDTO, int]) -> bool:
    """
    * Parameters: products
    * This function checks if the products contain tabbaco
    * Returns: True if the products contain tabbaco, False otherwise
    """
    for product in products:
        if 'tabbaco' in product.tags:
            return True
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

class Store:
    # id of store is storeId. It is unique for each store
    def __init__(self, store_id: int, location_id: int, store_name: str, store_founder_id: int):
        self.__store_id = store_id
        self.__location_id = location_id
        self.__store_name = store_name
        self.__store_founder_id = store_founder_id
        self.__is_active = True
        self.__store_products: Dict[int, Product] = {}
        self.__product_id_counter = 0  # product Id
        self.__product_id_lock = threading.Lock() # lock for product id
        self.__purchase_policy: Dict[str, Callable[[Dict[ProductDTO, int], PurchaseUserDTO], PurchaseComposite]] = {} # purchase policy
        self.__founded_date = datetime.now()
        self.__purchase_policy_id_counter = 0  # purchase policy Id
        self.__checkout_lock = threading.Lock() # lock for checkout
        logger.info('[Store] successfully created store with id: ' + str(store_id))

    # ---------------------getters and setters---------------------#
    @property
    def store_id(self) -> int:
        return self.__store_id

    @property
    def location_id(self) -> int:
        return self.__location_id

    @property
    def store_name(self) -> str:
        return self.__store_name

    @property
    def store_founder_id(self) -> int:
        return self.__store_founder_id

    @property
    def is_active(self) -> bool:
        return self.__is_active

    @property
    def store_products(self) -> List[int]:
        return list(self.__store_products.keys())

    @property
    def founded_date(self) -> datetime:
        return self.__founded_date

    @property
    def purchase_policy(self) -> List[str]:
        return list(self.__purchase_policy.keys())
    # ---------------------methods--------------------------------
    def close_store(self, user_id: int) -> None:
        """
        * Parameters: userId
        * This function closes the store
        * Returns: none
        """
        if user_id == self.__store_founder_id:
            with self.__checkout_lock:
                self.__is_active = False
                logger.info('[Store] successfully closed store with id: ' + str(self.__store_id))
        else:
            raise ValueError('User is not the founder of the store')
        
    def aquire_lock(self):
        self.__checkout_lock.acquire()

    def release_lock(self):
        self.__checkout_lock.release()

    # We assume that the marketFacade verified that the user attempting to add the product is a store Owner
    def add_product(self, name: str, description: str, price: float, tags: List[str], weight: float, amount: int = 0) -> int:
        """
        * Parameters: name, description, price, tags, amount
        * This function adds a product to the store
        * Returns: none
        """
        with self.__product_id_lock:
            product = Product(self.__product_id_counter, name, description, price, weight, amount)
            for tag in tags:
                product.add_tag(tag)
            self.__store_products[self.__product_id_counter] = product
            self.__product_id_counter += 1
        logger.info('[Store] successfully added product to store with id: ' + str(self.__store_id))
        return product.product_id

    # We assume that the marketFacade verified that the user attempting to remove the product is a store owner/purchased
    def remove_product(self, product_id: int) -> None:
        """
        * Parameters: productId
        * This function removes a product from the store
        * Returns: none
        """
        try:
            self.__store_products.pop(product_id)
            logger.info('Successfully removed product from store with id: {self.__store_id}')
        except KeyError:
            raise ValueError('Product is not found')

    def get_product_by_id(self, product_id: int) -> Product:
        """
        * Parameters: productId
        * This function gets a product by its ID
        * Returns: the product with the given ID
        """
        try:
            return self.__store_products[product_id]
        except KeyError:
            raise ValueError('Product is not found')

    def get_product_dto_by_id(self, product_id: int) -> ProductDTO:
        """
        * Parameters: productId
        * This function gets a product DTO by its ID
        * Returns: the product DTO with the given ID
        """
        return self.get_product_by_id(product_id).create_product_dto()
        
    def add_purchase_policy(self, policy_name: str) -> None:
        """
        * Parameters: policyName
        * This function adds a purchase policy to the store
        * Returns: none
        """
        if policy_name in AVAILABLE_POLICIES:
            self.__purchase_policy[policy_name] = AVAILABLE_POLICIES[policy_name]
            logger.info('[Store] successfully added purchase policy to store with id: ' + str(self.__store_id))
        else:
            raise ValueError('Policy name is not valid')

    def remove_purchase_policy(self, policy_name: str) -> None:
        if policy_name in self.__purchase_policy:
            self.__purchase_policy.pop(policy_name)
            logger.info('[Store] successfully removed purchase policy from store with id: ' + str(self.__store_id))
        else:
            raise ValueError('Policy name is not found')

    def check_purchase_policy(self, products: Dict[ProductDTO, int], user: PurchaseUserDTO) -> None:
        """
        * Parameters: products, user
        * This function checks if the purchase policy is satisfied
        * Returns: true if the purchase policy is satisfied
        """
        for policy in self.__purchase_policy.values():
            if not policy(products, user).pass_filter():
                raise ValueError(f'Purchase policy of store: {self.__store_name} is not satisfied!')
    
    def aquire_products_lock(self, product_ids: List[int]) -> None:
        """
        * Parameters: productIds
        * This function acquires the lock of the products
        * Returns: none
        """
        # sort the product ids to avoid deadlocks
        product_ids.sort()
        for product_id in product_ids:
            self.get_product_by_id(product_id).aquire_lock()

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
        self.aquire_products_lock(list(basket.keys()))
        for product_id, amount in basket.items():
            product = self.get_product_by_id(product_id)
            if product is not None:
                total_price += product.price * amount
            else:
                self.release_products_lock(list(basket.keys()))
                raise ValueError('Product is not found')
        self.release_products_lock(list(basket.keys()))
        return total_price

    def get_total_price_of_basket_after_discount(self, basket: Dict[int, int]) -> float:
        # TODO: implement this function
        pass

    def create_store_dto(self) -> StoreDTO:
        """
        * Parameters: none
        * This function creates a store DTO from the store
        * Returns: the store DTO
        """
        store_dto = StoreDTO(self.__store_id, self.__location_id, self.__store_name, self.__store_founder_id,
                             self.__is_active, self.__founded_date)
        product_dtos = [product.create_product_dto() for product in self.__store_products.values()]
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
        if product_id in self.__store_products:
            self.__store_products[product_id].restock(amount)
            logger.info('[Store] successfully restocked product with id: ' + str(product_id))
        else:
            raise ValueError('Product is not found')

    def remove_product_amount(self, product_id: int, amount: int) -> None:
        """
        * Parameters: productId, amount
        * This function removes a product from the store
        * Returns: none
        """
        if product_id not in self.__store_products:
            raise ValueError('Product is not found')
        if self.__store_products[product_id].amount < amount:
            raise ValueError('Amount is greater than the available amount of the product')
        self.__store_products[product_id].remove_amount(amount)
        logger.info('Successfully removed product amount with id: {product_id}')

    def change_description_of_product(self, product_id: int, new_description: str) -> None:
        """
        * Parameters: productId, newDescription
        * This function changes the description of the product
        * Returns: none
        """
        product = self.get_product_by_id(product_id)
        if product is not None:
            product.change_description(new_description)
            logger.info('Successfully changed description of product with id: {product_id}')
        else:
            raise ValueError('Product is not found')

    def change_price_of_product(self, product_id: int, new_price: float) -> None:
        """
        * Parameters: productId, newPrice
        * This function changes the price of the product
        * Returns: none
        """
        product = self.get_product_by_id(product_id)
        if product is not None:
            product.change_price(new_price)
            logger.info('Successfully changed price of product with id: {product_id} to {new_price}')
        else:
            raise ValueError('Product is not found')

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
            raise ValueError('Product is not found')

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
            raise ValueError('Product is not found')

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
            raise ValueError('Product is not found')

    def has_amount_of_product(self, product_id: int, amount: int) -> bool:
        """
        * Parameters: productId, amount
        * This function checks if the store has the given amount of the product
        * Returns: true if the store has the given amount of the product
        """
        if product_id in self.__store_products:
            self.__store_products[product_id].aquire_lock()
            ans =  self.__store_products[product_id].amount >= amount
            self.__store_products[product_id].release_lock()
            return ans
        return False

    def change_weight_of_product(self, product_id: int, new_weight: float) -> None:
        """
        * Parameters: productId, newWeight
        * This function changes the weight of the product
        * Returns: none
        """
        product = self.get_product_by_id(product_id)
        product.change_weight(new_weight)
# ---------------------end of classes---------------------#

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
            self.__stores: Dict[int, Store] = {}  # store_id: Store
            self.__discounts: List[DiscountStrategy] = []  # List to store discounts
            self.__category_id_counter = 0  # Counter for category IDs
            self.__category_id_lock = threading.Lock() # lock for category id
            self.__store_id_counter = 0  # Counter for store IDs
            self.__store_id_lock = threading.Lock() # lock for store id
            self.__discount_id_counter = 0  # Counter for discount IDs
            logger.info('successfully created storeFacade')

    def clean_data(self):
        """
        For testing purposes only
        """
        self.__categories = {}
        self.__stores = {}
        self.__discounts = []
        self.__category_id_counter = 0
        self.__store_id_counter = 0
        self.__discount_id_counter = 0

    # ---------------------getters and setters---------------------
    @property
    def categories(self) -> List[int]:
        return list(self.__categories.keys())

    @property
    def discounts(self) -> List[DiscountStrategy]:
        return self.__discounts

    @property
    def stores(self) -> List[int]:
        return list(self.__stores.keys())

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
            raise ValueError('Category is not found')

    def add_category(self, category_name: str) -> int:
        """
        * Parameters: categoryName, parentCategoryId
        * This function adds a category to the store
        * Returns: none
        """
        if category_name is not None:
            with self.__category_id_lock:
                category = Category(self.__category_id_counter, category_name)
                self.__categories[self.__category_id_counter] = category
                self.__category_id_counter += 1
            logger.info(f'[StoreFacade] successfully added category: {category_name}')
            return category.category_id
        else:
            raise ValueError('Category name is not a valid string')

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
                             tags: Optional[List[str]]=[], amount: Optional[int]=0) -> int:
        """
        * Parameters: productName, weight, description, tags, manufacturer, storeIds
        * This function adds a product to the store
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)

        if product_name is None or product_name == "":
            raise ValueError('Product name missing / empty')
        if description is None:
            raise ValueError('Description is missing')
        if price < 0:
            raise ValueError('Price is a negative value')
        logger.info(f'Successfully added product: {product_name} to store with the id: {store_id}')
        return store.add_product(product_name, description, price, tags, weight)

    def remove_product_from_store(self, store_id: int, product_id: int) -> None:
        """
        * Parameters: store_id, product_id
        * This function removes a product from the store
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.aquire_lock()
        store.remove_product(product_id)
        store.release_lock()

    def add_product_amount(self, store_id: int, product_id: int, amount: int) -> None:
        """
        * Parameters: store_id, product_id, amount, condition
        * This function adds a product to the store
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.aquire_lock()
        store.restock_product(product_id, amount)
        store.release_lock()
        logger.info(f'Successfully added {amount} of product with id: {product_id} to store with id: {store_id}')

    def remove_product_amount(self, store_id: int, product_id: int, amount: int) -> None:
        """
        * Parameters: store_id, product_id, amount, condition
        * This function removes a product from the store
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.remove_product_amount(product_id, amount)

    def change_description_of_product(self, store_id: int, product_id: int, new_description: str) -> None:
        """
        * Parameters: store_id, product_id, new_description
        * This function changes the description of the product
        * Returns: None
        """
        store = self.__get_store_by_id(store_id)
        store.change_description_of_product(product_id, new_description)

    def change_price_of_product(self, store_id: int, product_id: int, new_price: float) -> None:
        """
        * Parameters: store_id, product_id, new_price
        * This function changes the price of the product
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.change_price_of_product(product_id, new_price)

    def change_weight_of_product(self, store_id: int, product_id: int, new_weight: float) -> None:
        """
        * Parameters: store_id, product_id, new_weight
        * This function changes the weight of the product
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.change_weight_of_product(product_id, new_weight)

    def add_tag_to_product(self, store_id: int, product_id: int, tag: str) -> None:
        """
        * Parameters: store_id, product_id, tag
        * This function adds a tag to the product
        * Returns: None
        """
        store = self.__get_store_by_id(store_id)
        store.add_tag_to_product(product_id, tag)

    def remove_tag_from_product(self, store_id: int, product_id: int, tag: str) -> None:
        """
        * Parameters: store_id, product_id, tag
        * This function removes a tag from the product
        * Returns: None
        """
        store = self.__get_store_by_id(store_id)
        if store is None:
            raise ValueError('Store is not found')
        store.remove_tag_from_product(product_id, tag)

    def get_tags_of_product(self, store_id: int, product_id: int) -> List[str]:
        """
        * Parameters: product_id
        * This function gets all the tags of a product 
        * Returns: all the tags of the product 
        """
        store = self.__get_store_by_id(store_id)
        return store.get_tags_of_product(product_id)

    def add_store(self, location_id: int, store_name: str, store_founder_id: int) -> int:
        """
        * Parameters: locationId, storeName, storeFounderId, isActive, storeProducts, purchasePolicies, foundedDate,
         ratingsOfProduct_Id
        * This function adds a store to the store
        * Returns: None
        """
        if store_name is None:
            raise ValueError('Store name is missing')
        if store_name == "":
            raise ValueError('Store name is an empty string')
        with self.__store_id_lock:
            store = Store(self.__store_id_counter, location_id, store_name, store_founder_id)
            self.__stores[self.__store_id_counter] = store
            print(self.__stores)
            self.__store_id_counter += 1
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

    def __get_store_by_id(self, store_id: int) -> Store:
        """
        * Parameters: storeId
        * This function gets a store by its ID
        * Returns: the store with the given ID
        """
        if store_id in self.__stores:
            return self.__stores[store_id]
        raise ValueError('Store not found')
    
    ''' def add_purchase_policy_to_store(self, store_id: int) -> None:
        # TODO: for now we dont know how to implement the purchasePolicy and what fields it receives
        """
        * Parameters: storeId, purchasePolicy
        * This function adds a purchase policy to the store
        * Note: the marketFacade is responsible for verifying whether the purchase policy is added by someone with the
        necessary permissions.
        * Returns: True if the purchase policy is added successfully
        """
        logger.info('[StoreFacade] attempting to add purchase policy to store')
        if store_id is not None:
            # if purchasePolicy is not None:
            store = self.get_store_by_id(store_id)
            if store is not None:
                return store.add_purchase_policy()
            else:
                raise ValueError('Store not found')'''

    def update_purchase_policy_of_store(self, store_id: int, purchase_policy_id: int) -> None:
        # TODO: implement this function
        pass

    def check_policies_of_store(self, store_id: int, basket: List[int]) -> bool:
        # TODO: implement this function
        pass

    # we assume that the marketFacade verified that the user has necessary permissions to add a discount
    '''def add_discount(self, description: str, start_date: datetime, ending_date: datetime, percentage: float) -> None:
        """
        * Parameters: description, startDate, endingDate, percentage
        * This function adds a discount to the store
        * Returns: None
        """
        logger.info('[StoreFacade] attempting to add discount')
        if description is not None:
            if start_date is not None:
                if ending_date is not None:
                    if ending_date > start_date:
                        if percentage is not None:
                            if 0.0 <= percentage <= 1.0:
                                discount = DiscountStrategy(self.__discount_id_counter, description, start_date,
                                                            ending_date, percentage)
                                self.__discounts.append(discount)
                                self.__discount_id_counter += 1
                            else:
                                raise ValueError('Percentage is not between 0 and 1')
                        else:
                            raise ValueError('Percentage is not a valid float value')
                    else:
                        raise ValueError('Ending date is before start date')
                else:
                    raise ValueError('Ending date is not a valid datetime value')
            else:
                raise ValueError('Start date is not a valid datetime value')
        else:
            raise ValueError('Description is not a valid string')'''

    # we assume that the marketFacade verified that the user has necessary permissions to remove a discount
    def remove_discount(self, discount_id: int) -> None:
        # TODO: implement this function
        pass

    def change_discount_percentage(self, discount_id: int, new_percentage: float) -> None:
        # TODO: implement this function
        pass

    def change_discount_description(self, discount_id: int, new_description: str) -> None:
        # TODO: implement this function
        pass

    def get_discount_by_store(self, store_id: int) -> List[DiscountStrategy]:
        # TODO: implement this function
        pass

    def get_discount_by_product(self, product_id: int) -> List[DiscountStrategy]:
        # TODO: implement this function
        pass

    def get_discount_by_category(self, category_id: int) -> List[DiscountStrategy]:
        # TODO: implement this function
        pass

    def get_discount_by_discount_id(self, discount_id: int) -> Optional[DiscountStrategy]:
        # TODO: implement this function
        pass

    def apply_discounts(self, shopping_cart: Dict[int, Dict[int, int]]) -> float:
        # TODO: implement this function
        pass

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

    def get_total_price_after_discount(self, shopping_cart: Dict[int, Dict[int, int]]) -> float:
        # TODO: implement this function
        return self.get_total_price_before_discount(shopping_cart)

    def get_total_basket_price_after_discount(self, store_id: int, shopping_cart: Dict[int, int]) -> float:
        # TODO: implement this function
        return self.get_total_basket_price_before_discount(store_id, shopping_cart)

    def get_store_product_information(self, user_id: int, store_id: int) -> List[ProductDTO]:
        """
        * Parameters: storeId
        * This function returns the store information as a string
        * Returns: the store information as a string
        """
        store = self.__get_store_by_id(store_id)
        return store.create_store_dto().products

    def __aquire_store_locks(self, store_ids: List[int]) -> None:
        """
        * Parameters: storeIds
        * This function acquires locks for the given stores
        * Returns: none
        """
        # sort the store ids to avoid deadlock
        store_ids.sort()
        for store_id in store_ids:
            store = self.__get_store_by_id(store_id)
            store.aquire_lock()

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
        # TODO: get lock here
        self.__aquire_store_locks(list(shopping_cart.keys()))
        for store_id, products in shopping_cart.items():
            store = self.__get_store_by_id(store_id)
            for product_id, amount in products.items():
                if not store.has_amount_of_product(product_id, amount):
                    self.__release_store_locks(list(shopping_cart.keys()))
                    raise ValueError('Store does not have the given amount of the product')
        self.__release_store_locks(list(shopping_cart.keys()))

        for store_id, products in shopping_cart.items():
            for product_id, amount in products.items():
                self.remove_product_amount(store_id, product_id, amount)

    def get_purchase_shopping_cart(self, shopping_cart: Dict[int, Dict[int, int]]) \
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
            basket_price_after_discount = store.get_total_price_of_basket_after_discount(products)
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
            for store in self.__stores.values():
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
            for store in self.__stores.values():
                for product_id in store.store_products:
                    product = store.get_product_dto_by_id(product_id)
                    if product.name == product_name:
                        if store.store_id not in products:
                            products[store.store_id] = []
                        products[store.store_id].append(product)
        return products

    def add_purchase_policy_to_store(self, store_id: int, policy_name: str) -> None:
        """
        * Parameters: store_id, policy_name
        * This function adds a purchase policy to the store
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.add_purchase_policy(policy_name)

    def remove_purchase_policy_from_store(self, store_id: int, policy_name: str) -> None:
        """
        * Parameters: store_id, policy_name
        * This function removes a purchase policy from the store
        * Returns: none
        """
        store = self.__get_store_by_id(store_id)
        store.remove_purchase_policy(policy_name)

    def validate_purchase_policies(self, cart: Dict[int, Dict[int, int]], user: PurchaseUserDTO) -> None:
        """
        * Parameters: cart, user
        * This function validates the purchase policies of the stores
        * Returns: True if the purchase policies are satisfied
        """
        for store_id, products in cart.items():
            store = self.__get_store_by_id(store_id)
            products = {store.get_product_dto_by_id(product_id): amount for product_id, amount in products.items()}
            store.check_purchase_policy(products, user)