"use client";

import { useState } from 'react';
import SocketSingleton from "@/app/socket";
import Modal from '@/components/Modal'; // Import the Modal component
import api from '@/lib/api';
import Popup from '@/components/Popup';
import { useRouter } from 'next/navigation';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false); // State to control the modal visibility;
  const router = useRouter();


  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Clear previous errors

    try {
      // Send POST request to authenticate user
      const response = await api.post('/auth/login', { username, password });
      console.log('Response:', response.data); // Optional: log the response data for debugging
      const data = response.data;
      const token = data.token; // Extract the token from the response data
      const admin = data.admin; // Extract the admin status from the response data
      const notifications = data.notification;

      sessionStorage.setItem('token', token); // Store the token in sessionStorage
      sessionStorage.setItem('admin', admin);
      sessionStorage.setItem('notifications', JSON.stringify(notifications));
      console.log('Token:', token); // Optional: log the token for debugging
      console.log('Admin:', admin); // Optional: log the admin status for debugging
      console.log('Notifications:', notifications); // Optional: log the notifications for debugging
      sessionStorage.setItem('username', username);
      const socket = new SocketSingleton(token);
      socket.getInstance().on('connected', () => {
        window.location.href = '/';
      });

    } catch (error) {
      console.error('There was a problem with the axios operation:', error.response ? error.response.data : error.message);
      setError(error.response?.data?.message || error.message); // Set the error message for display
    }
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
            {error && <Popup initialMessage={error} is_closable={true} onClose={() => setError(null)} />}
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
