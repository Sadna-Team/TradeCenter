"use client";

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import Product from '@/components/Product'; // Adjust path as needed

const StoreDetail = () => {
  const searchParams = useSearchParams();
  const id = searchParams.get('id');

  // Mock data for demonstration purposes
  const storeData = {
    1: {
      title: 'Store One',
      products: [
        {
          id: 1,
          product_name: 'Product A',
          weight: '1kg',
          description: 'Lorem ipsum dolor sit amet.',
          price: 20.0,
        },
        {
          id: 2,
          product_name: 'Product B',
          weight: '500g',
          description: 'Consectetur adipiscing elit.',
          price: 15.0,
        },
      ],
    },
    2: {
      title: 'Store Two',
      products: [
        {
          id: 3,
          product_name: 'Product C',
          weight: '2kg',
          description: 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
          price: 25.0,
        },
        {
          id: 4,
          product_name: 'Product D',
          weight: '750g',
          description: 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
          price: 18.0,
        },
      ],
    },
    // Add more stores and products as needed
  };

  const [store, setStore] = useState(null);

  useEffect(() => {
    if (id && storeData[id]) {
      setStore(storeData[id]);
    } else {
      setStore(null); // Handle case where store is not found
    }
  }, [id]);

  if (!store) {
    return <div className="min-h-screen bg-gray-100 p-4">Store not found</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 p-4 flex items-center justify-center">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 mt-8 text-center">{store.title}</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {store.products.map((product) => (
            <Product key={product.id} product={product} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default StoreDetail;
