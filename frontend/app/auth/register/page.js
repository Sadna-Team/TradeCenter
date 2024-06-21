"use client";

import { useState } from 'react';

export default function Register() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [year, setYear] = useState('');
  const [month, setMonth] = useState('');
  const [day, setDay] = useState('');
  const [phone, setPhone] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle registration logic here
    console.log('Email:', email);
    console.log('Username:', username);
    console.log('Password:', password);
    console.log('Year:', year);
    console.log('Month:', month);
    console.log('Day:', day);
    console.log('Phone:', phone);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4 text-center">Register</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded mt-1"
              placeholder="Enter your email"
            />
          </div>
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
          <div className="mb-4">
            <label className="block text-gray-700">Date of Birth</label>
            <div className="flex space-x-2">
              <input
                type="text"
                value={year}
                onChange={(e) => setYear(e.target.value)}
                className="w-1/3 p-2 border border-gray-300 rounded mt-1"
                placeholder="Year"
              />
              <input
                type="text"
                value={month}
                onChange={(e) => setMonth(e.target.value)}
                className="w-1/3 p-2 border border-gray-300 rounded mt-1"
                placeholder="Month"
              />
              <input
                type="text"
                value={day}
                onChange={(e) => setDay(e.target.value)}
                className="w-1/3 p-2 border border-gray-300 rounded mt-1"
                placeholder="Day"
              />
            </div>
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Phone</label>
            <input
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded mt-1"
              placeholder="Enter your phone number"
            />
          </div>
          <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded">
            Register
          </button>
        </form>
      </div>
    </div>
  );
}
