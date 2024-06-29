"use client";

import { useState, useEffect } from 'react';
import api from '../../lib/api'; // Import the configured axios instance

export default function NominationsPage() {
  const [nominations, setNominations] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  // Fetch nominations from the backend
  useEffect(() => {
    const fetchNominations = async () => {
      try {
        const response = await api.get('/user/get_user_nominations');
        const data = response.data;
        console.log('Data:', data);
        const formattedNominations = Object.entries(data.nominations).map(([id, nomination]) => ({
          id,
          ...nomination,
        }));

        setNominations(formattedNominations);
      } catch (error) {
        setErrorMessage('Error fetching nominations');
        console.error('Error fetching nominations:', error.response ? error.response.data : error.message);
      }
    };

    fetchNominations();
  }, []);

  // Handle accept button click
  const handleAccept = async (id) => {
    try {
      await api.post('/user/accept_promotion', {
        promotion_id: id,
        accept: true,
      });
      // Remove the accepted nomination from the list
      setNominations(nominations.filter(nomination => nomination.id !== id));
      console.log(`Accepted nomination with id: ${id}`);
    } catch (error) {
      setErrorMessage('Error accepting nomination');
      console.error('Error accepting nomination:', error.response ? error.response.data : error.message);
    }
  };

  // Handle decline button click
  const handleDecline = async (id) => {
    try {
      await api.post('/user/accept_promotion', {
        promotion_id: id,
        accept: false,
      });
      // Remove the declined nomination from the list
      setNominations(nominations.filter(nomination => nomination.id !== id));
      console.log(`Declined nomination with id: ${id}`);
    } catch (error) {
      setErrorMessage('Error declining nomination');
      console.error('Error declining nomination:', error.response ? error.response.data : error.message);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">User Nominations</h1>
      {errorMessage && <p className="error">{errorMessage}</p>}
      {nominations.map((nomination) => (
        <div key={nomination.id} className="border p-4 mb-4 rounded shadow">
          <p><strong>Nominator Username:</strong> {nomination.nominator_name}</p>
          <p><strong>Store Name:</strong> {nomination.store_name}</p>
          <p><strong>Role:</strong> {nomination.role}</p>
          <div className="mt-4">
            <button
              className="bg-green-500 text-white py-2 px-4 rounded mr-2"
              onClick={() => handleAccept(nomination.id)}
            >
              Accept
            </button>
            <button
              className="bg-red-500 text-white py-2 px-4 rounded"
              onClick={() => handleDecline(nomination.id)}
            >
              Decline
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
