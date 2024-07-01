"use client";

import api from '@/lib/api';
import { useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

export default function UserPurchaseHistory() {
  const router = useRouter();
  const [purchaseHistory, setPurchaseHistory] = useState([]);
  const [error, setError] = useState(null);
  const searchParams = useSearchParams();
    
  const user_id = searchParams.get('userId');


  useEffect(() => {
    async function fetchPurchaseHistory() {
      if (!user_id) return; // Wait for user_id to be available
      try {
        const response = await api.post('/market/user_purchase_history', { user_id });
        setPurchaseHistory(response.data.message);
      } catch (error) {
        console.error('Failed to fetch purchase history:', error);
        setError('Failed to fetch purchase history');
      }
    }
    fetchPurchaseHistory();
  }, [user_id]);

  return (
    <div className="flex min-h-screen bg-gray-100 p-4">
      <div className="w-full max-w-4xl p-6 bg-white rounded-lg shadow-lg purchase-history-container">
        <h1 className="text-2xl font-semibold mb-4">Purchase History</h1>
        <h2 className="text-lg font-semibold">User ID: {user_id}</h2>
        {error && <p className="text-red-500">{error}</p>}
        {purchaseHistory.length > 0 ? (
          <div className="space-y-4">
            {purchaseHistory.map((purchase, index) => (
              <div key={index} className="p-4 bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
                <strong>Date: </strong> {purchase.date}<br />
                <strong>Store: </strong> {purchase.store_id}<br />
                <strong>Status: </strong> {purchase.status}<br />
                <strong>Price:</strong> {purchase.total_price_after_discounts}<br />
                <strong>Items:</strong><br />
                <ul>
                  {purchase.products.map((item, index) => (
                    <li key={index}>{item.name} - amount: {item.amount}, total price: {item.amount * item.price}, Description: {item.description}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        ) : (
          <p>No purchases yet</p>
        )}
      </div>
    </div>
  );
}
