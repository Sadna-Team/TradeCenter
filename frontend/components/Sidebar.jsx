"use client";

import Link from 'next/link';
// import { Link } from 'next/router';

export default function Sidebar({ isOpen, onClose, hasStores }) {

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
      {hasStores &&
        <Link href="/my-stores" onClick={onClose} className="py-2 px-4 bg-gray-700 hover:bg-gray-600 rounded">
          My Stores
        </Link>
      }
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
