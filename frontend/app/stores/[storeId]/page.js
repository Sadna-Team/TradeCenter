"use client";

import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import ManagerProduct from '@/components/ManagerProduct'; // Adjust path as needed
import Link from 'next/link';
import api from '@/lib/api';

const StoreDetail = () => {
  const searchParams = useSearchParams();
  const store_id = searchParams.get('storeId');
  const [store, setStore] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [rerender, setRerender] = useState(false);
  const [storeRole, setStoreRole] = useState('');
  const [isClosed, setIsClosed] = useState(false);

  const handleReload = () => {
    setRerender(!rerender);
  };

  const deleteProduct = async (store_id, product_id) => {
    if(isClosed) {
      console.error('Cannot delete product from closed store');
      setErrorMessage('Cannot delete product when store is closed!');
      return;
    }
    try {
      const response = await api.post('/store/remove_product', { store_id, product_id });
      if (response.status !== 200) {
        console.error('Failed to delete product:', response);
        setErrorMessage('Failed to delete product');
        return;
      }
      const data = response.data.message;
      if (data === null || data === undefined) {
        console.error('Failed to delete product:', response);
        setErrorMessage('Failed to delete product');
        return;
      }
      console.log('Product deleted:', data);
      setErrorMessage('');
      handleReload();
    } catch (error) {
      console.error('Failed to delete product:', error);
      setErrorMessage('Failed to delete product');
    }
  };

  const closeStore = async () => {
    try {
      const response = await api.post('/store/closing_store', { store_id });
      if (response.status !== 200) {
        console.error('Failed to close store:', response);
        setErrorMessage('Failed to close store');
        return;
      }
      console.log('Store closed:', response.data.message);
      setErrorMessage('');
      setIsClosed(true);
      handleReload();
    } catch (error) {
      console.error('Failed to close store:', error);
      setErrorMessage('Failed to close store');
    }
  };

  const openStore = async () => {
    try {
      const response = await api.post('/store/opening_store', { store_id });
      if (response.status !== 200) {
        console.error('Failed to open store:', response);
        setErrorMessage('Failed to open store');
        return;
      }
      console.log('Store opened:', response.data.message);
      setErrorMessage('');
      setIsClosed(false);
      handleReload();
    } catch (error) {
      console.error('Failed to open store:', error);
      setErrorMessage('Failed to open store');
    }
  };

  useEffect(() => {
    if (!store_id) {
      setErrorMessage('Store ID not given');
      return;
    }

    const fetchStoreInfo = async () => {
      try {
        const response = await api.post('/store/store_info', { store_id });
        if (response.status !== 200) {
          console.error('Failed to fetch store:', response);
          setErrorMessage('Failed to fetch store');
          return;
        }
        const data = response.data.message;
        if (data === null || data === undefined) {
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
    fetchStoreInfo();
    setRerender(!rerender);
  }, []);

  useEffect(() => {
    if (!store_id) {
      setErrorMessage('Store ID not given');
      return;
    }

    const fetchStoreRole = async () => {
      try {
        const response = await api.post('/market/get_store_role', { store_id });
        if (response.status !== 200) {
          console.error('Failed to fetch store role:', response);
          setErrorMessage('Failed to fetch store role');
          return;
        }
        const role = response.data.message;
        if (role === null || role === undefined) {
          console.error('Failed to fetch store role:', response);
          setErrorMessage('Failed to fetch store role');
          return;
        }
        console.log('Store Role: ', role);
        setStoreRole(role);
        setErrorMessage('');
      } catch (error) {
        console.error('Failed to fetch store role:', error);
        setErrorMessage('Failed to fetch store role');
      }
    };

    const fetchIsClosed = async () => {
      try {
        const response = await api.post('/store/is_store_closed', { store_id });
        if (response.status !== 200) {
          console.error('Failed to fetch store status:', response);
          setErrorMessage('Failed to fetch store status');
          return;
        }

        const data = response.data.message;

        if (data === null || data === undefined) {
          console.error('Failed to fetch store status:', response);
          setErrorMessage('Failed to fetch store status');
          return;
        }

        console.log('Store closed:', data);
        setIsClosed(data);
      }
      catch (error) {
        console.error('Failed to fetch store status:', error);
        setErrorMessage('Failed to fetch store status');
      }
    };

    fetchStoreRole();
    fetchIsClosed();
  }, [rerender]);

    const handleGiveupNomination = async () => {
      api.post('/store/give_up_role', { store_id }).then((response) => {
        if (response.status !== 200) {
          console.error('Failed to give up nomination:', response);
          setErrorMessage('Failed to give up nomination');
          return;
        }
        console.log('Give up nomination:', response.data.message);
        setErrorMessage('');
        const event = new Event('storeDeleted');
        window.dispatchEvent(event);
        handleReload();
      });
    }

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      {errorMessage.length > 0 && <div className="text-red-500">{errorMessage}</div>}
      {store === null && <div>Loading...</div>}
      {store &&
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 mt-8 text-center">{store.store_name}</h1>

        {/* Management Buttons */}
        <div className="mb-6 flex justify-center">
          <Link href={`/manage_employee/${store_id}`}>
            <div className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded mr-4 cursor-pointer">Employees Management</div>
          </Link>
          <div>
            {storeRole === 'Founder' && (
              <div>
                {!isClosed && (
                  <div className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded mr-4 cursor-pointer"
                  onClick={()=>closeStore()}>
                    Close Store
                  </div>)}
                {isClosed && (
                  <div className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mr-4 cursor-pointer"
                        onClick={()=> openStore()}>
                    Open Store
                  </div>)}
              </div>
            )}
          </div>
          <Link href="/manage_policy">
            <div className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded cursor-pointer">Policy Management</div>
          </Link>
        </div>

        {/* Products */}
        <div>
            {!isClosed && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {store.products.map((product) => (
                <ManagerProduct key={product.product_id} product={product} store_id={store_id} deleteProduct={deleteProduct} />
              ))}
            </div>
            )}
        </div>

        {/* Add Product Button */}
        <div>
          {!isClosed &&(
            <div className="mt-8 flex justify-center">
            <Link href={{
                        pathname: `/stores/${store_id}/add-product`,
                        query: { storeId: store_id },
                      }}>
              <div className="bg-red-600 text-white font-bold py-2 px-4 rounded cursor-pointer">Add Product</div>
            </Link>
          </div>
          )}
        </div>

        {/* Conditional "Giveup Nomination" Button */}
        {(storeRole === 'StoreOwner' || storeRole === 'StoreManager') && (
          <div className="mt-8 flex justify-center">
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={handleGiveupNomination}>
              Giveup Nomination
            </button>
          </div>
        )}
      </div>}
    </div>
  );
};

export default StoreDetail;
