"use client";

import { useState } from 'react';
import { buildSocket } from "@/app/socket";
import Modal from '@/components/Modal'; // Import the Modal component
import Popup from '@/components/Popup';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false); // State to control the modal visibility

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors

    // Send POST request to authenticate user
    fetch('http://localhost:5000/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + sessionStorage.getItem('token')
      },
      body: JSON.stringify({ username, password }),
    })
    .then((response) => {
      if (response.ok) {
        return response.json(); // Parse the JSON from the response
      } else {
        return response.json().then((data) => {
          throw new Error(data.message); // Throw an error with the message from the server
        });
      }
    })
    .then((data) => {
      const token = data.token; // Extract the token from the response data
      sessionStorage.setItem('token', token); // Store the token in sessionStorage
      console.log('Token:', token); // Optional: log the token for debugging

      // Open a WebSocket connection and emit join
      const socket = buildSocket(token);
      sessionStorage.setItem('isConnected', true); // Set the isConnected flag to true

      // Redirect to the home page
      window.location.href = '/'; // Redirect to the home page

    })
    .catch((error) => {
      console.error('There was a problem with the fetch operation:', error);
      setError(error.message); // Set the error message for display
    });
  };

  // Function to check if both username and password are filled
  const isFormValid = () => {
    return username.trim() !== '' && password.trim() !== '';
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded shadow-md w-full max-w-md relative">
        <h1 className="text-2xl font-bold mb-4 text-center">Login</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded mt-1"
              placeholder="Enter your username"
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded mt-1"
              placeholder="Enter your password"
            />
          </div>
          <div className="flex justify-center">
            {error && <Popup initialMessage={error} is_closable={true} onClose={() => setError('')} />}
          </div>
          <button
            type="submit"
            className={`w-full bg-blue-500 text-white py-2 rounded ${!isFormValid() && 'opacity-50 cursor-not-allowed'}`}
            disabled={!isFormValid()}
          >
            Login
          </button>
        </form>
      </div>
      <Modal isOpen={showModal} onClose={() => setShowModal(false)} />
    </div>
  );
}
