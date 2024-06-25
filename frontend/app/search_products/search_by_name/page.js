"use client"; // Add this at the top of the file

import React, { useState } from 'react';
import SearchForm from '../../components/SearchForm';

const SearchPage = () => {
    const [results, setResults] = useState([]);
    const [error, setError] = useState(null);

    const handleSearch = async (productName, storeName) => {
        // handle search logic here
        console.log('Searching for:', productName, storeName);
    };

    return (
        <div>
            <h1>Search Products</h1>
            <SearchForm onSearch={handleSearch} />
            {error && <div className="error">{error}</div>}
            {results.length > 0 && (
                <ul>
                    {results.map((product) => (
                        <li key={product.id}>{product.name}</li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default SearchPage;
