# ---------- Imports ------------#
from enum import Enum
from typing import List, Dict, Tuple, Optional
from .DiscountStrategy import DiscountStrategy
from .PurchasePolicyStrategy import PurchasePolicyStrategy
from datetime import datetime
from backend.business.DTOs import ProductDTO

# -------------logging configuration----------------
import logging

logger = logging.getLogger('myapp')
# ---------------------------------------------------

# -------- Magic Numbers --------#
POUNDS_PER_KILOGRAM = 2.20462



# ---------------------product class---------------------#
class Product:  
    # id of product is productId. It is unique for each physical product
    def __init__(self, product_id: int, store_id: int, product_name: str, weight: float, description: str, price: float):
        self.__product_id = product_id
        self.__store_id = store_id
        self.__product_name = product_name
        self.__weight = weight
        self.__description = description
        self.__tags: List[str] = [] # initialized with no tags
        self.__amount = 0 # amount of the product in the store
        self.__price = price  # price is in dollars
        logger.info('[Product] successfully created product with id: ' + str(product_id))

    # ---------------------getters and setters---------------------
    @property
    def product_id(self) -> int:
        return self.__product_id
    
    @property
    def store_id(self) -> int:
        return self.__store_id
    
    @property
    def product_name(self) -> str:
        return self.__product_name
    
    @property
    def weight(self) -> float:
        return self.__weight
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def tags(self) -> List[str]:
        return self.__tags
    
    @property
    def amount(self) -> int:
        return self.__amount

    @property
    def price(self) -> float:
        return self.__price

    # ---------------------methods--------------------------------
    def change_price(self, new_price: float) -> None:
        """
        * Parameters: newPrice
        * This function changes the price of the product
        * Returns: True if the price is changed successfully
        """
        if new_price is not None:
            if new_price >= 0:
                self.__price = new_price
                logger.info('[Product] successfully changed price of product with id: ' + str(self.__product_id))
            else:
                raise ValueError('New price is a negative value')
        else:
            raise ValueError('New price is not a valid float value')

    def change_description(self, new_description: str) -> None:
        """
        * Parameters: new_description
        * This function changes the description of the product 
        * Returns: none
        """
        if new_description is not None:
            self.__description = new_description
            logger.info(
                '[Product] successfully changed description of product with id: ' + str(self.__product_id))
        else:
            raise ValueError('New description is not a valid string')

    def change_weight(self, new_weight: float) -> None:
        """
        * Parameters: new_weight
        * This function changes the weight of the product 
        * Returns: None
        """
        if new_weight is not None:
            if new_weight >= 0:
                self.__weight = new_weight
                logger.info(
                    '[Product] successfully changed weight of product with id: ' + str(self.__product_id))
            else:
                raise ValueError('New weight is a negative value')
        else:
            raise ValueError('New weight is not a valid float value')

    # weight conversion from kilograms to pounds and vice versa for locations that use pounds instead of kilograms
    def get_weight_in_pounds(self) -> float:
        return self.__weight * POUNDS_PER_KILOGRAM  # assuming weight is in kilograms

    def set_weight_in_pounds(self, weight_in_pounds: float):
        self.__weight = weight_in_pounds / POUNDS_PER_KILOGRAM


    def add_tag(self, tag: str) -> None:
        """
        * Parameters: tag
        * This function adds a tag to the product 
        * Returns: true if successfully added tag
        """
        if tag is not None:
            if tag not in self.__tags:
                self.__tags.append(tag)
                logger.info('[Product] successfully added tag to product with id: ' + str(self.__product_id))
            else:
                raise ValueError('Tag is already in the list of tags')
        else:
            raise ValueError('Tag is not a valid string')


    def remove_tag(self, tag: str) -> None:
        """
        * Parameters: tag
        * This function removes a tag from the product 
        * Returns: none
        """
        if tag is not None:
            if tag in self.__tags:
                self.__tags.remove(tag)
                logger.info(
                    '[Product] successfully removed tag from product with id: ' + str(self.__product_id))
            else:
                raise ValueError('Tag is not in the list of tags')
        else:
            raise ValueError('Tag is not a valid string')


    def has_tag(self, tag: str) -> bool:
        """
        * Parameters: tag
        * This function checks if the product has a given tag
        * Returns: true if the product has the given tag
        """
        return tag in self.__tags

    def add_product(self, amount: int) -> None:
        """
        * Parameters: amount, condition
        * This function adds a product to the store
        * Returns: none
        """
        if amount is not None:
            if amount >= 0:
                self.__amount += amount
                logger.info('[Product] successfully added product to store with id: ' + str(self.__product_id))
            else:
                raise ValueError('Amount is a negative value')
        else:
            raise ValueError('Amount is not a valid integer value')


    def remove_product(self, amount: int) -> None:
        """
        * Parameters: amount, condition
        * This function removes a product from the store
        * Returns: none 
        """
        if amount is not None:
            if amount >= 0:
                if amount <= self.__amount: 
                    self.__amount -= amount
                    logger.info('[Product] successfully removed product from store with id: ' + str(self.__product_id))
                else:
                    raise ValueError('Amount is greater than the amount of the product')
            else:
                raise ValueError('Amount is a negative value')
        else:
            raise ValueError('Amount is not a valid integer value')



# ---------------------category class---------------------#
class Category:
    # id of category is categoryId. It is unique for each category. Products are stored in either the category or found
    # in one of its subcategories
    # important to note: a category can only have one parent category, and a category can't have a subcategory that is
    # already a subcategory of a subcategory.

    def __init__(self, category_id: int, category_name: str):
        self.__category_id = category_id
        self.__category_name = category_name
        self.__parent_category_id: int = -1 # -1 means that the category does not have a parent category for now
        self.__category_products: List[Product] = []
        self.__sub_categories: List['Category'] = []
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
    def category_products(self) -> List[Product]:
        return self.__category_products
    
    @property
    def category_name(self) -> str:
        return self.__category_name
    

    # ---------------------methods--------------------------------
    def add_parent_category(self, parent_category_id: int) -> None:
        """
        * Parameters: parentCategoryId
        * This function adds a parent category to the category
        * Returns: none
        """
        if self.__parent_category_id == -1:
            self.__parent_category_id = parent_category_id
            logger.info('[Category] successfully added parent category to category with id: ' + str(self.__category_id))
        else:
            logger.warning('[Category] Category already has a parent category')

    def remove_parent_category(self) -> None:
        """
        * Parameters: none
        * This function removes the parent category of the category
        * Returns: none
        """
        if self.__parent_category_id is not None:
            self.__parent_category_id = -1
            logger.info(
                '[Category] successfully removed parent category from category with id: ' + str(self.__category_id))
        else:
            raise ValueError('Category does not have a parent category')

    def add_sub_category(self, sub_category: 'Category') -> None:
        """
        * Parameters: subCategory
        * This function adds a sub category to the category and adds the current category as the parent category of the
        sub category
        * Returns: None
        """

        if sub_category is not None:
            if not self.is_sub_category(sub_category):
                if not sub_category.has_parent_category():
                    if sub_category.__category_id != self.__category_id:
                        sub_category.add_parent_category(self.__category_id)
                        self.__sub_categories.append(sub_category)
                        logger.info(
                            '[Category] successfully added sub category to category with id: '
                            + str(self.__category_id))
                    else:
                        raise ValueError('Sub category cannot be the same as the current category')
                else:
                    raise ValueError('Sub category already has a parent category')
            else:
                raise ValueError('Sub category is already a sub category of the current category')
        else:
            raise ValueError('Sub category is not a valid category')

    def remove_sub_category(self, sub_category: 'Category') -> None:
        """
        * Parameters: subCategory
        * This function removes a sub category from the category and removes the current category as the parent category
         of the sub category
        * Returns: None
        """
        if sub_category is not None:
            if sub_category in self.__sub_categories:
                if sub_category.is_parent_category(self):
                    sub_category.remove_parent_category()
                    self.__sub_categories.remove(sub_category)
                    logger.info(
                        '[Category] successfully removed sub category from category with id: '
                        + str(self.__category_id))
                else:
                    raise ValueError('Sub category is not a sub category of the current category')
            else:
                raise ValueError('Sub category is not in the list of sub categories')
        else:
            raise ValueError('Sub category is not a valid category')

    def is_parent_category(self, category: 'Category') -> bool:
        """
        * Parameters: category
        * This function checks that the given category is the parent category of the current category
        * Returns: True if the given category is the parent category of the current category, False otherwise
        """
        return self.__parent_category_id == category.__category_id

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
        return self.__parent_category_id >= 0

    def add_product_to_category(self, product: Product) -> None:
        """
        * Parameters: product
        * This function adds a product to the category, 
        * Note: the product can only be added to the category if the product is not already in the list of products of the category, or the sub categories, or their subcategories etc.
        * Returns: None
        """
        if product is not None:
            if product not in self.get_all_products_recursively():
                self.__category_products.append(product)
                logger.info('[Category] successfully added product to category with id: ' + str(self.__category_id))
            else:
                raise ValueError('Product is already in the list of products')
        else:
            raise ValueError('Product is not a valid product')

    def remove_product_from_category(self, product: Product) -> None:
        """
        * Parameters: product
        * This function removes a product from the category
        * Returns: None
        """
        if product is not None:
            if product in self.__category_products:
                self.__category_products.remove(product)
                logger.info('[Category] successfully removed product from category with id: ' + str(self.__category_id))
            else:
                raise ValueError('Product is not in the list of products')
        else:
            raise ValueError('Product is not a valid product')

    def get_all_products_recursively(self) -> List[Product]:
        """
        * Parameters: none
        * This function returns all the products in the category and its sub categories recursively
        * Returns: all the products in the category and its sub categories recursively
        """
        # Create a new list to avoid modifying the original list
        products = list(self.__category_products)
        
        for subCategory in self.__sub_categories:
            products.extend(subCategory.get_all_products_recursively())
        
        return products

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


# ---------------------store class---------------------#
class Store:
    # id of store is storeId. It is unique for each store
    def __init__(self, store_id: int, location_id: int, store_name: str, store_founder_id: int):
        self.__store_id = store_id
        self.__location_id = location_id
        self.__store_name = store_name
        self.__store_founder_id = store_founder_id
        self.__rating: float = 0.0
        self.__is_active = True
        self.__store_products: List[Product] = []
        self.__purchase_policies: List[PurchasePolicyStrategy] = []
        self.__founded_date = datetime.now()
        self.__ratings_of_product: Dict[int, float] = {}
        self.__purchase_policy_id_counter = 0 # purchase policy Id 
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
    def rating(self) -> float:
        return self.__rating

    @property
    def is_active(self) -> bool:
        return self.__is_active

    @property
    def store_products(self) -> List[Product]:
        return self.__store_products

    @property
    def purchase_policies(self) -> List[PurchasePolicyStrategy]:
        return self.__purchase_policies

    @property
    def founded_date(self) -> datetime:
        return self.__founded_date

    @property
    def ratings_of_product(self) -> Dict[int, float]:
        return self.__ratings_of_product
    
    # ---------------------methods--------------------------------
    def close_store(self, user_id: int) -> None:
        """
        * Parameters: userId
        * This function closes the store
        * Returns: none
        """
        if user_id == self.__store_founder_id:
            self.__is_active = False
            logger.info('[Store] successfully closed store with id: ' + str(self.__store_id))
        else:
            raise ValueError('User is not the founder of the store')

    # We assume that the marketFacade verified that the user attempting to add the product is a store Owner
    def add_product(self, product: Product) -> None:
        """
        * Parameters: product
        * This function adds a product to the store, and initializes the rating of the product to 0
        * Returns: none
        """
        if product is not None:
            if product not in self.__store_products:
                self.__store_products.append(product)
                self.__ratings_of_product[product.product_id] = 0
                logger.info('[Store] successfully added product to store with id: ' + str(self.__store_id))
            else:
                raise ValueError('Product is already in the list of products')
        else:
            raise ValueError('Product is not a valid product')

    # We assume that the marketFacade verified that the user attempting to remove the product is a store owner/purchased
    def remove_product(self, product_id: int) -> None:
        """
        * Parameters: productId
        * This function removes a product from the store
        * Returns: none
        """
        if product_id is not None:
            product = self.get_product_by_id(product_id)
            if product is not None:
                self.__store_products.remove(product)
                self.__ratings_of_product.pop(product_id)
                logger.info('[Store] successfully removed product from store with id: ' + str(self.__store_id))
            else:
                raise ValueError('Product is not found')
            
        else:
            raise ValueError('Product is not a valid product')

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """
        * Parameters: productId
        * This function gets a product by its ID
        * Returns: the product with the given ID
        """
        for product in self.__store_products:
            if product.product_id == product_id:
                return product
        return None

    # we assume that the marketFacade verified that the user has necessary permissions to add a purchase policy
    ''' def add_purchase_policy(self) -> None:  # TODO: for now we dont have the necessary fields for purchase_policy
        """
        * Parameters: none
        * This function adds a purchase policy to the store
        * Returns: True if the purchase policy is added successfully, False otherwise
        """
        purchase_policy = PurchasePolicyStrategy(self.__purchase_policy_id_counter, self.__store_id)
        self.__purchase_policies.append(purchase_policy)
        self.__purchase_policy_id_counter += 1
        logger.info('[Store] successfully added purchase policy to store with id: ' + str(self.__store_id))'''

    # we assume that the marketFacade verified that the user has necessary permissions to remove a purchase policy
    def remove_purchase_policy(self, purchase_policy_id: int) -> None:
        """
        * Parameters: purchasePolicyId
        * This function removes a purchase policy from the store
        * Returns: True if the purchase policy is removed successfully
        """
        purchase_policy = self.get_purchase_policy_by_id(purchase_policy_id)
        if purchase_policy is not None:
            self.__purchase_policies.remove(purchase_policy)
            logger.info('[Store] successfully removed purchase policy from store with id: ' + str(self.__store_id))
        else:
            raise ValueError('Purchase policy is not a valid purchase policy')

    def update_purchase_policy(self, purchase_policy: PurchasePolicyStrategy) -> None:
        # not implemented yet
        pass

    def get_purchase_policy_by_id(self, purchase_policy_id: int) -> Optional[PurchasePolicyStrategy]:
        """
        * Parameters: purchasePolicyId
        * This function gets a purchase policy by its ID
        * Returns: the purchase policy with the given ID
        """
        for policy in self.__purchase_policies:
            if policy.purchase_policy_id == purchase_policy_id:
                return policy
        return None

    # LATER WE MIGHT HAVE TO ADD LOCATION OF USER AND DATE OF BIRTH
    def check_policies(self, basket: List[int]) -> bool:
        """
        * Parameters: none
        * This function checks if the purchase policies are satisfied
        * Returns: True if the purchase policies are satisfied, False otherwise
        """
        for policy in self.__purchase_policies:
            if not policy.check_constraint(basket):
                return False

        return True  # TO IMPLEMENT VERSION 2

    def update_store_rating(self, new_rating: float) -> None:
        """
        * Parameters: newRating
        * This function updates the rating of the store
        * Returns: True if the rating is updated successfully
        """
        if 0.0 <= new_rating <= 5.0:
            self.__rating = new_rating
            logger.info('[Store] successfully updated rating of store with id: ' + str(self.__store_id))
        else: 
            raise ValueError('New rating is not a valid float value')

    def update_product_rating(self, product_id: int, new_rating: float) -> None:
        """
        * Parameters: product_id, new_rating
        * This function updates the rating of the product
        * Returns: none
        """
        if 0.0 <= new_rating <= 5.0:
            self.__ratings_of_product[product_id] = new_rating
            logger.info('[Store] successfully updated rating of product with id: ' + str(product_id))
        else:
            raise ValueError('New rating is not a valid float value')

    def get_total_price_of_basket_before_discount(self, basket: Dict[int,int]) -> float:
        """
        * Parameters: basket
        * This function calculates the total price of the basket
        * Returns: the total price of the basket
        """
        total_price = 0.0
        for product_id, amount in basket.items():
            product = self.get_product_by_id(product_id)
            if product is not None:
                total_price += product.price * amount
            else:
                raise ValueError('Product is not found')
        return total_price
    

    def get_total_price_of_basket_after_discount(self, basket: Dict[int,int]) -> float:
        return self.get_total_price_of_basket_before_discount(basket)  # for now, we assume that there is no discount

    def get_store_information(self) -> str:
        """ 
        * Parameters: none
        * This function returns the store information as a string
        * Returns: the store information as a string
        """
        products = ""
        for product in self.__store_products:
            products += str(product.product_id) + " "

        purchase_policy = ""
        for policy in self.__purchase_policies:
            purchase_policy += policy.purchase_policy_id + " "

        return "Store name: " + self.__store_name + " Store founder id: " + str(
            self.__store_founder_id) + " Store rating: " + str(self.__rating) + " Store founded date: " + str(
            self.__founded_date) + " Store products: " + products + " Store purchase policies: " + purchase_policy


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
            self.__categories: List[Category] = []  # List to store categories
            self.__stores: List[Store] = []  # List to store stores
            self.__discounts: List[DiscountStrategy] = []  # List to store discounts
            self.__category_id_counter = 0  # Counter for category IDs
            self.__store_id_counter = 0  # Counter for store IDs
            self.__discount_id_counter = 0  # Counter for discount IDs
            self.__product_id_counter = 0  # Counter for product IDs
            logger.info('successfully created storeFacade')

    def clean_data(self):
        """
        For testing purposes only
        """
        self.__categories = []
        self.__stores = []
        self.__discounts = []
        self.__category_id_counter = 0
        self.__store_id_counter = 0
        self.__discount_id_counter = 0
        self.__product_id_counter = 0

    # ---------------------getters and setters---------------------
    @property
    def categories(self) -> List[Category]:
        return self.__categories
    
    @property
    def discounts(self) -> List[DiscountStrategy]:
        return self.__discounts
    
    
    @property
    def stores(self) -> List[Store]:
        return self.__stores


    # ---------------------methods--------------------------------
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """
        * Parameters: categoryId
        * This function gets a category by its ID
        * Returns: the category with the given ID
        """
        for category in self.__categories:
            if category.category_id == category_id:
                return category
        return None
    
    
    
    
    def add_category(self, category_name: str) -> None:
        """
        * Parameters: categoryName, parentCategoryId
        * This function adds a category to the store
        * Returns: none
        """
        logger.info('[StoreFacade] attempting to add category')
        if category_name is not None:
            category = Category(self.__category_id_counter, category_name)
            self.__categories.append(category)
            self.__category_id_counter += 1
        else:
            raise ValueError('Category name is not a valid string')

    def remove_category(self, category_id: int) -> None:
        """
        * Parameters: categoryId
        * This function removes a category from the store removing all connections of the category with other categories
        * Note: The subcategories of the category will be moved to the parent category of the category
        * Returns: none
        """
        logger.info('[StoreFacade] attempting to remove category')
        category_to_remove = self.get_category_by_id(category_id)
        parent_category = None
        if category_to_remove is not None:
            
            if category_to_remove.has_parent_category():
                parent_category = self.get_category_by_id(category_to_remove.parent_category_id)

            #removing the subCategories of the category
            for subCategory in category_to_remove.sub_categories:
                subCategory.remove_parent_category()
                if parent_category is not None:
                    parent_category.add_sub_category(subCategory) #adding the parent to the sub is performed in the method

            #removing the category from the parent category
            if parent_category is not None:
                parent_category.remove_sub_category(category_to_remove)
            self.__categories.remove(category_to_remove)

    def assign_sub_category_to_category(self, sub_category_id: int, category_id: int) -> None:
        """
        * Parameters: subCategoryId ,categoryId
        * This function assigns a subcategory to a category
        * Note: the parent category is assigned in the method addSubCategory of the category class
        * Returns: True if the subcategory is assigned successfully
        """
        logger.info('[StoreFacade] attempting to assign subcategory to category')
        if sub_category_id is not None:
            if category_id is not None:
                sub_category = self.get_category_by_id(sub_category_id)
                category = self.get_category_by_id(category_id)
                if sub_category is not None and category is not None:
                    category.add_sub_category(sub_category)
                else:
                    raise ValueError('Subcategory or category is not found')
            else:
                raise ValueError('Category id is not a valid integer value')
        else:
            raise ValueError('Subcategory id is not a valid integer value')

    def delete_sub_category_from_category(self, category_id: int, sub_category_id: int) -> None:
        """
        * Parameters: categoryId, subCategoryId
        * This function deletes a subcategory from a category
        * Note: the parent category is removed in the method removeSubCategory of the category class
        * Returns: True if the subcategory is deleted successfully
        """
        logger.info('[StoreFacade] attempting to delete subcategory from category')
        if category_id is not None:
            if sub_category_id is not None:
                category = self.get_category_by_id(category_id)
                sub_category = self.get_category_by_id(sub_category_id)
                if category is not None and sub_category is not None:
                    category.remove_sub_category(sub_category)
                else:
                    raise ValueError('Subcategory or category is not found')
            else:
                raise ValueError('Subcategory id is not a valid integer value')
        else:
            raise ValueError('Category id is not a valid integer value')

    def assign_product_to_category(self, category_id: int, product_id: int) -> None:
        """
        * Parameters: category_id, product_id
        * This function assigns a product none to a category
        * Returns: none
        """
        logger.info('[StoreFacade] attempting to assign product to category')
        if category_id is not None:
            if product_id is not None:
                category = self.get_category_by_id(category_id)
                product = self.__get_product_by_id(product_id)
                if category is not None and product is not None:
                    category.add_product_to_category(product)
                else:
                    raise ValueError('Product or category is not found')
            else:
                raise ValueError('Product id is not a valid integer value')

        else:
            raise ValueError('Category id is not a valid integer value')

    def remove_product_from_category(self, category_id: int, product_id: int) -> None:
        """
        * Parameters: category_id, product_id
        * This function removes a product from a category
        * Note: the product can only be removed if it is stored in the category itself, not in
         subcategories
        * Returns: None
        """
        logger.info('[StoreFacade] attempting to remove product from category')
        if category_id is not None:
            if product_id is not None:
                category = self.get_category_by_id(category_id)
                product = self.__get_product_by_id(product_id)
                if category is not None and product is not None:
                    category.remove_product_from_category(product)
                else:
                    raise ValueError('Product or category is not found')
            else:
                raise ValueError('Product id is not a valid integer value')
        else:
            raise ValueError('Category id is not a valid integer value')

    # used for search!
    def get_product_of_category(self, category_id: int) -> List[Product]:
        """
        * Parameters: categoryId
        * This function gets all the product under a category (including the products of its
         subCategories)
        * Returns: all the products of a category
        """
        if category_id is not None:
            category = self.get_category_by_id(category_id)
            if category is not None:
                return category.get_all_products_recursively()
        return []
    
    def add_product_to_store(self, store_id: int, product_name: str, weight: float, description: str, price: float) -> None:
        """
        * Parameters: productName, weight, description, tags, manufacturer, storeIds
        * This function adds a product to the store
        * Returns: none
        """
        logger.info('[StoreFacade] attempting to add product')
        store = self.get_store_by_id(store_id)
        if store is not None:
            if product_name is not None:
                if product_name != "":
                    if weight is not None:
                        if weight >= 0:
                            if description is not None:
                                if price is not None:
                                    if price >= 0:
                                        product = Product(self.__product_id_counter, store_id, product_name,
                                                                weight, description, price)
                                        store.add_product(product)
                                        self.__product_id_counter += 1
                                        logger.info('[StoreFacade] successfully added product')
                                    else:
                                        raise ValueError('Price is a negative value')
                                else:
                                    raise ValueError('Price is not a valid float value')
                            else:
                                raise ValueError('Description is not a string')
                        else:
                            raise ValueError('Weight is a negative value')
                    else:
                        raise ValueError('Weight is not a valid float value')
                else:
                    raise ValueError('Product name is an empty string')
            else:
                raise ValueError('Product name is not a valid string')
        else:
            raise ValueError('Store is not found')
        
    def remove_product_from_store(self, store_id: int, product_id: int) -> None:
        """
        * Parameters: store_id, product_id
        * This function removes a product from the store
        * Returns: none
        """
        logger.info('[StoreFacade] attempting to remove product')
        store = self.get_store_by_id(store_id)
        if store is not None:
            store.remove_product(product_id)
            logger.info('[StoreFacade] successfully removed product')
        else:
            raise ValueError('Store is not found')

    def add_product_amount(self, store_id: int, product_id: int, amount: int) -> None:
        """
        * Parameters: store_id, product_id, amount, condition
        * This function adds a product to the store
        * Returns: none
        """
        logger.info('[StoreFacade] attempting to add product amount')
        store = self.get_store_by_id(store_id)
        if store is not None:
            product = store.get_product_by_id(product_id)
            if product is not None:
                product.add_product(amount)
                logger.info('[StoreFacade] successfully added product amount')
            else:
                raise ValueError('Product is not found')
        else:
            raise ValueError('Store is not found')

    def remove_product_amount(self, store_id: int, product_id: int, amount: int) -> None:
        """
        * Parameters: store_id, product_id, amount, condition
        * This function removes a product from the store
        * Returns: none
        """
        logger.info('[StoreFacade] attempting to remove product amount')
        store = self.get_store_by_id(store_id)
        if store is not None:
            product = store.get_product_by_id(product_id)
            if product is not None:
                product.remove_product(amount)
                logger.info('[StoreFacade] successfully removed product amount')
            else:
                raise ValueError('Product is not found')
        else:
            raise ValueError('Store is not found')

    def change_weight_of_product(self, store_id: int, product_id: int, new_weight: float) -> None:
        """
        * Parameters: store_id, product_id, new_weight
        * This function changes the weight of the product
        * Returns: None
        """
        logger.info('[StoreFacade] attempting to change weight of product')
        store = self.get_store_by_id(store_id)
        if store is not None:
            product = store.get_product_by_id(product_id)
            if product is not None:
                product.change_weight(new_weight)
                logger.info('[StoreFacade] successfully changed weight of product')
            else:
                raise ValueError('Product is not found')
        else:
            raise ValueError('Store is not found')
        

    def change_description_of_product(self, store_id: int ,product_id: int, new_description: str) -> None:
        """
        * Parameters: store_id, product_id, new_description
        * This function changes the description of the product
        * Returns: None
        """
        logger.info('[StoreFacade] attempting to change description of product')
        store = self.get_store_by_id(store_id)
        if store is not None:
            product = store.get_product_by_id(product_id)
            if product is not None:
                product.change_description(new_description)
                logger.info('[StoreFacade] successfully changed description of product')
            else:
                raise ValueError('Product is not found')
        else:
            raise ValueError('Store is not found')
        

    def change_price_of_product(self, store_id: int, product_id: int, new_price: float) -> None:
        """
        * Parameters: store_id, product_id, new_price
        * This function changes the price of the product
        * Returns: none
        """
        logger.info('[StoreFacade] attempting to change price of product')
        store = self.get_store_by_id(store_id)
        if store is not None:
            product = store.get_product_by_id(product_id)
            if product is not None:
                product.change_price(new_price)
                logger.info('[StoreFacade] successfully changed price of product')
            else:
                raise ValueError('Product is not found')
        else:
            raise ValueError('Store is not found')
    
    def add_tag_to_product(self, store_id: int, product_id: int, tag: str) -> None:
        """
        * Parameters: store_id, product_id, tag
        * This function adds a tag to the product
        * Returns: None
        """
        logger.info('[StoreFacade] attempting to add tag to product')
        store = self.get_store_by_id(store_id)
        if store is not None:
            product = store.get_product_by_id(product_id)
            if product is not None:
                product.add_tag(tag)
                logger.info('[StoreFacade] successfully added tag to product')
            else:
                raise ValueError('Product is not found')
        else:
            raise ValueError('Store is not found')
        
    
    def remove_tags_from_product(self,store_id: int, product_id: int, tag: str) -> None:
        """
        * Parameters: store_id, product_id, tag
        * This function removes a tag from the product
        * Returns: None
        """
        logger.info('[StoreFacade] attempting to remove tag from product')
        store = self.get_store_by_id(store_id)
        if store is not None:
            product = store.get_product_by_id(product_id)
            if product is not None:
                product.remove_tag(tag)
                logger.info('[StoreFacade] successfully removed tag from product')
            else:
                raise ValueError('Product is not found')
        else:
            raise ValueError('Store is not found')

    def get_tags_of_product(self, store_id: int, product_id: int) -> List[str]:
        """
        * Parameters: product_id
        * This function gets all the tags of a product 
        * Returns: all the tags of the product 
        """
        logger.info('[StoreFacade] attempting to get tags of product')
        store = self.get_store_by_id(store_id)
        if store is not None:
            product = store.get_product_by_id(product_id)
            if product is not None:
                return product.tags
            else:
                raise ValueError('Product is not found')
        else:
            raise ValueError('Store is not found')

    # used for searches
    def get_products_by_tags(self, tags: List[str]) -> List[Product]:
        """
        * Parameters: list of tags
        * This function gets all the products by a given list of tags
        * Returns: all the products by a given list of tags
        """
        products = []
        for store in self.__stores:
            for product in store.store_products:
                if all(tag in product.tags for tag in tags):
                    products.append(product)
        return products
    
    # used for searches
    def get_product_by_name(self, product_name: str) -> List[Product]:
        """
        * Parameters: product_Name
        * This function gets a product name
        * Returns: the products with the given name
        """
        products = []
        for store in self.__stores:
            for product in store.store_products:
                if product.product_name == product_name:
                    products.append(product)
        return products
    
    #used for searches
    def __get_product_by_id(self, product_id: int) -> Optional[Product]:
        """
        * Parameters: product_id
        * This function gets a product by its id
        * Returns: the product with the given id
        """
        for store in self.__stores:
            product = store.get_product_by_id(product_id)
            if product is not None:
                return product
        return None

    def get_product_by_id(self, product_id: int) -> Optional[ProductDTO]:
        """
        * Parameters: product_id
        * This function gets a product by its id
        * Returns: the product with the given id
        """
        for store in self.__stores:
            product = store.get_product_by_id(product_id)
            if product is not None:
                return ProductDTO(product.product_id, product.store_id, product.product_name, product.weight,
                                   product.description, product.price, product.amount, product.tags)
        return None

    def add_store(self, location_id: int, store_name: str, store_founder_id: int) -> None:
        """
        * Parameters: locationId, storeName, storeFounderId, isActive, storeProducts, purchasePolicies, foundedDate,
         ratingsOfProduct_Id
        * This function adds a store to the store
        * Returns: None
        """
        logger.info('[StoreFacade] attempting to add store')
        if store_name is not None:
            if store_name != "":
                store = Store(self.__store_id_counter, location_id, store_name, store_founder_id)
                self.__stores.append(store)
                self.__store_id_counter += 1
            else:
                raise ValueError('Store name is an empty string')
        else:
            raise ValueError('Store name is not a valid string')

    def close_store(self, store_id: int, user_id: int) -> None:
        """
        * Parameters: storeId, userId
        * This function closes the store
        * Note: the store verifies whether the userId is the id of the founder, only the founder can close the store
        * Returns: None
        """
        logger.info('[StoreFacade] attempting to close store')
        if store_id is not None:
            store = self.get_store_by_id(store_id)
            if store is not None:
                return store.close_store(user_id)
            else:
                raise ValueError('Store id is not a valid integer value')
        else:
            raise ValueError('Store id is not a valid integer value')

    def get_store_by_id(self, store_id: int) -> Optional[Store]:
        """
        * Parameters: storeId
        * This function gets a store by its ID
        * Returns: the store with the given ID
        """
        for store in self.__stores:
            if store.store_id == store_id:
                return store
        return None

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

    def remove_purchase_policy_from_store(self, store_id: int, purchase_policy_id: int) -> None:
        """
        * Parameters: storeId, purchasePolicyId
        * This function removes a purchase policy from the store
        * Note: the marketFacade is responsible for verifying whether the purchase policy is removed by someone with the
         necessary permissions.
        * Returns: True if the purchase policy is removed successfully
        """
        logger.info('[StoreFacade] attempting to remove purchase policy from store')
        if store_id is not None:
            if purchase_policy_id is not None:
                store = self.get_store_by_id(store_id)
                if store is not None:
                    purchase_policy = store.get_purchase_policy_by_id(purchase_policy_id)
                    if purchase_policy is not None:
                        return store.remove_purchase_policy(purchase_policy_id)
                    else:
                        raise ValueError('Purchase policy not found')
                else:
                    raise ValueError('Store not found')
            else:
                raise ValueError('Purchase policy id is not a valid integer value')
        else:
            raise ValueError('Store id is not a valid integer value')

    def update_purchase_policy_of_store(self, store_id: int, purchase_policy_id: int) -> None:
        pass

    def check_policies_of_store(self, store_id: int, basket: List[int]) -> bool:
        return True  # in the meantime

    def update_store_rating(self, store_id: int, new_rating: float) -> None:
        """
        * Parameters: storeId, newRating
        * This function updates the rating of the store
        * Returns: None
        """
        logger.info('[StoreFacade] attempting to update rating of store')
        if store_id is not None:
            if new_rating is not None:
                if new_rating >= 0.0:
                    if new_rating <= 5.0:
                        store = self.get_store_by_id(store_id)
                        if store is not None:
                            store.update_store_rating(new_rating)
                        else:
                            raise ValueError('Store not found')
                    else:
                        raise ValueError('New rating is greater than 5')
                else:
                    raise ValueError('New rating is negative')
            else:
                raise ValueError('New rating is not a valid float value')
        else:
            raise ValueError('Store id is not a valid integer value')

    def update_product_rating(self, store_id: int, product_id: int, new_rating: float) -> None:
        """
        * Parameters: store_id, product_id, new_rating
        * This function updates the rating of the product
        * Returns: None
        """
        logger.info('[StoreFacade] attempting to update rating of product')
        if store_id is not None:
            if product_id is not None:
                if new_rating is not None:
                    if new_rating >= 0.0:
                        if new_rating <= 5.0:
                            store = self.get_store_by_id(store_id)
                            if store is not None:
                                store.update_product_rating(product_id, new_rating)
                            else:
                                raise ValueError('Store not found')
                        else:
                            raise ValueError('New rating is greater than 5')
                    else:
                        raise ValueError('New rating is negative')
                else:
                    raise ValueError('New rating is not a valid float value')
            else:
                raise ValueError('Product id is not a valid integer value')
        else:
            raise ValueError('Store id is not a valid integer value')

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
        """
        * Parameters: discountId
        * This function removes a discount from the store
        * Returns: None
        """
        logger.info('[StoreFacade] attempting to remove discount')
        if discount_id is not None:
            discount = self.get_discount_by_discount_id(discount_id)
            if discount is not None:
                self.__discounts.remove(discount)
            else:
                raise ValueError('Discount not found')
        else:
            raise ValueError('Discount id is not a valid integer value')

    def change_discount_percentage(self, discount_id: int, new_percentage: float) -> None:
        """
        * Parameters: discountId, newPercentage
        * This function changes the percentage of the discount
        * Returns: none
        """
        logger.info('[StoreFacade] attempting to change percentage of discount')
        if discount_id is not None:
            if new_percentage is not None:
                discount = self.get_discount_by_discount_id(discount_id)
                if discount is not None:
                    discount.change_discount_percentage(new_percentage)
                else:
                    raise ValueError('Discount not found')
            else:
                raise ValueError('New percentage is not a valid float value')
        else:
            raise ValueError('Discount id is not a valid integer value')

    def change_discount_description(self, discount_id: int, new_description: str) -> None:
        """
        * Parameters: discountId, newDescription
        * This function changes the description of the discount
        * Returns: none
        """
        logger.info('[StoreFacade] attempting to change description of discount')
        if discount_id is not None:
            if new_description is not None:
                discount = self.get_discount_by_discount_id(discount_id)
                if discount is not None:
                    discount.change_discount_description(new_description)
                else:
                    raise ValueError('Discount not found')
            else:
                raise ValueError('New description is not a valid string')
        else:
            raise ValueError('Discount id is not a valid integer value')

    def get_discount_by_store(self, store_id: int) -> List[DiscountStrategy]:
        return []
        # not implemented yet
        

    def get_discount_by_product(self, product_id: int) -> List[DiscountStrategy]:
        return []
        # not implemented yet
        pass

    def get_discount_by_category(self, category_id: int) -> List[DiscountStrategy]:
        return []
        # not implemented yet
        pass

    def get_discount_by_discount_id(self, discount_id: int) -> Optional[DiscountStrategy]:
        """
        * Parameters: discountId
        * This function gets a discount by its ID
        * Returns: the discount with the given ID
        """
        for discount in self.__discounts:
            if discount.discount_id == discount_id:
                return discount
        return None

    def apply_discounts(self, shopping_cart: Dict[int, Dict[int,int]]) -> float:
        return 0.0
        # not implemented yet
        pass

    def get_total_price_before_discount(self, shopping_cart: Dict[int, Dict[int, int]]) -> float:
        """
        * Parameters: shoppingCart
        * This function calculates the total price of the shopping cart before applying any discounts
        * Returns: the total price of the shopping cart before applying any discounts
        """
        total_price = 0.0
        for store_id, products in shopping_cart.items():
            store = self.get_store_by_id(store_id)
            if store is not None:
                total_price += store.get_total_price_of_basket_before_discount(products)
            else:
                raise ValueError('Store not found')
        return total_price

    # TODO: get Dict[int, Dict[int, int]]
    def get_total_price_after_discount(self, shopping_cart: Dict[int, Dict[int,int]]) -> float:
        """
        * Parameters: shoppingCart
        * This function calculates the total price of the shopping cart after applying all discounts
        * Returns: the total price of the shopping cart after applying all discounts
        """
        return self.get_total_price_before_discount(shopping_cart)  # not implemented yet VERSION 2

    def get_store_product_information(self, user_id: int, store_id: int) -> str:
        """
        * Parameters: storeId
        * This function returns the store information as a string
        * Returns: the store information as a string
        """
        store = self.get_store_by_id(store_id)
        products = ""
        if store is not None:
            for product in store.store_products:
                products += str(product.product_id) + " " + "Product name: " + product.product_name + " Product weight: " + str(product.weight) + " Product description: " + product.description + " Product price: " + str(product.price) + " Product amount: " + str(product.amount) + " Product tags: " + ''.join(x for x in product.tags) + "\n"
            return "Store name: " + store.store_name + " Store founder id: " + str(store.store_founder_id) + " Store rating: " + str(store.rating) + " Store founded date: " + str(store.founded_date) + " Store products: " + products

        return products

    # --------------------methods for market facade used by users team---------------------------#
    def check_product_availability(self, store_id: int, product_id: int):
        """
        * Parameters: store_id, product_id
        * This function checks if the product is available in the store
        * Returns: True if the product is available, false otherwise
        """
        store = self.get_store_by_id(store_id)
        if store is not None:
            for product in store.store_products:
                if product.product_id == product_id:
                    return True
            return False
        else:
            raise ValueError('Store not found')
        

    def get_store_info(self, store_id: int) -> str:
        """
        * Parameters: store_id
        * This function gets the store information
        * Returns: the store information
        """
        store = self.get_store_by_id(store_id)
        if store is not None:
            return "Store: " + store.store_name + " Founded by: " + str(store.store_founder_id) + " Rating: " + str(store.rating) + " Founded Date: " + str(store.founded_date) + "is active: " + str(store.is_active)
        else:
            raise ValueError('Store not found')
        
    def search_by_category(self, category_id: int) -> Dict[Tuple[int, float], Dict[int, Tuple[Tuple[int, float], float]]]:
        """
        * Parameters: category_id
        * This function searches for products by category
        * Returns: a dict of <store,rating> with a dict of <product,<<amount,price> rating>>>
        """
        category = self.get_category_by_id(category_id)
        if category is not None:
            information: Dict[Tuple[int, float], Dict[int, Tuple[Tuple[int,float],float]]] = {}
            for store in self.__stores:
                products_in_store_that_are_in_category: Dict[int,Tuple[Tuple[int,float],float]] = {}
                for product in category.get_all_products_recursively():
                    if store.store_id == product.store_id:
                        products_in_store_that_are_in_category[product.product_id] = ((product.amount, product.price), store.rating)
                
                if len(products_in_store_that_are_in_category) > 0:
                    information[(store.store_id, store.rating)] = products_in_store_that_are_in_category
            return information
        else:
            raise ValueError('Category not found')

    def search_by_tags(self, tags: List[str]) -> Dict[Tuple[int, float], Dict[int, Tuple[Tuple[int, float], float]]]:
        """
        * Parameters: tags
        * This function searches for products by tags
        * Returns: a dict of <store,rating> with a dict of <product,<<amount,price> rating>>>
        """ 
        information: Dict[Tuple[int, float], Dict[int, Tuple[Tuple[int,float],float]]] = {}
        for store in self.__stores:
            products_in_store_that_have_tags: Dict[int,Tuple[Tuple[int,float],float]] = {}
            for product in store.store_products:
                if all(tag in product.tags for tag in tags):
                    products_in_store_that_have_tags[product.product_id] = ((product.amount, product.price), store.rating)
            
            if len(products_in_store_that_have_tags) > 0:
                information[(store.store_id, store.rating)] = products_in_store_that_have_tags
        return information
        
    def search_by_name(self, product_name: str) -> Dict[Tuple[int, float], Dict[int, Tuple[Tuple[int, float], float]]]:
        """
        * Parameters: product_name
        * This function searches for products by name
        * Returns: a dict of <store,rating> with a dict of <product,<<amount,price> rating>>>
        """
        information: Dict[Tuple[int, float], Dict[int, Tuple[Tuple[int,float],float]]] = {}
        for store in self.__stores:
            products_in_store_that_have_name: Dict[int,Tuple[Tuple[int,float],float]] = {}
            for product in store.store_products:
                if product.product_name == product_name:
                    products_in_store_that_have_name[product.product_id] = ((product.amount, product.price), store.rating)
            
            if len(products_in_store_that_have_name) > 0:
                information[(store.store_id, store.rating)] = products_in_store_that_have_name
        return information


    def search_in_store(self, store_id: int, product_name: str) -> Dict[int, Tuple[Tuple[int, float], float]]:
        """
        * Parameters: store_id, search_term
        * This function searches for products in a store
        * Returns: a dict of <product,<<amount,price> rating>>
        """
        store = self.get_store_by_id(store_id)
        if store is not None:
            products_in_store: Dict[int,Tuple[Tuple[int,float],float]] = {}
            for product in store.store_products:
                if product.product_name == product_name:
                    products_in_store[product.product_id] = ((product.amount, product.price), store.rating)
            return products_in_store
        else:
            raise ValueError('Store not found')
