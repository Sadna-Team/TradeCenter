"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import CartProduct from '@/components/CartProduct'; // Ensure this import path is correct

const Cart = () => {
  // Initial state for the cart, this could come from props, context, or be fetched from an API
  const initialCart = [
    { id: 1, product_name: 'Product A', weight: '1kg', description: 'Lorem ipsum dolor sit amet.', price: 20.0, rating: 4, amount: 1, store_name: 'Store 1' },
    { id: 2, product_name: 'Product B', weight: '500g', description: 'Consectetur adipiscing elit.', price: 15.0, rating: 5, amount: 2, store_name: 'Store 2' },
    // Add more products as needed
  ];

  const [cart, setCart] = useState(initialCart);

  // Calculate total sum of prices in the cart
  const totalPrice = cart.reduce((total, product) => total + (product.price * product.amount), 0);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4 text-center">Your Cart</h1>
        {cart.length === 0 ? (
          <p>Your cart is currently empty.</p>
        ) : (
          <>
            {cart.map(product => (
              <CartProduct key={product.id} product={product} storeName={product.store_name} />
            ))}
            <div className="cart-summary mt-4">
              <p className="text-lg">Total Price: ${totalPrice.toFixed(2)}</p>
            </div>
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
          </>
        )}
      </div>
    </div>
  );
};

export default Cart;
