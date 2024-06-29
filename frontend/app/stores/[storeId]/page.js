"use client";

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import ManagerProduct from '@/components/ManagerProduct'; // Adjust path as needed
import Link from 'next/link';
import api from '@/lib/api';

const StoreDetail = () => {
  const searchParams = useSearchParams();
  const store_id = searchParams.get('storeId');
  const [store, setStore] = useState(null);
  const [errorMessage, setErrorMessage] = useState(''); // Add error handling as needed

  useEffect(() => {
    if(!store_id) {
      setErrorMessage('Store ID not given');
      return;
    }
    
    const fetchData = async () => {
      try {
        const response = await api.post('/store/store_info', { store_id });
        if(response.status !== 200) {
          console.error('Failed to fetch store:', response);
          setErrorMessage('Failed to fetch store');
          return;
        }
        const data = response.data.message;
        if(data === null || data === undefined) {
          console.error('Failed to fetch store:', response);
          setErrorMessage('Failed to fetch store');
          return;
        }
        console.log('Store: ', data);
        setStore(data);
        setErrorMessage('');
      } catch (error) {
        console.error('Failed to fetch store:', error);
        setErrorMessage('Failed to fetch store');
      }
    };
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      {errorMessage.length > 0 && <div className="text-red-500">{errorMessage}</div>}
      {store === null && <div>Loading...</div>}
      {store && 
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 mt-8 text-center">{store.store_name}</h1>
        
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
            <ManagerProduct key={product.id} product={product} store_id={store_id} />
          ))}
        </div>

        {/* Add Product Button */}
        <div className="mt-8 flex justify-center">
          <Link href="/add-product">
            <div className="bg-red-600 text-white font-bold py-2 px-4 rounded cursor-pointer">Add Product</div>
          </Link>
        </div>
      </div>}
    </div>
  );
};

export default StoreDetail;
