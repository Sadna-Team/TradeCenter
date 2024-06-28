"use client";

import React, { useState, useEffect } from 'react';
import SearchForm from '@/components/TagSearchBar';
import api from '@/lib/api';

export default function SearchByTags() {
    //get tags from the server
    const [results, setResults] = useState([]);
    const [errorMessage, setErrorMessage] = useState(null);
    const [allTags, setAllTags] = useState(null);
    const [storeIdToName, setStoreIdToName] = useState({});

    const handleSearch = (tags, storeName) => {
        const store_id = Object.keys(storeIdToName).find((key) => storeIdToName[key] === storeName);       
        
        const makeCall = async (data) => {
            const response = await api.get('/market/search_products_by_tags', data);
            return response;
        };

        const response = storeName ? makeCall({ tags, store_id }) : makeCall({ tags });
        if (response.status === 200) {
            setResults(response.data.message);
            setErrorMessage(null);
        }
        else {
            setResults([]);
            setErrorMessage('Failed to fetch search results');
        }
    };
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                const tagsResponse = await api.get('/store/tags');
                setAllTags(tagsResponse.data.message);
            } catch (error) {
                console.error('Failed to fetch tags', error);
                setErrorMessage('Failed to fetch tags');
                return;
            }
    
            try {
                const storeIdToNameResponse = await api.get('/store/store_ids_to_names');
                console.log(storeIdToNameResponse.data);
                setStoreIdToName(storeIdToNameResponse.data.message);
            } catch (error) {
                console.error('Failed to fetch store IDs to names', error);
                setErrorMessage('Failed to fetch store IDs to names');
            }
        };
    
        fetchData();
    }, []);
    

    return (
        <div>
            <SearchForm onSearch={handleSearch} tags={allTags} stores={Object.values(storeIdToName)}/>
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
