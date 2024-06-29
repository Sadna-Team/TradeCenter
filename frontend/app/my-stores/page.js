"use client";

import Link from 'next/link';
import { useEffect, useState } from 'react';
import api from '@/lib/api';
import Button from '@/components/Button';

export default function MyStores() {
    const [stores, setStores] = useState([]);
    const [storeInfo, setStoreInfo] = useState({});

    // fetch stores from server
    useEffect(() => {
      async function fetchStores() {
        try {
          const response = await api.get('/store/my_stores');
          setStores(response.data.message);
        } catch (error) {
          console.error('Failed to fetch stores:', error);
        }
      }
      fetchStores();
      getStoreInfo(stores[0]);
      // stores.forEach(store_id => {
      //   setStoreInfo(getStoreInfo(store_id));
      //   console.log(storeInfo);
      // });
    }, []);
    
    async function getStoreInfo(store_id) {
      try {
        const response = await api.post('/store/store_info', { store_id });

        console.log(response.data.message);
        setStoreInfo(response.data.message);
        return response.data.message;
      } catch (error) {
        console.error('Failed to fetch store info:', error);
      }
    }

    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
        <div className="w-full max-w-4xl p-6 bg-white rounded-lg shadow-lg">
          <h1 className="text-2xl font-semibold mb-4">My Stores</h1>
          {stores.length > 0 ? (
            <div className="space-y-4">
              {Object.keys(storeInfo).map(key => (
                <div key={key}>
                  <strong>{key}:</strong> {storeInfo[key].toString()}
                </div>
              ))}
              {/* {stores.map(store_id => (
                <div key={store_id} className="p-4 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
                  <Button className="float-right">{store}</Button>
                  <p className="text-gray-600">{getStoreInfo(store_id)}</p>
                </div>
              ))} */}
            </div>
          ) : (
            <div className="text-gray-500">you have no stores</div>
          )}
        </div>
      </div>
    );
}
