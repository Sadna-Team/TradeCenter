"use client";
import api from '@/lib/api';
import { useState, useEffect } from 'react';
import { ScrollArea } from '@/components/ScrollArea';
import Link from 'next/link';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter
} from "@/components/Dialog";
import { Input } from "@/components/Input";
import { Label } from "@/components/Label";
import Button from "@/components/Button";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/AlertDialog";

const ManageUserBids = () => {
  const [errorMessage, setErrorMessage] = useState('');
  const [bids, setBids] = useState([]);
  const [expandedBids, setExpandedBids] = useState({});
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [currentBidId, setCurrentBidId] = useState(null);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [editCounterBid, setEditCounterBid] = useState('');

  useEffect(() => {
    fetchBids();
  }, []);

  
  const fetchBids = async () => {
    try {
      const response = await api.post('/market/view_bids_of_user', {});
      if (response.status !== 200) {
        console.error('Failed to fetch bids', response);
        setErrorMessage('Failed to fetch bids');
        return;
      }
      console.log("the bids of the user:", response.data.message)
      let data = response.data.message;

      if(data === null || data === undefined) {
        console.error('Failed to fetch bids of user', response);
        setErrorMessage('Failed to fetch bids of user');
        return;
      }

      let bids_to_show = [];
      
      for(let i = 0; i < data.length; i++){
        console.log("the current bid:", data[i])
        if (data[i].status === "onGoing" || data[i].status === "accepted" || data[i].status === "approved") {
          bids_to_show.push(data[i]);
        }
      }
      console.log("the bids to show:", bids_to_show)
      setBids(bids_to_show);
      setErrorMessage('');
      
    } catch (error) {
      console.error('Failed to fetch bids', error);
      setErrorMessage('Failed to fetch bids');
    }
  };

  const handleAcceptBid = async (bidId) => {
    try {
      const response = await api.post('/market/user_counter_accept', { bid_id: bidId });
      if (response.status !== 200) {
        console.error('Failed to accept bid', response);
        setErrorMessage('Failed to accept bid');
        return;
      }
      fetchBids();
    } catch (error) {
      console.error('Failed to accept bid', error);
      setErrorMessage('Failed to accept bid');
    }
  };

  //basically handle decline counter.
  const handleRemoveBid = (bidId) => {
    const removeBid = async () => {
      try {
        const response = await api.post('/market/user_counter_decline', { bid_id: bidId });
        if (response.status !== 200) {
          console.error('Failed to remove bid', response);
          setErrorMessage('Failed to remove bid');
          return;
        }
        fetchBids();
        setErrorMessage('');
      } catch (error) {
        console.error('Failed to remove bid', error);
        setErrorMessage('Failed to remove bid');
      }
    };
    removeBid();
  };


  //basically handle decline counter.
  const handleCancelBid = (bidId) => {
    const removeBid = async () => {
      try {
        const response = await api.post('/market/user_cancel_bid', { bid_id: bidId });
        if (response.status !== 200) {
          console.error('Failed to cancel bid', response);
          setErrorMessage('Failed to cancel bid');
          return;
        }
        fetchBids();
        setErrorMessage('');
      } catch (error) {
        console.error('Failed to cancel bid', error);
        setErrorMessage('Failed to cancel bid');
      }
    };
    removeBid();
  };


  const handleOpenEditDialog = (bidId) => {
    const bid = bids.find((bid) => bid.bid_id === bidId);
    if (bid) {
      setCurrentBidId(bidId);
      setEditCounterBid(bid.proposed_price.toString());
      setIsEditDialogOpen(true);
    }
  };

  const handleEditSaveChanges = () => {
    const editBid = async () => {
      try {
        if (editCounterBid === '') {
          setErrorMessage('Please enter a counter offer');
          return;
        }

        if (isNaN(editCounterBid)) {
          setErrorMessage('Counter offer must be a number');
          return;
        }

        if (parseFloat(editCounterBid) < 0) {
          setErrorMessage('Counter offer must be greater or equal to 0');
          return;
        }

        const response = await api.post('/market/user_counter_offer_bid', {
          bid_id: currentBidId,
          proposed_price: parseFloat(editCounterBid),
        });

        if (response.status !== 200) {
          console.error('Failed to counter bid offer', response);
          setErrorMessage('Failed to counter bid offer');
          return;
        }
        setIsEditDialogOpen(false);
        setEditCounterBid('');
        setErrorMessage('');
        fetchBids();
      } catch (error) {
        console.error('Failed to edit bid counter offer', error);
        setErrorMessage('Failed to edit bid counter offer');
      }
    };
    editBid();
  };

  //handle cancel bid!

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
      'approved': 'text-dark-pastel-turqoise'
    };

    let is_offer_to_store = "yes";
    if (!bid.is_offer_to_store) {
      is_offer_to_store = "no";
    }

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
            <p><strong>Is Offer To Store:</strong> {is_offer_to_store}</p>
            {bid.status === 'onGoing' && bid.is_offer_to_store && (
              <div className="flex justify-between mt-4">
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button className="bg-red-500 text-white py-1 px-3 rounded">Cancel Bid</Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent className="bg-white">
                    <AlertDialogHeader>
                      <AlertDialogTitle>Are you sure you want to cancel?</AlertDialogTitle>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                      <AlertDialogAction onClick={() => handleCancelBid(bid.bid_id)}>Yes, cancel</AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            )}
            {bid.status === 'onGoing' && !bid.is_offer_to_store && (
              <div className="flex justify-between mt-4">
                <Button className="bg-green-500 text-white py-1 px-3 rounded" onClick={() => handleAcceptBid(bid.bid_id)}>Accept</Button>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button className="bg-red-500 text-white py-1 px-3 rounded">Decline</Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent className="bg-white">
                    <AlertDialogHeader>
                      <AlertDialogTitle>Are you sure you want to decline?</AlertDialogTitle>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                      <AlertDialogAction onClick={() => handleRemoveBid(bid.bid_id)}>Yes, decline</AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
                <Button className="bg-black text-white py-1 px-3 rounded" onClick={() => handleOpenEditDialog(bid.bid_id)}>Counter</Button>
              </div>
            )}
            {bid.status === 'approved' && (
              <div className="flex justify-between mt-4">
                <Link href={{
                  pathname: `/checkout_bid/${bid.bid_id}`,
                  query: { bidId: bid.bid_id },
                }}>
                  <div className="bg-green-500 hover:bg-green-600 text-white font-bold py-1 px-3 rounded cursor-pointer">Proceed to Checkout</div>
                </Link>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button className="bg-red-500 text-white py-1 px-3 rounded">Cancel</Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent className="bg-white">
                    <AlertDialogHeader>
                      <AlertDialogTitle>Are you sure you want to cancel?</AlertDialogTitle>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                      <AlertDialogAction onClick={() => handleCancelBid(bid.bid_id)}>Yes, cancel</AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex flex-wrap justify-center">
      <div className="w-full max-w-md p-4">
        <h2 className="text-center font-bold mb-4">User Bids</h2>
        <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
          {bids.map((bid) => renderBid(bid))}
        </ScrollArea>
        <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
          <DialogContent className="sm:max-w-[425px] bg-white">
            <DialogHeader>
              <DialogTitle>Counter Proposed Price</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              {errorMessage && (
                <div className="text-red-500 text-sm">{errorMessage}</div>
              )}
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="edit-counter-bid" className="block mt-2">Counter Offer</Label>
                <Input
                  id="edit-counter-bid"
                  placeholder="Counter Offer"
                  value={editCounterBid}
                  onChange={(e) => setEditCounterBid(e.target.value)}
                  className="col-span-3 border border-black"
                />
              </div>
            </div>
            <DialogFooter>
              <Button type="button" onClick={handleEditSaveChanges}>Confirm</Button>
              <Button type="button" onClick={() => setIsEditDialogOpen(false)}>Cancel</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
};

export default ManageUserBids;