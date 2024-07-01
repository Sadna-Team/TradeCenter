"use client";

import { useParams } from 'next/navigation';
import { useState, useEffect } from 'react';
import api from '@/lib/api'; // Import the configured axios instance

export default function NominateEmployeesPage() {
  const { storeid } = useParams();
  const [users, setUsers] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [errorMessage, setErrorMessage] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [updateFlag, setUpdateFlag] = useState(false); // State variable to trigger useEffect

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await api.post('/user/get_unemployed_users', {
          store_id: storeid,
        });
        const data = response.data.unemployed_users;
        setUsers(data);
        setFilteredUsers(data); // Initialize filtered users with fetched data
      } catch (error) {
        setErrorMessage('Error fetching users');
        console.error('Error fetching users:', error.response ? error.response.data : error.message);
      }
    };

    fetchUsers();
  }, [storeid, updateFlag]); // Include updateFlag in the dependency array

  useEffect(() => {
    setFilteredUsers(
      users.filter((user) =>
        user.username.toLowerCase().includes(searchQuery.toLowerCase())
      )
    );
  }, [searchQuery, users]);

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleNominate = async (username, role) => {
    try {
      const endpoint = role === 'owner' ? '/store/add_store_owner' : '/store/add_store_manager';
      const response = await api.post(endpoint, {
        store_id: storeid,
        username,
      });
      setSuccessMessage(`Successfully nominated ${username} as ${role}`);
      setErrorMessage(null);
      
      // Trigger useEffect to re-fetch users
      setUpdateFlag((prevFlag) => !prevFlag);

      // Clear the success message after 3 seconds
      setTimeout(() => {
        setSuccessMessage(null);
      }, 3000);
    } catch (error) {
      setErrorMessage(`Error nominating ${username} as ${role}`);
      setSuccessMessage(null);
      console.error(`Error nominating ${username} as ${role}:`, error.response ? error.response.data : error.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-md">
        <h1 className="text-3xl font-bold mb-4">Nominate Employees</h1>
        {errorMessage && <p className="text-red-500 mb-4">{errorMessage}</p>}
        {successMessage && <p className="text-green-500 mb-4">{successMessage}</p>}
        <input
          type="text"
          placeholder="Search users"
          value={searchQuery}
          onChange={handleSearchChange}
          className="w-full p-2 mb-4 border rounded"
        />
        <div className="grid grid-cols-1 gap-6">
          {filteredUsers.map((user) => (
            <div key={user.user_id} className="p-4 border rounded-lg bg-gray-50 flex items-center justify-between">
              <p className="text-lg font-bold">{user.username}</p>
              <div className="space-x-4">
                <button
                  onClick={() => handleNominate(user.username, 'owner')}
                  className="bg-blue-500 text-white py-2 px-4 rounded"
                >
                  Nominate Owner
                </button>
                <button
                  onClick={() => handleNominate(user.username, 'manager')}
                  className="bg-green-500 text-white py-2 px-4 rounded"
                >
                  Nominate Manager
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
