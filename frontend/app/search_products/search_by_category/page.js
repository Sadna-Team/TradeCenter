"use client";

import React, { useState } from "react";
import SearchForm from "@/components/CategorySearchBar";

export default function SearchByCategory() {

    const [results, setResults] = useState([]);
    const [errorMessage, setErrorMessage] = useState(null);

    const handleSearch = (selectedCategory, storeName) => {
        // Handle search logic here
        console.log('Category:', selectedCategory);
        console.log('Store Name:', storeName);
        setErrorMessage("Connect API to search for products by category");
        setResults([]);
    };

    // get categories from the server (category id -> category name)
    const categories = [
        {id: 1, name: 'category1'}, 
        {id: 2, name: 'category2'}, 
        {id: 3, name: 'category3'}, 
        {id: 4, name: 'category4'}, 
        {id: 5, name: 'category5'}
    ];

    return (
        <div>
            <SearchForm onSearch={handleSearch} categories={categories}/>
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