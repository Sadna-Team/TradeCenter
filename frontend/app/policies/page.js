"use client";
import { useEffect, useState } from 'react';
import api from '@/lib/api';

const fetchPolicies = async (storeId, setPolicies, setError) => {
  try {
    const response = await api.get(`/store/view_all_policies_of_store?store_id=${storeId}`);
    setPolicies(response.data.message);
  } catch (error) {
    console.error('Failed to fetch policies', error);
    setError('Failed to fetch policies');
  }
};

const ManagePolicy = () => {
  const [policies, setPolicies] = useState([]);
  const [expandedPolicy, setExpandedPolicy] = useState(null);
  const [error, setError] = useState(null);
  const storeId = 1; // Replace with the actual store ID you want to use

  useEffect(() => {
    fetchPolicies(storeId, setPolicies, setError);
  }, [storeId]);

  const handleToggle = (policyId) => {
    setExpandedPolicy(expandedPolicy === policyId ? null : policyId);
  };

  return (
    <div>
      <h1>Policies</h1>
      {error && <div className="error">{error}</div>}
      {policies.map(policy => (
        <div key={policy.purchase_policy_id}>
          <button onClick={() => handleToggle(policy.purchase_policy_id)}>
            {policy.policy_name}
          </button>
          {expandedPolicy === policy.purchase_policy_id && (
            <div className="accordion-content">
              <pre>{JSON.stringify(policy.details, null, 2)}</pre>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default ManagePolicy;
