"use client";

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

const StoreDetail = () => {
  const router = useRouter();
  const { id } = router.query;

  // Mock data for demonstration purposes
  const storeData = {
    1: { title: 'Store One', description: 'Description of Store One' },
    2: { title: 'Store Two', description: 'Description of Store Two' },
    3: { title: 'Store Three', description: 'Description of Store Three' },
  };

  const [store, setStore] = useState(null);

  useEffect(() => {
    if (id) {
      setStore(storeData[id]);
    }
  }, [id]);

  if (!store) {
    return <div>Store not found</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 p-4 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-2xl w-full">
        <h1 className="text-2xl font-semibold mb-4">{store.title}</h1>
        <p>{store.description}</p>
      </div>
    </div>
  );
};

export default StoreDetail;