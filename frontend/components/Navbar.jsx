"use client";

import Link from 'next/link';
import { useState } from 'react';
import Logo from './Logo';
import Button from './Button';

export default function Navbar() {
  const [showNotifications, setShowNotifications] = useState(false);

  const toggleNotifications = () => {
    setShowNotifications(!showNotifications);
  };

  return (
    <nav className="flex justify-between items-center p-4 bg-gray-800 text-white">
      <Link href="/">
        <Logo />
      </Link>
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
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8a1 1 0 011-1h12a1 1 0 011 1v11a2 2 0 01-2 2H7a2 2 0 01-2-2V8z" />
  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8V6a5 5 0 0110 0v2" />
</svg>

          </button>
        </Link>
        <Link href="/auth/login">
          <Button className="bg-blue-500 text-white py-2 px-4 rounded">
            Login
          </Button>
        </Link>
        <Link href="/auth/register">
          <Button>
            Register
          </Button>
        </Link>
        <Link href="/search_products">
          <Button>
            Search Products
          </Button>
        </Link>
      </div>
    </nav>
  );
}
