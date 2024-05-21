from .user import UserFacade
from .authentication.authentication import Authentication
from .roles import RolesFacade
from .DTOs import NotificationDTO
from .store import StoreFacade
from .purchase import PurchaseFacade
from .ThirdPartyHandlers import PaymentHandler, SupplyHandler
from .notifier import Notifier
from typing import Optional, List, Dict, Tuple
import datetime
import threading
import logging

logger = logging.getLogger('myapp')

class AddressDTO:
    def __init__(self, address_id, address, city, state, country, postal_code):
        self.address_id = address_id
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code

    def to_dict(self):
        return {
            'address_id': self.address_id,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code
        }


class MarketFacade:
    # singleton
    __instance = None
    __lock = threading.Lock()

    def __new__(cls):
        if MarketFacade.__instance is None:
            MarketFacade.__instance = object.__new__(cls)
        return MarketFacade.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True

            # initialize all the facades
            self.user_facade = UserFacade()
            self.store_facade = StoreFacade()
            self.roles_facade = RolesFacade()
            self.purchase_facade = PurchaseFacade()
            self.addresses = []
            self.auth_facade = Authentication()
            self.notifier = Notifier()

            # create the admin?
            self.__create_admin()

    def __create_admin(self, currency: str = "USD") -> None:
        man_id = self.user_facade.create_user(currency)
        hashed_password = self.auth_facade.hash_password("admin")
        self.user_facade.register_user(man_id, "admin@admin.com", "admin", hashed_password, 2000, 1, 1, "123456789")
        self.roles_facade.add_admin(man_id)

    def clean_data(self):
        """
        For testing purposes only
        """
        self.user_facade.clean_data()
        self.store_facade.clean_data()
        self.roles_facade.clean_data()
        # create the admin?

    def show_notifications(self, user_id: int) -> List[NotificationDTO]:
        return self.user_facade.get_notifications(user_id)

    def add_product_to_basket(self, user_id: int, store_id: int, product_id: int):
        with MarketFacade.__lock:
            if self.store_facade.check_product_availability(store_id, product_id):
                self.user_facade.add_product_to_basket(user_id, store_id, product_id)
                
                
                
                

    def checkout(self, user_id: int, payment_details: Dict, address: Dict): #needs a whole revamp to work with the discounts and purchase policies and location restrictions
        cart = self.user_facade.get_shopping_cart(user_id)
        
        
        # lock the __lock
        with MarketFacade.__lock:
            # check if the products are still available
            for store_id, products in cart.items():
                for product_id in products:
                    if not self.store_facade.check_product_availability(store_id, product_id):
                        raise ValueError(f"Product {product_id} is not available in the required amount")
                    

            # TODO: create an immediate purchase
            

            # TODO: calculate the discounts of the purchase using storeFacade
                        
            # TODO: calculate the policies of the purchase using storeFacade + user location constraints
            

            # TODO: attempt to find a delivery method for user
            deliveryDate= datetime.datetime.now() #dummy
            
        
                #if not found, invalidate purchase
                #self.purchase_facade.invalidatePurchaseOfUser(purchaseId, user_id)

                
                
                
                
            # charge the user:
            
            amount = self.store_facade.calculate_total_price(cart)
            if "payment method" not in payment_details:
                #invalidate Purchase
                self.purchase_facade.invalidatePurchaseOfUser(purchaseId, user_id)
                raise ValueError("Payment method not specified")
            
            if not PaymentHandler().process_payment(amount, payment_details):
                #invalidate Purchase
                self.purchase_facade.invalidatePurchaseOfUser(purchaseId, user_id)
                raise ValueError("Payment failed")


            # remove the products from the store
            for store_id, products in basket.items():  #TODO: fix basket???
                for product_id in products:
                    self.store_facade.removeProductFromStore(store_id, product_id)
                    
                    
            #if successful, validate purchase with deliveryDate
            self.purchase_facade.validatePurchaseOfUser(purchaseId, user_id, deliveryDate)

            
            
            
        # clear the cart
        self.user_facade.clear_basket(user_id)

        package_details = {'shopping cart': cart, 'address': address}
        if "supply method" not in package_details:
            raise ValueError("Supply method not specified")
        if package_details.get("supply method") not in self.supported_supply_methods:
            raise ValueError("Invalid supply method")
        if not SupplyHandler().process_supply(package_details, user_id):
            raise ValueError("Supply failed")
        for store_id in cart.keys():
            Notifier().notify_new_purchase(store_id, user_id)
            
            
            
            
            

    def nominate_store_owner(self, store_id: int, owner_id: int, new_owner_id: int):
        nomination_id = self.roles_facade.nominate_owner(store_id, owner_id, new_owner_id)
        # TODO: different implementation later
        self.user_facade.notify_user(-1, NotificationDTO(
            f"You have been nominated to be the owner of store {store_id}", nomination_id))

    def nominate_store_manager(self, store_id: int, owner_id: int, new_manager_id: int):
        nomination_id = self.roles_facade.nominate_manager(store_id, owner_id, new_manager_id)
        self.user_facade.notify_user(-1, NotificationDTO(
            f"You have been nominated to be the manager of store {store_id}", nomination_id))

    def accept_nomination(self, user_id: int, nomination_id: int, accept: bool):
        if accept:
            self.roles_facade.accept_nomination(nomination_id, user_id)
        else:
            self.roles_facade.decline_nomination(nomination_id, user_id)

    def change_permissions(self, actor_id: int, store_id: int, manager_id: int, add_product: bool,
                           change_purchase_policy: bool, change_purchase_types: bool, change_discount_policy: bool,
                           change_discount_types: bool, add_manager: bool, get_bid: bool):
        self.roles_facade.set_manager_permissions(store_id, actor_id, manager_id, add_product, change_purchase_policy,
                                                  change_purchase_types, change_discount_policy, change_discount_types,
                                                  add_manager, get_bid)

    def add_system_manager(self, actor: int, user_id: int):
        self.roles_facade.add_system_manager(actor, user_id)

    def remove_system_manager(self, actor: int, user_id: int):
        self.roles_facade.remove_system_manager(actor, user_id)

    def add_payment_method(self, method_name: str, payment_config: Dict):
        PaymentHandler().add_payment_method(method_name, payment_config)
    
    def edit_payment_method(self, method_name: str, editing_data: Dict):
        PaymentHandler().edit_payment_method(method_name, editing_data)

    def remove_payment_method(self, method_name: str):
        PaymentHandler().remove_payment_method(method_name)

    def add_supply_method(self, method_name: str, supply_config: Dict):
        SupplyHandler().add_supply_method(method_name, supply_config)

    def edit_supply_method(self, method_name: str, editing_data: Dict):
        SupplyHandler().edit_supply_method(method_name, editing_data)

    def remove_supply_method(self, method_name: str):
        SupplyHandler().remove_supply_method(method_name)

    #-------------------------------------- Store Related Methods --------------------------------------#
    def searchByCategory(self, categoryId: int, sortType: int) -> List[Tuple[Tuple[int, int], Tuple[float,float]]]:
        '''
        * Parameters: categoryId, sortByLowesToHighestPrice
        * This function returns the list of all productIds
        * Note: if sortType is 1, the list will be sorted by lowest to highest price, 2 is highest to lowest, 3 is by rating lowest to Highest, 4 is by highest to lowest
        * Returns a list of product ids of the products in the category with categoryId
        '''
        productSpecificationsOfCategory = self.store_facade.getProductSpecOfCategory(categoryId)
        productIdsToStore = [Tuple[Tuple[int, int], Tuple[float,float]]]
        for store in self.store_facade.stores():
            for product in store.products():
                if product.get_specificationId() in productSpecificationsOfCategory:
                    productIdsToStore.append((product.get_productId(), product.get_specificationId(), store.get_storeId(), store.get_storeName(), product.get_price(), store.get_ratingOfProductSpecId()[product.get_specificationId()]))
        if sortType == 1:
            productIdsToStore.sort(key=lambda x: x[1][0])
        elif sortType == 2:
            productIdsToStore.sort(key=lambda x: x[1][0], reverse=True)
        elif sortType == 3:
            productIdsToStore.sort(key=lambda x: x[1][1])
        elif sortType == 4:
            productIdsToStore.sort(key=lambda x: x[1][1], reverse=True)
        return productIdsToStore
        
    def searchByTags(self, tags: List[str], sortType: int) -> List[Tuple[Tuple[int, int], Tuple[float,float]]]:
        '''
        * Parameters: tags, sortByLowesToHighestPrice
        * This function returns the list of all productIds
        * Note: if sortType is 1, the list will be sorted by lowest to highest price, 2 is highest to lowest, 3 is by rating lowest to Highest, 4 is by highest to lowest
        * Returns a list of product ids of the products with the tags in tags
        '''
        productSpecificationsOfTags = self.store_facade.getProductSpecOfTags(tags)
        productIdsToStore = [Tuple[Tuple[int, int], Tuple[float, float]]]
        for store in self.store_facade.stores():
            for product in store.products():
                if product.get_specificationId() in productSpecificationsOfTags:
                    productIdsToStore.append((product.get_productId(), product.get_specificationId(), store.get_storeId(), store.get_storeName(), product.get_price(), store.get_ratingOfProductSpecId()[product.get_specificationId()]))

        if sortType == 1:
            productIdsToStore.sort(key=lambda x: x[1][0])
        elif sortType == 2:
            productIdsToStore.sort(key=lambda x: x[1][0], reverse=True)
        elif sortType == 3:
            productIdsToStore.sort(key=lambda x: x[1][1])
        elif sortType == 4:
            productIdsToStore.sort(key=lambda x: x[1][1], reverse=True)
        return productIdsToStore
    
    def searchByNames(self, name: str, sortType: int) -> List[Tuple[Tuple[int, int], Tuple[float,float]]]:
        '''
        * Parameters: names, sortByLowesToHighestPrice
        * This function returns the list of all productIds
        * Note: if sortType is 1, the list will be sorted by lowest to highest price, 2 is highest to lowest, 3 is by rating lowest to Highest, 4 is by highest to lowest
        * Returns a list of product ids of the products with the names in names
        '''
        productSpecificationsOfNames = self.store_facade.getProductSpecByName(name)
        productIdsToStore = [Tuple[Tuple[int, int], Tuple[float, float]]]
        for store in self.store_facade.stores():
            for product in store.products():
                if product.get_specificationId() in productSpecificationsOfNames:
                    productIdsToStore.append((product.get_productId(), product.get_specificationId(), store.get_storeId(), store.get_storeName(), product.get_price(), store.get_ratingOfProductSpecId()[product.get_specificationId()]))

        if sortType == 1:
            productIdsToStore.sort(key=lambda x: x[1][0])
        elif sortType == 2:
            productIdsToStore.sort(key=lambda x: x[1][0], reverse=True)
        elif sortType == 3:
            productIdsToStore.sort(key=lambda x: x[1][1])
        elif sortType == 4:
            productIdsToStore.sort(key=lambda x: x[1][1], reverse=True)
        return productIdsToStore


#-------------Discount related methods-------------------#
    def addDiscount(self, userId: int, description: str, startDate: datetime, endingDate: datetime, percentage: float): #later on we need to support the creation of different types of discounts using hasStoreId?: int etc, maybe wildcards could be useful
        #TODO: check if user has necessary permissions to add a discount
        #if self.roles_facade.check_permissions(userId, "add_discount"):
        if self.store_facade.addDiscount(description, startDate, endingDate, percentage):
            logger.info(f"User {userId} has added a discount")
        else:
            logger.info(f"User {userId} has failed to add a discount")
        

    def changeDiscount(self, user_id: int, discount_id: int):
        #TODO: not implemented yet, but supported partially in purchaseFacade, see changeDiscountPercentage for example
        pass

    def removeDiscount(self, user_id: int, discount_id: int):
        #TODO: check if user has necessary permissions to remove a discount
        #if self.roles_facade.check_permissions(userId, "remove_discount"):
        if self.store_facade.removeDiscount(discount_id):
            logger.info(f"User {user_id} has removed a discount")
        else:
            logger.info(f"User {user_id} has failed to remove a discount")


#-------------Rating related methods-------------------#
    def addStoreRating(self, user_id: int, purchase_id: int, description: str, rating: float):
        '''
        * Parameters: user_id, purchase_id, description, rating
        * This function adds a rating to a store
        * Returns None
        '''
        storeId = self.purchase_facade.getPurchaseById(purchase_id).get_storeId()
        newRating = self.purchase_facade.rateStore(purchase_id, user_id, storeId, rating, description)
        if newRating is not None:
            self.store_facade.updateStoreRating(storeId, newRating)
            logger.info(f"User {user_id} has rated store {storeId} with {rating}")
        else:
            logger.info(f"User {user_id} has failed to rate store {storeId}")

    

    def addProductRating(self, user_id: int, purchase_id:int, description: str, productSpec_id: int, rating: float):
        '''
        * Parameters: user_id, purchase_id, description, productSpec_id, rating
        * This function adds a rating to a product
        * Returns None
        '''
        storeId = self.purchase_facade.getPurchaseById(purchase_id).get_storeId()
        newRating = self.purchase_facade.rateProduct(purchase_id, user_id, storeId, productSpec_id, rating, description)
        if newRating is not None:
            self.store_facade.updateProductRating(storeId, productSpec_id, newRating)
            logger.info(f"User {user_id} has rated product {productSpec_id} with {rating}")
        else:
            logger.info(f"User {user_id} has failed to rate product {productSpec_id}")


#-------------Policies related methods-------------------#
    def addPurchasePolicy(self, userId: int, store_id: int): #for now, we dont support the creation of different types of policies
        '''
        * Parameters: userId, store_id
        * This function adds a purchase policy to the store
        * Returns None
        '''
        if self.roles_facade.has_change_purchase_policy_permission(store_id, userId):
            self.store_facade.addPurchasePolicyToStore(store_id)
        else:
            raise ValueError("User does not have the necessary permissions to add a policy to the store")

    def removePurchasePolicy(self, user_id, store_id: int, policy_id: int):
        '''
        * Parameters: store_id, policy_id
        * This function removes a purchase policy from the store
        * Returns None
        '''
        if self.roles_facade.has_change_purchase_policy_permission(store_id, user_id):
            self.store_facade.removePurchasePolicyFromStore(store_id, policy_id)
        else:
            raise ValueError("User does not have the necessary permissions to remove a policy from the store")

    def changePurchasePolicy(self, user_id: int, store_id: int, policy_id: int): #not implemented yet
        pass


#-------------Products related methods-------------------#
    def addProduct(self,user_id:int, store_id: int, productSpecId: int, expirationDate: datetime, condition: int, price: float):
        '''
        * Parameters: user_id, store_id, productSpecId, expirationDate, condition, price
        * This function adds a product to the store
        * Returns None
        '''
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError("User does not have the necessary permissions to add a product to the store")
        if self.store_facade.addProductToStore(store_id, productSpecId, expirationDate, condition, price):
            logger.info(f"User {user_id} has added a product to store {store_id}")
        else:
            logger.info(f"User {user_id} has failed to add a product to store {store_id}")

    def removeProduct(self, user_id:int, store_id: int, product_id: int):
        '''
        * Parameters: store_id, product_id
        * This function removes a product from the store
        * Returns None
        '''
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError("User does not have the necessary permissions to remove a product from the store")
        if self.store_facade.removeProductFromStore(store_id, product_id):
            logger.info(f"User {user_id} has removed a product from store {store_id}")
        else:
            logger.info(f"User {user_id} has failed to remove a product from store {store_id}")


    def changeProductPrice(self, user_id: int, store_id: int, product_id: int, newPrice: float):
        '''
        * Parameters: userId, store_id, product_id, newPrice
        * This function changes the price of a product
        * Returns None
        '''
        if not self.roles_facade.has_add_product_permission(store_id, user_id):
            raise ValueError("User does not have the necessary permissions to change the price of a product in the store")
        if self.store_facade.changePriceOfProduct(store_id, product_id, newPrice):
            logger.info(f"User {user_id} has changed the price of product {product_id} in store {store_id}")
        else:
            logger.info(f"User {user_id} has failed to change the price of product {product_id} in store {store_id}")


#-------------Store related methods-------------------#
    def addStore(self, founder_id: int, locationId: int, storeName: str):
        '''
        * Parameters: founderId, locationId, storeName
        * This function adds a store to the system
        * Returns None
        '''
        if not self.user_facade.is_member(founder_id):
            raise ValueError("User is not a member")
        store = self.store_facade.addStore(locationId, storeName, founder_id)


    def closeStore(self, userId: int, store_id: int):
        '''
        * Parameters: userId, store_id
        * This function closes a store
        * Returns None
        '''
        #TODO: check if user is logged in
        if not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not logged in")
        if self.store_facade.closeStore(store_id, userId):
            logger.info(f"User {userId} has closed store {store_id}")
        else:
            logger.info(f"User {userId} has failed to close store {store_id}")

    def addProductSpec(self, userId: int, name: str, weightInKilos: float, description: str, tags: List[str], manufacturer: str):
        '''
        * Parameters: userId, name, weightInKilos, tags, manufacturer
        * This function adds a product specification to the system
        * Returns None
        '''
        if not self.roles_facade.is_system_manager(userId):
            raise ValueError("User is not a system manager")
        if self.store_facade.addProductSpecification(name, weightInKilos, description, tags, manufacturer):
            logger.info(f"User {userId} has added a product specification")
        else:
            logger.info(f"User {userId} has failed to add a product specification")


#-------------Tags related methods-------------------#
    def addTagToProductSpec(self, userId: int, productSpecId: int, tag: str):
        '''
        * Parameters: userId, productSpecId, tag
        * This function adds a tag to a product specification
        * Returns None
        '''
        if not self.roles_facade.is_system_manager(userId):
            raise ValueError("User is not a system manager")
        if self.store_facade.addTagToProductSpecification(productSpecId, tag):
            logger.info(f"User {userId} has added a tag to product specification {productSpecId}")
        else:
            logger.info(f"User {userId} has failed to add a tag to product specification {productSpecId}")


    def removeTagFromProductSpec(self, userId: int, productSpecId: int, tag: str):
        '''
        * Parameters: userId, productSpecId, tag
        * This function removes a tag from a product specification
        * Returns None
        '''
        if not self.roles_facade.is_system_manager(userId):
            raise ValueError("User is not a system manager")
        if self.store_facade.removeTagFromProductSpecification(productSpecId, tag):
            logger.info(f"User {userId} has removed a tag from product specification {productSpecId}")
        else:
            logger.info(f"User {userId} has failed to remove a tag from product specification {productSpecId}")





#-------------ProductSpec related methods-------------------#
    def changeProductSpecName(self, userId: int, productSpecId: int, newName: str):
        '''
        * Parameters: userId, productSpecId, newName
        * This function changes the name of a product specification
        * Returns None
        '''
        if not self.roles_facade.is_system_manager(userId):
            raise ValueError("User is not a system manager")
        if self.store_facade.changeNameOfProductSpec(productSpecId, newName):
            logger.info(f"User {userId} has changed the name of product specification {productSpecId}")
        else:
            logger.info(f"User {userId} has failed to change the name of product specification {productSpecId}")


    def changeProductSpecManufacturer(self, userId: int, productSpecId: int, manufacturer: str):
        '''
        * Parameters: userId, productSpecId, manufacturer
        * This function changes the manufacturer of a product specification
        * Returns None
        '''
        if not self.roles_facade.is_system_manager(userId):
            raise ValueError("User is not a system manager")
        if self.store_facade.changeManufacturer(productSpecId, manufacturer):
            logger.info(f"User {userId} has changed the manufacturer of product specification {productSpecId}")
        else:
            logger.info(f"User {userId} has failed to change the manufacturer of product specification {productSpecId}")


    def changeProductSpecDescription(self, userId: int, productSpecId: int, description: str):
        '''
        * Parameters: userId, productSpecId, description
        * This function changes the description of a product specification
        * Returns None
        '''
        if not self.roles_facade.is_system_manager(userId):
            raise ValueError("User is not a system manager")
        if self.store_facade.changeDescription(productSpecId, description):
            logger.info(f"User {userId} has changed the description of product specification {productSpecId}")
        else:
            logger.info(f"User {userId} has failed to change the description of product specification {productSpecId}")


    def changeProductSpecWeight(self, userId: int, productSpecId: int, weightInKilos: float):
        '''
        * Parameters: userId, productSpecId, weightInKilos
        * This function changes the weight of a product specification
        * Returns None
        '''
        if not self.roles_facade.is_system_manager(userId):
            raise ValueError("User is not a system manager")
        if self.store_facade.changeWeight(productSpecId, weightInKilos):
            logger.info(f"User {userId} has changed the weight of product specification {productSpecId}")
        else:
            logger.info(f"User {userId} has failed to change the weight of product specification {productSpecId}")




#-------------Category related methods-------------------#
    def addCategory(self, userId: int, categoryName: str):
        '''
        * Parameters: userId, categoryName
        * This function adds a category to the system
        * Returns None
        '''
        if not self.roles_facade.is_system_manager(userId):
            raise ValueError("User is not a system manager")
        if self.store_facade.addCategory(categoryName):
            logger.info(f"User {userId} has added a category")
        else:
            logger.info(f"User {userId} has failed to add a category")


    def removeCategory(self, userId: int, categoryId: int):
        '''
        * Parameters: userId, categoryId
        * This function removes a category from the system
        * Returns None
        '''
        if not self.roles_facade.is_system_manager(userId):
            raise ValueError("User is not a system manager")
        if self.store_facade.removeCategory(categoryId):
            logger.info(f"User {userId} has removed a category")
        else:
            logger.info(f"User {userId} has failed to remove a category")
        


    def addSubCategoryToCategory(self, userId: int, subCategoryId: int, parentCategoryId: int):
        '''
        * Parameters: userId, subCategoryId, parentCategoryId
        * This function adds a sub category to a category
        * NOTE: It is assumed that the subCategory is already created and exists in the system
        * Returns None
        '''
        if not self.roles_facade.is_system_manager(userId):
            raise ValueError("User is not a system manager")
        if self.store_facade.assignSubCategoryToCategory(subCategoryId, parentCategoryId):
            logger.info(f"User {userId} has added a sub category to category {parentCategoryId}")
        else:
            logger.info(f"User {userId} has failed to add a sub category to category {parentCategoryId}")
    

    def removeSubCategoryFromCategory(self, userId: int, categoryId: int, subCategoryId: int):
        '''
        * Parameters: userId, categoryId, subCategoryId
        * This function removes a sub category from a category
        * Returns None
        '''
        if not self.roles_facade.is_system_manager(userId):
            raise ValueError("User is not a system manager")
        if self.store_facade.deleteSubCategoryFromCategory(categoryId, subCategoryId):
            logger.info(f"User {userId} has removed a sub category from category {categoryId}")
        else:
            logger.info(f"User {userId} has failed to remove a sub category from category {categoryId}")



    def assignProductSpecToCategory(self, userId: int, categoryId: int, productSpecId: int):
        '''
        * Parameters: userId, categoryId, productSpecId
        * This function assigns a product specification to a category
        * NOTE: it is assumed that the product specification exists in the system
        * Returns None
        '''
        if not self.roles_facade.is_system_manager(userId):
            raise ValueError("User is not a system manager")
        if self.store_facade.assignProductSpecToCategory(categoryId, productSpecId):
            logger.info(f"User {userId} has assigned a product specification to category {categoryId}")
        else:
            logger.info(f"User {userId} has failed to assign a product specification to category {categoryId}")
    

    def removeProductSpecFromCategory(self, userId: int, categoryId: int, productSpecId: int):
        '''
        * Parameters: userId, categoryId, productSpecId
        * This function removes a product specification from a category
        * Returns None
        '''
        if not self.roles_facade.is_system_manager(userId):
            raise ValueError("User is not a system manager")
        if self.store_facade.removeProductSpecFromCategory(categoryId, productSpecId):
            logger.info(f"User {userId} has removed a product specification from category {categoryId}")
        else:
            logger.info(f"User {userId} has failed to remove a product specification from category {categoryId}")


#-------------PurchaseFacade methods:-------------------#

#-------------Purchase management related methods-------------------#
   
    
    def createBidPurchase(self, userId: int, proposedPrice : float, productId: int, storeId: int):
        '''
        * Parameters: userId, proposedPrice, productId, storeId
        * This function creates a bid purchase
        * Returns None
        '''
        if not self.user_facade.is_member(userId) or not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not a member or is not logged in")
        product = self.store_facade.getStoreById(storeId).getProductById(productId)
        productSpecId = product.get_specificationId()
        if self.purchase_facade.createBidPurchase(userId, proposedPrice, productId, productSpecId, storeId):
            logger.info(f"User {userId} has created a bid purchase")
            #TODO: notify the store owners and all relevant parties, await for their reaction
        else:
            logger.info(f"User {userId} has failed to create a bid purchase")
        


    def createAuctionPurchase(self, userId: int, basePrice: float, startingDate: datetime, endingDate: datetime,  storeId: int, productId: int,):
        '''
        * Parameters: userId, basePrice, startingDate, endingDate, productId, storeId
        * This function creates an auction purchase
        * Returns None
        '''
        if not self.user_facade.is_member(userId) or not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not a member or is not logged in")
        product = self.store_facade.getStoreById(storeId).getProductById(productId)
        productSpecId = product.get_specificationId()
        if self.purchase_facade.createAuctionPurchase(basePrice, startingDate, endingDate, storeId, productId, productSpecId):
            logger.info(f"User {userId} has created an auction purchase")
            
        


    def createLotteryPurchase(self, userId: int, fullPrice: float, storeId: int, productId: int, startingDate: datetime, endingDate: datetime):
        '''
        * Parameters: userId, fullPrice, storeId, productId, startingDate, endingDate
        * This function creates a lottery purchase
        * Returns None
        '''
        if not self.user_facade.is_member(userId) or not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not a member or is not logged in")
        product = self.store_facade.getStoreById(storeId).getProductById(productId)
        productSpecId = product.get_specificationId()
        if self.purchase_facade.createLotteryPurchase(userId, fullPrice, storeId, productId, productSpecId, startingDate, endingDate):
            logger.info(f"User {userId} has created a lottery purchase")
        else:
            logger.info(f"User {userId} has failed to create a lottery purchase")





    def viewPurchasesOfUser(self, user_id: int) -> str:
        '''
        * Parameters: user_id
        * This function returns the purchases of a user
        * Returns a string
        '''
        if not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not logged in")
        purchases= self.purchase_facade.getPurchasesOfUser(user_id)
        strOutput= ""
        for purchase in purchases:
            strOutput+= purchase.__str__()
        return strOutput
            
        


    def viewPurchasesOfStore(self, userId: int, store_id: int) -> str:
        '''
        * Parameters: userId, store_id
        * This function returns the purchases of a store
        * Returns a string
        '''
        if not self.user_facade.is_member(userId) or not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not a member or is not logged in")
        purchases= self.purchase_facade.getPurchasesOfStore(store_id)
        strOutput= ""
        for purchase in purchases:
            strOutput+= purchase.__str__()
        return strOutput
        
        


    def viewOnGoingPurchases(self, userId: int) -> str:
        '''
        * Parameters: userId
        * This function returns the ongoing purchases
        * Returns a string
        '''
        if not self.user_facade.is_member(userId) or not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not a member or is not logged in")
        purchases= self.purchase_facade.getOnGoingPurchases()
        strOutput= ""
        for purchase in purchases:
            strOutput+= purchase.__str__()
        return strOutput


    def viewCompletedPurchases(self, userId: int) -> str:
        '''
        * Parameters: userId
        * This function returns the completed purchases
        * Returns a string
        '''
        if not self.user_facade.is_member(userId) or not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not a member or is not logged in")
        purchases= self.purchase_facade.getCompletedPurchases()
        strOutput= ""
        for purchase in purchases:
            strOutput+= purchase.__str__()
        return strOutput


    def viewFailedPurchases(self, userId: int) -> str:
        '''
        * Parameters: userId
        * This function returns the failed purchases
        * Returns a string
        '''
        if not self.user_facade.is_member(userId) or not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not a member or is not logged in")
        purchases= self.purchase_facade.getFailedPurchases()
        strOutput= ""
        for purchase in purchases:
            strOutput+= purchase.__str__()
        return strOutput


    def viewAcceptedPurchases(self, userId: int) -> str:
        '''
        * Parameters: userId
        * This function returns the accepted purchases
        * Returns a string
        '''
        if not self.user_facade.is_member(userId) or not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not a member or is not logged in")
        purchases= self.purchase_facade.getAcceptedPurchases()
        strOutput= ""
        for purchase in purchases:
            strOutput+= purchase.__str__()
        return strOutput
        
        
        
    
    
    def handleAcceptedPurchases(self):
        '''
        * Parameters: None
        * This function handles the accepted purchases
        * Returns None
        '''
        acceptedPurchases = self.purchase_facade.getAcceptedPurchases()
        for purchase in acceptedPurchases:
            if self.purchase_facade.checkIfCompletedPurchase(purchase.get_purchaseId()):
                logger.info(f"Purchase {purchase.get_purchaseId()} has been completed")
            
          
        

    

    #-------------Bid Purchase related methods-------------------#
    def storeAcceptOffer(self, purchase_id: int):
        pass #cant be implemented yet without notifications


    def storeRejectOffer(self, purchase_id: int):
        pass #cant be implemented yet without notifications


    def storeCounterOffer(self, new_price: float, purchase_id: int):
        pass #cant be implemented yet without notifications


    def userAcceptOffer(self, userId: int, purchase_id: int):
        '''
        * Parameters: userId, purchase_id
        * This function accepts an offer
        * Returns None
        '''
        if not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not logged in")
        self.purchase_facade.userAcceptOffer(purchase_id,userId)
        
        #TODO: notify the store owners and all relevant parties
        


    def userRejectOffer(self, userId: int , purchase_id: int):
        '''
        * Parameters: userId, purchase_id
        * This function rejects an offer
        * Returns None
        '''
        if not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not logged in")
        self.purchase_facade.userRejectOffer(purchase_id,userId)
        
        #TODO: notify the store owners and all relevant parties
        


    def userCounterOffer(self, userId: int, counterOffer: float, purchase_id: int):
        
        '''
        * Parameters: userId, counterOffer, purchase_id
        * This function makes a counter offer
        * Returns None
        '''
        if not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not logged in")
        self.purchase_facade.userCounterOffer(counterOffer, purchase_id, userId)
        
        #TODO: notify the store owners and all relevant parties


    #-------------Auction Purchase related methods-------------------#
    def addAuctionBid(self, purchase_id: int, user_id: int, price: float):
        '''
        * Parameters: purchase_id, user_id, price
        * This function adds a bid to an auction purchase
        * Returns None
        '''
        if not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not logged in")
        if self.purchase_facade.addAuctionBid(purchase_id, user_id, price):
            logger.info(f"User {user_id} has added a bid to purchase {purchase_id}")
            
            #TODO: notify the store owners and all relevant parties
        else:
            logger.info(f"User {user_id} has failed to add a bid to purchase {purchase_id}")
            
        

        
    
    def viewHighestBid(self, purchase_id: int, userId: int)-> float:
        '''
        * Parameters: purchase_id, userId
        * This function returns the highest bid of an auction purchase
        * Returns a float
        '''
        if not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not logged in")
        
        #TODO: notify the store owners and all relevant parties

        return self.purchase_facade.viewHighestBiddingOffer(purchase_id)



    def calculateRemainingTimeOfAuction(self, purchase_id: int, useId: int)-> datetime:
        '''
        * Parameters: purchase_id, userId
        * This function calculates the remaining time of an auction purchase
        * Returns a float
        '''
        if not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not logged in")
        
        #TODO: notify the store owners and all relevant parties

        return self.purchase_facade.calculateRemainingTimeOfAuction(purchase_id)

    
    def handleOngoingAuctions(self):
        '''
        * Parameters: None
        * This function handles the ongoing auctions
        * Returns None
        '''
        ongoingPurchases = self.purchase_facade.getOngoingPurchases()
        for purchase in ongoingPurchases:
            if purchase.getPurchaseType(purchase.get_purchaseId()) == 2:
                if self.purchase_facade.checkIfAuctionEnded(purchase.get_purchaseId()):
                    
                    #TODO: notify the store owners and all relevant parties
                    #TODO: notify the user who won the auction
                    #TODO: third party services
                    #if thirdparty services work, then:
                        #TODO: call validatePurchaseOfUser(purchase.get_purchaseId(), purchase.get_userId(), deliveryDate)
                    #else:
                        #TODO: call invalidatePurchase(purchase.get_purchaseId(), purchase.get_userId()
                    logger.info(f"Auction {purchase.get_purchaseId()} has been completed")
                    
                
                
    
        

    #-------------Lottery Purchase related methods-------------------#
    def addLotteryTicket(self, user_id: int, proposedPrice: float, purchase_id: int) :
        '''
        * Parameters: user_id, proposedPrice, purchase_id
        * This function adds a lottery ticket to a lottery purchase
        * Returns None
        '''
        if not self.auth_facade.is_logged_in(user_id) or not self.user_facade.is_member(user_id):
            raise ValueError("User is not logged in or is not a member")
        if self.purchase_facade.addLotteryTicket(user_id, proposedPrice, purchase_id):
            logger.info(f"User {user_id} has added a lottery ticket to purchase {purchase_id}")
            
            #TODO: notify the store owners and all relevant parties
        else:
            logger.info(f"User {user_id} has failed to add a lottery ticket to purchase {purchase_id}")


    def calculateRemainingTimeOfLottery(self, purchase_id: int, userId: int)-> datetime:
        '''
        * Parameters: purchase_id, userId
        * This function calculates the remaining time of a lottery purchase
        * Returns a float
        '''
        if not self.auth_facade.is_logged_in(userId):
            raise ValueError("User is not logged in")
        
        #TODO: notify the store owners and all relevant parties

        return self.purchase_facade.calculateRemainingTimeOfLottery(purchase_id)


    def calculateProbabilityOfUser(self, purchase_id: int, user_id: int)-> float:
        '''
        * Parameters: purchase_id, user_id
        * This function calculates the probability of a user in a lottery purchase
        * Returns a float
        '''
        if not self.auth_facade.is_logged_in(user_id):
            raise ValueError("User is not logged in")
        #TODO: notify the store owners and all relevant parties
        return self.purchase_facade.calculateProbabilityOfUser(purchase_id, user_id)
        
    


    def handleOngoingLotteries(self):
        '''
        * Parameters: None
        * This function handles the ongoing lotteries
        * Returns None
        '''
        ongoingPurchases = self.purchase_facade.getOngoingPurchases()
        for purchase in ongoingPurchases:
            if purchase.getPurchaseType(purchase.get_purchaseId()) == 3:
                if self.purchase_facade.validateUserOffers(purchase.get_purchaseId()):
                    userIdOfWinner = self.purchase_facade.pickWinner(purchase.get_purchaseId())
                    if userIdOfWinner is not None:
                        #TODO: notify the user who won the lottery
                        #TODO: third party services
                        #if thirdparty services work, then:
                            #TODO: call validateDeliveryOfWinner(purchase.get_purchaseId(), purchase.get_userId(), deliveryDate)
                        #else:
                            #TODO: call invalidateDeliveryOfWinner(purchase.get_purchaseId(), purchase.get_userId()
                            logger.info(f"Lottery {purchase.get_purchaseId()} has been won!")
                    else:
                        #TODO: refund users who participated in the lottery
                        logger.info(f"Lottery {purchase.get_purchaseId()} has failed! Refunded all participants")
                    
                