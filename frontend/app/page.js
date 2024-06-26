"use client";

import { useState } from "react";
import ErrorPopup from "../components/ErrorPopup";
import Button from "../components/Button";

export default function Home() {
  const [error, setError] = useState(null);

  const showError = (message) => {
    setError(message);
  };

  // Example usage: Triggering an error
  const simulateError = () => {
    console.log("Simulating error...");
    showError("Oops! Something went wrong.");
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold text-blue-500">Welcome to the Home Page</h1>
    </div>
  );
}
