// pages/add-store.js

"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from "@/lib/api";
import Popup from "@/components/Popup";

export default function AddStorePage() {
  const router = useRouter();
  const [storeName, setStoreName] = useState('');
  const [address, setAddress] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [country, setCountry] = useState('');
  const [zipCode, setZipCode] = useState('');
  const [errors, setErrors] = useState({});
  const [isFormValid, setIsFormValid] = useState(false);
  const [message, setMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    setIsFormValid(
      storeName.trim() !== '' &&
      address.trim() !== '' &&
      city.trim() !== '' &&
      state.trim() !== '' &&
      country.trim() !== '' &&
      zipCode.trim() !== ''
    );
  }, [storeName, address, city, state, country, zipCode]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    // Post a request to the server
    const storeData = {
      "store_name": storeName,
      "address": address,
      "city": city,
      "state": state,
      "country": country,
      "zip_code": zipCode
    };

    api.post('/store/add_store', storeData)
      .then(() => {
        setMessage('Store added successfully');
        setErrorMessage(null); // Clear any previous error message
      })
      .catch((error) => {
        console.error('Error adding store:', error);
        setErrorMessage('Error adding store: ' + (error.response?.data?.message || error.message));
        setMessage(null); // Clear any previous success message
      });
  };

  const validate = () => {
    const newErrors = {};
    if (!storeName.trim()) {
      newErrors.storeName = 'Store name is required';
    }
    if (!address.trim()) {
      newErrors.address = 'Address is required';
    }
    if (!city.trim()) {
      newErrors.city = 'City is required';
    }
    if (!state.trim()) {
      newErrors.state = 'State is required';
    }
    if (!country.trim()) {
      newErrors.country = 'Country is required';
    }
    if (!zipCode.trim()) {
      newErrors.zipCode = 'Zip code is required';
    }
    return newErrors;
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    switch (name) {
      case 'storeName':
        setStoreName(value);
        break;
      case 'address':
        setAddress(value);
        break;
      case 'city':
        setCity(value);
        break;
      case 'state':
        setState(value);
        break;
      case 'country':
        setCountry(value);
        break;
      case 'zipCode':
        setZipCode(value);
        break;
      default:
        break;
    }
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
              name="storeName"
              value={storeName}
              onChange={handleInputChange}
              className={`w-full p-2 border border-gray-300 rounded mt-1 ${errors.storeName ? 'border-red-500' : ''}`}
              placeholder="Enter store name"
            />
            {errors.storeName && <span className="text-red-500 text-sm">{errors.storeName}</span>}
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Address</label>
            <input
              type="text"
              name="address"
              value={address}
              onChange={handleInputChange}
              className={`w-full p-2 border border-gray-300 rounded mt-1 ${errors.address ? 'border-red-500' : ''}`}
              placeholder="Enter address"
            />
            {errors.address && <span className="text-red-500 text-sm">{errors.address}</span>}
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">City</label>
            <input
              type="text"
              name="city"
              value={city}
              onChange={handleInputChange}
              className={`w-full p-2 border border-gray-300 rounded mt-1 ${errors.city ? 'border-red-500' : ''}`}
              placeholder="Enter city"
            />
            {errors.city && <span className="text-red-500 text-sm">{errors.city}</span>}
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">State</label>
            <input
              type="text"
              name="state"
              value={state}
              onChange={handleInputChange}
              className={`w-full p-2 border border-gray-300 rounded mt-1 ${errors.state ? 'border-red-500' : ''}`}
              placeholder="Enter state"
            />
            {errors.state && <span className="text-red-500 text-sm">{errors.state}</span>}
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Country</label>
            <input
              type="text"
              name="country"
              value={country}
              onChange={handleInputChange}
              className={`w-full p-2 border border-gray-300 rounded mt-1 ${errors.country ? 'border-red-500' : ''}`}
              placeholder="Enter country"
            />
            {errors.country && <span className="text-red-500 text-sm">{errors.country}</span>}
          </div>
          <div className="mb-4">
            <label className="block text-gray-700">Zip Code</label>
            <input
              type="text"
              name="zipCode"
              value={zipCode}
              onChange={handleInputChange}
              className={`w-full p-2 border border-gray-300 rounded mt-1 ${errors.zipCode ? 'border-red-500' : ''}`}
              placeholder="Enter zip code"
            />
            {errors.zipCode && <span className="text-red-500 text-sm">{errors.zipCode}</span>}
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
            const event = new Event('storeAdded');
            window.dispatchEvent(event);
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
