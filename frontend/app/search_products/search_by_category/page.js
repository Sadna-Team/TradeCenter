"use client";

import React, { useState, useEffect } from "react";
import SearchForm from "@/components/CategorySearchBar";
import api from '@/lib/api';


export default function SearchByCategory() {

    const [results, setResults] = useState([]);
    const [errorMessage, setErrorMessage] = useState(null);
    const [cateoryIdToName, setCategoryIdToName] = useState({});
    const [storeIdToName, setStoreIdToName] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            try {
                const categoriesResponse = await api.get('/store/category_ids_to_names');
                setCategoryIdToName(categoriesResponse.data.message);
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

    const handleSearch = async (selectedCategory, storeName) => {
        const store_id = Object.keys(storeIdToName).find((key) => storeIdToName[key] === storeName);
        const category_id = Object.keys(cateoryIdToName).find((key) => cateoryIdToName[key] === selectedCategory);
        
        console.log("category id: ", category_id);
        console.log("store id: ", store_id);
        
        const makeCall = async (data) => {
            const response = await api.post('/market/search_products_by_category', data);
            return response;
        };

        const response = (storeName ? await makeCall({ category_id, store_id }) : await makeCall({ category_id }));
        if (response.status === 200) {
            setResults(response.data.message);
            setErrorMessage(null);
        }
        else {
            console.error('Failed to fetch search results', response);
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
                    <strong className="block text-lg font-bold">Store Name: {storeIdToName[storeId]}</strong>
                    <div className="product-list mt-2">
                      {Object.keys(results[storeId]).map(productId => (
                        <div key={productId} className="product-item mb-2">
                          <div><strong>Name:</strong> {results[storeId][productId].name}</div>
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
            <SearchForm onSearch={handleSearch} categories={Object.values(cateoryIdToName)} stores={Object.values(storeIdToName)}/>
            {errorMessage && <div className="error">{errorMessage}</div>}
            {Object.keys(results).length > 0 && (
                <div>
                    {renderResults()}
                </div>
            )}
        </div>
      );
}