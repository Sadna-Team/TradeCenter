import unittest
from unittest.mock import patch, Mock

from backend.business.store.store import *

from backend.business.store.store import Product
from backend.business.store.store import ProductSpecification
from backend.business.store.store import Category


class Test_productFunctions(unittest.TestCase):

    def setUp(self, mock_obj) -> None:
        self.mock_product = Mock(spec = Product)
        self.mock_product.product_id = 1
        self.mock_product.storeId = 1
        self.mock_product.specificationId = 1
        self.mock_product.exporationDate = '2024-12-31'
        self.mock_product.condition = 'New'
        self.mock_product.price = 10.00
        
    def test_get_productId(self):
        self.assertEqual(self.mock_product.get_productId(), 1)

    def test_set_productId(self):
        self.mock_product.set_productId(2)
        self.assertEqual(self.mock_product.get_productId(), 2)

    def test_get_storeId(self):
        self.assertEqual(self.mock_product.get_storeId(), 1)

    def test_set_storeId(self):
        self.mock_product.set_storeId(2)
        self.assertEqual(self.mock_product.get_storeId(), 2)
    
    def test_get_specificationId(self):
        self.assertEqual(self.mock_product.get_specificationId(), 1)

    def test_set_specificationId(self):
        self.mock_product.set_specificationId(2)
        self.assertEqual(self.mock_product.get_specificationId(), 2)
    
    def test_get_exporationDate(self):
        self.assertEqual(self.mock_product.get_exporationDate(), '2024-12-31')

    def test_set_exporationDate(self):
        self.mock_product.set_exporationDate('2025-12-31')
        self.assertEqual(self.mock_product.get_exporationDate(), '2025-12-31')
    
    def test_get_condition(self):
        self.assertEqual(self.mock_product.get_condition(), 'New')

    def test_set_condition(self):
        self.mock_product.set_condition('Used')
        self.assertEqual(self.mock_product.get_condition(), 'Used')
    
    def test_get_price(self):
        self.assertEqual(self.mock_product.get_price(), 10.00)
    
    def test_set_price(self):
        self.mock_product.set_price(20.00)
        self.assertEqual(self.mock_product.get_price(), 20.00)
    
    def test_isExpired(self):
        self.assertEqual(self.mock_product.isExpired(), False)
    
    def test_changePrice_success(self):
        self.assertEqual(self.mock_product.changePrice(5.00), True)
        self.assertEqual(self.mock_product.get_price(), 5.00)

    def test_changePrice_fail(self):
        self.assertEqual(self.mock_product.changePrice(-5.00), False)
        self.assertEqual(self.mock_product.get_price(), 10.00)


class Test_productSpecificationFunctions:

    def setUp(self):
        self.mock_productSpecification = Mock(spec = ProductSpecification)
        self.mock_productSpecification.specificationId = 1
        self.mock_productSpecification.productName = 'Test Product'
        self.mock_productSpecification.weight = 1.0
        self.mock_productSpecification.description = 'Test Description'
        self.mock_productSpecification.tags = ['Test', 'Product']
        self.mock_productSpecification.manufacturer = 'Test Manufacturer'
        self.mock_productSpecification.storeIds = [1, 2]

    def test_get_specificationId(self):
        self.assertEqual(self.mock_productSpecification.get_specificationId(), 1)

    def test_set_specificationId(self):
        self.mock_productSpecification.set_specificationId(2)
        self.assertEqual(self.mock_productSpecification.get_specificationId(), 2)

    def test_get_productName(self):
        self.assertEqual(self.mock_productSpecification.get_productName(), 'Test Product')
    
    def test_set_productName(self):
        self.mock_productSpecification.set_productName('New Product')
        self.assertEqual(self.mock_productSpecification.get_productName(), 'New Product')
    
    def test_get_weight(self):
        self.assertEqual(self.mock_productSpecification.get_weight(), 1.0)

    def test_set_weight(self):
        self.mock_productSpecification.set_weight(2.0)
        self.assertEqual(self.mock_productSpecification.get_weight(), 2.0)

    def test_get_description(self):
        self.assertEqual(self.mock_productSpecification.get_description(), 'Test Description')
    
    def test_set_description(self):
        self.mock_productSpecification.set_description('New Description')
        self.assertEqual(self.mock_productSpecification.get_description(), 'New Description')

    def test_get_tags(self):
        self.assertEqual(self.mock_productSpecification.get_tags(), ['Test', 'Product'])

    def test_set_tags(self):
        self.mock_productSpecification.set_tags(['New', 'Product'])
        self.assertEqual(self.mock_productSpecification.get_tags(), ['New', 'Product'])
    
    def test_get_manufacturer(self):
        self.assertEqual(self.mock_productSpecification, 'Test Manufacturer')

    def test_set_manufacturer(self):
        self.mock_productSpecification.set_manufacturer('New Manufacturer')
        self.assertEqual(self.mock_productSpecification.get_manufacturer(), 'New Manufacturer')

    def test_get_storeIds(self):
        self.assertEqual(self.mock_productSpecification.get_storeIds(), [1, 2])

    def test_set_storeIds(self):
        self.mock_productSpecification.set_storeIds([2, 3])
        self.assertEqual(self.mock_productSpecification.get_storeIds(), [2, 3])

    def test_addTag_Success(self):
        result = self.mock_productSpecification.addTag('New')
        self.assertEqual(result, True)
        self.assertEqual(self.mock_productSpecification.get_tags(), ['Test', 'Product', 'New'])
    
    def test_addTag_Fail_None(self):
        result = self.mock_productSpecification.addTag(None)
        self.assertEqual(result, False)
        self.assertEqual(self.mock_productSpecification.get_tags(), ['Test', 'Product'])

    def test_addTag_Fail_Exists(self):
        result = self.mock_productSpecification.addTag('Test')
        self.assertEqual(result, False)
        self.assertEqual(self.mock_productSpecification.get_tags(), ['Test', 'Product'])

    def test_removeTag_Success(self):
        result = self.mock_productSpecification.removeTag('Test')
        self.assertEqual(result, True)
        self.assertEqual(self.mock_productSpecification.get_tags(), ['Product'])

    def test_removeTag_Fail_None(self):
        result = self.mock_productSpecification.removeTag(None)
        self.assertEqual(result, False)
        self.assertEqual(self.mock_productSpecification.get_tags(), ['Test', 'Product'])

    def test_removeTag_Fail_NotExists(self):
        result = self.mock_productSpecification.removeTag('New')
        self.assertEqual(result, False)
        self.assertEqual(self.mock_productSpecification.get_tags(), ['Test', 'Product'])

    def test_hasTag(self):
        self.assertEqual(self.mock_productSpecification.hasTag('Test'), True)
        self.assertEqual(self.mock_productSpecification.hasTag('New'), False)

    def test_addStoreId_Success(self):
        result = self.mock_productSpecification.addStoreId(3)
        self.assertEqual(result, True)
        self.assertEqual(self.mock_productSpecification.get_storeIds(), [1, 2, 3])
    
    def test_addStoreId_Fail_Exists(self):
        result = self.mock_productSpecification.addStoreId(1)
        self.assertEqual(result, False)
        self.assertEqual(self.mock_productSpecification.get_storeIds(), [1, 2])

    def test_removeStoreId_Success(self):
        result = self.mock_productSpecification.removeStoreId(2)
        self.assertEqual(result, True)
        self.assertEqual(self.mock_productSpecification.get_storeIds(), [1])

    def test_removeStoreId_Fail_NotExists(self):
        result = self.mock_productSpecification.removeStoreId(3)
        self.assertEqual(result, False)
        self.assertEqual(self.mock_productSpecification.get_storeIds(), [1, 2])

    def test_isSoldByStore(self):
        self.assertEqual(self.mock_productSpecification.isSoldByStore(1), True)
        self.assertEqual(self.mock_productSpecification.isSoldByStore(3), False)    
    

    def test_changeNameOfProductSpecification(self):
        self.assertEqual(self.mock_productSpecification.changeNameOfProductSpecification('New Product'), True)
        self.assertEqual(self.mock_productSpecification.get_productName(), 'New Product')

# ------------------------ Catagory Tests ------------------------------------
class TestCategory(unittest.TestCase):

    def test_add_parent_category(self):
        category = Category(categoryId=1, categoryName="Parent Category")
        category.set_parentCategoryId = Mock()

        category.addParentCategory(parentCategoryId=2)

        category.set_parentCategoryId.assert_called_once_with(2)

    def test_remove_parent_category(self):
        category = Category(categoryId=1, categoryName="Parent Category", parentCategoryId=2)
        category.set_parentCategoryId = Mock()

        category.removeParentCategory()

        category.set_parentCategoryId.assert_called_once_with(None)

    def test_add_sub_category_success(self):
        category = Category(categoryId=1, categoryName="Parent Category")
        sub_category = Category(categoryId=2, categoryName="Sub Category")

        sub_category.addParentCategory = Mock()
        category.addSubCategory(sub_category)

        sub_category.addParentCategory.assert_called_once_with(category.get_categoryId())
        self.assertIn(sub_category, category.get_subCategories())

    def test_add_sub_category_fail_invalid(self):
        category = Category(categoryId=1, categoryName="Parent Category")
        sub_category = Category(categoryId=1, categoryName="Sub Category")  # Same ID as parent

        sub_category.addParentCategory = Mock()
        category.addSubCategory(sub_category)

        sub_category.addParentCategory.assert_not_called()
        self.assertNotIn(sub_category, category.get_subCategories())

    def test_add_sub_category_fail_already_has_parent(self):
        category = Category(categoryId=1, categoryName="Parent Category", parentCategoryId=2)
        sub_category = Category(categoryId=2, categoryName="Sub Category")

        sub_category.addParentCategory = Mock()
        category.addSubCategory(sub_category)

        sub_category.addParentCategory.assert_not_called()
        self.assertNotIn(sub_category, category.get_subCategories())

    def test_remove_sub_category_success(self):
        category = Category(categoryId=1, categoryName="Parent Category")
        sub_category = Category(categoryId=2, categoryName="Sub Category")
        category.addSubCategory(sub_category)

        sub_category.removeParentCategory = Mock()
        category.removeSubCategory(sub_category)

        sub_category.removeParentCategory.assert_called_once()
        self.assertNotIn(sub_category, category.get_subCategories())

    def test_remove_sub_category_fail_not_sub_category(self):
        category = Category(categoryId=1, categoryName="Parent Category")
        sub_category = Category(categoryId=2, categoryName="Sub Category")

        sub_category.removeParentCategory = Mock()
        category.removeSubCategory(sub_category)

        sub_category.removeParentCategory.assert_not_called()
        self.assertNotIn(sub_category, category.get_subCategories())

    def test_is_parent_category(self):
        parent_category = Category(categoryId=1, categoryName="Parent Category")
        sub_category = Category(categoryId=2, categoryName="Sub Category", parentCategoryId=1)

        self.assertTrue(parent_category.isParentCategory(sub_category))
        self.assertFalse(sub_category.isParentCategory(parent_category))

    def test_is_sub_category(self):
        parent_category = Category(categoryId=1, categoryName="Parent Category")
        sub_category = Category(categoryId=2, categoryName="Sub Category", parentCategoryId=1)

        self.assertTrue(sub_category.isSubCategory(parent_category))
        self.assertFalse(parent_category.isSubCategory(sub_category))

    def test_has_parent_category(self):
        parent_category = Category(categoryId=1, categoryName="Parent Category")
        sub_category = Category(categoryId=2, categoryName="Sub Category", parentCategoryId=1)

        self.assertTrue(sub_category.hasParentCategory())
        self.assertFalse(parent_category.hasParentCategory())

    def test_add_product_to_category_success(self):
        category = Category(categoryId=1, categoryName="Category")
        product = Mock()

        category.addProductToCategory(product)

        self.assertIn(product, category.get_categoryProducts())

    def test_add_product_to_category_fail_already_exists(self):
        category = Category(categoryId=1, categoryName="Category")
        product = Mock()
        category.addProductToCategory(product)

        result = category.addProductToCategory(product)

        self.assertFalse(result)

    def test_remove_product_from_category_success(self):
        category = Category(categoryId=1, categoryName="Category")
        product = Mock()
        category.addProductToCategory(product)

        result = category.removeProductFromCategory(product)

        self.assertTrue(result)
        self.assertNotIn(product, category.get_categoryProducts())

    def test_remove_product_from_category_fail_not_exists(self):
        category = Category(categoryId=1, categoryName="Category")
        product = Mock()

        result = category.removeProductFromCategory(product)

        self.assertFalse(result)

    def test_get_all_products_recursively(self):
        category = Category(categoryId=1, categoryName="Category")
        product1 = Mock()
        product2 = Mock()
        category.addProductToCategory(product1)

        sub_category = Category(categoryId=2, categoryName="Sub Category")
        sub_category.addProductToCategory(product2)
        category.addSubCategory(sub_category)

        all_products = category.getAllProductsRecursively()

        self.assertIn(product1, all_products)
        self.assertIn(product2, all_products)

    def test_get_all_product_names(self):
        category = Category(categoryId=1, categoryName="Category")
        product1 = Mock()
        product1.get_productName.return_value = "Product 1"
        product2 = Mock()
        product2.get_productName.return_value = "Product 2"
        category.addProductToCategory(product1)

        sub_category = Category(categoryId=2, categoryName="Sub Category")
        sub_category.addProductToCategory(product2)
        category.addSubCategory(sub_category)

        all_product_names = category.getAllProductNames()

        self.assertIn("Product 1", all_product_names)
        self.assertIn("Product 2", all_product_names)

class TestStore(unittest.TestCase):

    def test_close_store_success(self):
        store = Store(storeId=1, locationId=1, storeName="Test Store", storeFounderId=1, isActive=True)
        store.set_isActive = Mock()

        result = store.closeStore(userId=1)

        store.set_isActive.assert_called_once_with(False)
        self.assertTrue(result)

    def test_close_store_fail_not_founder(self):
        store = Store(storeId=1, locationId=1, storeName="Test Store", storeFounderId=1, isActive=True)
        store.set_isActive = Mock()

        result = store.closeStore(userId=2)

        store.set_isActive.assert_not_called()
        self.assertFalse(result)

    def test_add_product_success(self):
        store = Store(storeId=1, locationId=1, storeName="Test Store", storeFounderId=1, isActive=True)
        product = Mock()

        result = store.addProduct(product)

        self.assertIn(product, store.get_storeProducts())
        self.assertTrue(result)

    def test_add_product_fail_already_exists(self):
        store = Store(storeId=1, locationId=1, storeName="Test Store", storeFounderId=1, isActive=True)
        product = Mock()
        store.addProduct(product)

        result = store.addProduct(product)

        self.assertFalse(result)

    def test_remove_product_success(self):
        store = Store(storeId=1, locationId=1, storeName="Test Store", storeFounderId=1, isActive=True)
        product = Mock()
        store.addProduct(product)

        result = store.removeProduct(productId=product.get_productId())

        self.assertNotIn(product, store.get_storeProducts())
        self.assertTrue(result)

    def test_remove_product_fail_not_exists(self):
        store = Store(storeId=1, locationId=1, storeName="Test Store", storeFounderId=1, isActive=True)

        result = store.removeProduct(productId=1)

        self.assertFalse(result)

    def test_change_price_of_product_success(self):
        store = Store(storeId=1, locationId=1, storeName="Test Store", storeFounderId=1, isActive=True)
        product = Mock()
        store.addProduct(product)

        result = store.changePriceOfProduct(productId=product.get_productId(), newPrice=50)

        self.assertTrue(result)

    def test_change_price_of_product_fail_invalid_product_id(self):
        store = Store(storeId=1, locationId=1, storeName="Test Store", storeFounderId=1, isActive=True)

        result = store.changePriceOfProduct(productId=1, newPrice=50)

        self.assertFalse(result)

    def test_change_price_of_product_fail_product_not_found(self):
        store = Store(storeId=1, locationId=1, storeName="Test Store", storeFounderId=1, isActive=True)

        result = store.changePriceOfProduct(productId=1, newPrice=50)

        self.assertFalse(result)

    def test_get_product_by_id_success(self):
        store = Store(storeId=1, locationId=1, storeName="Test Store", storeFounderId=1, isActive=True)
        product = Mock()
        product.get_productId.return_value = 1
        store.addProduct(product)

        result = store.getProductById(productId=1)

        self.assertEqual(result, product)

    def test_get_product_by_id_fail_not_exists(self):
        store = Store(storeId=1, locationId=1, storeName="Test Store", storeFounderId=1, isActive=True)

        result = store.getProductById(productId=1)

        self.assertIsNone(result)

class TestStoreFacade(unittest.TestCase):

    def setUp(self):
        self.store_facade = StoreFacade()

    def test_add_store_success(self):
        result = self.store_facade.addStore(1, "Test Store", 1, True)
        self.assertTrue(result)

    def test_add_store_fail_invalid_name(self):
        result = self.store_facade.addStore(1, "", 1, True)
        self.assertFalse(result)

    def test_close_store_success(self):
        self.store_facade.addStore(1, "Test Store", 1, True)
        result = self.store_facade.closeStore(0, 1)
        self.assertTrue(result)

    def test_close_store_fail_invalid_id(self):
        self.store_facade.addStore(1, "Test Store", 1, True)
        result = self.store_facade.closeStore(1, 1)
        self.assertFalse(result)

    def test_add_product_to_store_success(self):
        self.store_facade.addProductSpecification("Laptop", 2.5, "Description", ["electronics"], "Manufacturer")
        self.store_facade.addStore(1, "Test Store", 1, True)
        result = self.store_facade.addProductToStore(0, 0, datetime.now(), 1, 1000.0)
        self.assertTrue(result)

    def test_add_product_to_store_fail_invalid_store_id(self):
        self.store_facade.addProductSpecification("Laptop", 2.5, "Description", ["electronics"], "Manufacturer")
        result = self.store_facade.addProductToStore(0, 0, datetime.now(), 1, 1000.0)
        self.assertFalse(result)

    def test_add_product_to_store_fail_invalid_product_id(self):
        self.store_facade.addStore(1, "Test Store", 1, True)
        result = self.store_facade.addProductToStore(0, 0, datetime.now(), 1, 1000.0)
        self.assertFalse(result)

    # Add more relevant tests here

    def test_add_category_success(self):
        result = self.store_facade.addCategory("Electronics")
        self.assertTrue(result)

    def test_add_category_fail_duplicate_name(self):
        self.store_facade.addCategory("Electronics")
        result = self.store_facade.addCategory("Electronics")
        self.assertFalse(result)

    def test_remove_category_success(self):
        self.store_facade.addCategory("Electronics")
        result = self.store_facade.removeCategory(0)
        self.assertTrue(result)

    def test_remove_category_fail_invalid_id(self):
        result = self.store_facade.removeCategory(0)
        self.assertFalse(result)

    def test_get_category_by_id_success(self):
        self.store_facade.addCategory("Electronics")
        category = self.store_facade.getCategoryById(0)
        self.assertIsNotNone(category)

    def test_get_category_by_id_fail_invalid_id(self):
        category = self.store_facade.getCategoryById(0)
        self.assertIsNone(category)

    def test_assign_subcategory_to_category_success(self):
        self.store_facade.addCategory("Electronics")
        self.store_facade.addCategory("Phones")
        result = self.store_facade.assignSubCategoryToCategory(1, 0)
        self.assertTrue(result)

    def test_assign_subcategory_to_category_fail_invalid_category_id(self):
        self.store_facade.addCategory("Electronics")
        result = self.store_facade.assignSubCategoryToCategory(1, 0)
        self.assertFalse(result)

    def test_delete_subcategory_from_category_success(self):
        self.store_facade.addCategory("Electronics")
        self.store_facade.addCategory("Phones")
        self.store_facade.assignSubCategoryToCategory(1, 0)
        result = self.store_facade.deleteSubCategoryFromCategory(0, 1)
        self.assertTrue(result)

    def test_delete_subcategory_from_category_fail_invalid_category_id(self):
        self.store_facade.addCategory("Electronics")
        self.store_facade.addCategory("Phones")
        self.store_facade.assignSubCategoryToCategory(1, 0)
        result = self.store_facade.deleteSubCategoryFromCategory(0, 1)
        self.assertFalse(result)

    def test_assign_product_spec_to_category_success(self):
        self.store_facade.addCategory("Electronics")
        self.store_facade.addProductSpecification("Laptop", 2.5, "Description", ["electronics"], "Manufacturer")
        result = self.store_facade.assignProductSpecToCategory(0, 0)
        self.assertTrue(result)

    def test_assign_product_spec_to_category_fail_invalid_category_id(self):
        self.store_facade.addProductSpecification("Laptop", 2.5, "Description", ["electronics"], "Manufacturer")
        result = self.store_facade.assignProductSpecToCategory(0, 0)
        self.assertFalse(result)

    def test_remove_product_spec_from_category_success(self):
        self.store_facade.addCategory("Electronics")
        self.store_facade.addProductSpecification("Laptop", 2.5, "Description", ["electronics"], "Manufacturer")
        self.store_facade.assignProductSpecToCategory(0, 0)
        result = self.store_facade.removeProductSpecFromCategory(0, 0)
        self.assertTrue(result)

    def test_remove_product_spec_from_category_fail_invalid_category_id(self):
        self.store_facade.addProductSpecification("Laptop", 2.5, "Description", ["electronics"], "Manufacturer")
        self.store_facade.assignProductSpecToCategory(0, 0)
        result = self.store_facade.removeProductSpecFromCategory(0, 0)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
