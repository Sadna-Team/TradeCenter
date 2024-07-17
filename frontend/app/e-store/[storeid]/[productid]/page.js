"use client";

import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';

import api from '@/lib/api'; // Import the configured axios instance
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter
} from "@/components/Dialog";
import Button from "@/components/Button";
import { Input } from "@/components/Input";


export default function ProductPage() {
  const { storeid, productid } = useParams();
  const [product, setProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [currentProposedPrice, setCurrentProposedPrice] = useState(0);
  const [errorMessage, setErrorMessage] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

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
        quantity: quantity,
      });
      const data = response.data;
      setSuccessMessage(data.message);
      console.log('Add to Cart Response:', data);
    } catch (error) {
      setErrorMessage('Error adding product to cart');
      console.error('Error adding product to cart:', error.response ? error.response.data : error.message);
    }
  };

  const BidOffer = async () => {
    try {
      const response = await api.post('/market/user_bid_offer', {
        store_id: storeid,
        product_id: productid,
        proposed_price: currentProposedPrice,
      });

      if (response.status !== 200) {
        console.error('Failed to check if store worker accepted bid', response);
        return;
      }

      const data = response.data;
      setSuccessMessage(`Sucessfully added bid offer with id: ${data.message}`);
      console.log('Bid offer response:', data);
    } catch (error) {
      setErrorMessage('Error adding bid offer on product');
      console.error('Error adding bid offer on product:', error.response ? error.response.data : error.message);
    }
  };
  
  const handleBidDialogOpen = () => {
    setIsDialogOpen(true);
  };

  const handleBidDialogClose = () => {
    setIsDialogOpen(false);
    setErrorMessage('');
    setCurrentProposedPrice(0);
  };

  const handleBidDialogConfirm = () => {
    if (isNaN(currentProposedPrice) || currentProposedPrice < 0) {
      setErrorMessage('Please enter a valid proposed price.');
      return;
    }
    BidOffer();
    handleBidDialogClose();
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
        <div className="amount-control mb-4 flex items-center">
          <button
            className="amount-btn bg-gray-300 text-gray-800 border-none py-2 px-3 mr-2"
            onClick={() => { quantity > 1 ? setQuantity(quantity - 1) : setQuantity(quantity) }}
          >
            -
          </button>
          <input
            type="text"
            className="amount-input w-16 text-center py-2"
            value={quantity}
            readOnly
          />
          <button
            className="amount-btn bg-gray-300 text-gray-800 border-none py-2 px-3 ml-2"
            onClick={() => setQuantity(quantity + 1)}
          >
            +
          </button>
        </div>
        <button
          className="bg-blue-500 text-white py-2 px-4 rounded mb-4 mr-2"
          onClick={addToCart}
        >
          Add to Cart
        </button>

        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <button
              className="bg-blue-500 text-white py-2 px-4 rounded"
              onClick={handleBidDialogOpen}
            >
              Bid
            </button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px] bg-white">
            <DialogHeader>
              <DialogTitle>Proposed Price</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              {errorMessage && (
                <div className="text-red-500 text-sm">{errorMessage}</div>
              )}
              <Input
                placeholder="Proposed Price"
                value={currentProposedPrice}
                onChange={(e) => setCurrentProposedPrice(e.target.value)}
                className="border border-black"
              />
            </div>
            <DialogFooter>
              <Button type="button" onClick={handleBidDialogConfirm}>Confirm</Button>
              <Button type="button" onClick={handleBidDialogClose}>Exit</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {successMessage && <p className="text-green-500 mt-4">{successMessage}</p>}
      </div>
    </div>
  );
}