"use client"; // Add this at the top of the file

import Link from 'next/link';

export default function SearchProducts() {
    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
          <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
            <h1 className="text-2xl font-bold mb-4 text-center">Choose Search Method</h1>
            <Link href="/search_products/search_by_name">
                <button className="w-full bg-blue-500 text-white py-2 rounded">
                    Search By Name
                </button>
            </Link>
            <Link href="/search_products/search_by_tags">
                <button className="w-full bg-blue-500 text-white py-2 rounded">
                    Search By tags
                </button>
            </Link>
            <Link href="/search_products/search_by_category">
                <button className="w-full bg-blue-500 text-white py-2 rounded">
                    Search By Category
                </button>
            </Link>
          </div>
        </div>
      );
}