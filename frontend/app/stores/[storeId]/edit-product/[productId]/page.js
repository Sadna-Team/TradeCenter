"use client";

import React, { useState, useEffect } from 'react';
import ProductPage from '@/components/ProductEditable';
import { useSearchParams, useRouter } from 'next/navigation';
import api from '@/lib/api';

export default function EditProduct() {
    const router = useRouter();
    const [errorMessage, setErrorMessage] = useState(null);
    const searchParams = useSearchParams();
    
    const product_id = searchParams.get('productId');
    const store_id = searchParams.get('storeId');

    const [product, setProduct] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            try {
                console.log("store_id", store_id);
                console.log("product_id", product_id);
                const response = await api.post(`/store/get_product_info`, {store_id, product_id});
                setProduct(response.data.message);
            } catch (error) {
                setErrorMessage("Failed to fetch product data");
            }
        };
        fetchData();
    }, []);
    

    const handleSave = (name, description, price, weight, amount, selectedTags) => {
        const product_name = name;
        const tags = selectedTags;
        const data = {
            store_id,
            product_id,
            product_name,
            description,
            price,
            weight,
            amount,
            tags
        };

        const saveData = async () => {
            try {
                console.log("data: ", data);
                const response = await api.post(`/store/edit_product`, data);
                if(response.status !== 200) {
                    setErrorMessage("Failed to save product data");
                    return;
                }
                setErrorMessage(null);
                // move to store window:
                router.push(`/stores/${store_id}?storeId=${store_id}`);
            } catch (error) {
                setErrorMessage("Failed to save product data");
            }
        };
        saveData();
    };

    return (
        <div>
            <ProductPage onSave={handleSave} existingData={product}/>
            {errorMessage && <div className="error">{errorMessage}</div>}
        </div>
    );
}