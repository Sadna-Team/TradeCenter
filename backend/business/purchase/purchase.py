#----------------- imports -----------------#
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import numpy as np
from numpy.random import choice
from typing import List, Tuple
import concurrent.futures

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
    # Enum for the status of the purchase
    notStarted = 1
    onGoing = 2
    failed = 3
    accepted = 4
    completed = 5

PurchaseStatus = Enum('PurchaseStatus', ['notStarted', 'onGoing','failed','accepted','completed'])



#-----------------Purchase Class-----------------#
class Purchase(ABC):
    #interface for the purchase classes, contains the common attributes and methods for the purchase classes
    def __init__(self, purchaseId: int, userId: int, storeId: int, dateOfPurchase: datetime, totalPrice: float, status: PurchaseStatus):
        self.purchaseId = purchaseId
        self.userId = userId
        self.storeId = storeId
        self.dateOfPurchase = dateOfPurchase
        self.totalPrice = totalPrice
        self.status = status
 
    @abstractmethod
    def updateStatus(self, status: PurchaseStatus):
        pass

    @abstractmethod
    def updateDateOfPurchase(self, dateOfPurchase: datetime):
        pass

    @abstractmethod
    def calculateTotalPrice(self) -> float:
        pass

#-----------------ImmediateSubPurchases class-----------------#
class ImmediateSubPurchases(Purchase):
    # purchaseId and storeId are unique identifier of the immediate purchase, storeId used to retrieve the details of the store
    def __init__(self, purchaseId: int, storeId: int, userId: int, dateOfPurchase: datetime, totalPrice: float, status: PurchaseStatus, productIds: List[int]):
        super().__init__(purchaseId, userId, storeId, dateOfPurchase, totalPrice, status)
        self.productIds = productIds


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
    def get_storeId(self):
        return self.storeId
    
    @property
    def __set_storeId(self, storeId: int):
        self.storeId = storeId

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
    def get_productIds(self):
        return self.productIds
    
    @property
    def __set_productIds(self, productIds: List[int]):
        self.productIds = productIds

    #---------------------------------Methods---------------------------------#
    def updateStatus(self, status: PurchaseStatus):
        ''' 
        * Parameters: status
        * This function is responsible for updating the status of the purchase
        * Returns: none
        '''
        self.__set_status(status)

    def updateDateOfPurchase(self, dateOfPurchase: datetime):
        ''' 
        * Parameters: dateOfPurchase
        * This function is responsible for updating the date of the purchase
        * Returns: none
        '''
        self.__set_dateOfPurchase(dateOfPurchase)

    
    def calculateTotalPrice(self) -> float:
        '''
        * Parameters: none
        * This function is responsible for calculating the total price of the products in the shoppingBasket
        * Returns: total price of the current purchase
        '''
        return self.get_totalPrice()

    def calculateTotalPriceAfterDiscount(self) -> float:
        '''
        * Parameters: none
        * This function is responsible for calculating the total price of the products in the shoppingBasket after discount
        * Returns: total price of the current purchase after discount
        '''
        # call method of shoppingBasket to calculate the total price of the products in the shoppingBasket after discount
        pass

#-----------------ImmediatePurchase class-----------------#
class ImmediatePurchase(Purchase):
    # purchaseId is the unique identifier of the immediate purchase, purchase by a user of their shoppingCart
    # Note: storeId is -1 since immediatePurchase is not directly related to a store
    # Note: List[Tuple[Tuple[int,float],List[int]]] -> List of shoppingBaskets where shoppingBasket is a tuple of a tuple of storeId and totalPrice and a list of productIds
    def __init__(self, purchaseId: int, userId: int, dateOfPurchase: datetime, totalPrice: float, status: PurchaseStatus, deliveryDate: datetime, shoppingCart: List[Tuple[Tuple[int,float],List[int]]], totalPriceAfterDiscounts: float = -1):
        super().__init__(purchaseId, userId, -1, dateOfPurchase, totalPrice, status)
        self.deliveryDate = deliveryDate
        self.totalPriceAfterDiscounts = totalPriceAfterDiscounts
        for shoppingBasket in shoppingCart:
            self.immediateSubPurchases.append(ImmediateSubPurchases(purchaseId, userId, shoppingBasket[0][0], dateOfPurchase, shoppingBasket[0][1], status, shoppingBasket[1]))




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
    def get_storeId(self):
        return self.storeId
    
    @property
    def __set_storeId(self, storeId: int):
        self.storeId = storeId

    @property
    def get_dateOfPurchase(self):
        return self.dateOfPurchase
    
    @property
    def __set_dateOfPurchase(self, dateOfPurchase: datetime):
        self.dateOfPurchase = dateOfPurchase

    @property
    def get_deliveryDate(self):
        return self.deliveryDate
    
    @property
    def __set_deliveryDate(self, deliveryDate: datetime):
        self.deliveryDate = deliveryDate

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
    def get_totalPriceAfterDiscounts(self):
        return self.totalPriceAfterDiscounts
    
    @property
    def __set_totalPriceAfterDiscounts(self, totalPriceAfterDiscounts: float):
        self.totalPriceAfterDiscounts = totalPriceAfterDiscounts

    @property
    def get_immediateSubPurchases(self):
        return self.immediateSubPurchases
    
    @property
    def __set_immediateSubPurchases(self, immediateSubPurchases: List[ImmediateSubPurchases]):
        self.immediateSubPurchases = immediateSubPurchases

    #---------------------------------Methods---------------------------------#
    def updateStatus(self, status: PurchaseStatus):
        ''' 
        * Parameters: status
        * This function is responsible for updating the status of the purchase
        * Returns: none
        '''
        self.__set_status(status) 

    def updateDateOfPurchase(self, dateOfPurchase: datetime):
        ''' 
        * Parameters: dateOfPurchase
        * This function is responsible for updating the date of the purchase
        * Returns: none
        '''
        self.__set_dateOfPurchase(dateOfPurchase)
        

    def calculateTotalPrice(self) -> float:
        '''
        * Parameters: none
        * This function is responsible for calculating the total price of the products in the shoppingCart before discount
        * Returns: total price of the current purchase
        '''
        totalPrice = 0
        for subPurchase in self.get_immediateSubPurchases():
            totalPrice += subPurchase.calculateTotalPrice()
        return totalPrice

    def calculateTotalPriceAfterDiscounts(self) -> float:
        '''
        * Parameters: none
        * This function is responsible for calculating the total price of the products in the shoppingCart after discount
        * Returns: total price of the current purchase after discount
        '''
        # call method of shoppingCart to calculate the total price of the products in the shoppingCart after discount
        return self.calculateTotalPrice() #for now not implemented


#-----------------BidPurchase class-----------------#
class BidPurchase(Purchase):
    # purchaseId and productId are the unique identifiers for the product rating, productSpec used to retrieve the details of product   
    def __init__(self, purchaseId: int, userId: int, dateOfPurchase: datetime, totalPrice: float, status: PurchaseStatus, proposedPrice: float, productId: int, productSpecId: int, storeId: int, isOfferToStore: bool = True):
        super().__init__(purchaseId, userId,storeId ,dateOfPurchase, totalPrice, status)
        self.proposedPrice = proposedPrice
        self.productId = productId
        self.productSpecId = productSpecId
        self.isOfferToStore = isOfferToStore

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
    def get_storeId(self):
        return self.storeId
    
    @property
    def __set_storeId(self, storeId: int):
        self.storeId = storeId

    @property
    def get_isOfferToStore(self):
        return self.isOfferToStore
    
    @property
    def __set_isOfferToStore(self, isOfferToStore: bool):
        self.isOfferToStore = isOfferToStore

#---------------------------------Methods---------------------------------#
    def updateStatus(self, status: PurchaseStatus):
        ''' 
        * Parameters: status
        * This function is responsible for updating the status of the purchase
        * Returns: none
        '''
        self.__set_status(status) 


    def StoreAcceptOffer(self):
        '''
        * Parameters: 
        * Validate that all store owners and managers with permissions accepted the offer
        * Returns: none
        '''
        self.__set_status(PurchaseStatus.accepted)

    
    def UseracceptOffer(self, userId: int):
        '''
        * Parameters: userId
        * Function to accept the offer by the store
        * Returns: none
        '''
        if userId == self.get_userId():
            self.__set_status(PurchaseStatus.accepted)
        

    def StoreRejectOffer(self):
        '''
        * Parameters: 
        * Validate that one store owner or managers with permissions rejected the offer
        * Returns: none
        '''
        self.__set_status(PurchaseStatus.failed)

    def UserRejectOffer(self, userId: int):
        '''
        * Parameters: userId
        * Function to reject the offer by the store
        * Returns: none
        '''
        if userId == self.get_userId():
            self.__set_status(PurchaseStatus.accepted)


    def StoreCounterOffer(self, counterOffer: float):
        ''' 
        * Parameters: counterOffer
        * This function is responsible for updating the counter offer of the purchase
        * Returns: none
        '''
        if self.get_status() == PurchaseStatus.onGoing:
            if counterOffer >= 0:
                self.__set_counterOffer(counterOffer)
                self.__set_isOfferToStore(False)

    def UserCounterOffer(self, counterOffer: float):
        ''' 
        * Parameters: counterOffer
        * This function is responsible for updating the counter offer of the purchase
        * Returns: none
        '''
        if self.get_status() == PurchaseStatus.onGoing:
            if counterOffer >= 0:
                self.__set_counterOffer(counterOffer)
                self.__set_isOfferToStore(True)


    def updateDateOfPurchase(self, dateOfPurchase: datetime):
        ''' 
        * Parameters: dateOfPurchase
        * This function is responsible for updating the date of the purchase
        * Returns: none
        '''
        self.__set_dateOfPurchase(dateOfPurchase)
        

    def calculateTotalPrice(self) -> float:
        '''
        * Parameters: none
        * This function is responsible for returning the proposed price for the product on bid, maybe plus delivery fee later on
        * Returns: float of proposed price
        '''
        return self.get_proposedPrice()
    

#-----------------AuctionPurchase class-----------------#
class AuctionPurchase(Purchase):
    def __init__(self, purchaseId: int, userId: int, dateOfPurchase: datetime, totalPrice: float, 
                 status: PurchaseStatus, basePrice: float, startingDate: datetime, endingDate: datetime, 
                 storeId: int ,productId: int, productSpecId: int, usersWithProposedPrices: List[Tuple[int, float]] = []):
        super().__init__(purchaseId, userId, storeId, dateOfPurchase, totalPrice, status)
        self.basePrice = basePrice
        self.startingDate = startingDate
        self.endingDate = endingDate
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
    def __set_usersWithProposedPrices(self, usersWithProposedPrices: List[Tuple[int, float]]):
        self.usersWithProposedPrices = usersWithProposedPrices

    #---------------------------------Methods---------------------------------#
    def updateStatus(self, status: PurchaseStatus):
        ''' 
        * Parameters: status
        * This function is responsible for updating the status of the purchase
        * Returns: none
        '''
        self.__set_status(status) 

    def updateDateOfPurchase(self, dateOfPurchase: datetime):
        ''' 
        * Parameters: dateOfPurchase
        * This function is responsible for updating the date of the purchase
        * Returns: none
        '''
        self.__set_dateOfPurchase(dateOfPurchase)
        

    #maybe add synchronization?!?!
    def addAuctionBid(self, userId: int, proposedPrice: float) -> bool:
        ''' 
        * Parameters: userId, proposedPrice
        * This function is responsible for adding the user and their proposed price to the list of users with proposed prices, the same user can bid multiple times
        * Note: a bid can only be added if it is bigger than the current highest bid
        * Returns: true if bid was added, false if not
        '''
        if userId is not None: #For NEXT TIME, VALIDATE THAT THE USERID ISNT A STORE MANAGER/OWNER OF THE STORE PUTTING THE AUCTION
            if self.calculatedRemainingTime() > datetime.timedelta(0) and self.get_status() == PurchaseStatus.onGoing:
                if self.get_usersWithProposedPrices() == [] and proposedPrice > self.basePrice:
                    self.__set_usersWithProposedPrices(self.get_usersWithProposedPrices().append((userId, proposedPrice)))
                    return True
                if proposedPrice > self.viewHighestBiddingOffer(): #MAYBE ADD LATER ON SOME LIKE CONSTRAINTS THAT THE STORE CAN DECLARE, FOR EXAMPLE, CAN ONLY BID ATLEAST 5 DOLLARS MORE THAN HIGHEST.
                    self.__set_usersWithProposedPrices(self.get_usersWithProposedPrices().append((userId, proposedPrice)))
                    return True
        return False


    def calculateTotalPrice(self) -> float:
        '''
        * Parameters: none
        * This function is responsible for returning the highest bidding offer
        * Returns: float of highest bidding offer
        '''
        return self.viewHighestBiddingOffer()


    def viewHighestBiddingOffer(self) -> float:
        '''
        * Parameters: none
        * This function is responsible for returning the highest bidding offer
        * Returns: float of highest bidding offer
        '''
        return max(self.get_usersWithProposedPrices(), key = lambda x : x[1])[1]
        

    def calculateRemainingTime(self) -> datetime:
        '''
        * Parameters: none
        * This function is responsible for calculating the remaining time for the auction
        * Returns: datetime of remaining time
        '''
        if self.get_startingDate() < datetime.datetime.now():
            if self.get_endingDate() > datetime.datetime.now():
                return datetime.datetime.now() - self.get_endingDate()
        return datetime.timedelta(0)
    

#-----------------LotteryPurchase class-----------------#
class LotteryPurchase(Purchase):
    def __init__(self, purchaseId: int, userId: int, dateOfPurchase: datetime, totalPrice: float, status: PurchaseStatus, 
                 fullPrice: float, storeId: int, productId: int, productSpecId: int, startingDate: datetime, endingDate: datetime,  usersWithPrices: List[Tuple[int, float]] = [], winner: int = None):
        super().__init__(purchaseId, userId, storeId, dateOfPurchase, totalPrice, status)
        self.__fullPrice = fullPrice
        self.__productId = productId
        self.__productSpecId = productSpecId
        self.__usersWithPrices = usersWithPrices
        self.__startingDate = startingDate
        self.__endingDate = endingDate
        self.__winner = winner


#---------------------------------Getters and Setters---------------------------------#
    @property
    def get_purchaseId(self):
        return self.__purchaseId
    
    @property
    def __set_purchaseId(self, purchaseId: int):
        self.__purchaseId = purchaseId

    @property
    def get_userId(self):
        return self.__userId
    
    @property
    def __set_userId(self, userId: int):
        self.__userId = userId

    @property
    def get_dateOfPurchase(self):
        return self.__dateOfPurchase
    
    @property
    def __set_dateOfPurchase(self, dateOfPurchase: datetime):
        self.__dateOfPurchase = dateOfPurchase

    @property
    def get_totalPrice(self):
        return self.__totalPrice
    
    @property
    def __set_totalPrice(self, totalPrice: float):
        self.__totalPrice = totalPrice

    @property
    def get_status(self):
        return self.__status
    
    @property
    def __set_status(self, status: PurchaseStatus):
        self.__status = status

    @property
    def get_fullPrice(self):
        return self.__fullPrice
    
    @property
    def __set_fullPrice(self, fullPrice: float):
        self.__fullPrice = fullPrice

    @property
    def get_storeId(self):
        return self.__storeId
    
    @property
    def __set_storeId(self, storeId: int):
        self.__storeId = storeId

    @property
    def get_productId(self):
        return self.__productId
    
    @property
    def __set_productId(self, productId: int):
        self.__productId = productId

    @property
    def get_productSpecId(self):
        return self.__productSpecId
    
    @property
    def __set_productSpecId(self, productSpecId: int):
        self.__productSpecId = productSpecId

    @property
    def get_usersWithPrices(self):
        return self.__usersWithPrices
    
    @property
    def __set_usersWithPrices(self, usersWithPrices: List[Tuple[int, float]]):
        self.__usersWithPrices = usersWithPrices

    @property
    def get_startingDate(self):
        return self.__startingDate
    
    @property
    def __set_startingDate(self, startingDate: datetime):
        self.__startingDate = startingDate

    @property
    def get_endingDate(self):
        return self.__endingDate
    
    @property
    def __set_endingDate(self, endingDate: datetime):
        self.__endingDate = endingDate

    @property
    def get_winner(self):
        return self.__winner
    
    @property
    def __set_winner(self, winner: int):
        self.__winner = winner


#---------------------------------Methods---------------------------------#
    def updateStatus(self, status: PurchaseStatus):
        ''' 
        * Parameters: status
        * This function is responsible for updating the status of the purchase
        * Returns: none
        '''
        self.__set_status(status) 

    def updateDateOfPurchase(self, dateOfPurchase: datetime):
        ''' 
        * Parameters: dateOfPurchase
        * This function is responsible for updating the date of the purchase
        * Returns: none
        '''
        self.__set_dateOfPurchase(dateOfPurchase)
        
    def calculateTotalPrice(self) -> float:
        '''
        * Parameters: none
        * This function is responsible for returning the current total price paid in the lottery
        * Returns: float of total price so far
        '''
        return sum([x[1] for x in self.get_usersWithPrices()])


    def calculateRemainingTime(self) -> datetime:
        '''
        * Parameters: none
        * This function is responsible for calculating the remaining time for the auction
        * Returns: datetime of remaining time
        '''
        if self.get_startingDate() < datetime.datetime.now():
            if self.get_endingDate() > datetime.datetime.now():
                return datetime.datetime.now() - self.get_endingDate()
        return datetime.timedelta(0)
    
    
    def addLotteryOffer(self, userId: int, proposedPrice: float) -> bool:
        ''' 
        * Parameters: userId, proposedPrice
        * This function is responsible for adding the user and their proposed price to the list of users with proposed prices, the same user can bid multiple times
        * Note: a bid can only be added if it is bigger than the current highest bid
        * Returns: true if bid was added, false if not
        '''
        if userId is not None:
            if self.calculatedRemainingTime() > datetime.timedelta(0) and self.get_status() == PurchaseStatus.onGoing:
                if  proposedPrice + self.get_totalPrice() <= self.get_fullPrice():
                    self.__set_usersWithPrices(self.get_usersWithPrices().append((userId, proposedPrice)))
                    self.__set_totalPrice(self.get_totalPrice() + proposedPrice)

                    if proposedPrice + self.get_totalPrice() == self.get_fullPrice():
                        self.__set_status(PurchaseStatus.accepted)
                    return True
        return False


    def calculateProbabilityOfUser(self, userId: int) -> float:
        '''
        * Parameters: userId
        * This function is responsible for calculating the probability of the user winning the lottery
        * Returns: float of probability
        '''
        if userId is not None:
            if self.get_status() == PurchaseStatus.completed:
                return sum([x[1] for x in self.get_usersWithPrices() if x[0] == userId]) / self.get_fullPrice()
        return 0.0
    
    def validateUserOffers(self) -> bool:
        '''
        * Parameters: none
        * This function is responsible for validating that all users with offers have paid the full price
        * Returns: true if all users have paid the full price, false if not
        '''
        if self.get_endingDate() < datetime.datetime.now():
            if self.get_totalPrice() == self.get_fullPrice():
                self.__set_status(PurchaseStatus.accepted)
                return True
            if self.get_totalPrice() < self.get_fullPrice():
                self.__set_status(PurchaseStatus.failed)
                return False
            #log.error("this should not happen")


    def pickWinner(self) -> int:
        '''
        * Parameters: none
        * This function is responsible for picking the winner of the lottery
        * Returns: userId of the winner
        '''
        if self.get_status() == PurchaseStatus.accepted:
            usersWithPrices = self.get_usersWithPrices()
            uniqueUsersWithSumOfPrices: List[Tuple[int, float]] = []
            for user in usersWithPrices:
                if user[0] not in [x[0] for x in uniqueUsersWithSumOfPrices]:
                    uniqueUsersWithSumOfPrices.append((user[0], sum([x[1] for x in usersWithPrices if x[0] == user[0]])))
            
            #in the case of only one user
            if len(uniqueUsersWithSumOfPrices) == 1:
                self.__set_winner(uniqueUsersWithSumOfPrices[0][0])
                return uniqueUsersWithSumOfPrices[0][0]
            else:
                #in the case of multiple users
                userWinner = np.random.choice([x[0] for x in uniqueUsersWithSumOfPrices], p=[x[1] / self.get_fullPrice() for x in uniqueUsersWithSumOfPrices]) 
                self.__set_winner(userWinner)
                return userWinner
           
        return None


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
            self.purchases = []
            self.purchasesIdCounter = 0


    @property
    def get_purchases(self):
        return self.purchases
    
    @property
    def __set_purchases(self, purchases: List[Purchase]):
        self.purchases = purchases


    @property
    def get_purchasesIdCounter(self):
        return self.purchasesIdCounter
    
    @property
    def __set_purchasesIdCounter(self, purchasesIdCounter: int):
        self.purchasesIdCounter = purchasesIdCounter

#-----------------Purchases in general-----------------#

    def handleImmediatePurchase(self, purchase: ImmediatePurchase):
        '''
        * Parameters: none
        * This function is responsible for handling all immediate purchases
        * Returns: none
        '''
        
        
        

    def handleBidPurchase(self, purchase: BidPurchase):
        '''
        * Parameters: none
        * This function is responsible for handling all bid purchases
        * Returns: none
        '''
        

    def handleAuctionPurchase(self, purchase: AuctionPurchase):
        '''
        * Parameters: none
        * This function is responsible for handling all auction purchases
        * Returns: none
        '''

    def handleLotteryPurchase(self, purchase: LotteryPurchase):
        '''
        * Parameters: none
        * This function is responsible for handling all lottery purchases
        * Returns: none
        '''
        
        
        
    def handlePurchases(self): 
        '''
        * Parameters: none
        * This function is responsible for handling all purchases
        * Returns: none
        '''        
        for purchase in self.get_purchases():
            if purchase is ImmediatePurchase:
                self.handleImmediatePurchase(purchase)
            elif purchase is BidPurchase:
                self.handleBidPurchase(purchase)
            elif purchase is AuctionPurchase:
                self.handleAuctionPurchase(purchase)
            elif purchase is LotteryPurchase:
                self.handleLotteryPurchase(purchase)
            else:
                #log.error("this should not happen")
                pass


    def createImmediatePurchase(self, userId: int, dateOfPurchase: datetime, totalPrice: float, deliveryDate: datetime, shoppingCart: List[Tuple[Tuple[int,float],List[int]]]) -> bool:
        '''
        * Parameters: userId, dateOfPurchase, deliveryDate, shoppingCart, totalPriceAfterDiscounts
        * This function is responsible for creating an immediate purchase
        * Note: totalPriceAfterDiscounts is not calculated yet! Initialized as -1!
        * Returns: ImmediatePurchase object
        '''
        if userId is not None: 
            if dateOfPurchase is not None:
                if totalPrice is not None and totalPrice >= 0:
                    if deliveryDate is not None and deliveryDate > dateOfPurchase:
                        if shoppingCart is not None:
                            totalPriceAfterDiscounts = -1
                            immediatePurchase = ImmediatePurchase(self.get_purchasesIdCounter(), userId, dateOfPurchase, totalPrice, PurchaseStatus.onGoing, deliveryDate, shoppingCart, totalPriceAfterDiscounts)
                            self.get_purchases.append(immediatePurchase)
                            self.__set_purchasesIdCounter(self.get_purchasesIdCounter() + 1)
                            return True
        return False
        

    def createBidPurchase(self, userId: int, dateOfPurchase: datetime, proposedPrice: float, productId: int, productSpecId: int, storeId: int, isOfferToStore: bool = True) -> bool:
        '''
        * Parameters: userId, dateOfPurchase, proposedPrice, productId, productSpecId, storeId, isOfferToStore
        * This function is responsible for creating a bid purchase
        * Note: totalPrice initialized as -1 until it is accepted!
        * Returns: BidPurchase object
        '''
        if userId is not None:
            if dateOfPurchase is not None:
                if proposedPrice is not None and proposedPrice >= 0:
                    if productId is not None and productSpecId is not None and storeId is not None:
                        totalPrice = -1
                        bidPurchase = BidPurchase(self.get_purchasesIdCounter(), userId, dateOfPurchase, totalPrice, PurchaseStatus.onGoing, proposedPrice, productId, productSpecId, storeId, isOfferToStore)
                        self.get_purchases.append(bidPurchase)
                        self.__set_purchasesIdCounter(self.get_purchasesIdCounter() + 1)
                        return True
        return False
        

    def createAuctionPurchase(self, userId: int, dateOfPurchase: datetime, basePrice: float, startingDate: datetime, endingDate: datetime, storeId: int, productId: int, productSpecId: int, usersWithProposedPrices: List[Tuple[int, float]] = []) -> bool:
        '''
        * Parameters: userId, dateOfPurchase, totalPrice, basePrice, startingDate, endingDate, storeId, productId, productSpecId, usersWithProposedPrices
        * This function is responsible for creating an auction purchase
        * Returns: AuctionPurchase object
        '''
        status = PurchaseStatus.onGoing
        if startingDate > datetime.datetime.now():
            status = PurchaseStatus.notStarted
        
        if userId is not None:
            if dateOfPurchase is not None:
                if basePrice is not None and basePrice >= 0:
                    if startingDate is not None and startingDate > dateOfPurchase:
                        if endingDate is not None and endingDate > startingDate:
                            if storeId is not None and productId is not None and productSpecId is not None:
                                totalPrice = -1
                                auctionPurchase = AuctionPurchase(self.get_purchasesIdCounter(), userId, dateOfPurchase, totalPrice, status, basePrice, startingDate, endingDate, storeId, productId, productSpecId, usersWithProposedPrices)
                                self.get_purchases.append(auctionPurchase)
                                self.__set_purchasesIdCounter(self.get_purchasesIdCounter() + 1)
                                return True
        return False
        

    def createLotteryPurchase(self , userId: int, dateOfPurchase: datetime, fullPrice: float, storeId: int, productId: int, productSpecId: int, startingDate: datetime, endingDate: datetime, usersWithPrices: List[Tuple[int, float]] = [], winner: int = None) -> LotteryPurchase:
        '''
        * Parameters: userId, dateOfPurchase, totalPrice, fullPrice, storeId, productId, productSpecId, startingDate, endingDate, usersWithPrices, winner
        * This function is responsible for creating a lottery purchase
        * Note: totalPrice initialized as 0 until people bought lottery tickets!
        * Returns: LotteryPurchase object
        '''
        status = PurchaseStatus.onGoing
        if startingDate > datetime.datetime.now():
            status = PurchaseStatus.notStarted

        if userId is not None:
            if dateOfPurchase is not None:
                    if fullPrice is not None and fullPrice >= 0:
                        if storeId is not None and productId is not None and productSpecId is not None:
                            if startingDate is not None and startingDate > dateOfPurchase:
                                if endingDate is not None and endingDate > startingDate:
                                    totalPrice = 0 
                                    lotteryPurchase = LotteryPurchase(self.get_purchasesIdCounter(), userId, dateOfPurchase, totalPrice, status, fullPrice, storeId, productId, productSpecId, startingDate, endingDate, usersWithPrices, winner)
                                    self.get_purchases.append(lotteryPurchase)
                                    self.__set_purchasesIdCounter(self.get_purchasesIdCounter() + 1)
                                    return True
        return False
        



    def getPurchasesOfUser(self, userId: int) -> List[Purchase]:
        '''
        * Parameters: userId
        * This function is responsible for returning the purchases of the user
        * Returns: list of Purchase objects
        '''
        if userId is not None:
            return [purchase for purchase in self.purchases if purchase.get_userId() == userId]
        return None


    def getPurchasesOfStore(self, storeId: int) -> List[Purchase]:
        '''
        * Parameters: storeId
        * This function is responsible for returning the purchases of the store
        * Returns: list of Purchase objects
        '''
        purchases = []
        if storeId is not None:
            for purchase in self.purchases:
                if purchase is BidPurchase:
                    if purchase.get_storeId() == storeId:
                        purchases.append(purchase)
                
                if purchase is AuctionPurchase:
                    if purchase.get_storeId() == storeId:
                        purchases.append(purchase)
                
                if purchase is LotteryPurchase:
                    if purchase.get_storeId() == storeId:
                        purchases.append(purchase)
                
                if purchase is ImmediatePurchase:
                    for subPurchase in purchase.get_immediateSubPurchases():
                        if subPurchase.get_storeId() == storeId:
                            purchases.append(subPurchase) 
                
        return purchases



    def getOnGoingPurchases(self ) -> List[Purchase]:
        '''
        * Parameters: none
        * This function is responsible for returning the ongoing purchases
        * Returns: list of Purchase objects
        '''
        return [purchase for purchase in self.purchases if purchase.get_status() == PurchaseStatus.onGoing]
        

    def getCompletedPurchases(self) -> List[Purchase]:
        '''
        * Parameters: none
        * This function is responsible for returning the completed purchases
        * Returns: list of Purchase objects
        '''
        return [purchase for purchase in self.purchases if purchase.get_status() == PurchaseStatus.completed]

    def getFailedPurchases(self) -> List[Purchase]:
        '''
        * Parameters: none
        * This function is responsible for returning the failed purchases
        * Returns: list of Purchase objects
        '''
        return [purchase for purchase in self.purchases if purchase.get_status() == PurchaseStatus.failed]

    def getAcceptedPurchases(self) -> List[Purchase]:
        '''
        * Parameters: none
        * This function is responsible for returning the accepted purchases
        * Returns: list of Purchase objects
        '''
        return [purchase for purchase in self.purchases if purchase.get_status() == PurchaseStatus.accepted]

        
    def getPurchaseById(self, purchaseId: int) -> Purchase:
        '''
        * Parameters: purchaseId
        * This function is responsible for returning the purchase by its id
        * Returns: Purchase object
        '''
        if purchaseId is not None:
            for purchase in self.purchases:
                if purchase.get_purchaseId() == purchaseId:
                    return purchase
        return None
    

    def updateStatus(self, purchaseId: int, status: PurchaseStatus):
        '''
        * Parameters: purchaseId
        * This function is responsible for updating the status of the purchase
        * Returns: none
        '''
        purchase = self.getPurchaseById(purchaseId)
        if purchase is not None:
            purchase.updateStatus(status)

    def updateDateOfPurchase(self, purchaseId: int, dateOfPurchase: datetime):
        '''
        * Parameters: purchaseId
        * This function is responsible for updating the date of the purchase
        * Returns: none
        '''
        purchase = self.getPurchaseById(purchaseId)
        if purchase is not None:
            purchase.updateDateOfPurchase(dateOfPurchase)
        

    def calculateTotalPrice(self, purchaseId: int) -> float:
        '''
        * Parameters: purchaseId
        * This function is responsible for calculating the total price of the purchase
        * Returns: float of total price
        '''
        purchase = self.getPurchaseById(purchaseId)
        if purchase is not None:
            return purchase.calculateTotalPrice()
        return None
        


#-----------------Immediate-----------------#
    #For now, we will return the price without any discounts.
    def calculateTotalPriceAfterDiscounts(self, purchaseId: int) -> float:
        '''
        * Parameters: purchaseId
        * This function is responsible for calculating the total price of the purchase after discounts
        * Returns: float of total price after discounts
        '''
        immediatePurchase = self.getPurchaseById(purchaseId)
        if immediatePurchase is ImmediatePurchase:
            if immediatePurchase.get_status() == PurchaseStatus.onGoing or immediatePurchase.get_status() == PurchaseStatus.accepted:
                return immediatePurchase.calculateTotalPriceAfterDiscounts()
        return None
    


    
   

#-----------------Bid-----------------#


    def storeAcceptOffer(self, purchaseId: int):
        '''
        * Parameters: purchaseId
        * Validate that all store owners and managers with permissions accepted the offer
        * Returns: none
        '''
        bidPurchase = self.getPurchaseById(purchaseId)
        if bidPurchase is BidPurchase:
            if bidPurchase.get_status() == PurchaseStatus.onGoing:
                 bidPurchase.StoreAcceptOffer()
    

        
    def userAcceptOffer(self, purchaseId: int, userId: int):
        '''
        * Parameters: purchaseId, userId
        * Function to accept the offer by the store
        * Returns: none
        '''
        bidPurchase = self.getPurchaseById(purchaseId)
        if bidPurchase is BidPurchase:
            if bidPurchase.get_status() == PurchaseStatus.onGoing:
                 bidPurchase.UseracceptOffer(userId)
    

    
    def storeRejectOffer(self, purchaseId: int):
        '''
        * Parameters: purchaseId
        * Validate that one store owner or managers with permissions rejected the offer
        * Returns: none
        '''
        bidPurchase = self.getPurchaseById(purchaseId)
        if bidPurchase is BidPurchase:
            if bidPurchase.get_status() == PurchaseStatus.onGoing:
                 bidPurchase.StoreRejectOffer()
    

    def userRejectOffer(self, purchaseId: int, userId: int) :
        '''
        * Parameters: purchaseId, userId
        * Function to reject the offer by the store
        * Returns: none
        '''
        bidPurchase = self.getPurchaseById(purchaseId)
        if bidPurchase is BidPurchase:
            if bidPurchase.get_status() == PurchaseStatus.onGoing:
                bidPurchase.UserRejectOffer(userId)


    
    def storeCounterOffer(self, purchaseId: int, counterOffer: float) :
        '''
        * Parameters: purchaseId, counterOffer
        * This function is responsible for updating the counter offer of the purchase
        * Returns: none
        '''
        bidPurchase = self.getPurchaseById(purchaseId)
        if bidPurchase is BidPurchase:
            if bidPurchase.get_status() == PurchaseStatus.onGoing:
                 bidPurchase.StoreCounterOffer(counterOffer)
  

    

    def userCounterOffer(self, counterOffer: float,purchaseId: int):
        '''
        * Parameters: purchaseId, counterOffer
        * This function is responsible for updating the counter offer of the purchase
        * Returns: none
        '''
        bidPurchase = self.getPurchaseById(purchaseId)
        if bidPurchase is BidPurchase:
            if bidPurchase.get_status() == PurchaseStatus.onGoing:
                bidPurchase.UserCounterOffer(counterOffer)
    


#-----------------Auction-----------------#
        

    def addAuctionBid(self, userId: int, proposedPrice: float, purchaseId: int) -> bool:
        '''
        * Parameters: userId, proposedPrice, purchaseId
        * This function is responsible for adding the user and their proposed price to the list of users with proposed prices, the same user can bid multiple times
        * Note: a bid can only be added if it is bigger than the current highest bid
        * Returns: true if bid was added, false if not
        '''
        auctionPurchase = self.getPurchaseById(purchaseId)
        if auctionPurchase is AuctionPurchase:
            if auctionPurchase.get_status() == PurchaseStatus.onGoing:
                return auctionPurchase.addAuctionBid(userId, proposedPrice)
        return False
   


    def viewHighestBiddingOffer(self, purchaseId: int) -> float:
        '''
        * Parameters: purchaseId
        * This function is responsible for returning the highest bidding offer
        * Returns: float of highest bidding offer
        '''
        auctionPurchase = self.getPurchaseById(purchaseId)
        if auctionPurchase is AuctionPurchase:
            if auctionPurchase.get_status() == PurchaseStatus.onGoing or auctionPurchase.get_status() == PurchaseStatus.accepted:
                return auctionPurchase.viewHighestBiddingOffer()
        return None
    
        

    def calculateRemainingTime(self, purchaseId: int) -> datetime:
        '''
        * Parameters: purchaseId
        * This function is responsible for calculating the remaining time for the auction
        * Returns: datetime of remaining time
        '''
        auctionPurchase = self.getPurchaseById(purchaseId)
        if auctionPurchase is AuctionPurchase:
            if auctionPurchase.get_status() == PurchaseStatus.onGoing:
                return auctionPurchase.calculateRemainingTime()
        return datetime.timedelta(0)
   
        

#-----------------Lottery-----------------#

    def calculateRemainingTime(self, purchaseId: int) -> datetime:
        '''
        * Parameters: purchaseId
        * This function is responsible for calculating the remaining time for the auction
        * Returns: datetime of remaining time
        '''
        lotteryPurchase = self.getPurchaseById(purchaseId)
        if lotteryPurchase is LotteryPurchase:
            if lotteryPurchase.get_status() == PurchaseStatus.onGoing:
                return lotteryPurchase.calculateRemainingTime()
        return datetime.timedelta(0)
   
        

    def addLotteryOffer(self, userId: int, proposedPrice: float,purchaseId: int) -> bool:
        '''
        * Parameters: userId, proposedPrice, purchaseId
        * This function is responsible for adding the user and their proposed price to the list of users with proposed prices, the same user can bid multiple times
        * Note: a bid can only be added if it is bigger than the current highest bid
        * Returns: true if bid was added, false if not
        '''
        lotteryPurchase = self.getPurchaseById(purchaseId)
        if lotteryPurchase is LotteryPurchase:
            if lotteryPurchase.get_status() == PurchaseStatus.onGoing:
                return lotteryPurchase.addLotteryOffer(userId, proposedPrice)
        return False
    
        

    def calculateProbabilityOfUser(self, userId: int, purchaseId: int) -> float:
        '''
        * Parameters: userId, purchaseId
        * This function is responsible for calculating the probability of the user winning the lottery
        * Returns: float of probability
        '''
        lotteryPurchase = self.getPurchaseById(purchaseId)
        if lotteryPurchase is LotteryPurchase:
            if lotteryPurchase.get_status() == PurchaseStatus.onGoing or lotteryPurchase.get_status() == PurchaseStatus.accepted:
                return lotteryPurchase.calculateProbabilityOfUser(userId)
        return None
     
        


    def validateUserOffers(self, purchaseId: int) -> bool:
        '''
        * Parameters: purchaseId
        * This function is responsible for validating that all users with offers have paid the full price
        * Returns: true if all users have paid the full price, false if not
        '''
        lotteryPurchase = self.getPurchaseById(purchaseId)
        if lotteryPurchase is LotteryPurchase:
            if lotteryPurchase.get_endingDate() < datetime.datetime.now:
                return lotteryPurchase.validateUserOffers()
        return False
   

        

    def pickWinner(self,purchaseId: int) -> int:
        '''
        * Parameters: purchaseId
        * This function is responsible for picking the winner of the lottery
        * Returns: userId of the winner
        '''
        lotteryPurchase = self.getPurchaseById(purchaseId)
        if lotteryPurchase is LotteryPurchase:
            if lotteryPurchase.get_status() == PurchaseStatus.accepted:
                return lotteryPurchase.pickWinner()
        return None
