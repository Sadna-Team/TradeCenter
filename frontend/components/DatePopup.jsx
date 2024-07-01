import React, { useState, useEffect } from 'react';

const DatePopup = ({ initialMessage, onClose, onCancel }) => {
  const [isOpen, setIsOpen] = useState(true);
  const [message, setMessage] = useState(initialMessage);
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');

  useEffect(() => {
    setMessage(initialMessage);
  }, [initialMessage]);

  const handleClose = () => {
    // Ensure time is in 24-hour format
    const formattedTime = time ? new Date(`1970-01-01T${time}:00`).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', hour12: false }) : '';
    const time_dict = { hour: formattedTime.slice(0, 2), minute: formattedTime.slice(3, 5) };
    const date_dict = { year: date.slice(0, 4), month: date.slice(5, 7), day: date.slice(8, 10) };
    console.log('Date:', date_dict, 'Time:', time_dict);
    onClose({date: date_dict, time: time_dict });
    setIsOpen(false);
  };

  const handleCloseNoDate = () => {
    onClose(null);
    setIsOpen(false);
  };

  const handleCancel = () => {
    onCancel();
    setIsOpen(false);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    handleClose();
  };

  if (!isOpen) return null;

  return (
    <div style={overlayStyle}>
      <div style={popupStyle}>
        <p style={messageStyle}>{message}</p>
        <form onSubmit={handleSubmit}>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded mt-1"
            placeholder="Enter your date"
            required
          />
          <input
            type="time"
            value={time}
            onChange={(e) => setTime(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded mt-1"
            placeholder="Enter time (HH:MM)"
            required
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px' }}>
            <button type="submit" style={submitButtonStyle}>Submit Date</button>
            <button onClick={handleCloseNoDate} style={noDateButtonStyle}>No Date</button>
          </div>
        </form>
        <button onClick={handleCancel} style={cancelButtonStyle}>Cancel</button>
      </div>
    </div>
  );
};

const messageStyle = {
  color: 'black',
  fontSize: '16px',
  fontWeight: 'bold',
  margin: '10px 0',
};

const overlayStyle = {
  position: 'fixed',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  backgroundColor: 'rgba(0, 0, 0, 0.5)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};

const popupStyle = {
  backgroundColor: 'white',
  padding: '20px',
  borderRadius: '10px',
  boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  maxWidth: '300px',
  width: '100%',
  textAlign: 'center',
};

const submitButtonStyle = {
  padding: '10px 10px',
  backgroundColor: '#007BFF',
  color: 'white',
  border: 'none',
  borderRadius: '5px',
  cursor: 'pointer',
  fontSize: '12px',
};

const noDateButtonStyle = {
  padding: '10px 10px',
  backgroundColor: '#007BFF',
  color: 'white',
  border: 'none',
  borderRadius: '5px',
  cursor: 'pointer',
  fontSize: '16px',
};

const cancelButtonStyle = {
  marginTop: '10px',
  padding: '8px 16px',
  backgroundColor: 'red',
  color: 'white',
  border: 'none',
  borderRadius: '5px',
  cursor: 'pointer',
  fontSize: '14px',
};

export default DatePopup;
