// ClientNavBar.jsx

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Logo from './Logo';
import Button from './Button';
import Popup from './Popup';
import NotificationPopup from './NotificationPopup';
import SocketSingleton from "@/app/socket";
import api from '@/lib/api';

const ClientNavBar = ({ onToggleSidebar }) => {
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState(null);
  const socket = new SocketSingleton(sessionStorage.getItem('token'));

  // Load notifications from sessionStorage on initialization
    useEffect(() => {
      const storedNotifications = sessionStorage.getItem('notifications');
      if (storedNotifications) {
        setNotifications(JSON.parse(storedNotifications));
        setShowNotifications(true)
      }
    }, []);

    useEffect(() => {
      if (socket.getInstance().connected && !sessionStorage.getItem('listener') === 'true') {
        socket.getInstance().removeAllListeners('message')
        socket.getInstance().on('message', handleMessages);
      }
      else
        if (socket.getInstance() !== null) {
        socket.getInstance().on('connected', () => {
            socket.getInstance().removeAllListeners('message')
            socket.getInstance().on('message', handleMessages);
        });}
        else {
            console.log('Socket is null');
            }
      } , [socket]);

  useEffect(() => {
     const handleBeforeUnload = async (event) => {
      // Prevent the default action
      event.preventDefault();
      // Send a logout request to the server
      try {
        await api.post('auth/logout');
      } catch (error) {
        console.error('Error logging out:', error.response ? error.response.data : error.message);
      }
      // Set a custom message for the confirmation dialog
      event.returnValue = ''; // Standard for most browsers
      return ''; // For old browsers
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);


  const handleMessages = (data) => {
    console.log('Received message:', data);
    setNotifications((prev) => [...prev, data]);
    setShowNotifications(true)
    // clear the socket
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

    socket.getInstance().disconnect();
    sessionStorage.removeItem('token');
    sessionStorage.setItem('isConnected', false);
    sessionStorage.setItem('listener', false);
    sessionStorage.removeItem('admin')
    sessionStorage.removeItem('notifications')
    window.location.href = '/';
  };

    const handleDebugClick = () => {
      api.get('/market/test')
    }

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
          <button onClick={handleDebugClick} className="relative">
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
                  d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
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
                {/*<div className="p-4">*/}
                {/*  <p>No new notifications</p>*/}
                {/*</div>*/}
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
