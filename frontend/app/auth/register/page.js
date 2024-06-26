"use client";

import { useState, useEffect } from 'react';
import api from '@/lib/api';

export default function Register() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [year, setYear] = useState('');
  const [month, setMonth] = useState('');
  const [day, setDay] = useState('');
  const [phone, setPhone] = useState('');
  const [errors, setErrors] = useState({});
  const [isFormValid, setIsFormValid] = useState(false);

  useEffect(() => {
    // Check if all fields are filled
    if (email && username && password && year && month && day && phone) {
      setIsFormValid(true);
    } else {
      setIsFormValid(false);
    }
  }, [email, username, password, year, month, day, phone]);

  const validate = () => {
    const newErrors = {};
    if (!/^\d{4}$/.test(year)) {
      newErrors.year = 'Year must be a 4-digit number';
    }
    if (!/^(0?[1-9]|1[0-2])$/.test(month)) {
      newErrors.month = 'Month must be between 1 and 12';
    }
    if (!/^(0?[1-9]|[12]\d|3[01])$/.test(day)) {
      newErrors.day = 'Day must be between 1 and 31';
    }
    if (!/^\d+$/.test(phone)) {
      newErrors.phone = 'Phone number must contain only digits';
    }
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    // Post a request to the server
    const register_credentials = {
      email,
      username,
      password,
      day,
      month,
      year,
      phone,
    };
    const token = localStorage.getItem('token');

    try {
      const response = await api.post('/auth/register', { register_credentials });
      if (response.status === 201) {
        alert('Registration successful');
        window.location.href = '/auth/login';
      } else {
        alert('Registration failed');
      }
    } catch (error) {
      console.error('Error during registration:', error.response ? error.response.data : error.message);
      alert('Registration failed');
    }
  };

  const handleKeyPress = (e) => {
    const charCode = e.charCode;
    if (charCode < 48 || charCode > 57) {
      e.preventDefault();
    }
  };

  const handleYearChange = (e) => {
    if (e.target.value.length <= 4) {
      setYear(e.target.value);
    }
  };

  const handleMonthChange = (e) => {
    const value = e.target.value;
    if (value === '' || (parseInt(value, 10) >= 1 && parseInt(value, 10) <= 12)) {
      setMonth(value);
    }
  };

  const handleDayChange = (e) => {
    const value = e.target.value;
    if (value === '' || (parseInt(value, 10) >= 1 && parseInt(value, 10) <= 31)) {
      setDay(value);
    }
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
                onChange={handleYearChange}
                onKeyPress={handleKeyPress}
                className="w-1/3 p-2 border border-gray-300 rounded mt-1"
                placeholder="Year"
              />
              {errors.year && <span className="text-red-500 text-sm">{errors.year}</span>}
              <input
                type="text"
                value={month}
                onChange={handleMonthChange}
                onKeyPress={handleKeyPress}
                className="w-1/3 p-2 border border-gray-300 rounded mt-1"
                placeholder="Month"
              />
              {errors.month && <span className="text-red-500 text-sm">{errors.month}</span>}
              <input
                type="text"
                value={day}
                onChange={handleDayChange}
                onKeyPress={handleKeyPress}
                className="w-1/3 p-2 border border-gray-300 rounded mt-1"
                placeholder="Day"
              />
              {errors.day && <span className="text-red-500 text-sm">{errors.day}</span>}
            </div>
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Phone</label>
            <input
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              onKeyPress={handleKeyPress}
              className="w-full p-2 border border-gray-300 rounded mt-1"
              placeholder="Enter your phone number"
            />
            {errors.phone && <span className="text-red-500 text-sm">{errors.phone}</span>}
          </div>
          <button
            type="submit"
            className={`w-full py-2 rounded ${isFormValid ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-500 cursor-not-allowed'}`}
            disabled={!isFormValid}
          >
            Register
          </button>
        </form>
      </div>
    </div>
  );
}
