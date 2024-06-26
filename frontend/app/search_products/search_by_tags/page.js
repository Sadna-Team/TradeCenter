"use client";

import React, { useState } from 'react';
import SearchForm from '@/components/TagSearchBar';

export default function SearchByTags() {
    
    // get store names from the server
    const storeNames = [
        {id: 1, name: 'Store 1'},
        {id: 2, name: 'Store 2'},
        {id: 3, name: 'Store 3'},
        {id: 4, name: 'Store 4'},
        {id: 5, name: 'Store 5'},
    ];
    // get tags from the server
    const tags = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5'];

    const [results, setResults] = useState([]);
    const [errorMessage, setErrorMessage] = useState(null);

    const handleSearch = (selectedTags, storeName) => {
        // Handle search logic here
        console.log('Selected Tags:', selectedTags);
        console.log('Store Name:', storeName);
        setErrorMessage("Connect API to search for products by tags");
        setResults([]);
    };
  
    return (
        <div>
            <SearchForm onSearch={handleSearch} tags={tags} stores={storeNames}/>
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
