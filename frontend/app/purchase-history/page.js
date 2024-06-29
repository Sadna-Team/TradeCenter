"use client";

import api from '@/lib/api';
import { useState, useEffect } from 'react';

export default function PurchaseHistory() {
  const [purchaseHistory, setPurchaseHistory] = useState({});

  useEffect(() => {
    async function fetchPurchaseHistory() {
      try {
        const response = await api.get('/market/show_purchase_history');
        // console.log('Fetched data:', response.data.message);
        setPurchaseHistory(response.data.message);
      } catch (error) {
        console.error('Failed to fetch purchase history:', error);
      }
    }
    fetchPurchaseHistory();
  }, []);

  useEffect(() => {
    console.log('Updated purchase history:', purchaseHistory);
    console.log('Purchase history keys:', Object.keys(purchaseHistory));

  }, [purchaseHistory]);

  return (
    <div className="flex min-h-screen bg-gray-100 p-4">
      <div className="w-full max-w-4xl p-6 bg-white rounded-lg shadow-lg purchase-history-container">
        <h1 className="text-2xl font-semibold mb-4">Purchase History</h1>
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
