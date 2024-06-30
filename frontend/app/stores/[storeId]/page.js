"use client";

import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import ManagerProduct from '@/components/ManagerProduct'; // Adjust path as needed
import Link from 'next/link';
import api from '@/lib/api';

const StoreDetail = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const store_id = searchParams.get('storeId');
  const [store, setStore] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [rerender, setRerender] = useState(false);
  const [storeRole, setStoreRole] = useState('');

  const handleReload = () => {
    setRerender(!rerender);
  };

  const deleteProduct = async (store_id, product_id) => {
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

    fetchStoreRole();
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
            <ManagerProduct key={product.product_id} product={product} store_id={store_id} deleteProduct={deleteProduct} />
          ))}
        </div>

        {/* Add Product Button */}
        <div className="mt-8 flex justify-center">
          <Link href={{
                      pathname: `/stores/${store_id}/add-product`,
                      query: { storeId: store_id },
                    }}>
            <div className="bg-red-600 text-white font-bold py-2 px-4 rounded cursor-pointer">Add Product</div>
          </Link>
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
