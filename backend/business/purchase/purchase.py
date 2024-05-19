#----------------- imports -----------------#
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Tuple
from backend.business.user import ShoppingCart #check if good

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
    def __init__(self, purchaseId: int, userId: int, dateOfPurchase: datetime, totalPrice: float, status: PurchaseStatus):
        self.purchaseId = purchaseId
        self.userId = userId
        self.dateOfPurchase = dateOfPurchase
        self.totalPrice = totalPrice
        self.status = status
 
    @abstractmethod
    def updateStatus(self):
        pass

    @abstractmethod
    def updateDateOfPurchase(self):
        pass

    @abstractmethod
    def calculateTotalPrice(self) -> float:
        pass


#-----------------ImmediatePurchase class-----------------#
class ImmediatePurchase(Purchase):
    # purchaseId is the unique identifier of the immediate purchase, purchase by a user of their shoppingCart
    def __init__(self, purchaseId: int, userId: int, dateOfPurchase: datetime, totalPrice: float, status: PurchaseStatus, deliveryDate: datetime, shoppingCart: 'ShoppingCart'):
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
        # call method of shoppingCart to calculate the total price of the products in the shoppingCart
        pass 


#-----------------BidPurchase class-----------------#
class BidPurchase(Purchase):
    # purchaseId and productId are the unique identifiers for the product rating, productSpec used to retrieve the details of product   
    def __init__(self, purchaseId: int, userId: int, dateOfPurchase: datetime, totalPrice: float, status: PurchaseStatus, proposedPrice: float, productId: int, productSpecId: int, storedId: int, isOfferToStore: bool = True):
        super().__init__(purchaseId, userId, dateOfPurchase, totalPrice, status)
        self.proposedPrice = proposedPrice
        self.productId = productId
        self.productSpecId = productSpecId
        self.storedId = storedId
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
    def get_storedId(self):
        return self.storedId
    
    @property
    def __set_storedId(self, storedId: int):
        self.storedId = storedId

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
            self.__set_counterOffer(counterOffer)
            self.__set_isOfferToStore(False)

    def UserCounterOffer(self, counterOffer: float):
        ''' 
        * Parameters: counterOffer
        * This function is responsible for updating the counter offer of the purchase
        * Returns: none
        '''
        if self.get_status() == PurchaseStatus.onGoing:
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
        if userId is not None:
            if self.calculatedRemainingTime() > datetime.timedelta(0) and self.get_status() == PurchaseStatus.onGoing:
                if self.get_usersWithProposedPrices() == [] and proposedPrice > self.basePrice:
                    self.__set_usersWithProposedPrices(self.get_usersWithProposedPrices().append((userId, proposedPrice)))
                    return True
                if proposedPrice > self.viewHighestBiddingOffer():
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
        return max(self.get_usersWithProposedPrices(), key=lambda x: x[1])[1]
        

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
                 fullPrice: float, storeId: int, productId: int, productSpecId: int, startingDate: datetime, endingDate: datetime,  usersWithPrices: list[Tuple[int, float]] = []):
        super().__init__(purchaseId, userId, dateOfPurchase, totalPrice, status)
        self.fullPrice = fullPrice
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
    def get_fullPrice(self):
        return self.fullPrice
    
    @property
    def __set_fullPrice(self, fullPrice: float):
        self.fullPrice = fullPrice

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
                if  proposedPrice + self.get_totalPrice() <= self.basePrice:
                    self.__set_usersWithPrices(self.get_usersWithPrices().append((userId, proposedPrice)))
                    self.__set_totalPrice(self.get_totalPrice() + proposedPrice)

                    if proposedPrice + self.get_totalPrice() == self.basePrice:
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
                self.__set_status(PurchaseStatus.completed)
                return True
            if self.get_totalPrice() < self.get_fullPrice():
                self.__set_status(PurchaseStatus.failed)
                return False
            log.error("this should not happen")


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

