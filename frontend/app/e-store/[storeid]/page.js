"use client";

import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import api from '@/lib/api'; // Import the configured axios instance

export default function StorePage() {
  const { storeid } = useParams(); // Get the storeid from the URL
  const [store, setStore] = useState(null);
  const [products, setProducts] = useState([]);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    const fetchStoreData = async () => {
      try {
        const response = await api.post('/store/store_info', {
          store_id: storeid,
        });
        const data = response.data.message;
        console.log('Store Data:', data);

        const storeInfo = {
          name: data.store_name,
          owner: 'Example Owner', // Update this as needed based on your actual data
          products: data.products.map((product) => ({
            id: product.product_id,
            name: product.name,
            price: product.price,
          })),
        };

        setStore(storeInfo);
      } catch (error) {
        setErrorMessage('Error fetching store data');
        console.error('Error fetching store data:', error.response ? error.response.data : error.message);
      }
    };

    if (storeid) {
      fetchStoreData();
    }
  }, [storeid]);

  if (errorMessage) {
    return <div className="min-h-screen bg-gray-100 p-4">{errorMessage}</div>;
  }

  if (!store) {
    return <div className="min-h-screen bg-gray-100 p-4">Store not found</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 mt-8 text-center">{store.name}</h1>
        <p className="text-xl text-gray-700 mb-8 text-center">Owner: {store.owner}</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {store.products.map((product) => (
            <Link key={product.id} href={`/e-store/${storeid}/${product.id}`}>
              <div className="p-4 border rounded-lg bg-gray-50 cursor-pointer hover:bg-gray-100">
                <p className="text-lg font-bold text-blue-600">{product.name}</p>
                <p className="text-gray-700">Price: ${product.price.toFixed(2)}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}