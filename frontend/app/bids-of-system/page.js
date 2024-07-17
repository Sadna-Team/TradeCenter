"use client";
import api from '@/lib/api';
import { useState, useEffect } from 'react';
import { ScrollArea } from '@/components/ScrollArea';

const BidsOfSystem = () => {
  const [errorMessage, setErrorMessage] = useState('');
  const [bids, setBids] = useState([]);
  const [expandedBids, setExpandedBids] = useState({});

  useEffect(() => {
    fetchBids();
  }, []);

  const fetchBids = async () => {
    try {
      const response = await api.post('/market/view_all_bids', {});
      if (response.status !== 200) {
        console.error('Failed to fetch bids', response);
        setErrorMessage('Failed to fetch bids');
        return;
      }
      console.log("the bids of the system:", response.data.message)
      let data = response.data.message;

      if (data === null || data === undefined) {
        console.error('Failed to fetch bids of the system', response);
        setErrorMessage('Failed to fetch bids of the system');
        return;
      }

      setBids(data);
      setErrorMessage('');
    } catch (error) {
      console.error('Failed to fetch bids', error);
      setErrorMessage('Failed to fetch bids');
    }
  };

  const handleToggle = (bidId) => {
    setExpandedBids((prevState) => ({
      ...prevState,
      [bidId]: !prevState[bidId],
    }));
  };

  const renderBid = (bid) => {
    const statusColors = {
      'onGoing': 'text-dark-pastel-blue',
      'accepted': 'text-dark-pastel-green',
      'approved': 'text-dark-pastel-turqoise',
      'offer_rejected': 'text-dark-pastel-red',
      'completed': 'text-light-pastel-green',
    };

    return (
      <div key={bid.bid_id} className="mb-4 p-4 border-2 border-gray-300 rounded-md">
        <button onClick={() => handleToggle(bid.bid_id)} className="flex justify-between items-center w-full text-left bid-button">
          <span>{`Bid ID: ${bid.bid_id}`}</span>
          <span className="status-text">
            Status: <span className={`status-value ${statusColors[bid.status]}`}>{bid.status}</span>
          </span>
        </button>
        {expandedBids[bid.bid_id] && (
          <div className="mt-2">
            <p><strong>Store ID:</strong> {bid.store_id}</p>
            <p><strong>Product ID:</strong> {bid.product_id}</p>
            <p><strong>Proposed Price:</strong> {bid.proposed_price}</p>
            <p><strong>Status:</strong> {bid.status}</p>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex flex-wrap justify-center">
      <div className="w-full max-w-md p-4">
        <h2 className="text-center font-bold mb-4">Bids of System</h2>
        <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
          {bids.map((bid) => renderBid(bid))}
        </ScrollArea>
        {errorMessage && (
          <div className="text-red-500 text-center mt-4">{errorMessage}</div>
        )}
      </div>
    </div>
  );
};

export default BidsOfSystem;
