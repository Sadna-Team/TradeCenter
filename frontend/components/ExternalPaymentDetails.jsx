import React, { useState, useEffect } from 'react';

const CreditCardForm = ({ handleChange }) => {
  const [cardNumber, setCardNumber] = useState('');
  const [expiryMonth, setExpiryMonth] = useState('');
  const [expiryYear, setExpiryYear] = useState('');
  const [cvv, setCvv] = useState('');
  const [holderName, setHolderName] = useState('');
  const [holderId, setHolderId] = useState('');

    useEffect(() => {
    handleChange({
      "card_number": cardNumber,
      "month": expiryMonth,
      "year": expiryYear,
      "cvv": cvv,
      "holder": holderName,
      "id": holderId,
    });
    }, [cardNumber, expiryMonth, expiryYear, cvv, holderName, holderId]);

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
            <label htmlFor="cardNumber" style={{ marginBottom: '5px', display: 'block' }}>
            Card Number:
            </label>
            <input
            type="text"
            id="cardNumber"
            value={cardNumber}
            onChange={(e) => setCardNumber(e.target.value)}
            placeholder={'Enter card number'}
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
        <div style={{ marginBottom: '15px' }}>
            <label htmlFor="expiryMonth" style={{ marginBottom: '5px', display: 'block' }}>
            Expiry Month:
            <select
                id="expiryMonth"
                value={expiryMonth}
                onChange={(e) => setExpiryMonth(e.target.value)}
                required
                style={{
                width: 'calc(100% - 10px)',
                padding: '8px',
                boxSizing: 'border-box',
                fontSize: '14px',
                color: expiryMonth === '' ? 'grey' : 'black',
                }}
            >
                <option value="" disabled hidden>
                MM
                </option>
                {Array.from({ length: 12 }, (_, i) => {
                const month = (i + 1).toString().padStart(2, '0');
                return (
                    <option key={month} value={month}>
                    {month}
                    </option>
                );
                })}
            </select>
            </label>
        </div>
        <div style={{ marginBottom: '15px' }}>
            <label htmlFor="expiryYear" style={{ marginBottom: '5px', display: 'block' }}>
            Expiry Year:
            <select
                id="expiryYear"
                value={expiryYear}
                onChange={(e) => setExpiryYear(e.target.value)}
                required
                style={{
                width: 'calc(100% - 10px)',
                padding: '8px',
                boxSizing: 'border-box',
                fontSize: '14px',
                color: expiryYear === '' ? 'grey' : 'black',
                }}
            >
                <option value="" disabled hidden>
                YYYY
                </option>
                {Array.from({ length: 16 }, (_, i) => {
                const year = (2025 + i).toString();
                return (
                    <option key={year} value={year}>
                    {year}
                    </option>
                );
                })}
            </select>
            </label>
        </div>
        <div style={{ marginBottom: '15px' }}>
            <label htmlFor="cvv" style={{ marginBottom: '5px', display: 'block' }}>
            cvv:
            <input
                type="text"
                id="cvv"
                value={cvv}
                onChange={(e) => setCvv(e.target.value)}
                placeholder='cvv'
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
            </label>
        </div>
        <div style={{ marginBottom: '15px' }}>
            <label htmlFor="holderName" style={{ marginBottom: '5px', display: 'block' }}>
            Holder Name:
            <input
                type="text"
                id="holderName"
                value={holderName}
                onChange={(e) => setHolderName(e.target.value)}
                placeholder="Full name as on card"
                required
                style={{
                width: 'calc(100% - 10px)',
                padding: '8px',
                boxSizing: 'border-box',
                fontSize: '14px',
                }}
            />
            </label>
        </div>
        <div style={{ marginBottom: '15px' }}>
            <label htmlFor="holderId" style={{ marginBottom: '5px', display: 'block' }}>
            Holder ID:
            <input
                type="text"
                id="holderId"
                value={holderId}
                onChange={(e) => setHolderId(e.target.value)}
                placeholder='ID number'
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
            </label>
        </div>
        <style jsx>{`
            select:invalid {
            color: grey;
            }
        `}</style>
        </div>
  );
};

export default CreditCardForm;
