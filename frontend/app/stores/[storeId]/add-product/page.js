"use client";

import React, { useState, useEffect } from 'react';
import ProductPage from '@/components/ProductEditable';
import { useSearchParams, useRouter } from 'next/navigation';
import api from '@/lib/api';

export default function AddProduct() {
    const router = useRouter();
    const [errorMessage, setErrorMessage] = useState(null);
    const searchParams = useSearchParams();
    
    const store_id = searchParams.get('storeId');

    const handleSave = (name, description, price, weight, amount, selectedTags) => {
        const product_name = name;
        const tags = selectedTags;
        const data = {
            store_id,
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
                const response = await api.post(`/store/add_product`, data);
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
            <ProductPage onSave={handleSave} />
            {errorMessage && <div className="error">{errorMessage}</div>}
        </div>
    );
}