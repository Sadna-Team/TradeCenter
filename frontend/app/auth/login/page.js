import {useState, useEffect, useRef} from 'react';
import socket from "@/app/socket";

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const renderAfter = useRef(false);


  const handleSubmit = (e) => {
    e.preventDefault();
    // Send POST request to authenticate user
    fetch('http://localhost:5000/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'authorization' : 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify({username, password}),
    })
      .then((response) => {
        if (response.ok) {
          // Redirect to dashboard
          window.location.href = '/dashboard';
        } else {
          // Display error message
          console.error('Failed to login:', response.statusText);
        }
      })
      .catch((error) => {
        // Display error message
        console.error('Error logging in:', error);
      });
  }


  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
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
          <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
}
