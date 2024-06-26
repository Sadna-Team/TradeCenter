"use client";

import SearchForm from "@/components/NameSearchBar";
import React, { useState } from "react";

export default function SearchByName() {
    const [results, setResults] = useState([]);
    const [errorMessage, setErrorMessage] = useState(null);

    // get store names from the server
    const storeNames = [
        {id: 1, name: 'Store 1'},
        {id: 2, name: 'Store 2'},
        {id: 3, name: 'Store 3'},
        {id: 4, name: 'Store 4'},
        {id: 5, name: 'Store 5'},
    ];

    const handleSearch = (productName, storeName) => {
        // Handle search logic here
        console.log('Product Name:', productName);
        console.log('Store Name:', storeName);
        setErrorMessage("Connect API to search for products by name");
        setResults([]);
    };

    return (
        <div>
            <SearchForm onSearch={handleSearch} stores={storeNames} />
            {errorMessage && <div className="error">{errorMessage}</div>}
            {results.length > 0 && (
                <div className="results">
                    <h2>Results</h2>
                    <ul>
                        {results.map((result) => (
                            <li key={result.id}>{result.name}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}
