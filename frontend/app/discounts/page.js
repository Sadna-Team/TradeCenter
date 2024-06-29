"use client";
import { useEffect, useState } from 'react';
import api from '@/lib/api';

const fetchDiscounts = async (setDiscounts, setError) => {
  try {
    const response = await api.get('/store/view_all_discounts');
    setDiscounts(response.data.message);
  } catch (error) {
    console.error('Failed to fetch discounts', error);
    setError('Failed to fetch discounts');
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
