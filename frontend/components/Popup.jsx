

import React, { useState, useEffect } from 'react';

const Popup = ({ initialMessage, is_closable, onClose }) => {
  const [isOpen, setIsOpen] = useState(true); // Initially open with error message
  const [Message, setMessage] = useState(initialMessage);

  useEffect(() => {
    setMessage(initialMessage);
  }, [initialMessage]);

  const closePopup = () => {
    setIsOpen(false);
    onClose(); // Notify parent component
  };

  if (!isOpen) return null;

  return (
    <div style={overlayStyle}>
      <div style={popupStyle}>
        <p style={messageStyle}>{Message}</p>
        {is_closable && <button onClick={closePopup} style={buttonStyle}>Close</button>}
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
  maxWidth: '250px',
  width: '100%',
  textAlign: 'center',
};

const buttonStyle = {
  marginTop: '10px',
  padding: '7px 20px',
  backgroundColor: '#007BFF',
  color: 'white',
  border: 'none',
  borderRadius: '5px',
  cursor: 'pointer',
  fontSize: '16px',
};

export default Popup;
