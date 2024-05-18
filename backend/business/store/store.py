#---------- Imports ------------#
from enum import Enum
from typing import List
import datetime

#-------- Magic Numbers --------#
POUNDS_PER_KILOGRAM = 2.20462

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
            # here you can add fields




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
    
    
    


    


    


 


    


    


