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
  const [errorMessage, setErrorMessage] = useState('');
  const [rerender, setRerender] = useState(false);
  const [storeRole, setStoreRole] = useState('');
  const [isClosed, setIsClosed] = useState(false);
  const [permission, setPermission] = useState({
    'add_product': false,
    'change_purchase_policy': false,
    'change_purchase_types': false,
    'change_discount_policy': false,
    'change_discount_types': false,
    'add_manager': false,
    'get_bid': false,
  });
  const [loading, setLoading] = useState(true);

  const handleReload = () => {
    setRerender(!rerender);
  };

  const deleteProduct = async (store_id, product_id) => {
    if (isClosed) {
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

  const has_permission = async (permission) => {
    if (storeRole === 'StoreOwner') {
      return true;
    }

    let request = "has_" + permission + "_permission";
    try {
      const response = await api.post('/user/' + request, { store_id });
      if (response.status !== 200) {
        console.error('Failed to check permission:', response);
        setErrorMessage('Failed to check permission');
        return false;
      }
      const data = response.data.has_permission;
      if (data === null || data === undefined) {
        console.error('Failed to check permission:', response);
        setErrorMessage('Failed to check permission');
        return false;
      }
      console.log('Permission:', data);
      setErrorMessage('');
      return data;
    } catch (error) {
      console.error('Failed to check permission:', error);
      setErrorMessage('Failed to check permission');
      return false;
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

    const fetchStoreData = async () => {
      try {
        const [storeRoleResponse, storeStatusResponse, permissions] = await Promise.all([
          api.post('/market/get_store_role', { store_id }),
          api.post('/store/is_store_closed', { store_id }),
          (async () => {
            const permissions = {
              'add_product': await has_permission('add_product'),
              'change_purchase_policy': await has_permission('change_purchase_policy'),
              'change_purchase_types': await has_permission('change_purchase_types'),
              'change_discount_policy': await has_permission('change_discount_policy'),
              'change_discount_types': await has_permission('change_discount_types'),
              'add_manager': await has_permission('add_manager'),
              'get_bid': await has_permission('get_bid'),
            };
            return permissions;
          })(),
        ]);

        if (storeRoleResponse.status !== 200) {
          console.error('Failed to fetch store role:', storeRoleResponse);
          setErrorMessage('Failed to fetch store role');
          return;
        }
        const role = storeRoleResponse.data.message;
        if (role === null || role === undefined) {
          console.error('Failed to fetch store role:', storeRoleResponse);
          setErrorMessage('Failed to fetch store role');
          return;
        }
        console.log('Store Role: ', role);
        setStoreRole(role);
        setErrorMessage('');

        if (storeStatusResponse.status !== 200) {
          console.error('Failed to fetch store status:', storeStatusResponse);
          setErrorMessage('Failed to fetch store status');
          return;
        }
        const data = storeStatusResponse.data.message;
        if (data === null || data === undefined) {
          console.error('Failed to fetch store status:', storeStatusResponse);
          setErrorMessage('Failed to fetch store status');
          return;
        }
        console.log('Store closed:', data);
        setIsClosed(data);

        setPermission(permissions);
      } catch (error) {
        console.error('Failed to fetch store data:', error);
        setErrorMessage('Failed to fetch store data');
      } finally {
        setLoading(false);
      }
    };

    fetchStoreData();
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
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      {errorMessage.length > 0 && <div className="text-red-500">{errorMessage}</div>}
      {store === null && loading && <div>Loading...</div>}
      {store && !loading &&
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
          {(storeRole === 'StoreOwner' || permission['change_purchase_policy']) && 
           <Link href={{
              pathname: `/manage_policy/${store_id}`,
              query: { id: store_id },
            }}>
            <div className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded mr-4 cursor-pointer">Manage Policies</div>
          </Link>}
          {(storeRole === 'StoreOwner' || permission['change_discount_policy']) && 
           <Link href={{
              pathname: `/discounts/${store_id}`,
              query: { id: store_id },
            }}>
            <div className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded mr-4 cursor-pointer">Manage Discounts</div>
          </Link>} 
          {(storeRole === 'StoreOwner' || permission['get_bid']) && 
           <Link href={{
              pathname: `/manage_bids/${store_id}`,
              query: { storeId: store_id },
            }}>
            <div className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded mr-4 cursor-pointer">Manage Bids</div>
          </Link>}   
        </div>
        {/* Products */}
        <div>
            {!isClosed && permission['add_product'] &&(
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {store.products.map((product) => (
                <ManagerProduct key={product.product_id} product={product} store_id={store_id} deleteProduct={deleteProduct} />
              ))}
            </div>
            )}
        </div>

        {/* Add Product Button */}
        <div>
          {!isClosed && permission['add_product'] && (
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

        {/*add purchase history button*/}
        <div className="mt-8 flex justify-center">
          <Link href={{
                      pathname: `/stores/${store_id}/store-purchase-history`,
                      query: { storeId: store_id },
                    }}>
            <div className="bg-red-600 text-white font-bold py-2 px-4 rounded cursor-pointer">Purchase History</div>
          </Link>
        </div>

        {/* Conditional "Giveup Nomination" Button */}
        {(storeRole === 'StoreOwner' || storeRole === 'StoreManager') && (
          <div className="mt-8 flex justify-center">
            <Link href={""} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={handleGiveupNomination}>
              Give Up Nomination
            </Link>
          </div>
        )}
      </div>}
    </div>
  );
};

export default StoreDetail;
