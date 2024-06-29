// Import React and other necessary modules
"use client";
import Popup from '@/components/Popup';
import { Router } from 'next/router';
import React, { useEffect, useRef, useState } from 'react';
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


  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold text-red-600">Welcome to Abu Ali Home Page</h1>
      
      {errorMessage && (
        <Popup initialMessage={errorMessage} is_closable={false} onClose={() => setErrorMessage(null)} />
      )}
    </div>
  );
}
