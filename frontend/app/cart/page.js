"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import CartProduct from '@/components/CartProduct';
import api from "@/lib/api"; // Ensure this import path is correct

const Cart = () => {
  const [cart, setCart] = useState([]);
  const [totalPrice, setTotalPrice] = useState(0);

  useEffect(() => {
    // Fetch cart from server
    async function fetchCart() {
      try {
        const response = await api.get('/user/show_cart');
        console.log('Cart:', response.data.shopping_cart);

        // Transform the response object into an array of products
        const fetchedCart = [];
        const cartData = response.data.shopping_cart;
        for (const storeId in cartData) {
          for (const productId in cartData[storeId]) {
            fetchedCart.push({
              storeId: storeId,
              productId: productId,
              quantity: cartData[storeId][productId],
            });
          }
        }
        setCart(fetchedCart);
      } catch (error) {
        console.error('Failed to fetch cart:', error);
        setCart([]); // Ensure cart is always an array
      }
    }
    fetchCart();
  }, []);

  useEffect(() => {
    if (Array.isArray(cart)) {
      const fetchProductDetails = async () => {
        let total = 0;
        for (const item of cart) {
          try {
            const response = await api.post('store/get_product_info', { store_id: item.storeId, product_id: item.productId });
            const product = response.data.message;
            total += product.price * item.quantity;

            // Update item with fetched product details
            item.product_name = product.name;
            item.weight = product.weight;
            item.description = product.description;
            item.price = product.price;
            item.rating = product.rating;
            item.storeName = response.data.store_name;
          } catch (error) {
            console.error('Failed to fetch product:', error);
          }
        }
        setTotalPrice(total);
        setCart([...cart]); // Ensure state update triggers re-render
      }
      fetchProductDetails();
    }
  }, [cart]);

  const onRemove = async (productId) => {
    console.log('Removing product:', productId);
    // Implement removal logic here
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4 text-center">Your Cart</h1>
        {Array.isArray(cart) && cart.length === 0 ? (
          <p>Your cart is currently empty.</p>
        ) : (
          <>
            {cart.map(item => (
              <CartProduct
                key={`${item.storeId}-${item.productId}`} // Unique key
                product_id={item.productId}
                store_id={item.storeId}
                product_name={item.product_name}
                weight={item.weight}
                description={item.description}
                price={item.price}
                rating={item.rating}
                storeName={item.storeName}
                onRemove={() => onRemove(item.productId)} // Pass correct handler
              />
            ))}
            <div className="cart-summary mt-4">
              <p className="text-lg">Total Price: ${totalPrice.toFixed(2)}</p>
            </div>
            {cart.length > 0 && (
              <div className="flex justify-between mt-4">
                <Link href="/checkout">
                  <div className="bg-red-600 hover:bg-red-800 text-white font-bold py-2 px-4 rounded inline-block text-center">
                    Checkout
                  </div>
                </Link>
                <Link href="/bid">
                  <div className="bg-blue-600 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded inline-block text-center">
                    Bid
                  </div>
                </Link>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Cart;
