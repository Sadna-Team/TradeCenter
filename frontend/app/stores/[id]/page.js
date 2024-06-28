"use client";

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import ManagerProduct from '@/components/ManagerProduct'; // Adjust path as needed
import Link from 'next/link';

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
          amount: 10,
        },
        {
          id: 2,
          product_name: 'Product B',
          weight: '500g',
          description: 'Consectetur adipiscing elit.',
          price: 15.0,
          amount: 5,
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
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 mt-8 text-center">{store.title}</h1>
        
        {/* Management Buttons */}
        <div className="mb-6 flex justify-center">
          <Link href="/manage_employee">
            <div className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded mr-4 cursor-pointer">Employees Management</div>
          </Link>
          <Link href="/manage_policy">
            <div className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded cursor-pointer">Policy Management</div>
          </Link>
        </div>

        {/* Products */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {store.products.map((product) => (
            <ManagerProduct key={product.id} product={product} />
          ))}
        </div>

        {/* Add Product Button */}
        <div className="mt-8 flex justify-center">
          <Link href="/add-product">
            <div className="bg-red-600 text-white font-bold py-2 px-4 rounded cursor-pointer">Add Product</div>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default StoreDetail;
