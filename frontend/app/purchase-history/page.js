"use client";

import api from '@/lib/api';
import { useState, useEffect } from 'react';

export default function PurchaseHistory() {
  const [token, setToken] = useState('');

  useEffect(() => {
    const getToken = async () => {
      try {
        const response = await api.get('/auth/');
        const token = response.data.message;
        console.log(token);
        setToken(token);
      } catch (error) {
        console.error('Failed to fetch token:', error);
      }
    };

    getToken();
  }, []);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      token = {token}
    </div>
  );
}
