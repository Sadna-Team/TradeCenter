"use client";

import Link from 'next/link';
import { useEffect, useState } from "react";
import api from "@/lib/api";

export default function Sidebar({ isOpen, onClose, hasStores, isSystemManager }) {
  const [showMyStoresLink, setShowMyStoresLink] = useState(false);

  useEffect(() => {
    const storeAdded = (e) => {
      console.log('Store added:', e.detail);
      setShowMyStoresLink(true); // Set showMyStoresLink to true when storeAdded event occurs
      onClose();
    };

    window.addEventListener('storeAdded', storeAdded);

    // Clean up the event listener
    return () => {
      window.removeEventListener('storeAdded', storeAdded);
    };
  }, [onClose]);

  useEffect(() => {
    const storeDeleted = (e) => {
      api.get('/market/get_user_stores').then((response) => {
        if (response.data.message.length === 0) {
          setShowMyStoresLink(false); // Set showMyStoresLink to false when user has no stores
        }
        else {
            setShowMyStoresLink(true); // Set showMyStoresLink to true when user has stores

        }
      });
    }
    window.addEventListener('storeDeleted', storeDeleted);

    return () => {
        window.removeEventListener('storeDeleted', storeDeleted);
    }
  }, []);

  console.log('isSystemManager:', isSystemManager);

  return (
    <div
      className={`fixed top-0 left-0 h-full w-64 bg-gray-800 text-white flex flex-col p-4 space-y-2 transform ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      } transition-transform duration-300 ease-in-out`}
    >
      <button onClick={onClose} className="self-end mb-4">
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
      <Link href="/add-store" onClick={onClose} className="py-2 px-4 bg-gray-700 hover:bg-gray-600 rounded">
        Add Store
      </Link>
      {(showMyStoresLink || hasStores) && (
        <Link href="/my-stores" onClick={onClose} className="py-2 px-4 bg-gray-700 hover:bg-gray-600 rounded">
          My Stores
        </Link>
      )}
      {isSystemManager && (
        <Link href="/system-manager" onClick={onClose} className="py-2 px-4 bg-gray-700 hover:bg-gray-600 rounded">
          System Manager Page
        </Link>
      )}
      {isSystemManager && (
        <Link href="/discounts" className="py-2 px-4 bg-gray-700 hover:bg-gray-600 rounded">
        Manage Discounts
        </Link>
      )}
      <Link href="/purchase-history" onClick={onClose} className="py-2 px-4 bg-gray-700 hover:bg-gray-600 rounded">
        Purchase History
      </Link>
      <Link href="/nominations" onClick={onClose} className="py-2 px-4 bg-gray-700 hover:bg-gray-600 rounded">
        Nominations
      </Link>
      <Link href="/bid-status" onClick={onClose} className="py-2 px-4 bg-gray-700 hover:bg-gray-600 rounded">
        Bid Status
      </Link>
    </div>
  );
}
