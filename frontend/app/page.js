// Import React and other necessary modules
"use client";
import Popup from '@/components/Popup';
import React, { useEffect, useRef, useState } from 'react';
// import { AuthContext } from '@/app/AuthContext';

// Mark the component to run on the client side

export default function Home() {
  const [errorMessage, setErrorMessage] = useState(null);
  const renderAfter = useRef(false);


  useEffect(() => {
    if (!renderAfter.current) {
      const fetchToken = async () => {
        try {
          // Send GET request to obtain token
          const response = await fetch('http://localhost:5000/auth/');
          const data = await response.json();

          if (response.ok) {
            const token = data.token; // Assuming the response contains the token
            // Do something with the token (e.g., store it globally)
            console.log('Token:', token);

            // Save the token to local storage
            localStorage.setItem('token', token);
          } else {
            // Display error message
            setErrorMessage('Failed to fetch token');
            console.error('Error fetching token:', data);
          }
        } catch (error) {
          // Display error message
          setErrorMessage('Error fetching token');
          console.error('Error fetching token:', error);
        }
      };

      renderAfter.current = true;
      fetchToken();
    }
  }, []); // Empty dependency array to run the effect only once after mount


  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold text-blue-500">Welcome to the Home Page</h1>
      
      {errorMessage && (
        <Popup initialMessage={errorMessage} is_closable={false} onClose={() => setErrorMessage(null)} />
      )}
    </div>
  );
}
