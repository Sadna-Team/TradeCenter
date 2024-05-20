from typing import Dict
#---------- Imports ------------#
from enum import Enum
from typing import List, Dict
from .DiscountStrategy import DiscountStrategy
from .PurchasePolicyStrategy import PurchasePolicyStrategy
import datetime


#-------------logging configuration----------------
from logging_config import setup_logging
import logging

logger = logging.getLogger('myapp')
#---------------------------------------------------

#-------- Magic Numbers --------#
POUNDS_PER_KILOGRAM = 2.20462


#---------------------productCondition Enum---------------------#
class ProductCondition(Enum):
    NEW = 1
    USED = 2

ProductCondition = Enum('ProductCondition', ['NEW', 'USED'])


#---------------------product class---------------------#
class Product:
    # id of product is productId. It is unique for each physical product
    def __init__(self, productId: int, storeId: int, specificationId: int, expirationDate: datetime,
                condition: ProductCondition, price: float):
        self.__productId = productId
        self.__storeId = storeId
        self.__specificationId = specificationId
        self.__expirationDate = expirationDate
        self.__condition = condition
        self.__price = price # price is in dollars
        
        logger.info('[Product] successfully created product with id: ' + str(productId))



    #---------------------getters and setters---------------------
    @property
    def get_productId(self) -> int:
        return self.__productId
    
    @property
    def __set_productId(self, productId: int):
        self.__productId = productId

    @property
    def get_storeId(self) -> int:
        return self.__storeId
    
    @property
    def __set_storeId(self, storeId: int):
        self.__storeId = storeId

    @property
    def get_specificationId(self) -> int:
        return self.__specificationId
    
    @property
    def __set_specificationId(self, specificationId: int):
        self.__specificationId = specificationId

    @property
    def get_expirationDate(self) -> datetime:
        return self.__expirationDate
    
    @property
    def __set_expirationDate(self, expirationDate: datetime):
        self.__expirationDate = expirationDate

    @property
    def get_condition(self) -> ProductCondition:
        return self.__condition
    
    @property   
    def __set_condition(self, condition: ProductCondition):
        self.__condition = condition

    @property
    def get_price(self) -> float:
        return self.__price
    
    @property
    def __set_price(self, price: float):
        self.__price = price
    

    #---------------------methods--------------------------------
    def isExpired(self) -> bool:
        ''' 
        * Parameters: none
        * This function checks whether the product is expired or not
        * Returns: True if the product is expired, False otherwise
        '''
        return self.__expirationDate < datetime.datetime.now()
    
    def changePrice(self, newPrice: float) -> bool:
        '''
        * Parameters: newPrice
        * This function changes the price of the product
        * Returns: True if the price is changed successfully, False otherwise
        '''
        if newPrice is not None:
            if newPrice >= 0:
                self.__set_price(newPrice) 
                logger.info('[Product] successfully changed price of product with id: ' + str(self.__productId))
                return True
            else:
                logger.warn('[Product] New price is a negative value')
                return False
        else:
            raise ValueError('New price is not a valid float value')
    

#---------------------productSpecification class---------------------#
class ProductSpecification:
    # id of product specification is specificationId. It is unique for each product specification
    # it is assumed that weight is stored in kilograms
    def __init__(self, specificationId: int, productName: str, weight: float, description: str, tags: List[str], manufacturer: str, storeIds: List[int] = []): 
        self.__specificationId = specificationId
        self.__productName = productName
        self.__weight = weight
        self.__description = description 
        self.__tags = tags
        self.__manufacturer = manufacturer
        self.__storeIds = storeIds
        logger.info('[ProductSpecification] successfully created product specification with id: ' + str(specificationId))


    #---------------------getters and setters---------------------
    @property
    def get_specificationId(self) -> int:
        return self.__specificationId

    @property
    def __set_specificationId(self, specificationId: int):
        self.__specificationId = specificationId

    @property
    def get_productName(self) -> str:
        return self.__productName

    @property
    def __set_productName(self, productName: str):
        self.__productName = productName

    @property
    def get_weight(self) -> float:
        return self.__weight

    @property
    def __set_weight(self, weight: float):
        self.__weight = weight

    @property
    def get_description(self) -> str:
        return self.__description

    @property
    def __set_description(self, description: str):
        self.__description = description

    @property
    def get_tags(self) -> List[str]:
        return self.__tags

    @property
    def __set_tags(self, tags: List[str]):
        self.__tags = tags

    @property
    def get_manufacturer(self) -> str:
        return self.__manufacturer

    @property
    def __set_manufacturer(self, manufacturer: str):
        self.__manufacturer = manufacturer

    @property
    def get_storeIds(self) -> List[int]:
        return self.__storeIds
    
    @property
    def __set_storeIds(self, storeIds: List[int]):
        self.__storeIds = storeIds


    #---------------------methods-------------------------------- 
    def addTag(self, tag: str) -> bool:
        ''' 
        * Parameters: tag
        * This function adds a tag to the product specification
        * Returns: true if successfully added tag, false otherwise
        '''
        if tag is not None:
            if tag not in self.__tags:
                self.__tags.append(tag)
                logger.info('[ProductSpecification] successfully added tag to product specification with id: ' + str(self.__specificationId))
                return True
            else:
                logger.warn('[ProductSpecification] Tag is already in the list of tags')
                return False
        else:
            raise ValueError('Tag is not a valid string')
    

    def removeTag(self, tag: str) -> bool:
        ''' 
        * Parameters: tag
        * This function removes a tag from the product specification
        * Returns: none
        '''
        if tag is not None:
            if tag in self.__tags:
                self.__tags.remove(tag)
                logger.info('[ProductSpecification] successfully removed tag from product specification with id: ' + str(self.__specificationId))  
                return True
            else:
                logger.warn('[ProductSpecification] Tag is not in the list of tags')
                return False
        else:
            raise ValueError('Tag is not a valid string')
    

    def hasTag(self, tag: str) -> bool:
        ''' 
        * Parameters: tag
        * This function checks if the product specification has a given tag
        * Returns: true if the product specification has the given tag, false otherwise
        '''
        return tag in self.__tags


    def addStoreId(self, storeId: int) -> bool:
        ''' 
        * Parameters: storeId
        * This function adds a store id to the product specification
        * Returns: true if successfully added store id, false otherwise
        '''
        if storeId is not None:
            if storeId not in self.__storeIds:
                self.__storeIds.append(storeId)
                logger.info('[ProductSpecification] successfully added store id to product specification with id: ' + str(self.__specificationId))
                return True
            else:
                logger.warn('[ProductSpecification] Store id is already in the list of store ids')
                return False
        else:
            raise ValueError('Store id is not a valid integer value')

    def removeStoreId(self, storeId: int) -> bool:
        ''' 
        * Parameters: storeId
        * This function removes a store id from the product specification
        * Returns: true if successfully removed store id, false otherwise
        '''
        if storeId is not None:
            if storeId in self.__storeIds:
                self.__storeIds.remove(storeId)
                logger.info('[ProductSpecification] successfully removed store id from product specification with id: ' + str(self.__specificationId))
                return True
            else:
                logger.warn('[ProductSpecification] Store id is not in the list of store ids')
        else:
            raise ValueError('Store id is not a valid integer value')


    def isSoldByStore(self, storeId: int) -> bool:
        ''' 
        * Parameters: storeId
        * This function checks if the product specification is sold at given store
        * Returns: true if sold by store, false otherwise
        '''
        return storeId in self.__storeIds
    
    # weight conversion from kilograms to pounds and vice versa for locations that use pounds instead of kilograms
    def get_weight_in_pounds(self) -> float:
        return self.__weight * POUNDS_PER_KILOGRAM   # assuming weight is in kilograms

    def set_weight_in_pounds(self, weight_in_pounds: float):
        self.__weight = weight_in_pounds / POUNDS_PER_KILOGRAM 

    def changeNameOfProductSpecification(self, newName: str) -> bool:
        '''
        * Parameters: newName
        * This function changes the name of the product specification
        * Returns: True if the name is changed successfully, False otherwise
        '''
        if newName is not None:
            if newName != "":
                self.__set_productName(newName)
                logger.info('[ProductSpecification] successfully changed name of product specification with id: ' + str(self.__specificationId))
                return True
            else:
                logger.warn('[ProductSpecification] New name is an empty string')
                return False
            
        else:
            raise ValueError('New name is not a valid string')
    
    def changeManufacturerOfProductSpecification(self, newManufacturer: str) -> bool:
        '''
        * Parameters: newManufacturer
        * This function changes the manufacturer of the product specification
        * Returns: True if the manufacturer is changed successfully, False otherwise
        '''
        if newManufacturer is not None:
            if newManufacturer != "":
                self.__set_manufacturer(newManufacturer)
                logger.info('[ProductSpecification] successfully changed manufacturer of product specification with id: ' + str(self.__specificationId))
                return True
            else:
                logger.warn('[ProductSpecification] New manufacturer is an empty string')
                return False
        else:
            raise ValueError('New manufacturer is not a valid string')
    
    def changeDescriptionOfProductSpecification(self, newDescription: str) -> bool:
        '''
        * Parameters: newDescription
        * This function changes the description of the product specification
        * Returns: True if the description is changed successfully, False otherwise
        '''
        if newDescription is not None:
            self.__set_description(newDescription)
            logger.info('[ProductSpecification] successfully changed description of product specification with id: ' + str(self.__specificationId))
            return True
        else:
            raise ValueError('New description is not a valid string')
    
    def changeWeightOfProductSpecification(self, newWeight: float) -> bool:
        '''
        * Parameters: newWeight
        * This function changes the weight of the product specification
        * Returns: True if the weight is changed successfully, False otherwise
        '''
        if newWeight is not None:
            if newWeight >= 0:
                self.__set_weight(newWeight)
                logger.info('[ProductSpecification] successfully changed weight of product specification with id: ' + str(self.__specificationId))
                return True
            else: 
                logger.warn('[ProductSpecification] New weight is a negative value')
                return False
        else:
            raise ValueError('New weight is not a valid float value')
    
    

#---------------------category class---------------------#
class Category:
    # id of category is categoryId. It is unique for each category. Products are stored in either the category or found in one of its subcategories
    # important to note: a category can only have one parentcategory, and a category can't have a subcategory that is already a subcategory of a subcategory.

    def __init__(self, categoryId: int, categoryName: str, parentCategoryId: int = None, categoryProducts: List[ProductSpecification] = [], subCategories: List['Category'] = []):
        self.__categoryId = categoryId
        self.__categoryName = categoryName
        self.__parentCategoryId = parentCategoryId
        self.__categoryProducts = categoryProducts
        self.__subCategories = subCategories
        logger.info('[Category] successfully created category with id: ' + str(categoryId))



    #---------------------getters and setters---------------------
    @property
    def get_categoryId(self) -> int:
        return self.__categoryId
    
    @property
    def __set_categoryId(self, categoryId: int):
        self.__categoryId = categoryId

    @property
    def get_categoryName(self) -> str:
        return self.__categoryName
    
    @property
    def __set_categoryName(self, categoryName: str):
        self.__categoryName = categoryName

    @property
    def get_parentCategoryId(self) -> int:
        return self.__parentCategoryId
    
    @property
    def __set_parentCategoryId(self, parentCategoryId: int):
        self.__parentCategoryId = parentCategoryId

    @property
    def get_categoryProducts(self) -> List[ProductSpecification]:
        return self.__categoryProducts
    
    @property
    def __set_categoryProducts(self, categoryProducts: List[ProductSpecification]):
        self.__categoryProducts = categoryProducts

    @property
    def get_subCategories(self) -> List['Category']:
        return self.__subCategories
    
    @property
    def __set_subCategories(self, subCategories: List['Category']):
        self.__subCategories = subCategories

    

    #---------------------methods--------------------------------
    def addParentCategory(self, parentCategoryId: int):
        ''' 
        * Parameters: parentCategoryId
        * This function adds a parent category to the category
        * Returns: none
        '''
        if self.__parentCategoryId is None:
            self.set_parentCategoryId(parentCategoryId)
            logger.info('[Category] successfully added parent category to category with id: ' + str(self.__categoryId))
        else:
            logger.warn('[Category] Category already has a parent category')
            

    
    def removeParentCategory(self):
        ''' 
        * Parameters: none
        * This function removes the parent category of the category
        * Returns: none
        '''
        if self.__parentCategoryId is not None:
            self.set_parentCategoryId(None)
            logger.info('[Category] successfully removed parent category from category with id: ' + str(self.__categoryId))
        else:
            raise ValueError('Category does not have a parent category')


    def addSubCategory(self, subCategory: 'Category') -> bool:
        ''' 
        * Parameters: subCategory
        * This function adds a sub category to the category and adds the current category as the parent category of the sub category
        * Returns: True if the sub category is added successfully, False otherwise
        '''

        if subCategory is not None:
            if not self.isSubCategory(subCategory):
                if not subCategory.hasParentCategory():
                    if subCategory.get_categoryId() != self.__categoryId:
                        subCategory.addParentCategory(self.__categoryId)
                        self.__subCategories.append(subCategory)
                        logger.info('[Category] successfully added sub category to category with id: ' + str(self.__categoryId))
                        return True
                else:
                    logger.warn('[Category] Sub category already has a parent category')
            else:
                logger.warn('[Category] Sub category is already a sub category of the current category')
        else:
            raise ValueError('Sub category is not a valid category')
    

    def removeSubCategory(self, subCategory: 'Category') -> bool:
        ''' 
        * Parameters: subCategory
        * This function removes a sub category from the category and removes the current category as the parent category of the sub category
        * Returns: True if the sub category is removed successfully, False otherwise
        '''
        if subCategory is not None:
            if subCategory in self.__subCategories:
                if subCategory.isParentCategory(self):
                    subCategory.removeParentCategory()
                    self.__subCategories.remove(subCategory)
                    logger.info('[Category] successfully removed sub category from category with id: ' + str(self.__categoryId))
                    return True
                else:
                    logger.warn('[Category] Sub category is not a sub category of the current category')
            else:
                logger.warn('[Category] Sub category is not in the list of sub categories')
        else:
            raise ValueError('Sub category is not a valid category')
    

    def isParentCategory(self, category: 'Category') -> bool:
        ''' 
        * Parameters: category
        * This function checks that the given category is the parent category of the current category
        * Returns: True if the given category is the parent category of the current category, False otherwise
        '''
        return self.__parentCategoryId == category.get_categoryId()
    

    def isSubCategory(self, category: 'Category') -> bool:
        ''' 
        * Parameters: category
        * This function checks that the given category is the sub category of the current category
        * Returns: True if the given category is the sub category of the current category, False otherwise
        '''
        return category in self.__subCategories or any(subCategory.isSubCategory(category) for subCategory in self.__subCategories)

    def hasParentCategory(self) -> bool:
        ''' 
        * Parameters: none
        * This function checks that the current category has a parent category or not
        * Returns: True if the current category has a parent category, False otherwise
        '''
        return self.__parentCategoryId is not None and self.__parentCategoryId >= 0

    
    def addProductToCategory(self, product: ProductSpecification) -> bool:
        ''' 
        * Parameters: product
        * This function adds a product to the category
        * Returns: True if the product is added successfully, False otherwise
        '''
        if product is not None:
            if product not in self.getAllProductsRecursively():
                self.__categoryProducts.append(product)
                logger.info('[Category] successfully added product to category with id: ' + str(self.__categoryId))
                return True
            else:
                logger.warn('[Category] Product is already in the list of products')
        else:   
            raise ValueError('Product is not a valid product')
    

    def removeProductFromCategory(self, product: ProductSpecification) -> bool:
        ''' 
        * Parameters: product
        * This function removes a product from the category
        * Returns: True if the product is removed successfully, False otherwise
        '''
        if product is not None:
            if product in self.__categoryProducts:
                self.__categoryProducts.remove(product)
                logger.info('[Category] successfully removed product from category with id: ' + str(self.__categoryId))
                return True
            else:
                logger.warn('[Category] Product is not in the list of products')
        else:    
            raise ValueError('Product is not a valid product')
    
    
    def getAllProductsRecursively(self) -> List[ProductSpecification]:
        ''' 
        * Parameters: none
        * This function returns all the products in the category and its sub categories recursively
        * Returns: all the products in the category and its sub categories recursively
        '''
        products = self.__categoryProducts
        for subCategory in self.__subCategories:
            products += subCategory.getAllProductsRecursively()
        return products
    

    def getAllProductNames(self) -> str:
        ''' 
        * Parameters: none
        * This function returns all the names of the products in the category as a big string
        * Returns: all the names of the products in the category as a big string
        '''
        names = ""
        for product in self.getAllProductsRecursively():
            names += product.get_productName() + " "
        return names
    
    
    
#---------------------store class---------------------#
class Store: 
    # id of store is storeId. It is unique for each store
    def __init__(self, storeId: int, locationId: int, storeName: str, storeFounderId: int, storeProducts: List[Product] = [],
                   purchasePolicies: List[PurchasePolicyStrategy] = [], foundedDate: datetime = datetime.datetime.now(), 
                   ratingsOfProductSpecId: Dict[int, float] = {}):
        self.__storeId = storeId
        self.__locationId = locationId
        self.__storeName = storeName
        self.__storeFounderId = storeFounderId
        self.__rating = 0
        self.__isActive = True
        self.__storeProducts = storeProducts
        self.__purchasePolicies = purchasePolicies
        self.__foundedDate = foundedDate        
        self.__ratingsOfProductSpecId = ratingsOfProductSpecId
        self.__purchasePolicyIdCounter = 0
        logger.info('[Store] successfully created store with id: ' + str(storeId))
        

    #---------------------getters and setters---------------------#
    @property
    def get_storeId(self) -> int:
        return self.__storeId
    
    @property
    def __set_storeId(self, storeId: int):
        self.__storeId = storeId

    @property
    def get_locationId(self) -> int:
        return self.__locationId
    
    @property
    def __set_locationId(self, locationId: int):
        self.__locationId = locationId

    @property
    def get_storeName(self) -> str:
        return self.__storeName
    
    @property
    def __set_storeName(self, storeName: str):
        self.__storeName = storeName

    @property
    def get_storeFounderId(self) -> int:
        return self.__storeFounderId
    
    @property
    def __set_storeFounderId(self, storeFounderId: int):
        self.__storeFounderId = storeFounderId

    @property
    def get_rating(self) -> float:
        return self.__rating
    
    @property
    def __set_rating(self, rating: float):
        self.__rating = rating

    @property
    def get_isActive(self) -> bool:
        return self.__isActive
    
    @property
    def __set_isActive(self, isActive: bool):
        self.__isActive = isActive

    @property
    def get_storeProducts(self) -> List[Product]:
        return self.__storeProducts
    
    @property
    def __set_storeProducts(self, storeProducts: List[Product]):
        self.__storeProducts = storeProducts

    @property
    def get_purchasePolicies(self) -> List[PurchasePolicyStrategy]:
        return self.__purchasePolicies
    
    @property
    def __set_purchasePolicies(self, purchasePolicies: List[PurchasePolicyStrategy]):
        self.__purchasePolicies = purchasePolicies

    @property
    def get_foundedDate(self) -> datetime:
        return self.__foundedDate
    
    @property
    def __set_foundedDate(self, foundedDate: datetime):
        self.__foundedDate = foundedDate

    @property
    def get_ratingsOfProductSpecId(self) -> Dict[int, int]:
        return self.__ratingsOfProductSpecId
    
    @property
    def __set_ratingsOfProductSpecId(self, ratingsOfProductSpecId: Dict[int, float]):
        self.__ratingsOfProductSpecId = ratingsOfProductSpecId
    
    @property
    def get_purchasePolicyIdCounter(self) -> int:
        return self.__purchasePolicyIdCounter
    
    @property
    def __set_purchasePolicyIdCounter(self, purchasePolicyIdCounter: int):
        self.__purchasePolicyIdCounter = purchasePolicyIdCounter

    #---------------------methods--------------------------------
    def isActive(self) -> bool:
        ''' 
        * Parameters: none
        * This function checks if the store is active or not
        * Returns: True if the store is active, False otherwise
        '''
        return self.__isActive
    

    def closeStore(self, userId: int) -> bool:
        ''' 
        * Parameters: userId
        * This function closes the store
        * Returns: True if the store is closed, False otherwise
        '''
        if userId == self.__storeFounderId:
            self.set_isActive(False)
            logger.info('[Store] successfully closed store with id: ' + str(self.__storeId))
            return True
        logger.warn('[Store] User is not the founder of the store')
        return False
    

    # We assume that the marketFacade verified that the user attempting to add the product is a store Owner
    def addProduct(self, product: Product) -> bool:
        ''' 
        * Parameters: product
        * This function adds a product to the store, and initializes the rating of the product to 0
        * Returns: True if the product is added successfully, False otherwise
        '''
        if product is not None:
            if product not in self.__storeProducts:
                self.__storeProducts.append(product)
                self.__ratingsOfProductSpecId[product.get_specificationId()] = 0
                logger.info('[Store] successfully added product to store with id: ' + str(self.__storeId))
                return True
            else:
                logger.warn('[Store] Product is already in the list of products')
        else:
            raise ValueError('Product is not a valid product')
    
    # We assume that the marketFacade verified that the user attempting to remove the product is a store owner/purchased by a user
    def removeProduct(self, productId: int) -> bool:
        ''' 
        * Parameters: productId
        * This function removes a product from the store
        * Returns: True if the product is removed successfully, False otherwise
        '''
        if productId is not None:
            product = self.getProductById(productId)
            self.__storeProducts.remove(product)
            logger.info('[Store] successfully removed product from store with id: ' + str(self.__storeId))
            return True
        else:
            raise ValueError('Product is not a valid product')
    
    def changePriceOfProduct(self, productId: int, newPrice: float) -> bool:
        ''' 
        * Parameters: productId, newPrice
        * This function changes the price of the product
        * Returns: True if the price is changed successfully, False otherwise
        '''
        if productId is not None:
            product = self.getProductById(productId)
            if product is not None:            
                logger.info('[Store] successfully changed price of product with id: ' + str(productId))
                return product.changePrice(newPrice)
            else:
                raise ValueError('Product is not a valid product')
    

    def getProductById(self, productId: int) -> Product:
        ''' 
        * Parameters: productId
        * This function gets a product by its ID
        * Returns: the product with the given ID
        '''
        for product in self.__storeProducts:
            if product.get_productId() == productId:
                return product
        return None
    

    # we assume that the marketFacade verified that the user has necessary permissions to add a purchase policy
    def addPurchasePolicy(self) -> bool: #TODO: for now we dont have the necessary fields for purchasePolicy
        ''' 
        * Parameters: none
        * This function adds a purchase policy to the store
        * Returns: True if the purchase policy is added successfully, False otherwise
        '''
        purchasePolicy = PurchasePolicyStrategy(self.get_purchasePolicyIdCounter(), self.get_storeId())
        self.get_purchasePolicies.append(purchasePolicy)
        self.__set_purchasePolicyIdCounter(self.get_purchasePolicyIdCounter() + 1)        
        logger.info('[Store] successfully added purchase policy to store with id: ' + str(self.__storeId))
        return True
        

    # we assume that the marketFacade verified that the user has necessary permissions to remove a purchase policy
    def removePurchasePolicy(self, purchasePolicyId: int) -> bool:
        ''' 
        * Parameters: purchasePolicyId
        * This function removes a purchase policy from the store
        * Returns: True if the purchase policy is removed successfully, False otherwise
        '''
        purchasePolicy = self.getPurchasePolicyById(purchasePolicyId)
        if purchasePolicy is not None:
            self.__purchasePolicies.remove(purchasePolicy)
            logger.info('[Store] successfully removed purchase policy from store with id: ' + str(self.__storeId))
            return True
        else:
            raise ValueError('Purchase policy is not a valid purchase policy')
    

    def updatePurchasePolicy(self, purchasePolicy: PurchasePolicyStrategy) -> bool:
        # not implemented yet
        pass

    def getPurchasePolicyById(self, purchasePolicyId: int) -> PurchasePolicyStrategy:
        ''' 
        * Parameters: purchasePolicyId
        * This function gets a purchase policy by its ID
        * Returns: the purchase policy with the given ID
        '''
        for policy in self.__purchasePolicies:
            if policy.get_purchasePolicyId() == purchasePolicyId:
                return policy
        return None

    #LATER WE MIGHT HAVE TO ADD LOCATION OF USER AND DATE OF BIRTH
    def checkPolicies(self, basket: List[int]) -> bool:
        ''' 
        * Parameters: none
        * This function checks if the purchase policies are satisfied
        * Returns: True if the purchase policies are satisfied, False otherwise
        '''
        for policy in self.__purchasePolicies:
            if not policy.checkConstraint(basket):
               return False

        return True #TO IMPLEMENT VERSION 2
    

    def updateStoreRating(self, newRating: float) -> bool: 
        ''' 
        * Parameters: newRating
        * This function updates the rating of the store
        * Returns: True if the rating is updated successfully, False otherwise
        '''
        if newRating >= 0.0 and newRating <= 5.0:
            self.set_rating(newRating)
            logger.info('[Store] successfully updated rating of store with id: ' + str(self.__storeId))
            return True
        else:
            logger.warn('[Store] New rating is not a valid float value')
        return False
    

    def updateProductSpecRating(self, productSpecId: int, newRating: float) -> bool:
        ''' 
        * Parameters: productSpecId, newRating
        * This function updates the rating of the product
        * Returns: True if the rating is updated successfully, False otherwise
        '''
        if newRating >= 0.0 and newRating <= 5.0:
            self.__ratingsOfProductSpecId[productSpecId] = newRating
            logger.info('[Store] successfully updated rating of product specification with id: ' + str(productSpecId))
            return True
        logger.warn('[Store] New rating is not a valid integer value')
        return False
    


    def getTotalPriceOfBasketBeforeDiscount(self, basket: List[int]) -> float:
        ''' 
        * Parameters: basket
        * This function calculates the total price of the basket
        * Returns: the total price of the basket
        '''
        totalPrice = 0
        for productId in basket:
            product = self.getProductById(productId)
            if product is not None:
                totalPrice += product.get_price()
        return totalPrice
        
    def getTotalPriceOfBasketAfterDiscount(self, basket: List[int]) -> float:
        return self.getTotalPriceIfBasketBeforeDiscount(basket) #for now we assume that there is no discount
#---------------------storeFacade class---------------------#
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
            self.categories: List[Category] = []  # List to store categories
            self.productSpecifications: List[ProductSpecification] = []  # List to store product specifications
            self.stores: List[Store] = []  # List to store stores
            self.discounts: List[DiscountStrategy] = []  # List to store discounts
            self.categoryIdCounter = 0  # Counter for category IDs
            self.productSpecificationIdCounter = 0  # Counter for product specification IDs
            self.storeIdCounter = 0  # Counter for store IDs
            self.discountIdCounter = 0  # Counter for discount IDs
            self.productIdCounter = 0  # Counter for product IDs
            logger.info('successfully created storeFacade')


    def clean_data(self):
        """
        For testing purposes only
        """
        self.categories = []
        self.productSpecifications = []
        self.stores = []
        self.discounts = []
        self.categoryIdCounter = 0
        self.productSpecificationIdCounter = 0
        self.storeIdCounter = 0
        self.discountIdCounter = 0
        self.productIdCounter = 0

    def check_product_availability(self, store_id: int, product_id: int) -> bool:
        pass

    def calculate_total_price(self, basket: Dict[int, List[int]]) -> int: # store_id, product_id
        pass

    def remove_product(self, store_id:int, product_id:int) -> bool:
        pass
    #---------------------methods--------------------------------
    def addCategory(self, categoryName: str, parentCategoryId: int = None) -> bool:
        ''' 
        * Parameters: categoryName, parentCategoryId
        * This function adds a category to the store
        * Returns: True if the category is added successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to add category')
        if categoryName is not None:
            category = category(self.categoryIdCounter, categoryName, parentCategoryId)
            self.categories.append(category)
            self.categoryIdCounter += 1
            return True
        else:
            raise ValueError('Category name is not a valid string')
    

    def removeCategory(self, categoryId: int) -> bool:
        ''' 
        * Parameters: categoryId
        * This function removes a category from the store removing all connections of the category with other categories
        * Note: The subcategories of the category will be moved to the parent category of the category
        * Returns: True if the category is removed successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to remove category')
        hasParent = False
        if category.hasParentCategory():
            hasParent = True
        if categoryId is not None:
            for category in self.categories:
                if category.get_categoryId() == categoryId:
                    for subCategory in category.get_subCategories():
                        subCategory.removeParentCategory()
                        if hasParent:
                            subCategory.addParentCategory(category.get_parentCategoryId())
                    if hasParent:
                        parentCategory = self.getCategoryById(category.get_parentCategoryId())
                        parentCategory.removeSubCategory(category)
                    self.categories.remove(category)
                    return True
        else:
            raise ValueError('Category id is not a valid integer value')
        return False

    def getCategoryById(self, categoryId: int) -> Category:
        ''' 
        * Parameters: categoryId
        * This function gets a category by its ID
        * Returns: the category with the given ID
        '''
        for category in self.categories:
            if category.get_categoryId() == categoryId:
                return category
        return None
    
    def assignSubCategoryToCategory(self, subCategoryId: int, categoryId: int) -> bool:
        '''
        * Parameters: subCategoryId ,categoryId
        * This function assigns a subcategory to a category
        * Note: the parent category is assigned in the method addSubCategory of the category class
        * Returns: True if the subcategory is assigned successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to assign subcategory to category')
        if subCategoryId is not None:
            if categoryId is not None:
                subCategory = self.getCategoryById(subCategoryId)
                category = self.getCategoryById(categoryId)
                if subCategory is not None and category is not None:
                    return category.addSubCategory(subCategory)
                else:
                    logger.warn('[StoreFacade] Subcategory or category is not found')
                    return False
            else:
                raise ValueError('Category id is not a valid integer value')
        else:
            raise ValueError('Subcategory id is not a valid integer value')
            
    

    def deleteSubCategoryFromCategory(self, categoryId: int, subCategoryId: int) -> bool:
        '''
        * Parameters: categoryId, subCategoryId
        * This function deletes a subcategory from a category
        * Note: the parent category is removed in the method removeSubCategory of the category class
        * Returns: True if the subcategory is deleted successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to delete subcategory from category')
        if categoryId is not None:
            if subCategoryId is not None:
                category = self.getCategoryById(categoryId)
                subCategory = self.getCategoryById(subCategoryId)
                if category is not None and subCategory is not None:
                    return category.removeSubCategory(subCategory)
                else:
                    logger.warn('[StoreFacade] Subcategory or category is not found')
                    return False
            else:
                raise ValueError('Subcategory id is not a valid integer value')
        else:
            raise ValueError('Category id is not a valid integer value')
    
    def assignProductSpecToCategory(self, categoryId: int, productSpecId: int) -> bool:
        '''
        * Parameters: categoryId, productSpecId
        * This function assigns a product specification to a category
        * Returns: True if the product specification is assigned successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to assign product specification to category')
        if categoryId is not None:
            if productSpecId is not None:
                category = self.getCategoryById(categoryId)
                productSpec = self.getProductSpecById(productSpecId)
                if category is not None and productSpec is not None:
                    return category.addProductToCategory(productSpec)
                else:
                    logger.warn('[StoreFacade] Product specification or category is not found')
                    return False
            else:
                raise ValueError('Product specification id is not a valid integer value')
            
        else:
            raise ValueError('Category id is not a valid integer value')

    def removeProductSpecFromCategory(self, categoryId: int, productSpecId: int) -> bool:
        '''
        * Parameters: categoryId, productSpecId
        * This function removes a product specification from a category
        * Note: the product specification can only be removed if it is stored in the category itself, not in subcategories
        * Returns: True if the product specification is removed successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to remove product specification from category')
        if categoryId is not None:
            if productSpecId is not None:
                category = self.getCategoryById(categoryId)
                productSpec = self.getProductSpecById(productSpecId)
                if category is not None and productSpec is not None:
                    return category.removeProductFromCategory(productSpec)
                else:
                    logger.warn('[StoreFacade] Product specification or category is not found')
                    return False
            else:
                raise ValueError('Product specification id is not a valid integer value')
        else:
            raise ValueError('Category id is not a valid integer value')


    # used for search!
    def getProductSpecOfCategory(self, categoryId: int) -> List[ProductSpecification]:
        '''
        * Parameters: categoryId
        * This function gets all the product specifications under a category (including the productSpecs of its subCategories)
        * Returns: all the product specifications of a category
        '''
        if categoryId is not None:
            category = self.getCategoryById(categoryId)
            if category is not None:
                return category.getAllProductsRecursively()
        return []       

    def addProductSpecification(self, productName: str, weight: float, description: str, tags: List[str], manufacturer: str, storeIds: List[int] = []) -> bool:
        '''
        * Parameters: productName, weight, description, tags, manufacturer, storeIds
        * This function adds a product specification to the store
        * Returns: True if the product specification is added successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to add product specification')
        if productName is not None:
            if productName != "":
                if weight is not None:
                    if weight >= 0:
                        if manufacturer is not None and manufacturer != "":
                            productSpec = ProductSpecification(self.productSpecificationIdCounter, productName, weight, description, tags, manufacturer, storeIds)
                            self.productSpecifications.append(productSpec)
                            self.productSpecificationIdCounter += 1
                            logger.info('[StoreFacade] successfully added product specification')
                            return True
                    else:
                        logger.warn('[StoreFacade] Weight is a negative value')
                        return False
                else:
                    raise ValueError('Weight is not a valid float value')
            else:
                logger.warn('[StoreFacade] Product name is an empty string')
                return False
        else:
            raise ValueError('Product name is not a valid string')
    
    def changeWeightOfProductSpecification(self, productSpecId: int, newWeight: float) -> bool:
        '''
        * Parameters: productSpecId, newWeight
        * This function changes the weight of the product specification
        * Returns: True if the weight is changed successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to change weight of product specification')
        if productSpecId is not None:
            productSpec = self.getProductSpecById(productSpecId)
            if productSpec is not None:
                productSpec.changeWeightOfProductSpecification(newWeight)
                return True
            else:
                logger.warn('[StoreFacade] Product specification is not found')
                return False
        else:
            raise ValueError('Product specification id is not a valid integer value')
    
    def changeDescriptionOfProductSpecification(self, productSpecId: int, newDescription: str) -> bool:
        '''
        * Parameters: productSpecId, newDescription
        * This function changes the description of the product specification
        * Returns: True if the description is changed successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to change description of product specification')
        if productSpecId is not None:
            productSpec = self.getProductSpecById(productSpecId)
            if productSpec is not None:
                productSpec.changeDescriptionOfProductSpecification(newDescription)
                return True
        return False
    
    def changeManufacturerOfProductSpecification(self, productSpecId: int, newManufacturer: str) -> bool:
        '''
        * Parameters: productSpecId, newManufacturer
        * This function changes the manufacturer of the product specification
        * Returns: True if the manufacturer is changed successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to change manufacturer of product specification')
        if productSpecId is not None:
            productSpec = self.getProductSpecById(productSpecId)
            if productSpec is not None:
                productSpec.changeManufacturerOfProductSpecification(newManufacturer)
                return True
            else:
                logger.warn('[StoreFacade] Product specification is not found')
                return False
        else:
            raise ValueError('Product specification id is not a valid integer value')
    
    def changeNameOfProductSpecification(self, productSpecId: int, newName: str) -> bool:
        '''
        * Parameters: productSpecId, newName
        * This function changes the name of the product specification
        * Returns: True if the name is changed successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to change name of product specification')
        if productSpecId is not None:
            productSpec = self.getProductSpecById(productSpecId)
            if productSpec is not None:
                productSpec.changeNameOfProductSpecification(newName)
                return True
            else:
                logger.warn('[StoreFacade] Product specification is not found')
                return False
        else:
            raise ValueError('Product specification id is not a valid integer value')

    def addTagToProductSpecification(self, productSpecId: int, tag: str) -> bool:
        '''
        * Parameters: productSpecId, tag
        * This function adds a tag to the product specification
        * Returns: True if the tag is added successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to add tag to product specification')
        if productSpecId is not None:
            if tag is not None:
                productSpec = self.getProductSpecById(productSpecId)
                if productSpec is not None:
                    return productSpec.addTag(tag)
                else:
                    logger.warn('[StoreFacade] Product specification is not found')
                    return False
            else:
                raise ValueError('Tag is not a valid string')
        else:
            raise ValueError('Product specification id is not a valid integer value')


    def removeTagsFromProductSpecification(self, productSpecId: int, tag: str) -> bool:
        '''
        * Parameters: productSpecId, tag
        * This function removes a tag from the product specification
        * Returns: True if the tag is removed successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to remove tag from product specification')
        if productSpecId is not None:
            if tag is not None:
                productSpec = self.getProductSpecById(productSpecId)
                if productSpec is not None:
                    return productSpec.removeTag(tag)
                else:
                    logger.warn('[StoreFacade] Product specification is not found')
                    return False
            else:
                raise ValueError('Tag is not a valid string')
        else:
            raise ValueError('Product specification id is not a valid integer value')
        

    def getTagsOfProductSpecification(self, productSpecId: int) -> List[str]:
        '''
        * Parameters: productSpecId
        * This function gets all the tags of a product specification
        * Returns: all the tags of the product specification
        '''
        if productSpecId is not None:
            productSpec = self.getProductSpecById(productSpecId)
            if productSpec is not None:
                return productSpec.get_tags()
            else:
                logger.warn('[StoreFacade] Product specification is not found')
                return []
        else:
            raise ValueError('Product specification id is not a valid integer value')

    # used for searches
    def getProductSpecsByTags(self, tags: List[str]) -> List[ProductSpecification]:
        '''
        * Parameters: list of tags
        * This function gets all the product specifications by a given list of tags
        * Returns: all the product specifications by a given list of tags
        '''
        if tags is not None:
            productSpecs = []
            for productSpec in self.productSpecifications:
                hasAllTags = True
                for tag in tags:
                    if not productSpec.hasTag(tag):
                        hasAllTags = False
                        break
                if hasAllTags:
                    productSpecs.append(productSpec)
            return productSpecs
        else:
            raise ValueError('Tags are not a valid list of strings')   
    

    # used for searches
    def getProductSpecByName(self, productName: str) -> ProductSpecification:
        '''
        * Parameters: productName
        * This function gets a product specification by its name
        * Returns: the product specification with the given name
        '''
        for productSpec in self.productSpecifications:
            if productSpec.get_productName() == productName:
                return productSpec
        return None

    def getProductSpecById(self, productSpecId: int) -> ProductSpecification:
        '''
        * Parameters: productSpecId
        * This function gets a product specification by its ID
        * Returns: the product specification with the given ID
        '''
        for productSpec in self.productSpecifications:
            if productSpec.get_specificationId() == productSpecId:
                return productSpec
        return None


    def addStore(self, locationId: int, storeName: str, storeFounderId: int, storeProducts: List[Product] = [],
                     purchasePolicies: List[PurchasePolicyStrategy] = [], foundedDate: datetime = datetime.datetime.now(),
                        ratingsOfProductSpecId: Dict[int, int] = {}) -> bool:
        '''
        * Parameters: locationId, storeName, storeFounderId, isActive, storeProducts, purchasePolicies, foundedDate, ratingsOfProductSpecId
        * This function adds a store to the store
        * Returns: True if the store is added successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to add store')
        if storeName is not None:
            if storeName != "":
                store = Store(self.storeIdCounter, locationId, storeName, storeFounderId, storeProducts, purchasePolicies, foundedDate, ratingsOfProductSpecId)
                self.stores.append(store)
                self.storeIdCounter += 1
                return True
            else:
                logger.warn('[StoreFacade] Store name is an empty string')
                return False
        else:
            raise ValueError('Store name is not a valid string')

    def closeStore(self, storeId: int, userId: int) -> bool:
        '''
        * Parameters: storeId, userId
        * This function closes the store
        * Note: the store verifies whether the userId is the id of the founder, only the founder can close the store
        * Returns: True if the store is closed, False otherwise
        '''
        logger.info('[StoreFacade] attempting to close store')
        if storeId is not None:
            store = self.getStoreById(storeId)
            if store is not None:
                return store.closeStore(userId)
            else:
                raise ValueError('Store id is not a valid integer value')
        else:
            raise ValueError('Store id is not a valid integer value')
    
    def getStoreById(self, storeId: int) -> Store:
        '''
        * Parameters: storeId
        * This function gets a store by its ID
        * Returns: the store with the given ID
        '''
        for store in self.stores:
            if store.get_storeId() == storeId:
                return store
        return None


    def addProductToStore(self, storeId: int, productSpecificationId: int, expirationDate: datetime,
                          condition: int, price: float) -> bool: 
        '''
        * Parameters: storeId, productSpecificationId, expirationDate, condition, price
        * This function creates and adds a product to the store
        * Note: the condition is converted to a ProductCondition via the following: 1 = new, 2 = used
        * Returns: True if the product is added successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to add product to store')
        if storeId is not None:
            if productSpecificationId is not None:
                store = self.getStoreById(storeId)
                productSpec = self.getProductSpecById(productSpecificationId)
                if store is not None and productSpec is not None:
                    if expirationDate >= datetime.datetime.now():
                        if price >= 0:
                            productCondition = None
                            if condition == 1:
                                productCondition = ProductCondition.NEW
                            elif condition == 2:
                                productCondition = ProductCondition.USED
                            else:
                                return False
                            
                            product = product(self.productIdCounter, storeId, productSpec, expirationDate, productCondition, price)
                            store.addProduct(product)
                            self.productIdCounter += 1
                            return True
                        else:
                            logger.warn('[StoreFacade] Price is a negative value')
                            return False
                    else:
                        logger.warn('[StoreFacade] Expiration date is in the past')
                        return False
                else:
                    raise ValueError('Product specification id is not a valid integer value')
            else:
                raise ValueError('Product specification id is not a valid integer value')
        else:
            raise ValueError('Store id is not a valid integer value')
        

    def removeProductFromStore(self, storeId: int, productId: int) -> bool:
        '''
        * Parameters: storeId, productId
        * This function removes a product from the store
        * Note: the marketFacade is responsible for verifying whether the product is removed by someone with the necessary permissions.
        * Returns: True if the product is removed successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to remove product from store')
        if storeId is not None:
            if productId is not None:
                store = self.getStoreById(storeId)
                if store is not None:
                    return store.removeProduct(productId)
                else:
                    raise ValueError('Store not found')
            else:
                raise ValueError('Product id is not a valid integer value')
        else:
            raise ValueError('Store id is not a valid integer value')

        
    def changePriceOfProduct(self, storeId: int, productId: int, newPrice: float) -> bool:
        '''
        * Parameters: storeId, productId, newPrice
        * This function changes the price of the product
        * Note: the marketFacade is responsible for verifying whether the price is changed by someone with the necessary permissions.
        * Returns: True if the price is changed successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to change price of product')
        if storeId is not None:
            if productId is not None:
                if newPrice is not None:
                    store = self.getStoreById(storeId)
                    if store is not None:
                        product = store.getProductById(productId)
                        if product is not None:
                            return store.changePriceOfProduct(productId, newPrice)
                        else:
                            raise ValueError('Product not found')
                    else:
                        raise ValueError('Store not found')
                else:
                    raise ValueError('New price is not a valid float value')
            else:
                raise ValueError('Product id is not a valid integer value')
        else:
            raise ValueError('Store id is not a valid integer value')



    def addPurchasePolicyToStore(self, storeId: int) -> bool: #TODO: for now we dont know how to implement the purchasePolicy and what fields it receives
        '''
        * Parameters: storeId, purchasePolicy
        * This function adds a purchase policy to the store
        * Note: the marketFacade is responsible for verifying whether the purchase policy is added by someone with the necessary permissions.
        * Returns: True if the purchase policy is added successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to add purchase policy to store')
        if storeId is not None:
            #if purchasePolicy is not None:
                store = self.getStoreById(storeId)
                if store is not None:
                    return store.addPurchasePolicy()
                else:
                    raise ValueError('Store not found')

    def removePurchasePolicyFromStore(self, storeId: int, purchasePolicyId: int) -> bool:
        '''
        * Parameters: storeId, purchasePolicyId
        * This function removes a purchase policy from the store
        * Note: the marketFacade is responsible for verifying whether the purchase policy is removed by someone with the necessary permissions.
        * Returns: True if the purchase policy is removed successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to remove purchase policy from store')
        if storeId is not None:
            if purchasePolicyId is not None:
                store = self.getStoreById(storeId)
                if store is not None:
                    purchasePolicy = store.getPurchasePolicyById(purchasePolicyId)
                    if purchasePolicy is not None:
                        return store.removePurchasePolicy(purchasePolicy)
                    else:
                        raise ValueError('Purchase policy not found')
                else:
                    raise ValueError('Store not found')
            else:
                raise ValueError('Purchase policy id is not a valid integer value')
        else:
            raise ValueError('Store id is not a valid integer value')

    def updatePurchasePolicyOfStore(self, storeId: int, purchasePolicyId: int) -> bool:
        pass


    def checkPoliciesOfStore(self, storeId: int, basket: List[int]) -> bool:
        return True #in the meantime

    def updateStoreRating(self, storeId: int, newRating: float) -> bool:
        '''
        * Parameters: storeId, newRating
        * This function updates the rating of the store
        * Returns: True if the rating is updated successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to update rating of store')
        if storeId is not None:
            if newRating is not None:
                if newRating >= 0.0:
                    if newRating <= 5.0:
                        store = self.getStoreById(storeId)
                        if store is not None:
                            return store.updateStoreRating(newRating)
                        else:
                            raise ValueError('Store not found')
                    else:
                        logger.warn('[StoreFacade] New rating is greater than 5')
                        return False
                else:
                    logger.warn('[StoreFacade] New rating is negative')
                    return False
            else:
                raise ValueError('New rating is not a valid float value')
        else:
            raise ValueError('Store id is not a valid integer value')


    def updateProductSpecRating(self, storeId: int, productSpecId: int, newRating: float) -> bool:
        '''
        * Parameters: storeId, productSpecId, newRating
        * This function updates the rating of the product specification
        * Returns: True if the rating is updated successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to update rating of product specification')
        if storeId is not None:
            if productSpecId is not None:
                if newRating is not None:
                    if newRating >= 0.0: 
                        if newRating <= 5.0:
                            store = self.getStoreById(storeId)
                            if store is not None:
                                return store.updateProductSpecRating(productSpecId, newRating)
                            else:
                                raise ValueError('Store not found')
                        else:
                            logger.warn('[StoreFacade] New rating is greater than 5')
                            return False
                    else:
                        logger.warn('[StoreFacade] New rating is negative')
                        return False
                else:
                    raise ValueError('New rating is not a valid float value')
            else:
                raise ValueError('Product specification id is not a valid integer value')
        else:
            raise ValueError('Store id is not a valid integer value')

    
    # we assume that the marketFacade verified that the user has necessary permissions to add a discount    
    def addDiscount(self, description: str, startDate: datetime, endingDate: datetime, percentage: float) -> bool:
        '''
        * Parameters: description, startDate, endingDate, percentage
        * This function adds a discount to the store
        * Returns: True if the discount is added successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to add discount')
        if description is not None:
            if startDate is not None:
                if endingDate is not None:
                    if endingDate > startDate:
                        if percentage is not None:
                            if percentage >= 0.0 and percentage <= 1.0:
                                discount = DiscountStrategy(self.discountIdCounter, description, startDate, endingDate, percentage)
                                self.discounts.append(discount)
                                self.discountIdCounter += 1
                                return True
                            else:
                                logger.warn('[StoreFacade] Percentage is not between 0 and 1')
                                return False
                        else:
                            raise ValueError('Percentage is not a valid float value')
                    else:
                        logger.warn('[StoreFacade] Ending date is before start date')
                        return False
                else:
                    raise ValueError('Ending date is not a valid datetime value')
            else:
                raise ValueError('Start date is not a valid datetime value')
        else:
            raise ValueError('Description is not a valid string')


    # we assume that the marketFacade verified that the user has necessary permissions to remove a discount
    def removeDiscount(self, discountId: int) -> bool:
        ''' 
        * Parameters: discountId
        * This function removes a discount from the store
        * Returns: True if the discount is removed successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to remove discount')
        if discountId is not None:
            discount = self.getDiscountByDiscountId(discountId)
            if discount is not None:
                self.__discounts.remove(discount)
                return True
            else:
                logger.warn('[StoreFacade] Discount not found')
                return False
        else:
            raise ValueError('Discount id is not a valid integer value')

    def changeDiscountPercentage(self, discountId: int, newPercentage: float) -> bool:
        '''
        * Parameters: discountId, newPercentage
        * This function changes the percentage of the discount
        * Returns: True if the percentage is changed successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to change percentage of discount')
        if discountId is not None:
            if newPercentage is not None:
                discount = self.getDiscountByDiscountId(discountId)
                if discount is not None:
                    return discount.changeDiscountPercentage(newPercentage)
                else:
                    logger.warn('[StoreFacade] Discount not found')
                    return False
            else:
                raise ValueError('New percentage is not a valid float value')
        else:
            raise ValueError('Discount id is not a valid integer value')
        
    
    def changeDiscountDescription(self, discountId: int, newDescription: str) -> bool:
        '''
        * Parameters: discountId, newDescription
        * This function changes the description of the discount
        * Returns: True if the description is changed successfully, False otherwise
        '''
        logger.info('[StoreFacade] attempting to change description of discount')
        if discountId is not None:
            if newDescription is not None:
                discount = self.getDiscountByDiscountId(discountId)
                if discount is not None:
                    return discount.changeDiscountDescription(newDescription)
                else:
                    logger.warn('[StoreFacade] Discount not found')
                    return False
            else:
                raise ValueError('New description is not a valid string')
        else:
            raise ValueError('Discount id is not a valid integer value')
    
    def getDiscountByStore(self, storeId: int) -> List[DiscountStrategy]:
        # not implemented yet
        pass

    def getDiscountByProduct(self, productId: int) -> List[DiscountStrategy]:
        # not implemented yet
        pass

    def getDiscountByCategory(self, categoryId: int) -> List[DiscountStrategy]:
        # not implemented yet
        pass

    def getDiscountByDiscountId(self, discountId: int) -> DiscountStrategy:
        '''
        * Parameters: discountId
        * This function gets a discount by its ID
        * Returns: the discount with the given ID
        '''
        for discount in self.__discounts:
            if discount.getDiscountId() == discountId:
                return discount
        return None


    def applyDiscounts(self, shoppingCart: List[Tuple[int,List[int]]]) -> float:
        # not implemented yet
        pass


    def getTotalPriceBeforeDiscount(self, shoppingCart: List[Tuple[int,List[int]]]) -> float:
        ''' 
        * Parameters: shoppingCart
        * This function calculates the total price of the shopping cart before applying any discounts
        * Returns: the total price of the shopping cart before applying any discounts
        '''
        totalPrice = 0
        for basket in shoppingCart:
            store = self.getStoreById(basket[0])
            totalPrice = store.getTotalPriceOfBasketBeforeDiscount(basket[1])
        return totalPrice
            
    def getTotalPriceAfterDiscount(self, shoppingCart: List[Tuple[int,List[int]]]) -> float:
        '''
        * Parameters: shoppingCart
        * This function calculates the total price of the shopping cart after applying all discounts
        * Returns: the total price of the shopping cart after applying all discounts
        '''
        return self.getTotalPriceBeforeDiscount(shoppingCart) # not implemented yet VERSION 2
      

    #--------------------methods for market facade used by users team---------------------------#
    def check_product_availability(self, store_id: int, product_id: int):
        '''
        * Parameters: store_id, product_id
        * This function checks if the product is available in the store
        * Returns: True if the product is available, False otherwise
        '''
        store = self.getStoreById(store_id)
        if store is not None:
            for product in store.get_products():
                if product.get_productId() == product_id:
                    return True
            return False
        else:
            raise ValueError('Store not found')
        
    def calculate_total_price(self, basket: Dict[int, List[int]]) -> int:
        '''
        * Parameters: basket
        * This function calculates the total price of the basket
        * Returns: the total price of the basket
        '''
        totalPrice = 0
        for storeId, productIds in basket.items():
            store = self.getStoreById(storeId)
            totalPrice += store.getTotalPriceOfBasketAfterDiscount(productIds)
        return totalPrice
    