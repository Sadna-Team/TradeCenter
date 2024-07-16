"use client";
import api from '@/lib/api';
import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { ScrollArea } from '@/components/ScrollArea';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter
} from "@/components/Dialog";
import { format } from 'date-fns';
import { Input } from "@/components/Input";
import { Label } from "@/components/Label";
import Button from "@/components/Button";
import { MultiSelect } from 'react-multi-select-component';
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/Select";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/AlertDialog";
import { DatePickerDemo } from "@/components/DatePickerDemo";

const ManageBid = () => {
  const [errorMessage, setErrorMessage] = useState('');
  const searchParams = useSearchParams();
  const store_id = searchParams.get('storeId');

  const [bids, setBids] = useState([]);
  const [expandedBids, setExpandedBids] = useState({});
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [dialogType, setDialogType] = useState('');
  const [currentBidId, setCurrentBidId] = useState(null);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [editCounterBid, setEditCounterBid] = useState('');

  useEffect(() => {
    fetchBids();
  }, []);

  const fetchBids = async () => {
    try {
      console.log("the store id:", store_id)
      const response = await api.post('/market/show_store_bids', { 'store_id': store_id });
      if (response.status !== 200) {
        console.error('Failed to fetch bids', response);
        setErrorMessage('Failed to fetch bids');
        return;
      }
      console.log("the bids of the store:", response.data.message)
      let data = response.data.message;

      if(data === null || data === undefined) {
        console.error('Failed to fetch bids of store', response);
        setErrorMessage('Failed to fetch bids of store');
        return;
      }

      let bids_to_show = [];
      
      for(let i = 0; i < data.length; i++){
        console.log("the current bid:", data[i])
        if (data[i].status === "onGoing"){
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
      const response = await api.post('/market/store_worker_accept_bid', {
        'store_id': store_id,
        'bid_id': bidId,
      });
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

        if(parseFloat(editCounterBid) < 0){
          setErrorMessage('Counter offer must be greater or equal to 0');
          return;
        }

        const response = await api.post('/market/store_worker_counter_bid', {
          'store_id': store_id,
          'bid_id': currentBidId,
          'proposed_price': parseFloat(editCounterBid),
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

  const handleRemoveBid = (bidId) => {
    const removeBid = async () => {
      try {
        const response = await api.post('/market/store_worker_decline_bid', {
          'store_id': store_id,
          'bid_id': bidId,
        });
        if (response.status !== 200) {
          console.error('Failed to remove bid', response);
          setErrorMessage('Failed to remove bid');
          return;
        }
        setErrorMessage('');
        fetchBids();
      } catch (error) {
        console.error('Failed to remove bid', error);
        setErrorMessage('Failed to remove bid');
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

  const handleToggle = (bidId) => {
    setExpandedBids((prevState) => ({
      ...prevState,
      [bidId]: !prevState[bidId],
    }));
  };

  const hasStoreWorkerAcceptedBid = async (bidId) => {
    try {
      const response = await api.post('/market/has_store_worker_accepted_bid', { bid_id: bidId, store_id: store_id});
      if (response.status !== 200) {
        console.error('Failed to check if store worker accepted bid', response);
        return false;
      }
      return response.data.message;
    } catch (error) {
      console.error('Failed to check if store worker accepted bid', error);
      return false;
    }
  };
  

  const renderBid = (bid) => {  
    return (
      <div key={bid.bid_id} className="mb-4 p-4 border-2 border-gray-300 rounded-md">
        <button onClick={() => handleToggle(bid.bid_id)} className="text-left w-full">
          {`Bid ID: ${bid.bid_id}, Status: ${bid.status}`}
        </button>
        {expandedBids[bid.bid_id] && (
          <div className="mt-2">
            <p><strong>Store ID:</strong> {bid.store_id}</p>
            <p><strong>Product ID:</strong> {bid.product_id}</p>
            <p><strong>Proposed Price:</strong> {bid.proposed_price}</p>
            <p><strong>Status:</strong> {bid.status}</p>
            {bid.status === 'onGoing' && bid.is_offer_to_store && !hasStoreWorkerAcceptedBid(bid.bid_id) && (
              <div className="flex justify-between mt-4">
                <Button className="bg-green-500 text-white py-1 px-3 rounded" onClick={() => handleAcceptBid(bid.bid_id)}>Accept</Button>
                <AlertDialog>
                  <AlertDialogTrigger asChild>
                    <Button className="bg-red-500 text-white py-1 px-3 rounded">Reject</Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent className="bg-white">
                    <AlertDialogHeader>
                      <AlertDialogTitle>Are you sure you want to reject?</AlertDialogTitle>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                      <AlertDialogAction onClick={() => handleRemoveBid(bid.bid_id)}>Yes, reject</AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
                <Button className="bg-blue-500 text-white py-1 px-3 rounded" onClick={() => handleOpenEditDialog(bid.bid_id)}>Counter</Button>
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
        <h2 className="text-center font-bold mb-4">Manage Store Bids</h2>
        <ScrollArea className="h-[300px] w-full border-2 border-gray-800 p-4 rounded-md">
          {bids.map((bid) => renderBid(bid))}
        </ScrollArea>
        <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
          <DialogContent className="sm:max-w-[425px] bg-white">
            <DialogHeader>
              <DialogTitle>Editing a bid</DialogTitle>
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
              <Button type="button" onClick={handleEditSaveChanges}>Save changes</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );  
};

export default ManageBid;
