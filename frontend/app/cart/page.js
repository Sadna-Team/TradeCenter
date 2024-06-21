"use client";

export default function Cart() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4 text-center">Your Cart</h1>
        <p>Your cart is currently empty.</p>
      </div>
    </div>
  );
}
