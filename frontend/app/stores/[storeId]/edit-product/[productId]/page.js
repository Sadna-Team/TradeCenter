"use client";

import React, { useState } from 'react';
import ProductPage from '@/components/ProductEditable';
import { useSearchParams } from 'next/navigation';

export default function EditProduct() {
    const [errorMessage, setErrorMessage] = useState(null);
    const searchParams = useSearchParams();
    
    const productId = searchParams.get('productId');
    const storeId = searchParams.get('storeId');


    //get product data from the server
    const product = {
        'name': 'Product Name',
        'description': 'Product Description',
        'price': 100,
        'weight': 200,
        'amount': 10,
        'tags': ['tag1', 'tag2', 'tag3']
    };

    const handleSave = (name, description, price, weight, amount, selectedTags) => {
        const data = {
            'name': name,
            'description': description,
            'price': price,
            'weight': weight,
            'amount': amount,
            'tags': selectedTags
        };
        // Handle save logic here
        console.log(data);
        setErrorMessage("Connect API to save product");
    };

    return (
        <div>
            <ProductPage onSave={handleSave} existingData={product}/>
            {errorMessage && <div className="error">{errorMessage}</div>}
        </div>
    );
}