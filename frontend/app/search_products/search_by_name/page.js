"use client";

import SearchForm from "@/components/NameSearchBar";

import React, { useState } from "react";

export default function SearchByName() {

    const [results, setResults] = useState([]);
    const [error, setError] = useState(null);

    const handleSearch = (productName, storeName) => {
        // Handle search logic here
        console.log('Product Name:', productName);
        console.log('Store Name:', storeName);
        setError("Connect API to search for products by name");
    };

    return (
        <>
            <SearchForm onSearch={ handleSearch }/>
            {error && <div className="error">{error}</div>}
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
        </>
      );
}