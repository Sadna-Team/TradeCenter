import React from 'react';
import Link from 'next/link';

const MyStores = () => {
  // Mock data for the stores
  const stores = [
    { id: 0, title: 'Store One' },
    { id: 2, title: 'Store Two' },
    { id: 3, title: 'Store Three' },
  ];



  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="w-full max-w-4xl p-6 bg-white rounded-lg shadow-lg">
        <h1 className="text-2xl font-semibold mb-4">My Stores</h1>
        {stores.length > 0 ? (
          <div className="space-y-4">
            {stores.map(store => (
              <div key={store.id} className="p-4 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
                <Link 
                    href={{
                          pathname:`/stores/${store.id}`, 
                          query: { storeId: store.id },
                          }}>
                  <div className="text-lg font-semibold">{store.title}</div>
                </Link>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-gray-500">No Data</div>
        )}
      </div>
    </div>
  );
};

export default MyStores;
