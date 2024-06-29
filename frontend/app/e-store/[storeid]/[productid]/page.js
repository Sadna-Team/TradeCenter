"use client";

import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import api from '@/lib/api'; // Import the configured axios instance

export default function ProductPage() {
  const { storeid, productid } = useParams();
  const [product, setProduct] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  useEffect(() => {
    const fetchProductData = async () => {
      try {
        const response = await api.post('/store/get_product_info', {
          store_id: storeid,
          product_id: productid,
        });
        const data = response.data.message;
        console.log('Product Data:', data);

        const productInfo = {
          id: data.product_id,
          name: data.name,
          description: data.description,
          price: data.price,
          weight: '1kg', // Update this if you have the weight data in your response
          tags: ['tag1', 'tag2'], // Update this if you have tags data in your response
        };

        setProduct(productInfo);
      } catch (error) {
        setErrorMessage('Error fetching product data');
        console.error('Error fetching product data:', error.response ? error.response.data : error.message);
      }
    };

    if (storeid && productid) {
      fetchProductData();
    }
  }, [storeid, productid]);

  const addToCart = async () => {
    try {
      const response = await api.post('/user/add_to_basket', {
        store_id: storeid,
        product_id: productid,
        quantity: 1,
      });
      const data = response.data;
      setSuccessMessage(data.message);
      console.log('Add to Cart Response:', data);
    } catch (error) {
      setErrorMessage('Error adding product to cart');
      console.error('Error adding product to cart:', error.response ? error.response.data : error.message);
    }
  };

  if (errorMessage) {
    return <div className="min-h-screen bg-gray-100 p-4">{errorMessage}</div>;
  }

  if (!product) {
    return <div className="min-h-screen bg-gray-100 p-4">Product not found</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md">
        <h1 className="text-3xl font-bold mb-4">{product.name}</h1>
        <p className="text-gray-700 mb-4">{product.description}</p>
        <p className="text-lg font-semibold mb-4">Price: ${product.price.toFixed(2)}</p>
        <p className="text-lg font-semibold mb-4">Weight: {product.weight}</p>
        <div className="mb-4">
          <span className="font-semibold">Tags:</span>
          {product.tags.map((tag, index) => (
            <span key={index} className="ml-2 text-blue-600">{tag}</span>
          ))}
        </div>
        <button
          className="bg-blue-500 text-white py-2 px-4 rounded"
          onClick={addToCart}
        >
          Add to Cart
        </button>
        {successMessage && <p className="text-green-500 mt-4">{successMessage}</p>}
      </div>
    </div>
  );
}