import React, { useState } from 'react';

const SearchForm = ({ onSearch }) => {
    const [productName, setProductName] = useState('');
    const [storeName, setStoreName] = useState('');

    // Handle form submission is done by calling the onSearch function passed as a prop
    const handleSubmit = (e) => {
        e.preventDefault();
        onSearch(productName, storeName);
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Product Name:</label>
                <input
                    type="text"
                    value={productName}
                    onChange={(e) => setProductName(e.target.value)}
                    required
                />
            </div>
            <div>
                <label>Store Name (optional):</label>
                <input
                    type="text"
                    value={storeName}
                    onChange={(e) => setStoreName(e.target.value)}
                />
            </div>
            <button type="submit">Search</button>
        </form>
    );
};

export default SearchForm;
