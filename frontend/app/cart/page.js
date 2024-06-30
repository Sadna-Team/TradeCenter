"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import CartProduct from '@/components/CartProduct';
import api from "@/lib/api"; // Ensure this import path is correct

const Cart = () => {
  const [idsCart, setIdsCart] = useState([]); // [store_id, product_id, quantity]
  const [cart, setCart] = useState([]);
  const [totalPrice, setTotalPrice] = useState(0);
  const [loading, setLoading] = useState(true);
  const [rerender, setRerender] = useState(false);

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
        console.log('Fetched cart:', fetchedCart);
        await setIdsCart(fetchedCart);
        setRerender(!rerender);
      } catch (error) {
        console.error('Failed to fetch cart:', error);
        setIdsCart([]); // Ensure cart is always an array
      }
      setLoading(false);
    }
    fetchCart();
  }, []);

  useEffect(() => {
    if (idsCart.length > 0) {
      const fetchProductDetails = async () => {
        let total = 0;
        const updatedCart = await Promise.all(idsCart.map(async item => {
          try {
            const response = await api.post('store/get_product_info', { store_id: item.storeId, product_id: item.productId });
            const product = response.data.message;
            total += product.price * item.quantity;

            // Update item with fetched product details
            return {
              ...item,
              product_name: product.name,
              weight: product.weight,
              description: product.description,
              price: product.price,
              rating: product.rating,
              storeName: response.data.store_name,
            };
          } catch (error) {
            console.error('Failed to fetch product:', error);
            return item; // Return the item unchanged in case of error
          }
        }));
        setTotalPrice(total);
        setCart(updatedCart); // Ensure state update triggers re-render
      }
      fetchProductDetails();
    }
    else {
      setCart([]); // Ensure cart is always an array
    }
  }, [rerender]); // depend on rerender to update cart

  const onRemove = async (store_id, product_id, quantity) => {
    console.log('Removing all amount product with: ', product_id, " ", store_id);
    try {
      console.log('Removing product:', store_id, product_id, quantity);
      const response = await api.post('/user/remove_from_basket', { store_id, product_id, quantity });
      if (response.status !== 200) {
        console.error('Failed to remove product:', response);
        return;
      }
      console.log('Product removed:', response.data.message);
      const tempIdsCart = [...idsCart].filter(item => item.storeId !== store_id || item.productId !== product_id);
      setIdsCart(tempIdsCart);
      setRerender(!rerender);
    }
    catch (error) {
      console.error('Failed to remove product:', error);
    }
  }

  const onQuantityChange = async (store_id, product_id, quantity) => {
    console.log('Changing quantity of product with: ', product_id, " ", store_id, " to ", quantity);
    // change quantity of product with product_id and store_id to quantity in idsCart
    const updatedList = idsCart.map(item => {
      if (item.storeId === store_id && item.productId === product_id) {
        item.quantity = quantity;
      }
      return item;
    });
    setIdsCart(updatedList);
    setRerender(!rerender);
  }

  const onSaveCart = async () => {
    console.log('Saving cart:', idsCart);
    const cartToSend = {};
    idsCart.forEach(item => {
      if (!cartToSend[item.storeId]) {
        cartToSend[item.storeId] = {};
      }
      cartToSend[item.storeId][item.productId] = item.quantity;
    });
    try {
      const response = await api.post('/user/set_cart', { cart: cartToSend });
      if (response.status !== 200) {
        console.error('Failed to save cart:', response);
        return;
      }
      console.log('Cart saved:', response.data.message);
    } catch (error) {
      console.error('Failed to save cart:', error);
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4 text-center">Your Cart</h1>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <>
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
                    quantity={item.quantity}
                    onRemove={() => onRemove(item.storeId, item.productId, item.quantity)}
                    onQuantityChange={(quantity) => onQuantityChange(item.storeId, item.productId, quantity)}
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
                    <button onClick={onSaveCart} className="bg-gray-600 hover:bg-gray-800 text-white font-bold py-2 px-4 rounded inline-block text-center">
                      Save Changes
                    </button>
                  </div>
                )}
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Cart;