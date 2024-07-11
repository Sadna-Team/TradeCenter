import React, { useState, useEffect } from 'react';

const SupplyForm = ({ handleChange }) => {
  const [requestingName, setRequestingName] = useState('');

    useEffect(() => {
    handleChange({
      "name": requestingName,
    });
    }, [requestingName]);

    return (
        <div
        style={{
            maxWidth: '400px',
            margin: '0 auto',
            padding: '20px',
            border: '1px solid #ccc',
            borderRadius: '5px',
            backgroundColor: '#f9f9f9',
        }}
        >
        <div style={{ marginBottom: '15px' }}>
            <label htmlFor="requestingName" style={{ marginBottom: '5px', display: 'block' }}>
            Full Name:
            </label>
            <input
            type="text"
            id="requestingName"
            value={requestingName}
            onChange={(e) => setRequestingName(e.target.value)}
            placeholder={'Enter Full Name'}
            required
            style={{
                width: 'calc(100% - 10px)',
                padding: '8px',
                boxSizing: 'border-box',
                fontSize: '14px',
                borderColor: '#ccc',
                backgroundColor: 'white',
                color: 'black',
            }}
            />
        </div>
        </div>
  );
};

export default SupplyForm;
