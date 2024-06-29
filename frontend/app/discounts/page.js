"use client";
import { useState, useEffect } from 'react';
import api from '../../lib/api'; // Import the configured axios instance


export default function ManageDiscountsPage() {
  // The discounts are split into their groups in order to make it easier to manage them
  const [productDiscounts, setProductDiscounts] = useState([]);
  const [categoryDiscounts, setCategoryDiscounts] = useState([]);
  const [storeDiscounts, setStoreDiscounts] = useState([]);
  const [andDiscounts, setAndDiscounts] = useState([]); 
  const [orDiscounts, setOrDiscounts] = useState([]);
  const [xorDiscounts, setXorDiscounts] = useState([]);
  const [maxDiscounts, setMaxDiscounts] = useState([]);
  const [additiveDiscounts, setAdditiveDiscounts] = useState([]);
  const [stores, setStores] = useState([]);
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  //Fetch all relevant data for discount management from the backend
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch discounts
        const discountsResponse = await api.get('/view_discounts_info');
        setDiscounts(discountsResponse.data.message);

        // Fetch store information
        const storeInfoResponse = await api.get('/store_info');
        setStores(storeInfoResponse.data);

        // Fetch store products
        const storeProductsResponse = await api.get('/store_products');
        setProducts(storeProductsResponse.data);

        // Fetch category IDs to names mapping
        const categoryMappingResponse = await api.get('/category_ids_to_names');
        setCategories(categoryMappingResponse.data);

      } catch (error) {
        setErrorMessage('Error fetching data');
        console.error('Error fetching data:', error.response ? error.response.data : error.message);
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

