import unittest
from backend.business.purchase.purchase import *
from backend.business.store.DiscountStrategy import *
import datetime
from unittest.mock import patch, MagicMock


class TestProductRating(unittest.TestCase):
    def test_product_rating(self):
        rating = ProductRating(product_id=100, rating=5)
        self.assertEqual(rating.calculate_rating(), 5)

    def test_product_rating_invalid_rating(self):
        with self.assertRaises(ValueError):
            rating = ProductRating(product_id=100, rating=6)


class TestImmediateSubPurchases(unittest.TestCase):
    
    def setUp(self):
        # Initialize an ImmediateSubPurchases object
        self.purchase = ImmediateSubPurchases(
            purchaseId=1,
            storeId=5,
            userId=123,
            dateOfPurchase=datetime.datetime.now(),
            totalPrice=200.0,
            status=PurchaseStatus.onGoing,
            productIds=[10, 20, 30]
        )

    def test_initialization(self):
        self.assertEqual(self.purchase.purchaseId, 1)
        self.assertEqual(self.purchase.storeId, 5)
        self.assertEqual(self.purchase.userId, 123)
        self.assertEqual(self.purchase.dateOfPurchase, datetime(2023, 1, 1))
        self.assertEqual(self.purchase.totalPrice, 200.0)
        self.assertEqual(self.purchase.status, PurchaseStatus.onGoing)
        self.assertEqual(self.purchase.productIds, [10, 20, 30])

    def test_getters(self):
        self.assertEqual(self.purchase.get_purchaseId, 1)
        self.assertEqual(self.purchase.get_userId, 123)
        self.assertEqual(self.purchase.get_storeId, 5)
        self.assertEqual(self.purchase.get_dateOfPurchase, datetime(2023, 1, 1))
        self.assertEqual(self.purchase.get_totalPrice, 200.0)
        self.assertEqual(self.purchase.get_status, PurchaseStatus.onGoing)
        self.assertEqual(self.purchase.get_productIds, [10, 20, 30])

    def test_setters(self):
        self.purchase.__set_purchaseId(2)
        self.assertEqual(self.purchase.purchaseId, 2)
        self.purchase.__set_userId(321)
        self.assertEqual(self.purchase.userId, 321)
        self.purchase.__set_storeId(6)
        self.assertEqual(self.purchase.storeId, 6)
        self.purchase.__set_dateOfPurchase(datetime(2023, 12, 25))
        self.assertEqual(self.purchase.dateOfPurchase, datetime(2023, 12, 25))
        self.purchase.__set_totalPrice(150.0)
        self.assertEqual(self.purchase.totalPrice, 150.0)
        self.purchase.__set_status(PurchaseStatus.completed)
        self.assertEqual(self.purchase.status, PurchaseStatus.completed)
        self.purchase.__set_productIds([40, 50, 60])
        self.assertEqual(self.purchase.productIds, [40, 50, 60])

    def test_updateStatus(self):
        self.purchase.updateStatus(PurchaseStatus.failed)
        self.assertEqual(self.purchase.status, PurchaseStatus.failed)

    def test_updateDateOfPurchase(self):
        new_date = datetime(2024, 1, 1)
        self.purchase.updateDateOfPurchase(new_date)
        self.assertEqual(self.purchase.dateOfPurchase, new_date)

    def test_calculateTotalPrice(self):
        self.assertEqual(self.purchase.calculateTotalPrice(), 200.0)

    def test_calculateTotalPriceAfterDiscount(self):
        # TODO: Implement test for calculateTotalPriceAfterDiscount once the method is implemented
        pass

    # Negative Tests
    def test_set_invalid_purchaseId(self):
        with self.assertRaises(ValueError):
            self.purchase.__set_purchaseId(-1)
        
    def test_set_invalid_userId(self):
        with self.assertRaises(ValueError):
            self.purchase.__set_userId(-1)
        
    def test_set_invalid_storeId(self):
        with self.assertRaises(ValueError):
            self.purchase.__set_storeId(-1)
        
    def test_set_invalid_totalPrice(self):
        with self.assertRaises(ValueError):
            self.purchase.__set_totalPrice(-100.0)
        
    def test_set_invalid_status(self):
        with self.assertRaises(ValueError):
            self.purchase.__set_status(None)
        
    def test_set_invalid_productIds(self):
        with self.assertRaises(ValueError):
            self.purchase.__set_productIds("invalid")
        
    def test_updateStatus_with_invalid_status(self):
        with self.assertRaises(ValueError):
            self.purchase.updateStatus("invalid")

    def test_updateDateOfPurchase_with_invalid_date(self):
        with self.assertRaises(ValueError):
            self.purchase.updateDateOfPurchase("invalid")


class TestImmediatePurchase(unittest.TestCase):

    def setUp(self):
        shopping_cart = [
            ((1, 100.0), [10, 20]),
            ((2, 50.0), [30, 40])
        ]
        self.purchase = ImmediatePurchase(
            purchaseId=1,
            userId=123,
            totalPrice=150.0,
            shoppingCart=shopping_cart,
            totalPriceAfterDiscounts=140.0
        )

    def test_initialization(self):
        self.assertEqual(self.purchase.purchaseId, 1)
        self.assertEqual(self.purchase.userId, 123)
        self.assertEqual(self.purchase.totalPrice, 150.0)
        self.assertEqual(self.purchase.totalPriceAfterDiscounts, 140.0)
        self.assertEqual(len(self.purchase.immediateSubPurchases), 2)

    def test_getters(self):
        self.assertEqual(self.purchase.get_purchaseId, 1)
        self.assertEqual(self.purchase.get_userId, 123)
        self.assertEqual(self.purchase.get_totalPrice, 150.0)
        self.assertEqual(self.purchase.get_totalPriceAfterDiscounts, 140.0)
        self.assertEqual(len(self.purchase.get_immediateSubPurchases), 2)

    def test_setters(self):
        self.purchase._ImmediatePurchase__set_purchaseId(2)
        self.assertEqual(self.purchase.purchaseId, 2)
        self.purchase._ImmediatePurchase__set_userId(321)
        self.assertEqual(self.purchase.userId, 321)
        self.purchase._ImmediatePurchase__set_totalPrice(200.0)
        self.assertEqual(self.purchase.totalPrice, 200.0)
        self.purchase._ImmediatePurchase__set_totalPriceAfterDiscounts(180.0)
        self.assertEqual(self.purchase.totalPriceAfterDiscounts, 180.0)
        self.purchase._ImmediatePurchase__set_immediateSubPurchases([])
        self.assertEqual(self.purchase.immediateSubPurchases, [])

    def test_updateStatus(self):
        self.purchase.updateStatus(PurchaseStatus.failed)
        self.assertEqual(self.purchase.status, PurchaseStatus.failed)

    def test_updateDateOfPurchase(self):
        new_date = datetime(2024, 1, 1)
        self.purchase.updateDateOfPurchase(new_date)
        self.assertEqual(self.purchase.dateOfPurchase, new_date)

    def test_calculateTotalPrice(self):
        self.assertEqual(self.purchase.calculateTotalPrice(), 150.0)

    def test_calculateTotalPriceAfterDiscounts(self):
        # TODO: Implement the method in the class and update this test
        self.assertEqual(self.purchase.calculateTotalPriceAfterDiscounts([]), 150.0)

    def test_validatedPurchase(self):
        delivery_date = datetime(2024, 12, 25)
        self.purchase.validatedPurchase(delivery_date)
        self.assertEqual(self.purchase.status, PurchaseStatus.accepted)
        self.assertIsNotNone(self.purchase.dateOfPurchase)
        self.assertEqual(self.purchase.deliveryDate, delivery_date)

    def test_invalidPurchase(self):
        self.purchase.invalidPurchase()
        self.assertEqual(self.purchase.status, PurchaseStatus.failed)
        self.assertIsNone(self.purchase.dateOfPurchase)
        self.assertIsNone(self.purchase.deliveryDate)

    def test_checkIfCompletedPurchase(self):
        self.purchase.validatedPurchase(datetime(2023, 1, 1))
        self.purchase._ImmediatePurchase__set_deliveryDate(datetime(2022, 12, 25))
        self.assertTrue(self.purchase.checkIfCompletedPurchase())
        self.assertEqual(self.purchase.status, PurchaseStatus.completed)

    # Negative Tests
    def test_set_invalid_purchaseId(self):
        with self.assertRaises(ValueError):
            self.purchase._ImmediatePurchase__set_purchaseId(-1)

    def test_set_invalid_userId(self):
        with self.assertRaises(ValueError):
            self.purchase._ImmediatePurchase__set_userId(-1)

    def test_set_invalid_totalPrice(self):
        with self.assertRaises(ValueError):
            self.purchase._ImmediatePurchase__set_totalPrice(-100.0)

    def test_set_invalid_totalPriceAfterDiscounts(self):
        with self.assertRaises(ValueError):
            self.purchase._ImmediatePurchase__set_totalPriceAfterDiscounts(-100.0)

    def test_updateStatus_with_invalid_status(self):
        with self.assertRaises(ValueError):
            self.purchase.updateStatus("invalid")

    def test_updateDateOfPurchase_with_invalid_date(self):
        with self.assertRaises(ValueError):
            self.purchase.updateDateOfPurchase("invalid")

    def test_validatedPurchase_with_invalid_date(self):
        with self.assertRaises(ValueError):
            self.purchase.validatedPurchase("invalid")    

class TestBidPurchase(unittest.TestCase):
    
    def setUp(self):
        # Initialize a BidPurchase object
        self.purchase = BidPurchase(
            purchaseId=1,
            userId=123,
            proposedPrice=99.99,
            productId=10,
            productSpecId=100,
            storeId=5,
            isOfferToStore=True
        )

    def test_initialization(self):
        self.assertEqual(self.purchase.purchaseId, 1)
        self.assertEqual(self.purchase.userId, 123)
        self.assertEqual(self.purchase.proposedPrice, 99.99)
        self.assertEqual(self.purchase.productId, 10)
        self.assertEqual(self.purchase.productSpecId, 100)
        self.assertEqual(self.purchase.storeId, 5)
        self.assertIsNone(self.purchase.deliveryDate)
        self.assertTrue(self.purchase.isOfferToStore)

    def test_getters(self):
        self.assertEqual(self.purchase.get_purchaseId, 1)
        self.assertEqual(self.purchase.get_userId, 123)
        self.assertEqual(self.purchase.get_proposedPrice, 99.99)
        self.assertEqual(self.purchase.get_productId, 10)
        self.assertEqual(self.purchase.get_productSpecId, 100)
        self.assertEqual(self.purchase.get_storeId, 5)
        self.assertIsNone(self.purchase.get_deliveryDate)
        self.assertTrue(self.purchase.get_isOfferToStore)

    def test_setters(self):
        self.purchase.__set_purchaseId(2)
        self.assertEqual(self.purchase.purchaseId, 2)
        self.purchase.__set_userId(321)
        self.assertEqual(self.purchase.userId, 321)
        self.purchase.__set_proposedPrice(79.99)
        self.assertEqual(self.purchase.proposedPrice, 79.99)
        self.purchase.__set_productId(20)
        self.assertEqual(self.purchase.productId, 20)
        self.purchase.__set_productSpecId(200)
        self.assertEqual(self.purchase.productSpecId, 200)
        self.purchase.__set_storeId(6)
        self.assertEqual(self.purchase.storeId, 6)
        self.purchase.__set_deliveryDate(datetime(2023, 12, 25))
        self.assertEqual(self.purchase.deliveryDate, datetime(2023, 12, 25))
        self.purchase.__set_isOfferToStore(False)
        self.assertFalse(self.purchase.isOfferToStore)
    
    def test_updateStatus(self):
        self.purchase.updateStatus(PurchaseStatus.accepted)
        self.assertEqual(self.purchase.status, PurchaseStatus.accepted)

    def test_StoreAcceptOffer(self):
        delivery_date = datetime.datetime.now() + datetime.timedelta(days=5)
        self.purchase.StoreAcceptOffer(deliveryDate=delivery_date, totalPrice=120.0)
        self.assertEqual(self.purchase.status, PurchaseStatus.accepted)
        self.assertIsNotNone(self.purchase.dateOfPurchase)
        self.assertEqual(self.purchase.deliveryDate, delivery_date)

    def test_UserAcceptOffer(self):
        delivery_date = datetime.datetime.now() + datetime.timedelta(days=5)
        self.purchase.UseracceptOffer(userId=123, deliveryDate=delivery_date, totalPrice=120.0)
        self.assertEqual(self.purchase.status, PurchaseStatus.accepted)
        self.assertIsNotNone(self.purchase.dateOfPurchase)
        self.assertEqual(self.purchase.deliveryDate, delivery_date)

    def test_StoreRejectOffer(self):
        self.purchase.StoreRejectOffer()
        self.assertEqual(self.purchase.status, PurchaseStatus.failed)

    def test_UserRejectOffer(self):
        self.purchase.UserRejectOffer(userId=123)
        self.assertEqual(self.purchase.status, PurchaseStatus.failed)

    def test_StoreCounterOffer(self):
        self.purchase.StoreCounterOffer(110.0)
        self.assertEqual(self.purchase.proposedPrice, 110.0)
        self.assertFalse(self.purchase.isOfferToStore)

    def test_UserCounterOffer(self):
        self.purchase.UserCounterOffer(105.0)
        self.assertEqual(self.purchase.proposedPrice, 105.0)
        self.assertTrue(self.purchase.isOfferToStore)

    def test_updateDateOfPurchase(self):
        date_of_purchase = datetime(2023, 12, 25)
        self.purchase.updateDateOfPurchase(date_of_purchase)
        self.assertEqual(self.purchase.dateOfPurchase, date_of_purchase)

    def test_calculateTotalPrice(self):
        self.assertEqual(self.purchase.calculateTotalPrice(), 99.99)

    def test_checkIfCompletedPurchase(self):
        self.purchase.__set_status(PurchaseStatus.accepted)
        self.purchase.__set_deliveryDate(datetime.datetime.now() - datetime.timedelta(days=1))
        self.assertTrue(self.purchase.checkIfCompletedPurchase())
        self.assertEqual(self.purchase.status, PurchaseStatus.completed)

    # Negative Tests
    def test_UserAcceptOffer_with_wrong_userId(self):
        delivery_date = datetime.datetime.now() + datetime.timedelta(days=5)
        self.purchase.UseracceptOffer(userId=999, deliveryDate=delivery_date, totalPrice=120.0)
        self.assertNotEqual(self.purchase.status, PurchaseStatus.accepted)
        self.assertIsNone(self.purchase.dateOfPurchase)
        self.assertIsNone(self.purchase.deliveryDate)

    def test_UserRejectOffer_with_wrong_userId(self):
        self.purchase.UserRejectOffer(userId=999)
        self.assertNotEqual(self.purchase.status, PurchaseStatus.failed)

    def test_StoreCounterOffer_with_invalid_counterOffer(self):
        self.purchase.StoreCounterOffer(-10.0)
        self.assertNotEqual(self.purchase.proposedPrice, -10.0)
        self.assertTrue(self.purchase.isOfferToStore)

    def test_UserCounterOffer_with_invalid_counterOffer(self):
        self.purchase.UserCounterOffer(-5.0)
        self.assertNotEqual(self.purchase.proposedPrice, -5.0)
        self.assertTrue(self.purchase.isOfferToStore)
    
    def test_checkIfCompletedPurchase_with_incorrect_status(self):
        self.purchase.__set_status(PurchaseStatus.onGoing)
        self.purchase.__set_deliveryDate(datetime.datetime.now() - datetime.timedelta(days=1))
        self.assertFalse(self.purchase.checkIfCompletedPurchase())
        self.assertNotEqual(self.purchase.status, PurchaseStatus.completed)


class TestAuctionPurchase(unittest.TestCase):

    def setUp(self):
        self.purchase = AuctionPurchase(
            purchaseId=1,
            basePrice=100.0,
            startingDate=datetime(2023, 1, 1),
            endingDate=datetime(2023, 12, 31),
            storeId=1,
            productId=101,
            productSpecId=202,
            usersWithProposedPrices=[(10, 150.0), (20, 200.0)]
        )

    def test_initialization(self):
        self.assertEqual(self.purchase.purchaseId, 1)
        self.assertEqual(self.purchase.basePrice, 100.0)
        self.assertEqual(self.purchase.startingDate, datetime(2023, 1, 1))
        self.assertEqual(self.purchase.endingDate, datetime(2023, 12, 31))
        self.assertEqual(self.purchase.storeId, 1)
        self.assertEqual(self.purchase.productId, 101)
        self.assertEqual(self.purchase.productSpecId, 202)
        self.assertEqual(self.purchase.status, PurchaseStatus.onGoing)
        self.assertEqual(self.purchase.usersWithProposedPrices, [(10, 150.0), (20, 200.0)])

    def test_getters(self):
        self.assertEqual(self.purchase.get_purchaseId, 1)
        self.assertEqual(self.purchase.get_basePrice, 100.0)
        self.assertEqual(self.purchase.get_startingDate, datetime(2023, 1, 1))
        self.assertEqual(self.purchase.get_endingDate, datetime(2023, 12, 31))
        self.assertEqual(self.purchase.get_storeId, 1)
        self.assertEqual(self.purchase.get_productId, 101)
        self.assertEqual(self.purchase.get_productSpecId, 202)
        self.assertEqual(self.purchase.get_status, PurchaseStatus.onGoing)
        self.assertEqual(self.purchase.get_usersWithProposedPrices, [(10, 150.0), (20, 200.0)])

    def test_setters(self):
        self.purchase._AuctionPurchase__set_purchaseId(2)
        self.assertEqual(self.purchase.purchaseId, 2)
        self.purchase._AuctionPurchase__set_basePrice(200.0)
        self.assertEqual(self.purchase.basePrice, 200.0)
        self.purchase._AuctionPurchase__set_startingDate(datetime(2023, 2, 1))
        self.assertEqual(self.purchase.startingDate, datetime(2023, 2, 1))
        self.purchase._AuctionPurchase__set_endingDate(datetime(2023, 11, 30))
        self.assertEqual(self.purchase.endingDate, datetime(2023, 11, 30))
        self.purchase._AuctionPurchase__set_storeId(2)
        self.assertEqual(self.purchase.storeId, 2)
        self.purchase._AuctionPurchase__set_productId(102)
        self.assertEqual(self.purchase.productId, 102)
        self.purchase._AuctionPurchase__set_productSpecId(203)
        self.assertEqual(self.purchase.productSpecId, 203)
        self.purchase._AuctionPurchase__set_status(PurchaseStatus.accepted)
        self.assertEqual(self.purchase.status, PurchaseStatus.accepted)
        self.purchase._AuctionPurchase__set_usersWithProposedPrices([(30, 250.0)])
        self.assertEqual(self.purchase.usersWithProposedPrices, [(30, 250.0)])

    def test_updateStatus(self):
        self.purchase.updateStatus(PurchaseStatus.failed)
        self.assertEqual(self.purchase.status, PurchaseStatus.failed)

    def test_updateDateOfPurchase(self):
        new_date = datetime(2024, 1, 1)
        self.purchase.updateDateOfPurchase(new_date)
        self.assertEqual(self.purchase.dateOfPurchase, new_date)

    def test_addAuctionBid_success(self):
        success = self.purchase.addAuctionBid(30, 250.0)
        self.assertTrue(success)
        self.assertEqual(self.purchase.usersWithProposedPrices[-1], (30, 250.0))

    def test_addAuctionBid_failure(self):
        success = self.purchase.addAuctionBid(40, 150.0)
        self.assertFalse(success)

    def test_calculateTotalPrice(self):
        self.assertEqual(self.purchase.calculateTotalPrice(), 200.0)

    def test_viewHighestBiddingOffer(self):
        self.assertEqual(self.purchase.viewHighestBiddingOffer(), 200.0)

    def test_calculateRemainingTime(self):
        remaining_time = self.purchase.calculateRemainingTime()
        self.assertGreaterEqual(remaining_time, timedelta(0))

    def test_checkIfAuctionEnded(self):
        ended = self.purchase.checkIfAuctionEnded()
        self.assertFalse(ended)
        # Simulate ending of auction
        self.purchase._AuctionPurchase__set_endingDate(datetime(2023, 1, 1))
        ended = self.purchase.checkIfAuctionEnded()
        self.assertTrue(ended)
        self.assertEqual(self.purchase.status, PurchaseStatus.failed)

    def test_validatePurchaseOfUser_success(self):
        delivery_date = datetime(2024, 1, 1)
        self.purchase._AuctionPurchase__set_userId(20)
        validated = self.purchase.validatePurchaseOfUser(20, delivery_date)
        self.assertTrue(validated)
        self.assertEqual(self.purchase.status, PurchaseStatus.accepted)
        self.assertEqual(self.purchase.deliveryDate, delivery_date)

    def test_validatePurchaseOfUser_failure(self):
        delivery_date = datetime(2024, 1, 1)
        self.purchase._AuctionPurchase__set_userId(20)
        validated = self.purchase.validatePurchaseOfUser(30, delivery_date)
        self.assertFalse(validated)

    def test_invalidatePurchaseOfUser_success(self):
        self.purchase._AuctionPurchase__set_userId(20)
        invalidated = self.purchase.invalidatePurchaseOfUser(20)
        self.assertTrue(invalidated)
        self.assertEqual(self.purchase.status, PurchaseStatus.failed)

    def test_invalidatePurchaseOfUser_failure(self):
        self.purchase._AuctionPurchase__set_userId(20)
        invalidated = self.purchase.invalidatePurchaseOfUser(30)
        self.assertFalse(invalidated)

    def test_checkIfCompletedPurchase(self):
        self.purchase._AuctionPurchase__set_status(PurchaseStatus.accepted)
        self.purchase._AuctionPurchase__set_deliveryDate(datetime(2023, 1, 1))
        completed = self.purchase.checkIfCompletedPurchase()
        self.assertTrue(completed)
        self.assertEqual(self.purchase.status, PurchaseStatus.completed)

    # Negative Tests
    def test_set_invalid_basePrice(self):
        with self.assertRaises(ValueError):
            self.purchase._AuctionPurchase__set_basePrice(-100.0)

    def test_set_invalid_dates(self):
        with self.assertRaises(ValueError):
            self.purchase._AuctionPurchase__set_startingDate("invalid")
        with self.assertRaises(ValueError):
            self.purchase._AuctionPurchase__set_endingDate("invalid")

    def test_addAuctionBid_invalid(self):
        with self.assertRaises(ValueError):
            self.purchase.addAuctionBid(None, 250.0)

    def test_updateStatus_with_invalid_status(self):
        with self.assertRaises(ValueError):
            self.purchase.updateStatus("invalid")

    def test_updateDateOfPurchase_with_invalid_date(self):
        with self.assertRaises(ValueError):
            self.purchase.updateDateOfPurchase("invalid")


class TestLotteryPurchase(unittest.TestCase):

    def setUp(self):
        self.purchaseId = 1
        self.fullPrice = 100.0
        self.storeId = 1
        self.productId = 1
        self.productSpecId = 1
        self.startingDate = datetime.now() - timedelta(days=1)
        self.endingDate = datetime.now() + timedelta(days=1)
        self.usersWithPrices = [(1, 10), (2, 20)]
        self.lottery_purchase = LotteryPurchase(
            self.purchaseId, self.fullPrice, self.storeId, self.productId, 
            self.productSpecId, self.startingDate, self.endingDate, self.usersWithPrices
        )

    def test_initialization(self):
        self.assertEqual(self.lottery_purchase.get_fullPrice, self.fullPrice)
        self.assertEqual(self.lottery_purchase.get_storeId, self.storeId)
        self.assertEqual(self.lottery_purchase.get_productId, self.productId)
        self.assertEqual(self.lottery_purchase.get_productSpecId, self.productSpecId)
        self.assertEqual(self.lottery_purchase.get_startingDate, self.startingDate)
        self.assertEqual(self.lottery_purchase.get_endingDate, self.endingDate)
        self.assertEqual(self.lottery_purchase.get_usersWithPrices, self.usersWithPrices)
        self.assertEqual(self.lottery_purchase.get_totalPrice, 0)

    def test_calculate_total_price(self):
        self.assertEqual(self.lottery_purchase.calculateTotalPrice(), 30)

    def test_calculate_remaining_time(self):
        remaining_time = self.lottery_purchase.calculateRemainingTime()
        expected_time = datetime.now() - self.endingDate
        self.assertAlmostEqual(remaining_time.total_seconds(), expected_time.total_seconds(), delta=1)

    def test_add_lottery_offer(self):
        result = self.lottery_purchase.addLotteryOffer(3, 50)
        self.assertTrue(result)
        self.assertEqual(self.lottery_purchase.get_totalPrice, 50)

        result = self.lottery_purchase.addLotteryOffer(4, 60)
        self.assertFalse(result)  # Exceeds full price

    def test_calculate_probability_of_user(self):
        self.lottery_purchase.updateStatus(PurchaseStatus.completed)
        self.assertEqual(self.lottery_purchase.calculateProbabilityOfUser(1), 10 / self.fullPrice)
        self.assertEqual(self.lottery_purchase.calculateProbabilityOfUser(2), 20 / self.fullPrice)

    def test_validate_user_offers(self):
        self.lottery_purchase.__set_totalPrice(100)
        result = self.lottery_purchase.validateUserOffers()
        self.assertTrue(result)
        self.assertEqual(self.lottery_purchase.get_status, PurchaseStatus.accepted)

        self.lottery_purchase.__set_totalPrice(50)
        result = self.lottery_purchase.validateUserOffers()
        self.assertFalse(result)
        self.assertEqual(self.lottery_purchase.get_status, PurchaseStatus.failed)

    def test_check_if_lottery_ended_successfully(self):
        self.lottery_purchase.__set_totalPrice(100)
        self.lottery_purchase.__set_endingDate(datetime.now() - timedelta(days=1))
        result = self.lottery_purchase.checkIfLotteryEndedSuccessfully()
        self.assertTrue(result)
        self.assertEqual(self.lottery_purchase.get_status, PurchaseStatus.accepted)

        self.lottery_purchase.__set_totalPrice(50)
        self.lottery_purchase.__set_endingDate(datetime.now() - timedelta(days=1))
        result = self.lottery_purchase.checkIfLotteryEndedSuccessfully()
        self.assertTrue(result)
        self.assertEqual(self.lottery_purchase.get_status, PurchaseStatus.failed)

    def test_pick_winner(self):
        self.lottery_purchase.__set_totalPrice(100)
        self.lottery_purchase.__set_endingDate(datetime.now() - timedelta(days=1))
        self.lottery_purchase.__set_status(PurchaseStatus.accepted)
        winner = self.lottery_purchase.pickWinner()
        self.assertIn(winner, [1, 2])

    def test_validate_delivery_of_winner(self):
        self.lottery_purchase.__set_userId(1)
        self.lottery_purchase.validateDeliveryOfWinner(1, datetime.now())
        self.assertEqual(self.lottery_purchase.get_status, PurchaseStatus.accepted)
        self.assertIsNotNone(self.lottery_purchase.get_dateOfPurchase)
        self.assertIsNotNone(self.lottery_purchase.get_deliveryDate)

    def test_invalidate_delivery_of_winner(self):
        self.lottery_purchase.__set_userId(1)
        self.lottery_purchase.invalidateDeliveryOfWinner(1)
        self.assertEqual(self.lottery_purchase.get_status, PurchaseStatus.failed)

    def test_check_if_completed_purchase(self):
        self.lottery_purchase.__set_status(PurchaseStatus.accepted)
        self.lottery_purchase.__set_deliveryDate(datetime.now() - timedelta(days=1))
        result = self.lottery_purchase.checkIfCompletedPurchase()
        self.assertTrue(result)
        self.assertEqual(self.lottery_purchase.get_status, PurchaseStatus.completed)


import unittest
from unittest.mock import Mock
from datetime import datetime, timedelta

# Assuming these classes are imported or defined somewhere else in your project
# from your_module import PurchaseFacade, ImmediatePurchase, BidPurchase, AuctionPurchase, LotteryPurchase, StoreRating, ProductRating, PurchaseStatus

class TestPurchaseFacade(unittest.TestCase):

    def setUp(self):
        self.purchase_facade = PurchaseFacade()
        
        # Mocking purchases
        self.purchase_mock = MagicMock()
        self.purchase_mock.get_storeId.return_value = 1
        self.purchase_mock.get_status.return_value = PurchaseStatus.completed
        self.purchase_mock.get_userId.return_value = 1
        self.purchase_mock.rateStore.return_value = None  # Assuming rateStore of Purchase returns None

        # Mocking Immediate purchase
        self.immediate_purchase = MagicMock(spec=ImmediatePurchase)

        # Mocking Bid purchase
        self.bid_purchase_mock = MagicMock(spec=BidPurchase)

        # Mocking auction purchases
        self.auction_purchase_mock = MagicMock(spec=AuctionPurchase)

        # Mocking lottery purchases
        self.lottery_purchase_mock = MagicMock(spec=LotteryPurchase)

        # Mocking ratings
        self.purchase_facade.getPurchaseById = MagicMock(return_value=self.purchase_mock)
        self.purchase_facade.hasUserAlreadyRatedStore = MagicMock(return_value=False)
        self.purchase_facade.calculateNewStoreRating = MagicMock(return_value=4.5)
        
        self.purchase_facade.hasUserAlreadyRatedProduct = MagicMock(return_value=False)
        self.purchase_facade.calculateNewProductRating = MagicMock(return_value=4.5)

        self.purchase_facade.get_ratingIdCounter = MagicMock(return_value=1)
        self.purchase_facade.__set_ratingIdCounter = MagicMock()

    def test_singleton_instance(self):
        instance1 = PurchaseFacade()
        instance2 = PurchaseFacade()
        self.assertIs(instance1, instance2)

    def test_createImmediatePurchase(self):
        self.purchase_facade.purchases = []
        self.purchase_facade.purchasesIdCounter = 0
        userId = 1
        totalPrice = 100.0
        shoppingCart = [((1, 10.0), [1, 2])]
        result = self.purchase_facade.createImmediatePurchase(userId, totalPrice, shoppingCart)
        self.assertTrue(result)
        self.assertEqual(len(self.purchase_facade.purchases), 1)
        self.assertEqual(self.purchase_facade.purchasesIdCounter, 1)

    def test_createBidPurchase(self):
        self.purchase_facade.purchases = []
        self.purchase_facade.purchasesIdCounter = 0
        userId = 1
        proposedPrice = 50.0
        productId = 101
        productSpecId = 1001
        storeId = 201
        result = self.purchase_facade.createBidPurchase(userId, proposedPrice, productId, productSpecId, storeId)
        self.assertTrue(result)
        self.assertEqual(len(self.purchase_facade.purchases), 1)
        self.assertEqual(self.purchase_facade.purchasesIdCounter, 1)

    def test_createAuctionPurchase(self):
        self.purchase_facade.purchases = []
        self.purchase_facade.purchasesIdCounter = 0
        basePrice = 100.0
        startingDate = datetime.now()
        endingDate = startingDate + timedelta(days=1)
        storeId = 201
        productId = 101
        productSpecId = 1001
        usersWithProposedPrices = [(1, 110.0)]
        result = self.purchase_facade.createAuctionPurchase(basePrice, startingDate, endingDate, storeId, productId, productSpecId, usersWithProposedPrices)
        self.assertTrue(result)
        self.assertEqual(len(self.purchase_facade.purchases), 1)
        self.assertEqual(self.purchase_facade.purchasesIdCounter, 1)

    def test_createLotteryPurchase(self):
        self.purchase_facade.purchases = []
        self.purchase_facade.purchasesIdCounter = 0
        userId = 1
        fullPrice = 200.0
        storeId = 201
        productId = 101
        productSpecId = 1001
        startingDate = datetime.now()
        endingDate = startingDate + timedelta(days=1)
        usersWithPrices = [(1, 20.0)]
        result = self.purchase_facade.createLotteryPurchase(userId, fullPrice, storeId, productId, productSpecId, startingDate, endingDate, usersWithPrices)
        self.assertTrue(result)
        self.assertEqual(len(self.purchase_facade.purchases), 1)
        self.assertEqual(self.purchase_facade.purchasesIdCounter, 1)

    def test_getPurchasesOfUser(self):
        self.purchase_facade.purchases = []
        purchase1 = Mock()
        purchase1.get_userId.return_value = 1
        purchase2 = Mock()
        purchase2.get_userId.return_value = 2
        self.purchase_facade.purchases = [purchase1, purchase2]
        result = self.purchase_facade.getPurchasesOfUser(1)
        self.assertEqual(result, [purchase1])

    def test_getPurchasesOfStore(self):
        self.purchase_facade.purchases = []
        purchase1 = Mock(spec=BidPurchase)
        purchase1.get_storeId.return_value = 1
        purchase2 = Mock(spec=AuctionPurchase)
        purchase2.get_storeId.return_value = 2
        self.purchase_facade.purchases = [purchase1, purchase2]
        result = self.purchase_facade.getPurchasesOfStore(1)
        self.assertEqual(result, [purchase1])

    def test_getOnGoingPurchases(self):
        self.purchase_facade.purchases = []
        purchase1 = Mock()
        purchase1.get_status.return_value = PurchaseStatus.onGoing
        purchase2 = Mock()
        purchase2.get_status.return_value = PurchaseStatus.completed
        self.purchase_facade.purchases = [purchase1, purchase2]
        result = self.purchase_facade.getOnGoingPurchases()
        self.assertEqual(result, [purchase1])

    def test_getCompletedPurchases(self):
        self.purchase_facade.purchases = []
        purchase1 = Mock()
        purchase1.get_status.return_value = PurchaseStatus.onGoing
        purchase2 = Mock()
        purchase2.get_status.return_value = PurchaseStatus.completed
        self.purchase_facade.purchases = [purchase1, purchase2]
        result = self.purchase_facade.getCompletedPurchases()
        self.assertEqual(result, [purchase2])

    def test_getFailedPurchases(self):
        self.purchase_facade.purchases = []
        purchase1 = Mock()
        purchase1.get_status.return_value = PurchaseStatus.failed
        purchase2 = Mock()
        purchase2.get_status.return_value = PurchaseStatus.completed
        self.purchase_facade.purchases = [purchase1, purchase2]
        result = self.purchase_facade.getFailedPurchases()
        self.assertEqual(result, [purchase1])

    def test_getAcceptedPurchases(self):
        self.purchase_facade.purchases = []
        purchase1 = Mock()
        purchase1.get_status.return_value = PurchaseStatus.accepted
        purchase2 = Mock()
        purchase2.get_status.return_value = PurchaseStatus.completed
        self.purchase_facade.purchases = [purchase1, purchase2]
        result = self.purchase_facade.getAcceptedPurchases()
        self.assertEqual(result, [purchase1])

    def test_getPurchaseById(self):
        self.purchase_facade.purchases = []
        purchase1 = Mock()
        purchase1.get_purchaseId.return_value = 1
        purchase2 = Mock()
        purchase2.get_purchaseId.return_value = 2
        self.purchase_facade.purchases = [purchase1, purchase2]
        result = self.purchase_facade.getPurchaseById(1)
        self.assertEqual(result, purchase1)

    def test_updateStatus(self):
        purchase = Mock()
        purchase.get_purchaseId.return_value = 1
        self.purchase_facade.purchases = [purchase]
        self.purchase_facade.updateStatus(1, PurchaseStatus.completed)
        purchase.updateStatus.assert_called_once_with(PurchaseStatus.completed)

    def test_updateDateOfPurchase(self):
        purchase = Mock()
        purchase.get_purchaseId.return_value = 1
        self.purchase_facade.purchases = [purchase]
        date = datetime.now()
        self.purchase_facade.updateDateOfPurchase(1, date)
        purchase.updateDateOfPurchase.assert_called_once_with(date)

    def test_calculateTotalPrice(self):
        purchase = Mock()
        purchase.get_purchaseId.return_value = 1
        purchase.calculateTotalPrice.return_value = 100.0
        self.purchase_facade.purchases = [purchase]
        result = self.purchase_facade.calculateTotalPrice(1)
        self.assertEqual(result, 100.0)

    def test_hasUserAlreadyRatedStore(self):
        rating = Mock(spec=StoreRating)
        rating.get_purchaseId.return_value = 1
        rating.get_userId.return_value = 1
        rating.get_storeId.return_value = 1
        self.purchase_facade.ratings = [rating]
        result = self.purchase_facade.hasUserAlreadyRatedStore(1, 1, 1)
        self.assertTrue(result)

    def test_hasUserAlreadyRatedProduct(self):
        rating = Mock(spec=ProductRating)
        rating.get_purchaseId.return_value = 1
        rating.get_userId.return_value = 1
        rating.get_productSpecId.return_value = 1
        self.purchase_facade.ratings = [rating]
        result = self.purchase_facade.hasUserAlreadyRatedProduct(1, 1, 1)
        self.assertTrue(result)

    def test_calculateNewStoreRating(self):
        rating1 = Mock(spec=StoreRating)
        rating1.get_storeId.return_value = 1
        rating1.get_rating.return_value = 4.0
        rating2 = Mock(spec=StoreRating)
        rating2.get_storeId.return_value = 1
        rating2.get_rating.return_value = 5.0
        self.purchase_facade.ratings = [rating1, rating2]
        result = self.purchase_facade.calculateNewStoreRating(1)
        self.assertEqual(result, 4.5)

    def test_calculateNewProductRating(self):
        rating1 = Mock(spec=ProductRating)
        rating1.get_productSpecId.return_value = 1
        rating1.get_rating.return_value = 3.0
        rating2 = Mock(spec=ProductRating)
        rating2.get_productSpecId.return_value = 1
        rating2.get_rating.return_value = 5.0
        self.purchase_facade.ratings = [rating1, rating2]
        result = self.purchase_facade.calculateNewProductRating(1)
        self.assertEqual(result, 4.0)

    def test_rateStore(self):
        purchaseId = 1
        userId = 1
        storeId = 1
        rating = 4.0
        description = "Great service!"

        new_rating = self.facade.rateStore(purchaseId, userId, storeId, rating, description)
        
        self.facade.getPurchaseById.assert_called_with(purchaseId)
        self.purchase_mock.get_storeId.assert_called()
        self.purchase_mock.get_status.assert_called()
        self.facade.hasUserAlreadyRatedStore.assert_called_with(purchaseId, userId, storeId)
        self.purchase_mock.get_userId.assert_called()
        self.facade.calculateNewStoreRating.assert_called_with(storeId)
        
        self.assertEqual(new_rating, 4.5)
        self.assertEqual(len(self.facade.ratings), 1)

    def test_rateProduct(self):
        purchaseId = 1
        userId = 1
        productSpecId = 1
        rating = 5.0
        description = "Excellent product!"

        new_rating = self.facade.rateProduct(purchaseId, userId, productSpecId, rating, description)
        
        self.facade.getPurchaseById.assert_called_with(purchaseId)
        self.purchase_mock.get_status.assert_called()
        self.facade.hasUserAlreadyRatedProduct.assert_called_with(purchaseId, userId, productSpecId)
        self.purchase_mock.get_userId.assert_called()
        self.facade.calculateNewProductRating.assert_called_with(productSpecId)
        
        self.assertEqual(new_rating, 4.5)
        self.assertEqual(len(self.facade.ratings), 1)

    def test_checkIfCompletedPurchase(self):
        purchaseId = 1
        self.purchase_mock.checkIfCompletedPurchase.return_value = True

        is_completed = self.facade.checkIfCompletedPurchase(purchaseId)
        
        self.facade.getPurchaseById.assert_called_with(purchaseId)
        self.purchase_mock.checkIfCompletedPurchase.assert_called()
        
        self.assertTrue(is_completed)

    def test_calculateTotalPriceAfterDiscounts(self):
        purchaseId = 1
        
        # Test when status is onGoing
        self.immediate_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        self.immediate_purchase_mock.calculateTotalPriceAfterDiscounts.return_value = 100.0
        total_price = self.purchase_facade.calculateTotalPriceAfterDiscounts(purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.immediate_purchase_mock.get_status.assert_called()
        self.immediate_purchase_mock.calculateTotalPriceAfterDiscounts.assert_called()
        self.assertEqual(total_price, 100.0)

        # Test when status is accepted
        self.immediate_purchase_mock.get_status.return_value = PurchaseStatus.accepted
        self.immediate_purchase_mock.calculateTotalPriceAfterDiscounts.return_value = 200.0
        total_price = self.purchase_facade.calculateTotalPriceAfterDiscounts(purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.immediate_purchase_mock.get_status.assert_called()
        self.immediate_purchase_mock.calculateTotalPriceAfterDiscounts.assert_called()
        self.assertEqual(total_price, 200.0)

        # Test when status is neither onGoing nor accepted
        self.immediate_purchase_mock.get_status.return_value = PurchaseStatus.completed
        total_price = self.purchase_facade.calculateTotalPriceAfterDiscounts(purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.immediate_purchase_mock.get_status.assert_called()
        self.assertIsNone(total_price)

    def test_validatePurchaseOfUser(self):
        purchaseId = 1
        userId = 1
        deliveryDate = datetime.now()

        self.purchase_facade.validatePurchaseOfUser(purchaseId, userId, deliveryDate)
        
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.immediate_purchase_mock.validatePurchaseOfUser.assert_called_with(userId, deliveryDate)

    def test_invalidatePurchaseOfUser(self):
        purchaseId = 1
        userId = 1

        self.purchase_facade.invalidatePurchaseOfUser(purchaseId, userId)
        
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.immediate_purchase_mock.invalidatePurchaseOfUser.assert_called_with(userId)

    def test_storeAcceptOffer(self):
        purchaseId = 1

        # Test when status is onGoing
        self.bid_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        self.purchase_facade.storeAcceptOffer(purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.bid_purchase_mock.get_status.assert_called()
        self.bid_purchase_mock.StoreAcceptOffer.assert_called()

        # Test when status is not onGoing
        self.bid_purchase_mock.get_status.return_value = PurchaseStatus.completed
        self.purchase_facade.storeAcceptOffer(purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.bid_purchase_mock.get_status.assert_called()
        self.bid_purchase_mock.StoreAcceptOffer.assert_not_called()

    def test_userAcceptOffer(self):
        purchaseId = 1
        userId = 1

        # Test when status is onGoing
        self.bid_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        self.purchase_facade.userAcceptOffer(purchaseId, userId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.bid_purchase_mock.get_status.assert_called()
        self.bid_purchase_mock.UseracceptOffer.assert_called_with(userId)

        # Test when status is not onGoing
        self.bid_purchase_mock.get_status.return_value = PurchaseStatus.completed
        self.purchase_facade.userAcceptOffer(purchaseId, userId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.bid_purchase_mock.get_status.assert_called()
        self.bid_purchase_mock.UseracceptOffer.assert_not_called()

    def test_storeRejectOffer(self):
        purchaseId = 1

        # Test when status is onGoing
        self.bid_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        self.purchase_facade.storeRejectOffer(purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.bid_purchase_mock.get_status.assert_called()
        self.bid_purchase_mock.StoreRejectOffer.assert_called()

        # Test when status is not onGoing
        self.bid_purchase_mock.get_status.return_value = PurchaseStatus.completed
        self.purchase_facade.storeRejectOffer(purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.bid_purchase_mock.get_status.assert_called()
        self.bid_purchase_mock.StoreRejectOffer.assert_not_called()

    def test_userRejectOffer(self):
        purchaseId = 1
        userId = 1

        # Test when status is onGoing
        self.bid_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        self.purchase_facade.userRejectOffer(purchaseId, userId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.bid_purchase_mock.get_status.assert_called()
        self.bid_purchase_mock.UserRejectOffer.assert_called_with(userId)

        # Test when status is not onGoing
        self.bid_purchase_mock.get_status.return_value = PurchaseStatus.completed
        self.purchase_facade.userRejectOffer(purchaseId, userId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.bid_purchase_mock.get_status.assert_called()
        self.bid_purchase_mock.UserRejectOffer.assert_not_called()

    def test_storeCounterOffer(self):
        purchaseId = 1
        counterOffer = 150.0

        # Test when status is onGoing
        self.bid_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        self.purchase_facade.storeCounterOffer(purchaseId, counterOffer)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.bid_purchase_mock.get_status.assert_called()
        self.bid_purchase_mock.StoreCounterOffer.assert_called_with(counterOffer)

        # Test when status is not onGoing
        self.bid_purchase_mock.get_status.return_value = PurchaseStatus.completed
        self.purchase_facade.storeCounterOffer(purchaseId, counterOffer)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.bid_purchase_mock.get_status.assert_called()
        self.bid_purchase_mock.StoreCounterOffer.assert_not_called()

    def test_userCounterOffer(self):
        purchaseId = 1
        counterOffer = 150.0

        # Test when status is onGoing
        self.bid_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        self.purchase_facade.userCounterOffer(counterOffer, purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.bid_purchase_mock.get_status.assert_called()
        self.bid_purchase_mock.UserCounterOffer.assert_called_with(counterOffer)

        # Test when status is not onGoing
        self.bid_purchase_mock.get_status.return_value = PurchaseStatus.completed
        self.purchase_facade.userCounterOffer(counterOffer, purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.bid_purchase_mock.get_status.assert_called()
        self.bid_purchase_mock.UserCounterOffer.assert_not_called()

    def test_addAuctionBid(self):
        userId = 1
        proposedPrice = 150.0
        purchaseId = 1

        # Test when status is onGoing and bid is added
        self.auction_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        self.auction_purchase_mock.addAuctionBid.return_value = True
        result = self.purchase_facade.addAuctionBid(userId, proposedPrice, purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.auction_purchase_mock.get_status.assert_called()
        self.auction_purchase_mock.addAuctionBid.assert_called_with(userId, proposedPrice)
        self.assertTrue(result)

        # Test when status is onGoing and bid is not added
        self.auction_purchase_mock.addAuctionBid.return_value = False
        result = self.purchase_facade.addAuctionBid(userId, proposedPrice, purchaseId)
        self.assertFalse(result)

        # Test when status is not onGoing
        self.auction_purchase_mock.get_status.return_value = PurchaseStatus.completed
        result = self.purchase_facade.addAuctionBid(userId, proposedPrice, purchaseId)
        self.assertFalse(result)

    def test_viewHighestBiddingOffer(self):
        purchaseId = 1

        # Test when status is onGoing
        self.auction_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        self.auction_purchase_mock.viewHighestBiddingOffer.return_value = 200.0
        result = self.purchase_facade.viewHighestBiddingOffer(purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.auction_purchase_mock.get_status.assert_called()
        self.auction_purchase_mock.viewHighestBiddingOffer.assert_called()
        self.assertEqual(result, 200.0)

        # Test when status is accepted
        self.auction_purchase_mock.get_status.return_value = PurchaseStatus.accepted
        result = self.purchase_facade.viewHighestBiddingOffer(purchaseId)
        self.assertEqual(result, 200.0)

        # Test when status is neither onGoing nor accepted
        self.auction_purchase_mock.get_status.return_value = PurchaseStatus.completed
        result = self.purchase_facade.viewHighestBiddingOffer(purchaseId)
        self.assertIsNone(result)

    def test_calculateRemainingTime(self):
        purchaseId = 1

        # Test when status is onGoing
        self.auction_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        remaining_time = timedelta(hours=1)
        self.auction_purchase_mock.calculateRemainingTime.return_value = remaining_time
        result = self.purchase_facade.calculateRemainingTime(purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.auction_purchase_mock.get_status.assert_called()
        self.auction_purchase_mock.calculateRemainingTime.assert_called()
        self.assertEqual(result, remaining_time)

        # Test when status is not onGoing
        self.auction_purchase_mock.get_status.return_value = PurchaseStatus.completed
        result = self.purchase_facade.calculateRemainingTime(purchaseId)
        self.assertEqual(result, timedelta(0))

    def test_checkIfAuctionEnded(self):
        purchaseId = 1

        # Test when auction has ended
        self.auction_purchase_mock.checkIfAuctionEnded.return_value = True
        result = self.purchase_facade.checkIfAuctionEnded(purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.auction_purchase_mock.checkIfAuctionEnded.assert_called()
        self.assertTrue(result)

        # Test when auction has not ended
        self.auction_purchase_mock.checkIfAuctionEnded.return_value = False
        result = self.purchase_facade.checkIfAuctionEnded(purchaseId)
        self.assertFalse(result)

    def test_validatePurchaseOfUser(self):
        purchaseId = 1
        userId = 1
        deliveryDate = datetime.now()

        self.purchase_facade.validatePurchaseOfUser(purchaseId, userId, deliveryDate)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.auction_purchase_mock.validatePurchaseOfUser.assert_called_with(userId, deliveryDate)

    def test_invalidatePurchaseOfUser(self):
        purchaseId = 1
        userId = 1

        self.purchase_facade.invalidatePurchaseOfUser(purchaseId, userId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.auction_purchase_mock.invalidatePurchaseOfUser.assert_called_with(userId)

    def test_calculateRemainingTime(self):
        purchaseId = 1

        # Test when status is onGoing
        self.lottery_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        remaining_time = timedelta(hours=1)
        self.lottery_purchase_mock.calculateRemainingTime.return_value = remaining_time
        result = self.purchase_facade.calculateRemainingTime(purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.lottery_purchase_mock.get_status.assert_called()
        self.lottery_purchase_mock.calculateRemainingTime.assert_called()
        self.assertEqual(result, remaining_time)

        # Test when status is not onGoing
        self.lottery_purchase_mock.get_status.return_value = PurchaseStatus.completed
        result = self.purchase_facade.calculateRemainingTime(purchaseId)
        self.assertEqual(result, timedelta(0))

    def test_addLotteryOffer(self):
        userId = 1
        proposedPrice = 150.0
        purchaseId = 1

        # Test when status is onGoing and offer is added
        self.lottery_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        self.lottery_purchase_mock.addLotteryOffer.return_value = True
        result = self.purchase_facade.addLotteryOffer(userId, proposedPrice, purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.lottery_purchase_mock.get_status.assert_called()
        self.lottery_purchase_mock.addLotteryOffer.assert_called_with(userId, proposedPrice)
        self.assertTrue(result)

        # Test when status is onGoing and offer is not added
        self.lottery_purchase_mock.addLotteryOffer.return_value = False
        result = self.purchase_facade.addLotteryOffer(userId, proposedPrice, purchaseId)
        self.assertFalse(result)

        # Test when status is not onGoing
        self.lottery_purchase_mock.get_status.return_value = PurchaseStatus.completed
        result = self.purchase_facade.addLotteryOffer(userId, proposedPrice, purchaseId)
        self.assertFalse(result)

    def test_calculateProbabilityOfUser(self):
        userId = 1
        purchaseId = 1

        # Test when status is onGoing
        self.lottery_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        self.lottery_purchase_mock.calculateProbabilityOfUser.return_value = 0.5
        result = self.purchase_facade.calculateProbabilityOfUser(userId, purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.lottery_purchase_mock.get_status.assert_called()
        self.lottery_purchase_mock.calculateProbabilityOfUser.assert_called_with(userId)
        self.assertEqual(result, 0.5)

        # Test when status is accepted
        self.lottery_purchase_mock.get_status.return_value = PurchaseStatus.accepted
        result = self.purchase_facade.calculateProbabilityOfUser(userId, purchaseId)
        self.assertEqual(result, 0.5)

        # Test when status is neither onGoing nor accepted
        self.lottery_purchase_mock.get_status.return_value = PurchaseStatus.completed
        result = self.purchase_facade.calculateProbabilityOfUser(userId, purchaseId)
        self.assertIsNone(result)

    def test_validateUserOffers(self):
        purchaseId = 1

        # Test when endingDate is in the past and all users have paid the full price
        self.lottery_purchase_mock.get_endingDate.return_value = datetime.now() - timedelta(days=1)
        self.lottery_purchase_mock.validateUserOffers.return_value = True
        result = self.purchase_facade.validateUserOffers(purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.lottery_purchase_mock.get_endingDate.assert_called()
        self.lottery_purchase_mock.validateUserOffers.assert_called()
        self.assertTrue(result)

        # Test when endingDate is in the past and not all users have paid the full price
        self.lottery_purchase_mock.validateUserOffers.return_value = False
        result = self.purchase_facade.validateUserOffers(purchaseId)
        self.assertFalse(result)

        # Test when endingDate is in the future
        self.lottery_purchase_mock.get_endingDate.return_value = datetime.now() + timedelta(days=1)
        result = self.purchase_facade.validateUserOffers(purchaseId)
        self.assertFalse(result)

    def test_pickWinner(self):
        purchaseId = 1

        # Test when status is accepted
        self.lottery_purchase_mock.get_status.return_value = PurchaseStatus.accepted
        self.lottery_purchase_mock.pickWinner.return_value = 1
        result = self.purchase_facade.pickWinner(purchaseId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.lottery_purchase_mock.get_status.assert_called()
        self.lottery_purchase_mock.pickWinner.assert_called()
        self.assertEqual(result, 1)

        # Test when status is not accepted
        self.lottery_purchase_mock.get_status.return_value = PurchaseStatus.onGoing
        result = self.purchase_facade.pickWinner(purchaseId)
        self.assertIsNone(result)

    def test_validateDeliveryOfWinner(self):
        purchaseId = 1
        userId = 1
        deliveryDate = datetime.now()

        self.purchase_facade.validateDeliveryOfWinner(purchaseId, userId, deliveryDate)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.lottery_purchase_mock.validateDeliveryOfWinner.assert_called_with(userId, deliveryDate)

    def test_invalidateDeliveryOfWinner(self):
        purchaseId = 1
        userId = 1

        self.purchase_facade.invalidateDeliveryOfWinner(purchaseId, userId)
        self.purchase_facade.getPurchaseById.assert_called_with(purchaseId)
        self.lottery_purchase_mock.invalidateDeliveryOfWinner.assert_called_with(userId)

if __name__ == '__main__':
    unittest.main()
