"use client";

import React, { useState, useEffect } from 'react';
import SearchForm from '@/components/TagSearchBar';
import Link from 'next/link';
import api from '@/lib/api';

export default function SearchByTags() {
    const [results, setResults] = useState({});
    const [errorMessage, setErrorMessage] = useState(null);
    const [allTags, setAllTags] = useState([]);
    const [storeIdToName, setStoreIdToName] = useState({});
    const [initialSearch, setInitialSearch] = useState(true);

    const validate = (tags, storeName) => {
        return tags !== null && tags.length !== undefined && tags.length > 0;
    };

    const handleSearch = async (tags, storeName) => {
        if (!validate(tags, storeName)) {
            setErrorMessage('Please select at least one tag');
            return;
        }
        const store_id = Object.keys(storeIdToName).find((key) => storeIdToName[key] === storeName);

        console.log("tags: ", tags);
        console.log("store id: ", store_id);

        const makeCall = async (data) => {
            const response = await api.post('/market/search_products_by_tags', data);
            return response;
        };

        const response = (storeName ? await makeCall({ tags, store_id }) : await makeCall({ tags }));
        if (response.status === 200) {
            setResults(response.data.message);
            if (initialSearch) {
                setInitialSearch(false);
            }
            setErrorMessage(null);
        } else {
            console.error('Failed to fetch search results', response);
            setErrorMessage('Failed to fetch search results');
            setResults({});
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

    const renderResults = () => {
        console.log("results: ", results);

        const storeContainerStyle = {
            marginBottom: '20px',
            padding: '10px',
            border: '1px solid #ccc',
            borderRadius: '5px',
            backgroundColor: '#f9f9f9',
        };

        const productItemStyle = {
            marginBottom: '10px',
            padding: '5px',
            border: '1px solid #eee',
            borderRadius: '3px',
            backgroundColor: '#fff',
        };

        return (
            <div className="flex items-start justify-center bg-gray-100">
                <div className="bg-white p-6 rounded shadow-md w-full max-w-md mt-4">
                    <h1 className="text-2xl font-bold mb-4 text-center">Search Results</h1>
                    <div className="store-products">
                        {Object.keys(results).map(storeId => (
                            <div key={storeId} className="store-container mb-4">
                                <Link href={`/e-store/${storeId}`} passHref>
                                    <div className="block text-lg font-bold cursor-pointer">
                                        Store Name: {storeIdToName[storeId]}
                                    </div>
                                </Link>
                                <div className="product-list mt-2">
                                    {Object.keys(results[storeId]).map(productId => (
                                        <div key={productId} className="product-item mb-2">
                                            <Link href={`/e-store/${storeId}/${productId}`} passHref>
                                                <div className="cursor-pointer">
                                                    <strong>Name:</strong> {results[storeId][productId].name.replace(/ /g, '_')}
                                                </div>
                                            </Link>
                                            <div><strong>Description:</strong> {results[storeId][productId].description}</div>
                                            <div><strong>Price:</strong> {results[storeId][productId].price}</div>
                                            <div><strong>Amount:</strong> {results[storeId][productId].amount}</div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        );
    };

    return (
        <div>
            <SearchForm onSearch={handleSearch} tags={allTags} stores={Object.values(storeIdToName)} />
            {errorMessage && <span className="text-red-500 text-sm">{errorMessage}</span>}
            {Object.keys(storeIdToName).length === 0 && <span>Loading...</span>}
            {Object.keys(results).length === 0 && !initialSearch && <span>No Search Results Found</span>}
            {Object.keys(results).length > 0 && (
                <div>
                    {renderResults()}
                </div>
            )}
        </div>
    );
}
