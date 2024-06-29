import React, { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import Logo from './Logo';
import Button from './Button';
import api from '@/lib/api'; // Adjust the import according to your project structure

const GuestNavBar = () => {
  const [token, setToken] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const renderAfter = useRef(false);

  useEffect(() => {
    if (!renderAfter.current) {
      const fetchToken = async () => {
        try {
          const response = await api.get('/auth/');
          const data = response.data;
          const token = data.token;
          console.log('Token:', token);

          sessionStorage.setItem('token', token);
          sessionStorage.setItem('isConnected', false);
          setToken(token);
        } catch (error) {
          setErrorMessage('Error fetching token');
          console.error('Error fetching token:', error.response ? error.response.data : error.message);
        }
      };

      renderAfter.current = true;
      if (sessionStorage.getItem('token') === null) fetchToken();
      else setToken(sessionStorage.getItem('token'));
    }
  }, []);

  return (
    <nav className="flex justify-between items-center p-4 bg-gray-800 text-white">
      <div className="flex items-center">
        <Link href="/">
          <Logo />
        </Link>
      </div>
      <div className="flex space-x-4 items-center">
        <Link href="/cart">
          <button className="relative" disabled={!token}>
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
          <Button disabled={!token}>
            Search Products
          </Button>
        </Link>
        <Link href="/auth/login">
          <Button className="bg-blue-500 text-white py-2 px-4 rounded" disabled={!token}>
            Login
          </Button>
        </Link>
        <Link href="/auth/register">
          <Button disabled={!token}>
            Register
          </Button>
        </Link>
        {errorMessage && <div className="text-red-500">{errorMessage}</div>}
      </div>
    </nav>
  );
};

export default GuestNavBar;
