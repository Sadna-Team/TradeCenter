#----------------- imports -----------------#
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Tuple

#-----------------Rating class-----------------#
class Rating(ABC):
    def __init__(self, rating: int, purchaseId: int, description: str, creationDate: datetime):
        if not isinstance(rating, int) or not (0 <= rating <= 5):
            raise ValueError("Rating must be an integer between 0 and 5")
        self.rating = rating
        self.purchaseId = purchaseId
        self.description = description
        self.creationDate = creationDate

    @abstractmethod
    def calculate_rating(self):
        pass


#-----------------StoreRating class-----------------#
class StoreRating(Rating):
    # purchaseId and storeId are the unique identifiers for the store rating, storeId used to retrieve the details of store
    def __init__(self, rating: int, purchaseId: int, description: str, storeId: int, creationDate: datetime = datetime.datetime.now()):
        super().__init__(rating, purchaseId, description, creationDate)
        self.storeId = storeId

    #---------------------------------Getters and Setters---------------------------------#
    @property
    def get_rating(self):
        return self.rating
    
    @property
    def __set_rating(self, rating: int):
        self.rating = rating

    @property
    def get_purchaseId(self):
        return self.purchaseId
    
    @property
    def __set_purchaseId(self, purchaseId: int):
        self.purchaseId = purchaseId

    @property
    def get_description(self):
        return self.description
    
    @property
    def __set_description(self, description: str):
        self.description = description

    @property
    def get_creationDate(self):
        return self.creationDate

    @property
    def __set_creationDate(self, creationDate: datetime):
        self.creationDate = creationDate

    @property
    def get_storeId(self):
        return self.storeId
    
    @property
    def __set_storeId(self, storeId: int):
        self.storeId = storeId

    #---------------------------------Methods---------------------------------#
    def calculate_rating(self):
        return self.get_rating()
    


#-----------------ProductRating class-----------------#
class ProductRating(Rating):
    # purchaseId and productId are the unique identifiers for the product rating, productSpec used to retrieve the details of product
    def __init__(self, rating: int, purchaseId: int, description: str, productSpecId: int, productId: int, creationDate: datetime = datetime.datetime.now()):
        super().__init__(rating, purchaseId, description, creationDate)
        self.productSpecId = productSpecId
        self.productId = productId

    #---------------------------------Getters and Setters---------------------------------#
    @property
    def get_rating(self):
        return self.rating
    
    @property
    def __set_rating(self, rating: int):
        self.rating = rating

    @property
    def get_purchaseId(self):
        return self.purchaseId
    
    @property
    def __set_purchaseId(self, purchaseId: int):
        self.purchaseId = purchaseId

    @property
    def get_description(self):
        return self.description
    
    @property
    def __set_description(self, description: str):
        self.description = description

    @property
    def get_creationDate(self):
        return self.creationDate

    @property
    def __set_creationDate(self, creationDate: datetime):
        self.creationDate = creationDate

    @property
    def get_productSpecId(self):
        return self.productSpecId
    
    @property
    def __set_productSpecId(self, productSpecId: int):
        self.productSpecId = productSpecId

    @property
    def get_productId(self):
        return self.productId
    
    @property
    def __set_productId(self, productId: int):
        self.productId = productId

    #---------------------------------Methods---------------------------------#
    def calculate_rating(self):
        return self.get_rating()
    

#---------------------purchaseStatus Enum---------------------#

class PurchaseStatus(Enum):
    notStarted = 1
    onGoing = 2
    failed = 3
    completed = 4

PurchaseStatus = Enum('PurchaseStatus', ['notStarted', 'onGoing','failed','completed'])



#-----------------Purchase Class-----------------#
class Purchase(ABC):
    def __init__(self, purchaseId: int, userId: int, dateOfPurchase: datetime, totalPrice: float, status: PurchaseStatus):
        self.purchaseId = purchaseId
        self.userId = userId
        self.dateOfPurchase = dateOfPurchase
        self.totalPrice = totalPrice
        self.status= status
 
    @abstractmethod
    def updateStatus(self):
        pass

    @abstractmethod
    def updateDateOfPurchase(self):
        pass

    @abstractmethod
    def calculateTotalPrice(self):
        pass


#-----------------ImmediatePurchase class-----------------#
class ImmediatePurchase(Purchase):
    def __init__(self, purchaseId: int, userId: int, dateOfPurchase: datetime, totalPrice: float, status: PurchaseStatus, deliveryDate: datetime, shoppingCart: ShoppingCart):
        super().__init__(purchaseId, userId, dateOfPurchase, totalPrice, status)
        self.shoppingCart = shoppingCart

    #---------------------------------Getters and Setters---------------------------------#
    @property
    def get_purchaseId(self):
        return self.purchaseId
    
    @property
    def __set_purchaseId(self, purchaseId: int):
        self.purchaseId = purchaseId

    @property
    def get_userId(self):
        return self.userId
    
    @property
    def __set_userId(self, userId: int):
        self.userId = userId

    @property
    def get_dateOfPurchase(self):
        return self.dateOfPurchase
    
    @property
    def __set_dateOfPurchase(self, dateOfPurchase: datetime):
        self.dateOfPurchase = dateOfPurchase

    @property
    def get_totalPrice(self):
        return self.totalPrice
    
    @property
    def __set_totalPrice(self, totalPrice: float):
        self.totalPrice = totalPrice

    @property
    def get_status(self):
        return self.status
    
    @property
    def __set_status(self, status: PurchaseStatus):
        self.status = status

   

    #---------------------------------Methods---------------------------------#
    def updateStatus(self):
       pass 

    def updateDateOfPurchase(self):
        pass
    def calculateTotalPrice(self):
        pass


#-----------------BidPurchase class-----------------#
class BidPurchase(Purchase):
    # purchaseId and productId are the unique identifiers for the product rating, productSpec used to retrieve the details of product   
    def __init__(self, purchaseId: int, userId: int, dateOfPurchase: datetime, totalPrice: float, status: PurchaseStatus, proposedPrice: float, productId: int, productSpecId: int, storedId: int):
        super().__init__(purchaseId, userId, dateOfPurchase, totalPrice, status)
        self.proposedPrice = proposedPrice
        self.productId = productId
        self.productSpecId = productSpecId
        self.storedId = storedId

#---------------------------------Getters and Setters---------------------------------#
    @property
    def get_purchaseId(self):
        return self.purchaseId
    
    @property
    def __set_purchaseId(self, purchaseId: int):
        self.purchaseId = purchaseId

    @property
    def get_userId(self):
        return self.userId
    
    @property
    def __set_userId(self, userId: int):
        self.userId = userId

    @property
    def get_dateOfPurchase(self):
        return self.dateOfPurchase
    
    @property
    def __set_dateOfPurchase(self, dateOfPurchase: datetime):
        self.dateOfPurchase = dateOfPurchase

    @property
    def get_totalPrice(self):
        return self.totalPrice
    
    @property
    def __set_totalPrice(self, totalPrice: float):
        self.totalPrice = totalPrice

    @property
    def get_status(self):
        return self.status
    
    @property
    def __set_status(self, status: PurchaseStatus):
        self.status = status

    @property
    def get_proposedPrice(self):
        return self.proposedPrice
    
    @property
    def __set_proposedPrice(self, proposedPrice: float):
        self.proposedPrice = proposedPrice

    @property
    def get_productId(self):
        return self.productId
    
    @property
    def __set_productId(self, productId: int):
        self.productId = productId

    @property
    def get_productSpecId(self):
        return self.productSpecId
    
    @property
    def __set_productSpecId(self, productSpecId: int):
        self.productSpecId = productSpecId

    @property
    def get_storedId(self):
        return self.storedId
    
    @property
    def __set_storedId(self, storedId: int):
        self.storedId = storedId


#---------------------------------Methods---------------------------------#
    def updateStatus(self):
        pass
    def updateDateOfPurchase(self):
        pass
    def calculateTotalPrice(self):
        pass
    


#-----------------AuctionPurchase class-----------------#
class AuctionPurchase(Purchase):
    def __init__(self, purchaseId: int, userId: int, dateOfPurchase: datetime, totalPrice: float, 
                 status: PurchaseStatus, basePrice: float, startingDate: datetime, endingDate: datetime, 
                 storeId: int ,productId: int, productSpecId: int, usersWithProposedPrices: list[Tuple[int, float]] = []):
        super().__init__(purchaseId, userId, dateOfPurchase, totalPrice, status)
        self.basePrice = basePrice
        self.startingDate = startingDate
        self.endingDate = endingDate
        self.storeId = storeId
        self.productId = productId
        self.productSpecId = productSpecId
        self.usersWithProposedPrices = usersWithProposedPrices


    #---------------------------------Getters and Setters---------------------------------#
    @property
    def get_purchaseId(self):
        return self.purchaseId
    
    @property
    def __set_purchaseId(self, purchaseId: int):
        self.purchaseId = purchaseId

    @property
    def get_userId(self):
        return self.userId
    
    @property
    def __set_userId(self, userId: int):
        self.userId = userId

    @property
    def get_dateOfPurchase(self):
        return self.dateOfPurchase
    
    @property
    def __set_dateOfPurchase(self, dateOfPurchase: datetime):
        self.dateOfPurchase = dateOfPurchase

    @property
    def get_totalPrice(self):
        return self.totalPrice
    
    @property
    def __set_totalPrice(self, totalPrice: float):
        self.totalPrice = totalPrice

    @property
    def get_status(self):
        return self.status
    
    @property
    def __set_status(self, status: PurchaseStatus):
        self.status = status

    @property
    def get_basePrice(self):
        return self.basePrice
    
    @property
    def __set_basePrice(self, basePrice: float):
        self.basePrice = basePrice

    @property
    def get_startingDate(self):
        return self.startingDate
    
    @property
    def __set_startingDate(self, startingDate: datetime):
        self.startingDate = startingDate

    @property
    def get_endingDate(self):
        return self.endingDate
    
    @property
    def __set_endingDate(self, endingDate: datetime):
        self.endingDate = endingDate

    @property
    def get_storeId(self):
        return self.storeId
    
    @property
    def __set_storeId(self, storeId: int):
        self.storeId = storeId

    @property
    def get_productId(self):
        return self.productId
    
    @property
    def __set_productId(self, productId: int):
        self.productId = productId

    @property
    def get_productSpecId(self):
        return self.productSpecId
    
    @property
    def __set_productSpecId(self, productSpecId: int):
        self.productSpecId = productSpecId

    @property
    def get_usersWithProposedPrices(self):
        return self.usersWithProposedPrices
    
    @property
    def __set_usersWithProposedPrices(self, usersWithProposedPrices: list[Tuple[int, float]]):
        self.usersWithProposedPrices = usersWithProposedPrices

    #---------------------------------Methods---------------------------------#
    def updateStatus(self):
        pass

    def updateDateOfPurchase(self):
        pass

    def calculateTotalPrice(self):
        pass

    def viewHighestBiddingOffer(self):
        pass

    def calculateRemainingTime(self):
        return self.get_endingDate() - datetime.datetime.now()
    

#-----------------LotteryPurchase class-----------------#
class LotteryPurchase(Purchase):
    def __init__(self, purchaseId: int, userId: int, dateOfPurchase: datetime, totalPrice: float, status: PurchaseStatus, 
                 basePrice: float, storeId: int, productId: int, productSpecId: int, startingDate: datetime, endingDate: datetime,  usersWithPrices: list[Tuple[int, float]] = []):
        super().__init__(purchaseId, userId, dateOfPurchase, totalPrice, status)
        self.basePrice = basePrice
        self.storeId = storeId
        self.productId = productId
        self.productSpecId = productSpecId
        self.usersWithPrices = usersWithPrices
        self.startingDate = startingDate
        self.endingDate = endingDate


#---------------------------------Getters and Setters---------------------------------#

    @property
    def get_purchaseId(self):
        return self.purchaseId
    
    @property
    def __set_purchaseId(self, purchaseId: int):
        self.purchaseId = purchaseId

    @property
    def get_userId(self):
        return self.userId
    
    @property
    def __set_userId(self, userId: int):
        self.userId = userId

    @property
    def get_dateOfPurchase(self):
        return self.dateOfPurchase
    
    @property
    def __set_dateOfPurchase(self, dateOfPurchase: datetime):
        self.dateOfPurchase = dateOfPurchase

    @property
    def get_totalPrice(self):
        return self.totalPrice
    
    @property
    def __set_totalPrice(self, totalPrice: float):
        self.totalPrice = totalPrice

    @property
    def get_status(self):
        return self.status
    
    @property
    def __set_status(self, status: PurchaseStatus):
        self.status = status

    @property
    def get_basePrice(self):
        return self.basePrice
    
    @property
    def __set_basePrice(self, basePrice: float):
        self.basePrice = basePrice

    @property
    def get_storeId(self):
        return self.storeId
    
    @property
    def __set_storeId(self, storeId: int):
        self.storeId = storeId

    @property
    def get_productId(self):
        return self.productId
    
    @property
    def __set_productId(self, productId: int):
        self.productId = productId

    @property
    def get_productSpecId(self):
        return self.productSpecId
    
    @property
    def __set_productSpecId(self, productSpecId: int):
        self.productSpecId = productSpecId

    @property
    def get_usersWithPrices(self):
        return self.usersWithPrices
    
    @property
    def __set_usersWithPrices(self, usersWithPrices: list[Tuple[int, float]]):
        self.usersWithPrices = usersWithPrices

    @property
    def get_startingDate(self):
        return self.startingDate
    
    @property
    def __set_startingDate(self, startingDate: datetime):
        self.startingDate = startingDate

    @property
    def get_endingDate(self):
        return self.endingDate
    
    @property
    def __set_endingDate(self, endingDate: datetime):
        self.endingDate = endingDate


#---------------------------------Methods---------------------------------#
    def updateStatus(self):
        pass

    def updateDateOfPurchase(self):
        pass

    def calculateTotalPrice(self):
        pass


    def calculateRemainingTime(self):
        pass
    
    
    def handleLottery(self):
        pass

    
    def validateUserOffer(self):
        pass


#-----------------PurchaseFacade class-----------------#
class PurchaseFacade:
    # singleton
    __instance = None

    def __new__(cls):
        if PurchaseFacade.__instance is None:
            PurchaseFacade.__instance = object.__new__(cls)
        return PurchaseFacade.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # here you can add fields
