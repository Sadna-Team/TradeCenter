"use client";

import Popup from '@/components/Popup';
import React, { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import api from '@/lib/api';

export default function Home() {
  const [errorMessage, setErrorMessage] = useState(null);

  // const renderAfter = useRef(false);
  //
  // useEffect(() => {
  //   if (!renderAfter.current) {
  //     const fetchToken = async () => {
  //       try {
  //         const response = await api.get('/auth/');
  //         const data = response.data;
  //         const token = data.token; // Assuming the response contains the token
  //         console.log('Token:', token);
  //
  //         sessionStorage.setItem('token', token);
  //         sessionStorage.setItem('isConnected', false);
  //       } catch (error) {
  //         setErrorMessage('Error fetching token');
  //         console.error('Error fetching token:', error.response ? error.response.data : error.message);
  //       }
  //     };
  //
  //     renderAfter.current = true;
  //     if(sessionStorage.getItem('token') === null) fetchToken();
  //   }
  // }, []); // Empty dependency array to run the effect only once after mount


  const fetchStores = async (page) => {
    try {
      const limit = 4;
      const response = await api.post('/store/get_stores', {
        page, 
        limit,
      });
      const data = response.data;
      console.log('Data:', data);
      const formattedStores = Object.entries(data.message).map(([id, store]) => ({
        id,
        ...store,
      }));
      console.log('Stores:', formattedStores);
      if (formattedStores.length < limit) {
        setHasMore(false);
      }
      setStores((prevStores) => [...prevStores, ...formattedStores]);
      console.log('Stores:', stores);
    } catch (error) {
      setErrorMessage('Error fetching stores');
      console.error('Error fetching stores:', error.response ? error.response.data : error.message);
    }
  };

  useEffect(() => {
    if (tokenFetched) {
      fetchStores(page);
    }
  }, [page, tokenFetched]);

  const loadMoreStores = () => {
    setPage((prevPage) => prevPage + 1);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold text-red-600 mb-8">Welcome to Abu Ali Home Page</h1>
      
      {errorMessage && (
        <Popup initialMessage={errorMessage} is_closable={false} onClose={() => setErrorMessage(null)} />
      )}

      <div className="w-full max-w-3xl bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold mb-4">Stores</h2>
        <ul>
          {stores.map((store) => (
            <li key={store.store_id} className="mb-4">
              <Link href={`/e-store/${store.store_id}`}>
                <div className="p-4 border rounded-lg bg-gray-50 cursor-pointer hover:bg-gray-100 flex items-center justify-between">
                  <div>
                    <p className="text-lg font-bold text-blue-600">{store.store_name}</p>
                  </div>
                  <div>
                    {store.is_active ? (
                      <span className="text-green-500">&#x2714;</span> // Checkmark icon for active
                    ) : (
                      <span className="text-red-500">&#x2716;</span> // Cross icon for inactive
                    )}
                  </div>
                </div>
              </Link>
            </li>
          ))}
        </ul>
        {hasMore && (
          <button
            onClick={loadMoreStores}
            className="bg-blue-500 text-white py-2 px-4 rounded mt-4"
          >
            Load More
          </button>
        )}
      </div>
    </div>
  );
}