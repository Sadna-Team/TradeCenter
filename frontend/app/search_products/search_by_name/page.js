"use client";

import SearchForm from "@/components/NameSearchBar";
import React, { useState } from "react";

export default function SearchByName() {
    const [results, setResults] = useState([]);
    const [errorMessage, setErrorMessage] = useState(null);

    const handleSearch = (productName, storeName) => {
        // Handle search logic here
        console.log('Product Name:', productName);
        console.log('Store Name:', storeName);
        setErrorMessage("Connect API to search for products by name");
        setResults([]);
    };

    return (
        <div>
            <SearchForm onSearch={handleSearch} />
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
