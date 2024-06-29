"use client";
import { useEffect, useState } from 'react';
import api from '@/lib/api';

const DataFetchingComponent = () => {
  const [discounts, setDiscounts] = useState([]);
  const [stores, setStores] = useState([]);
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch discounts
        const discountsResponse = await axios.get('/view_discounts_info');
        setDiscounts(discountsResponse.data);

        // Fetch store information
        const storeInfoResponse = await axios.get('/store_info');
        setStores(storeInfoResponse.data);

        // Fetch store products
        const storeProductsResponse = await axios.get('/store_products');
        setProducts(storeProductsResponse.data);

        // Fetch category IDs to names mapping
        const categoryMappingResponse = await axios.get('/category_ids_to_names');
        setCategories(categoryMappingResponse.data);

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  // Functions for handling behavior-related actions (add, edit, remove discounts)

  const handleAddDiscount = async (newDiscountData) => {
    try {
      const response = await axios.post('/add_discount', newDiscountData);
      // Handle success (update UI, refresh data, etc.)
    } catch (error) {
      console.error('Error adding discount:', error);
    }
  };

  const handleEditDiscount = async (discountId, updatedDiscountData) => {
    try {
      const response = await axios.post(`/change_discount_description/${discountId}`, updatedDiscountData);
      // Handle success (update UI, refresh data, etc.)
    } catch (error) {
      console.error('Error editing discount:', error);
    }
  };

  const handleRemoveDiscount = async (discountId) => {
    try {
      const response = await axios.post(`/remove_discount/${discountId}`);
      // Handle success (update UI, refresh data, etc.)
    } catch (error) {
      console.error('Error removing discount:', error);
    }
  };

  return (
    <div>
      {/* Render UI components and use state variables (discounts, stores, products, categories) */}
    </div>
  );
};

export default DataFetchingComponent;
