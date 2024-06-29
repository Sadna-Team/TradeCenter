// pages/add-store.js

"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from "@/lib/api";
import Popup from "@/components/Popup";

export default function AddStorePage() {
  const router = useRouter();
  const [storeName, setStoreName] = useState('');
  const [locationId, setLocationId] = useState('');
  const [errors, setErrors] = useState({});
  const [isFormValid, setIsFormValid] = useState(false);
  const [message, setMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    setIsFormValid(storeName.trim() !== '' && /^\d+$/.test(locationId));
  }, [storeName, locationId]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    // Post a request to the server
    const storeData = {
      "location_id": locationId,
      "store_name": storeName
    };

    api.post('/store/add_store', storeData)
      .then(() => {
        setMessage('Store added successfully');
        setErrorMessage(null); // Clear any previous error message
      })
      .catch((error) => {
        console.error('Error adding store:', error);
        setErrorMessage('Error adding store: ' + error.response?.data?.message || error.message);
        setMessage(null); // Clear any previous success message
      });

    // For demonstration, navigate back to the previous page after submission

  };

  const validate = () => {
    const newErrors = {};
    // Example validation rules, adjust as needed
    if (!storeName.trim()) {
      newErrors.storeName = 'Store name is required';
    }
    if (!locationId.trim()) {
      newErrors.locationId = 'Location ID is required';
    } else if (!/^\d+$/.test(locationId)) {
      newErrors.locationId = 'Location ID must contain only numbers';
    }
    return newErrors;
  };

  const handleLocationIdChange = (e) => {
    const value = e.target.value;
    if (/^\d*$/.test(value)) {
      setLocationId(value);
    }
  };

  const handleStoreNameChange = (e) => {
    setStoreName(e.target.value);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4 text-center">Add Store</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700">Store Name</label>
            <input
              type="text"
              value={storeName}
              onChange={handleStoreNameChange}
              className={`w-full p-2 border border-gray-300 rounded mt-1 ${errors.storeName ? 'border-red-500' : ''}`}
              placeholder="Enter store name"
            />
            {errors.storeName && <span className="text-red-500 text-sm">{errors.storeName}</span>}
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Location ID</label>
            <input
              type="text"
              value={locationId}
              onChange={handleLocationIdChange}
              className={`w-full p-2 border border-gray-300 rounded mt-1 ${errors.locationId ? 'border-red-500' : ''}`}
              placeholder="Enter location ID (numbers only)"
            />
            {errors.locationId && <span className="text-red-500 text-sm">{errors.locationId}</span>}
          </div>
          <button
            type="submit"
            className={`w-full py-2 rounded ${isFormValid ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-500 cursor-not-allowed'}`}
            disabled={!isFormValid}
          >
            Add Store
          </button>
        </form>
        {message && (
          <Popup initialMessage={message} is_closable={true} onClose={() => {
            setMessage(null);
            router.back();
          }} />
        )}
        {errorMessage && (
          <Popup initialMessage={errorMessage} is_closable={true} onClose={() => {
            setErrorMessage(null);

          }} />
        )}
      </div>
    </div>
  );
}
