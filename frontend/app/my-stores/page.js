"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import api from '@/lib/api';

const MyStores = () => {

  const [stores, setStores] = useState({});
  const [errorMessage, setErrorMessage] = useState('');


  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/store/my_stores');
        if(response.status !== 200){
          console.error('Failed to fetch stores', response);
          setErrorMessage('Failed to fetch stores');
          return;
        }

        const data = response.data.message;

        if(data === null || data === undefined) {
          console.error('Failed to fetch stores', response);
          setErrorMessage('Failed to fetch stores');
          return;
        }
        
        setStores(data);
      
      } catch (error) {
        console.error('Failed to fetch stores', error);
        setErrorMessage('Failed to fetch stores');
        setStores({});
      }
    }

    fetchData();
  }, []);



  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="w-full max-w-4xl p-6 bg-white rounded-lg shadow-lg">
        <h1 className="text-2xl font-semibold mb-4">My Stores</h1>
        {errorMessage ? (
          <div className="text-red-500">{errorMessage}</div>
        ) : (
          Object.keys(stores).length > 0 ? (
            <div className="space-y-4">
              {Object.entries(stores).map(([storeId, store]) => (
                <div key={storeId} className="p-4 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
                  <Link
                    href={{
                      pathname: `/stores/${storeId}`,
                      query: { storeId },
                    }}
                  >
                    <div className="text-lg font-semibold">{store.store_name}</div>
                  </Link>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-gray-500">User Owns/Manages No Stores</div>
          )
        )}
      </div>
    </div>
  );
};

export default MyStores;
