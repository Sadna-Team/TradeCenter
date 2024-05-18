#---------- Imports ------------#
from enum import Enum
from typing import List, Dict
import datetime

#-------- Magic Numbers --------#
POUNDS_PER_KILOGRAM = 2.20462


#---------------------productCondition Enum---------------------#
class productCondition(Enum):
    NEW = 1
    USED = 2

productCondition = Enum('productCondition', ['NEW', 'USED'])


#---------------------product class---------------------#
class product:
    # id of product is productId. It is unique for each physical product
    def __init__(self, productId: int, storeId: int, specificationId: int, expirationDate: datetime,
                condition: productCondition, price: float):
        self.__productId = productId
        self.__storeId = storeId
        self.__specificationId = specificationId
        self.__expirationDate = expirationDate
        self.__condition = condition
        self.__price = price # price is in dollars


    #---------------------getters and setters---------------------
    @property
    def get_productId(self) -> int:
        return self.__productId
    
    @property
    def set_productId(self, productId: int):
        self.__productId = productId

    @property
    def get_storeId(self) -> int:
        return self.__storeId
    
    @property
    def set_storeId(self, storeId: int):
        self.__storeId = storeId

    @property
    def get_specificationId(self) -> int:
        return self.__specificationId
    
    @property
    def set_specificationId(self, specificationId: int):
        self.__specificationId = specificationId

    @property
    def get_expirationDate(self) -> datetime:
        return self.__expirationDate
    
    @property
    def set_expirationDate(self, expirationDate: datetime):
        self.__expirationDate = expirationDate

    @property
    def get_condition(self) -> productCondition:
        return self.__condition
    
    @property   
    def set_condition(self, condition: productCondition):
        self.__condition = condition

    @property
    def get_price(self) -> float:
        return self.__price
    
    @property
    def set_price(self, price: float):
        self.__price = price
    

    #---------------------methods--------------------------------
    def isExpired(self) -> bool:
        ''' 
        * Parameters: none
        * This function checks whether the product is expired or not
        * Returns: True if the product is expired, False otherwise
        '''
        return self.__expirationDate < datetime.datetime.now()


#---------------------productSpecification class---------------------#
class productSpecification:
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


    #---------------------getters and setters---------------------
    @property
    def get_specificationId(self) -> int:
        return self.__specificationId

    @property
    def set_specificationId(self, specificationId: int):
        self.__specificationId = specificationId

    @property
    def get_productName(self) -> str:
        return self.__productName

    @property
    def set_productName(self, productName: str):
        self.__productName = productName

    @property
    def get_weight(self) -> float:
        return self.__weight

    @property
    def set_weight(self, weight: float):
        self.__weight = weight

    @property
    def get_description(self) -> str:
        return self.__description

    @property
    def set_description(self, description: str):
        self.__description = description

    @property
    def get_tags(self) -> List[str]:
        return self.__tags

    @property
    def set_tags(self, tags: List[str]):
        self.__tags = tags

    @property
    def get_manufacturer(self) -> str:
        return self.__manufacturer

    @property
    def set_manufacturer(self, manufacturer: str):
        self.__manufacturer = manufacturer

    @property
    def get_storeIds(self) -> List[int]:
        return self.__storeIds
    
    @property
    def set_storeIds(self, storeIds: List[int]):
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
                return True
        return False
    

    def removeTag(self, tag: str) -> bool:
        ''' 
        * Parameters: tag
        * This function removes a tag from the product specification
        * Returns: none
        '''
        if tag is not None:
            if tag in self.__tags:
                self.__tags.remove(tag)
                return True
        return False
    

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
                return True
        return False


    def removeStoreId(self, storeId: int) -> bool:
        ''' 
        * Parameters: storeId
        * This function removes a store id from the product specification
        * Returns: true if successfully removed store id, false otherwise
        '''
        if storeId is not None:
            if storeId in self.__storeIds:
                self.__storeIds.remove(storeId)
                return True
        return False


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
    

#---------------------category class---------------------#
class category:
    # id of category is categoryId. It is unique for each category. Products are stored in either the category or found in one of its subcategories
    # important to note: a category can only have one parentcategory, and a category can't have a subcategory that is already a subcategory of a subcategory.
    def __init__(self, categoryId: int, categoryName: str, parentCategoryId: int = None, categoryProducts: List[productSpecificationint] = [], subCategories: List['category'] = []):
        self.__categoryId = categoryId
        self.__categoryName = categoryName
        self.__parentCategoryId = parentCategoryId
        self.__categoryProducts = categoryProducts
        self.__subCategories = subCategories



    #---------------------getters and setters---------------------
    @property
    def get_categoryId(self) -> int:
        return self.__categoryId
    
    @property
    def set_categoryId(self, categoryId: int):
        self.__categoryId = categoryId

    @property
    def get_categoryName(self) -> str:
        return self.__categoryName
    
    @property
    def set_categoryName(self, categoryName: str):
        self.__categoryName = categoryName

    @property
    def get_parentCategoryId(self) -> int:
        return self.__parentCategoryId
    
    @property
    def set_parentCategoryId(self, parentCategoryId: int):
        self.__parentCategoryId = parentCategoryId

    @property
    def get_categoryProducts(self) -> List[productSpecification]:
        return self.__categoryProducts
    
    @property
    def set_categoryProducts(self, categoryProducts: List[productSpecification]):
        self.__categoryProducts = categoryProducts

    @property
    def get_subCategories(self) -> List['category']:
        return self.__subCategories
    
    @property
    def set_subCategories(self, subCategories: List['category']):
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

    
    def removeParentCategory(self):
        ''' 
        * Parameters: none
        * This function removes the parent category of the category
        * Returns: none
        '''
        if self.__parentCategoryId is not None:
            self.set_parentCategoryId(None)


    def addSubCategory(self, subCategory: 'category') -> bool:
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
                        return True
        return False
    

    def removeSubCategory(self, subCategory: 'category') -> bool:
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
                    return True
        return False
    

    def isParentCategory(self, category: 'category') -> bool:
        ''' 
        * Parameters: category
        * This function checks that the given category is the parent category of the current category
        * Returns: True if the given category is the parent category of the current category, False otherwise
        '''
        return self.__parentCategoryId == category.get_categoryId()
    

    def isSubCategory(self, category: 'category') -> bool:
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
        return self.__parentCategoryId is not None

    
    def addProductToCategory(self, product: productSpecification) -> bool:
        ''' 
        * Parameters: product
        * This function adds a product to the category
        * Returns: True if the product is added successfully, False otherwise
        '''
        if product is not None:
            if product not in self.getAllProductsRecursively():
                self.__categoryProducts.append(product)
                return True
        return False
    

    def removeProductFromCategory(self, product: productSpecification) -> bool:
        ''' 
        * Parameters: product
        * This function removes a product from the category
        * Returns: True if the product is removed successfully, False otherwise
        '''
        if product is not None:
            if product in self.__categoryProducts:
                self.__categoryProducts.remove(product)
                return True
            return False
    
    
    def getAllProductsRecursively(self) -> List[productSpecification]:
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
class store: 
    # id of store is storeId. It is unique for each store
    def __init__(self, storeId: int, locationId: int, storeName: str, storeFounderId: int,  
                 isActive: bool, storeProducts: List[product] = [], discounts: List[discountStrategy] = [],
                   purchasePolicies: List[purchasePolicyStrategy] = [], foundedDate: datetime = datetime.datetime.now(), 
                   ratingsOfProductSpecId: Dict[int, int] = {}):
        self.__storeId = storeId
        self.__locationId = locationId
        self.__storeName = storeName
        self.__storeFounderId = storeFounderId
        self.__rating = 0
        self.__isActive = isActive
        self.__storeProducts = storeProducts
        self.__discounts = discounts
        self.__purchasePolicies = purchasePolicies
        self.__foundedDate = foundedDate        
        self.__ratingsOfProductSpecId = ratingsOfProductSpecId
        

    #---------------------getters and setters---------------------#
    @property
    def get_storeId(self) -> int:
        return self.__storeId
    
    @property
    def set_storeId(self, storeId: int):
        self.__storeId = storeId

    @property
    def get_locationId(self) -> int:
        return self.__locationId
    
    @property
    def set_locationId(self, locationId: int):
        self.__locationId = locationId

    @property
    def get_storeName(self) -> str:
        return self.__storeName
    
    @property
    def set_storeName(self, storeName: str):
        self.__storeName = storeName

    @property
    def get_storeFounderId(self) -> int:
        return self.__storeFounderId
    
    @property
    def set_storeFounderId(self, storeFounderId: int):
        self.__storeFounderId = storeFounderId

    @property
    def get_rating(self) -> int:
        return self.__rating
    
    @property
    def set_rating(self, rating: int):
        self.__rating = rating

    @property
    def get_isActive(self) -> bool:
        return self.__isActive
    
    @property
    def set_isActive(self, isActive: bool):
        self.__isActive = isActive

    @property
    def get_storeProducts(self) -> List[product]:
        return self.__storeProducts
    
    @property
    def set_storeProducts(self, storeProducts: List[product]):
        self.__storeProducts = storeProducts

    @property
    def get_discounts(self) -> List[discountStrategy]:
        return self.__discounts
    
    @property
    def set_discounts(self, discounts: List[discountStrategy]):
        self.__discounts = discounts

    @property
    def get_purchasePolicies(self) -> List[purchasePolicyStrategy]:
        return self.__purchasePolicies
    
    @property
    def set_purchasePolicies(self, purchasePolicies: List[purchasePolicyStrategy]):
        self.__purchasePolicies = purchasePolicies

    @property
    def get_foundedDate(self) -> datetime:
        return self.__foundedDate
    
    @property
    def set_foundedDate(self, foundedDate: datetime):
        self.__foundedDate = foundedDate

    @property
    def get_ratingsOfProductSpecId(self) -> Dict[int, int]:
        return self.__ratingsOfProductSpecId
    

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
            return True
        return False
    

    # We assume that the marketFacade verified that the user attempting to add the product is a store Owner
    def addProduct(self, product: product) -> bool:
        ''' 
        * Parameters: product
        * This function adds a product to the store, and initializes the rating of the product to 0
        * Returns: True if the product is added successfully, False otherwise
        '''
        if product is not None:
            if product not in self.__storeProducts:
                self.__storeProducts.append(product)
                self.__ratingsOfProductSpecId[product.get_specificationId()] = 0
                return True
        return False
    
    # We assume that the marketFacade verified that the user attempting to remove the product is a store owner/purchased by a user
    def removeProduct(self, product: product) -> bool:
        ''' 
        * Parameters: product
        * This function removes a product from the store
        * Returns: True if the product is removed successfully, False otherwise
        '''
        if product is not None:
            if product in self.__storeProducts:
                self.__storeProducts.remove(product)
                return True
        return False

    # we assume that the marketFacade verified that the user has necessary permissions to add a discount    
    def addDiscount(self, discount: discountStrategy) -> bool:
        ''' 
        * Parameters: discount
        * This function adds a discount to the store
        * Returns: True if the discount is added successfully, False otherwise
        '''
        if discount is not None:
            if discount not in self.__discounts:
                self.__discounts.append(discount)
                return True
        return False
    
    # we assume that the marketFacade verified that the user has necessary permissions to remove a discount
    def removeDiscount(self, discount: discountStrategy) -> bool:
        ''' 
        * Parameters: discount
        * This function removes a discount from the store
        * Returns: True if the discount is removed successfully, False otherwise
        '''
        if discount is not None:
            if discount in self.__discounts:
                self.__discounts.remove(discount)
                return True
        return False
    

    # we assume that the marketFacade verified that the user has necessary permissions to add a purchase policy
    def addPurchasePolicy(self, purchasePolicy: purchasePolicyStrategy) -> bool:
        ''' 
        * Parameters: purchasePolicy
        * This function adds a purchase policy to the store
        * Returns: True if the purchase policy is added successfully, False otherwise
        '''
        if purchasePolicy is not None:
            if purchasePolicy not in self.__purchasePolicies:
                self.__purchasePolicies.append(purchasePolicy)
                return True
        return False
    

    # we assume that the marketFacade verified that the user has necessary permissions to remove a purchase policy
    def removePurchasePolicy(self, purchasePolicy: purchasePolicyStrategy) -> bool:
        ''' 
        * Parameters: purchasePolicy
        * This function removes a purchase policy from the store
        * Returns: True if the purchase policy is removed successfully, False otherwise
        '''
        if purchasePolicy is not None:
            if purchasePolicy in self.__purchasePolicies:
                self.__purchasePolicies.remove(purchasePolicy)
                return True
        return False
    

    def updateStoreRating(self, newRating: int) -> bool:
        ''' 
        * Parameters: newRating
        * This function updates the rating of the store
        * Returns: True if the rating is updated successfully, False otherwise
        '''
        if newRating >= 0 and newRating <= 5:
            self.set_rating(newRating)
            return True
        return False
    

    def updateProductSpecRating(self, productSpecId: int, newRating: int) -> bool:
        ''' 
        * Parameters: productSpecId, newRating
        * This function updates the rating of the product
        * Returns: True if the rating is updated successfully, False otherwise
        '''
        if newRating >= 0 and newRating <= 5:
            self.__ratingsOfProductSpecId[productSpecId] = newRating
            return True
        return False
    

#---------------------storeFacade class---------------------#
class StoreFacade:
    # singleton
    __instance = None

    def __new__(cls):
        if StoreFacade.__instance is None:
            StoreFacade.__instance = object.__new__(cls)
        return StoreFacade.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.categories = []  # List to store categories
            self.productSpecifications = []  # List to store product specifications
            self.stores = []  # List to store stores
            self.categoryIdCounter = 0  # Counter for category IDs
            self.productSpecificationIdCounter = 0  # Counter for product specification IDs
            self.storeIdCounter = 0  # Counter for store IDs

    
    #---------------------methods--------------------------------
    def addCategory(self, categoryName: str, parentCategoryId: int = None) -> bool:
        ''' 
        * Parameters: categoryName, parentCategoryId
        * This function adds a category to the store
        * Returns: True if the category is added successfully, False otherwise
        '''
        if categoryName is not None:
            category = category(self.categoryIdCounter, categoryName, parentCategoryId)
            self.categories.append(category)
            self.categoryIdCounter += 1
            return True
        return False
    

    def removeCategory(self, categoryId: int) -> bool:
        ''' 
        * Parameters: categoryId
        * This function removes a category from the store removing all connections of the category with other categories
        * Returns: True if the category is removed successfully, False otherwise
        '''
        if categoryId is not None:
            for category in self.categories:
                if category.get_categoryId() == categoryId:
                    for subCategory in category.get_subCategories():
                        subCategory.removeParentCategory()
                    if category.hasParentCategory():
                        parentCategory = self.getCategoryById(category.get_parentCategoryId())
                        parentCategory.removeSubCategory(category)
                    self.categories.remove(category)
                    return True
        return False

    def getCategoryById(self, categoryId: int) -> category:
        ''' 
        * Parameters: categoryId
        * This function gets a category by its ID
        * Returns: the category with the given ID
        '''
        for category in self.categories:
            if category.get_categoryId() == categoryId:
                return category
        return None
    
    //add subCategory to category, make sure to also add the parentCategory



    


