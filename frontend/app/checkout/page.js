"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import BogoDetails from '@/components/BogoDetails';
import api from "@/lib/api";
import Popup from "@/components/Popup"; // Assuming Popup component is imported correctly

const Checkout = () => {

  const [allPaymentMethods, setAllPaymentMethods] = useState([]);
  const [allSupplyMethods, setAllSupplyMethods] = useState([]);
  const [paymentMethod, setPaymentMethod] = useState('');
  const [fullAddress, setFullAddress] = useState({
    address: '',
    city: '',
    state: '',
    country: '',
    zip_code: ''
  });
  const router = useRouter();

  const [supplyMethod, setSupplyMethod] = useState('');
  const [errors, setErrors] = useState({});
  const [isFormValid, setIsFormValid] = useState(false);
  const [submissionStatus, setSubmissionStatus] = useState('');
  const [message, setMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const validate = () => {
    const newErrors = {};
    if (!paymentMethod) {
      newErrors.paymentMethod = 'Payment method is required';
    }
    if (!fullAddress.address) {
      newErrors.address = 'Address is required';
    }
    if (!fullAddress.city) {
      newErrors.city = 'City is required';
    }
    if (!fullAddress.state) {
      newErrors.state = 'State is required';
    }
    if (!fullAddress.country) {
      newErrors.country = 'Country is required';
    }
    if (!fullAddress.zip_code) {
      newErrors.zip_code = 'Zip code is required';
    }
    if (!supplyMethod) {
      newErrors.supplyMethod = 'Supply method is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  useEffect(() => {
    const fetchPaymentMethods = async () => {
      try {
        const response = await api.get('/third_party/payment/get_all_active');
        setAllPaymentMethods(response.data.message);
      } catch (error) {
        console.error('Error fetching payment methods:', error);
      }
    };

    const fetchSupplyMethods = async () => {
      try {
        const response = await api.get('/third_party/delivery/get_all_active');
        setAllSupplyMethods(response.data.message);
      } catch (error) {
        console.error('Error fetching supply methods:', error);
      }
    };

    fetchPaymentMethods();
    fetchSupplyMethods();
  }, []);

  useEffect(() => {
    // Check if all fields are filled
    if (
      paymentMethod &&
      fullAddress.address &&
      fullAddress.city &&
      fullAddress.state &&
      fullAddress.country &&
      fullAddress.zip_code &&
      supplyMethod
    ) {
      setIsFormValid(true);
    } else {
      setIsFormValid(false);
    }
  }, [paymentMethod, fullAddress, supplyMethod]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFullAddress((prevAddress) => ({
      ...prevAddress,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      // Submit the form
      const data = {
        "payment_details" : {'payment method' : paymentMethod},
        'address' : fullAddress,
        'supply_method' : supplyMethod
      };

      api.post('/market/checkout', data)
        .then((response) => {
          console.log('Checkout response:', response.data);
          setSubmissionStatus('Submitted successfully');
          setMessage('Your order has been submitted successfully.');
        })
        .catch(error => {
          console.error('Error submitting checkout:', error);
          setSubmissionStatus('Error submitting checkout');
          setErrorMessage('There was an error submitting your order.');
        });

    } else {
      setSubmissionStatus('Please fill in all required fields.');
    }
  };

  return (
    <div className="container">
      <h1>Checkout</h1>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <h2>Payment Method</h2>
          <select
            id="payment-method"
            value={paymentMethod}
            onChange={(e) => setPaymentMethod(e.target.value)}
            required
          >
            <option value="">Select a payment method</option>
            {allPaymentMethods.map((method) => (
              <option key={method} value={method}>
                {method}
              </option>
            ))}
            {/* Add more payment methods here */}
          </select>
          {errors.paymentMethod && <p className="error">{errors.paymentMethod}</p>}
        </div>

        {paymentMethod === 'bogo' && <BogoDetails />}

        <div className="form-group">
          <h2>Supply Method</h2>
          <select
            id="supply-method"
            value={supplyMethod}
            onChange={(e) => setSupplyMethod(e.target.value)}
            required
          >
            <option value="">Select a supply method</option>
            {
              allSupplyMethods.map((method) => (
                <option key={method} value={method}>
                  {method}
                </option>
              ))
            }
          </select>
          {errors.supplyMethod && <p className="error">{errors.supplyMethod}</p>}
          {supplyMethod === 'bogo' && <BogoDetails />}
        </div>

        <h2>Shipping Address</h2>
        <div className="form-group">
          <label htmlFor="address">Street Address</label>
          <input
            type="text"
            id="address"
            name="address"
            value={fullAddress.address}
            onChange={handleInputChange}
            placeholder="Street, Number, Apartment"
            required
          />
          {errors.address && <p className="error">{errors.address}</p>}
        </div>
        <div className="form-group">
          <label htmlFor="city">City</label>
          <input
            type="text"
            id="city"
            name="city"
            value={fullAddress.city}
            onChange={handleInputChange}
            placeholder="City"
            required
          />
          {errors.city && <p className="error">{errors.city}</p>}
        </div>
        <div className="form-group">
          <label htmlFor="state">State</label>
          <input
            type="text"
            id="state"
            name="state"
            value={fullAddress.state}
            onChange={handleInputChange}
            placeholder="State"
            required
          />
          {errors.state && <p className="error">{errors.state}</p>}
        </div>
        <div className="form-group">
          <label htmlFor="country">Country</label>
          <input
            type="text"
            id="country"
            name="country"
            value={fullAddress.country}
            onChange={handleInputChange}
            placeholder="Country"
            required
          />
          {errors.country && <p className="error">{errors.country}</p>}
        </div>
        <div className="form-group">
          <label htmlFor="zip">Zip Code</label>
          <input
            type="text"
            id="zip_code"
            name="zip_code"
            value={fullAddress.zip_code}
            onChange={handleInputChange}
            placeholder="Zip Code"
            required
          />
          {errors.zip_code && <p className="error">{errors.zip_code}</p>}
        </div>

        <button type="submit">Submit</button>
      </form>

      {submissionStatus && <p className="submission-status">{submissionStatus}</p>}

      {message && (
        <Popup
          initialMessage={message}
          is_closable={true}
          onClose={() => {
            setMessage('');
            router.back();
          }}
        />
      )}

      {errorMessage && (
        <Popup
          initialMessage={errorMessage}
          is_closable={true}
          onClose={() => {
            setErrorMessage('');
          }}
        />
      )}

      <style jsx>{`
        .container {
          max-width: 600px;
          margin: 0 auto;
          padding: 20px;
          border: 1px solid #ccc;
          border-radius: 5px;
          background-color: #f9f9f9;
        }
        h1 {
          text-align: center;
          margin-bottom: 20px;
          font-weight: bold;
          font-size: 24px;
        }
        h2 {
          font-size: 17px;
          margin-bottom: 10px;
          font-weight: bold;
        }
        .form-group {
          margin-bottom: 15px;
        }
        label {
          display: block;
          margin-bottom: 5px;
        }
        input, select {
          width: 100%;
          padding: 8px;
          box-sizing: border-box;
        }
        button {
          display: block;
          width: 100%;
          padding: 10px;
          background-color: #0070f3;
          color: white;
          border: none;
          border-radius: 5px;
          cursor: pointer;
        }
        button:hover {
          background-color: #005bb5;
        }
        .error {
          color: red;
          font-size: 0.9em;
          margin-top: 5px;
        }
        .submission-status {
          margin-top: 20px;
          font-size: 1.2em;
          color: ${submissionStatus === 'Submitted successfully' ? 'green' : 'red'};
          text-align: center;
        }
      `}</style>
    </div>
  );
}

export default Checkout;
