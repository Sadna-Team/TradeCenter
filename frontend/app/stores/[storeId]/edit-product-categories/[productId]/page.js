"use client";

import { useSearchParams, useRouter } from 'next/navigation';
import { useState, useEffect, use } from 'react';
import api from '/lib/api';


export default function EditProductCategoriesPage() {
    const searchParams = useSearchParams();
    const storeId = searchParams.get('storeId');
    const productId = searchParams.get('productId');
    const [errorMessage, setErrorMessage] = useState('');
    const [categories, setCategories] = useState({});

    useEffect(() => {
        console.log('Store ID:', storeId);
        console.log('Product ID:', productId);

        const fetchData = async () => {
            try {
                const response = await api.post("/store/get_product_categories", { store_id: storeId, product_id: productId });
                if(response.status !== 200) {
                    console.error('Failed to fetch product categories:', response);
                    setErrorMessage('Failed to fetch product categories');
                    return;
                }
                setCategories(response.data.message);   
            }
            catch(error) {
                console.error('Failed to fetch product categories:', error);
                setErrorMessage('Failed to fetch product categories');
            }
        };
        fetchData();
    }, []);

    return (
        <div>
            <h1>Edit product categories</h1>
            {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
            <p>Store ID: {storeId}</p>
            <p>Product ID: {productId}</p>
            {categories && (
                <div>
                    <h2>Categories:</h2>
                    <ul>
                        {Object.keys(categories).map((category) => (
                            <p>{categories[category].category_name}</p>
                        )
                        )}
                    </ul>
                </div>
            )}
        </div>
    );
}