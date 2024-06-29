"use client";
import { useEffect, useState } from 'react';
import api from '@/lib/api';

const fetchDiscounts = async (setDiscounts, setError) => {
  try {
    const response = await api.get('/store/view_discounts_info', {});
    if (response.status === 200) {
      setDiscounts(response.data.message);
    } else {
      setError(`Unexpected response status: ${response.status}`);
    }
  } catch (error) {
    if (error.response) {
      setError(`Failed to fetch discounts: ${error.response.data.message || error.response.status}`);
    } else {
      setError('Failed to fetch discounts');
    }
  }
};

const ManageDiscount = () => {
  const [discounts, setDiscounts] = useState([]);
  const [expandedDiscount, setExpandedDiscount] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDiscounts(setDiscounts, setError);
  }, []);

  const handleToggle = (discountId) => {
    setExpandedDiscount(expandedDiscount === discountId ? null : discountId);
  };

  return (
    <div>
      <h1>Discounts</h1>
      {error && <div className="error">{error}</div>}
      {discounts.map(discount => (
        <div key={discount.discount_id}>
          <button onClick={() => handleToggle(discount.discount_id)}>
            {discount.discount_description}
          </button>
          {expandedDiscount === discount.discount_id && (
            <div className="accordion-content">
              <pre>{JSON.stringify(discount, null, 2)}</pre>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default ManageDiscount;
