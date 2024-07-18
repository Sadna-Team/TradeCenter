"use client";

import SearchForm from "@/components/NameSearchBar";
import React, { useState, useEffect } from "react";
import Link from "next/link"; // Import Link from next/link
import api from '@/lib/api';

export default function SearchByName() {
    const [results, setResults] = useState({});
    const [errorMessage, setErrorMessage] = useState(null);
    const [storeIdToName, setstoreIdToName] = useState({});
    const [initialSearch, setInitialSearch] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const storeIdToNameResponse = await api.get('/store/store_ids_to_names');
                console.log(storeIdToNameResponse.data);
                setstoreIdToName(storeIdToNameResponse.data.message);
            } catch (error) {
                console.error('Failed to fetch store IDs to names', error);
                setErrorMessage('Failed to fetch store IDs to names');
            }
        };

        fetchData();
    }, []);

    const handleSearch = async (name, storeName) => {
        const store_id = Object.keys(storeIdToName).find((key) => storeIdToName[key] === storeName);

        console.log("product name: ", name);
        console.log("store id: ", store_id);
        
        try{
            const makeCall = async (data) => {
                const response = await api.post('/market/search_products_by_name', data);
                return response;
            };

            const response = (storeName ? await makeCall({ name, store_id }) : await makeCall({ name }));
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
        }
        catch (error) {
            console.error('Failed to fetch search results', error);
            setErrorMessage('Failed to fetch search results');
            setResults({});
        }
    };

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
                                        Store_Name: {storeIdToName[storeId].replace(/ /g, '_')}
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
            <SearchForm onSearch={handleSearch} stores={Object.values(storeIdToName)} />
            {errorMessage && <div className="error">{errorMessage}</div>}
            {Object.keys(results).length === 0 && !initialSearch && <div className="no-results">No results found</div>}
            {Object.keys(results).length > 0 && (
                <div>
                    {renderResults()}
                </div>
            )}
        </div>
    );
}
