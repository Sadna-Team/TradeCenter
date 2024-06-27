// ClientNavBar.jsx

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Logo from './Logo';
import Button from './Button';
import Popup from './Popup';
import NotificationPopup from './NotificationPopup';
import {  useSocket } from "@/app/socket"; // Use the custom hook

const ClientNavBar = ({ onToggleSidebar, isConnected }) => {
  const { socket, closeSocket } = useSocket(); // Get the socket instance and close function

  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (socket && !sessionStorage.getItem('listener')) {
      sessionStorage.setItem('listener', true); // Set the listener flag to true
      socket.on('message', (data) => {
        sessionStorage.setItem('received', true);
      } );

      console.log('Socket listener added');

      return () => {
        socket.off('message'); // Clean up socket listener on unmount
      };
    }
  }, [socket]);

  const handleMessages = (data) => {
    setNotifications((prev) => [...prev, data]);
  }

  const toggleNotifications = () => {
    setShowNotifications(!showNotifications);
  };

  const handleLogout = async () => {
    setError(null); // Clear previous errors

    await fetch('http://localhost:5000/auth/logout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + sessionStorage.getItem('token')
      },
    })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((data) => {
          throw new Error(data); // Throw an error with the message from the server
        });
      }
    })
    .catch((error) => {
      console.error('There was a problem with the fetch operation:', error);
      setError(error.message); // Set the error message for display
    });

    closeSocket();
    sessionStorage.removeItem('token');
    sessionStorage.setItem('isConnected', false);
    sessionStorage.setItem('listener', false);
    window.location.href = '/';
  };

  return (
    <nav className="flex justify-between items-center p-4 bg-gray-800 text-white">
      <div className="flex items-center">
        <button onClick={onToggleSidebar} className="mr-4">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-7 w-7"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16m-7 6h7"
            />
          </svg>
        </button>
        <Link href="/">
          <Logo />
        </Link>
      </div>
      <div className="flex space-x-4 items-center">
        <div className="relative">
          <button onClick={toggleNotifications} className="relative">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-7 w-7"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V4a2 2 0 10-4 0v1.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h11z"
              />
            </svg>
          </button>
          {showNotifications && (
            <div className="absolute right-0 mt-2 w-48 bg-white text-black rounded-md shadow-lg z-10">
              <div className="p-4">
                <p>No new notifications</p>
              </div>
            </div>
          )}
        </div>
        <Link href="/cart">
          <button className="relative">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 8a1 1 0 011-1h12a1 1 0 011 1v11a2 2 0 01-2 2H7a2 2 0 01-2-2V8z"
              />
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 8V6a5 5 0 0110 0v2"
              />
            </svg>
          </button>
        </Link>
        <Link href="/search_products">
          <Button>
            Search Products
          </Button>
        </Link>
        <Button onClick={handleLogout} className="bg-red-500 text-white py-2 px-4 rounded">
          Logout
        </Button>
        {showNotifications && (
          <NotificationPopup
            notifications={notifications}
            onClose={() => setShowNotifications(false)} />
        )}
        {error && <Popup initialMessage={error} is_closable={true} onClose={() => setError(null)} />}
      </div>
    </nav>
  );
};

export default ClientNavBar;
