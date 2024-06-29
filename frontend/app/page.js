"use client";

import Popup from '@/components/Popup';
import React, { useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import api from '@/lib/api';

export default function Home() {
  const [errorMessage, setErrorMessage] = useState(null);
  const [stores, setStores] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [tokenFetched, setTokenFetched] = useState(false);
  const renderAfter = useRef(false);

  useEffect(() => {

    if (sessionStorage.getItem('token') !== null) {
        setTokenFetched(true);
    }
    const handleTokenFetched = (event) => {
      console.log('Token fetched:', event.detail);
      setTokenFetched(true);
    };

    window.addEventListener('tokenFetched', handleTokenFetched);

    return () => {
      window.removeEventListener('tokenFetched', handleTokenFetched);
    };
  }, []);

  const fetchStores = async (page) => {
    try {
      const limit = 4;
      const response = await api.post('/store/get_stores', {
        page,
        limit,
      });
      const data = response.data;
      const formattedStores = Object.entries(data.message).map(([id, store]) => ({
        id,
        ...store,
      }));
      if (formattedStores.length < limit) {
        setHasMore(false);
      }
      setStores((prevStores) => [...prevStores, ...formattedStores]);
      sessionStorage.setItem('stores', JSON.stringify(stores));
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
