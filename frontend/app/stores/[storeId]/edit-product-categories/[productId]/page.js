"use client";

import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { useState, useEffect } from 'react';
import api from '/lib/api';

export default function EditProductCategoriesPage() {
    const searchParams = useSearchParams();
    const storeId = searchParams.get('storeId');
    const productId = searchParams.get('productId');
    const [errorMessage, setErrorMessage] = useState('');
    const [categories, setCategories] = useState({});
    const [allCategories, setAllCategories] = useState({});
    const [addedCategories, setAddedCategories] = useState([]);
    const [removedCategories, setRemovedCategories] = useState([]);
    const [successMessage, setSuccessMessage] = useState('');
    const [rerender, setRerender] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.post("/store/get_product_categories", { store_id: storeId, product_id: productId });
                if (response.status !== 200) {
                    console.error('Failed to fetch product categories:', response);
                    setErrorMessage('Failed to fetch product categories');
                    setSuccessMessage('');
                    return;
                }
                setCategories(response.data.message);
            } catch (error) {
                console.error('Failed to fetch product categories:', error);
                setErrorMessage('Failed to fetch product categories');
                setSuccessMessage('');
            }
            try {
                const allCategoriesResponse = await api.get("/store/category_ids_to_names");
                if (allCategoriesResponse.status !== 200) {
                    console.error('Failed to fetch all categories:', allCategoriesResponse);
                    setErrorMessage('Failed to fetch all categories');
                    setSuccessMessage('');
                    return;
                }
                setAllCategories(allCategoriesResponse.data.message);
            } catch (error) {
                console.error('Failed to fetch all categories:', error);
                setErrorMessage('Failed to fetch all categories');
                setSuccessMessage('');
            }
        };
        fetchData();
    }, [storeId, productId]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.post("/store/get_product_categories", { store_id: storeId, product_id: productId });
                if (response.status !== 200) {
                    console.error('Failed to fetch product categories:', response);
                    setErrorMessage('Failed to fetch product categories');
                    setSuccessMessage('');
                    return;
                }
                setCategories(response.data.message);
                setAddedCategories([]);
                setRemovedCategories([]);
            } catch (error) {
                console.error('Failed to fetch product categories:', error);
                setErrorMessage('Failed to fetch product categories');
                setSuccessMessage('');
            }
        };
        fetchData();
    }, [rerender]);


    const handleAddCategory = (categoryId) => {
        if (Object.keys(categories).includes(categoryId)) {
            setRemovedCategories((prev) => prev.filter((category) => category !== categoryId));
            return;
        }
        setAddedCategories((prev) => [...prev, categoryId]);
    }

    const handleRemoveCategory = (categoryId) => {
        if (Object.keys(categories).includes(categoryId)) {
            setRemovedCategories((prev) => [...prev, categoryId]);
            return;
        }
        setAddedCategories((prev) => prev.filter((category) => category !== categoryId));
    }

    const handleCheckboxChange = (categoryId) => {
        if (Object.keys(categories).includes(categoryId) && !removedCategories.includes(categoryId)) {
            handleRemoveCategory(categoryId);
            console.log('removing category:', categoryId);
            return;
        }
        else if (Object.keys(categories).includes(categoryId) && removedCategories.includes(categoryId)) {
            handleAddCategory(categoryId);
            console.log('adding category:', categoryId);
            return;
        }
        else if (!Object.keys(categories).includes(categoryId) && addedCategories.includes(categoryId)) {
            handleRemoveCategory(categoryId);
            console.log('removing category:', categoryId);
            return;
        }
        console.log('adding category:', categoryId);
        handleAddCategory(categoryId);
    };

    const onSubmit = async () => {
        try {
            console.log('categories:', categories);
            console.log('added categories:', addedCategories);
            console.log('removed categories:', removedCategories);
            for (const categoryId of addedCategories) {
                const response = await api.post("/store/assign_product_to_category", { store_id: storeId, product_id: productId, category_id: categoryId });
                if (response.status !== 200) {
                    console.error('Failed to add product category:', response);
                    setErrorMessage('Failed to add product category');
                    setSuccessMessage('');
                    return;
                }
            }
        }
        catch (error) {
            console.error('Failed to add product category:', error);
            setErrorMessage('Failed to add product category');
            setSuccessMessage('');
        }
        try {
            for (const categoryId of removedCategories) {
                const response = await api.post("/store/remove_product_from_category", { store_id: storeId, product_id: productId, category_id: categoryId });
                if (response.status !== 200) {
                    console.error('Failed to remove product category:', response);
                    setErrorMessage('Failed to remove product category');
                    setSuccessMessage('');
                    return;
                }
            }
            setSuccessMessage('Product categories updated successfully');
            setErrorMessage('');
            setRerender(!rerender);
        }
        catch (error) {
            console.error('Failed to remove product category:', error);
            setErrorMessage('Failed to remove product category');
            setSuccessMessage('');
        }

    };

    return (
        <div style={styles.container}>
            <h1 style={styles.header}>Edit Product Categories</h1>
            {errorMessage && <p style={styles.error}>{errorMessage}</p>}
            <div style={styles.infoContainer}>
                <p><strong>Store ID:</strong> {storeId}</p>
                <p><strong>Product ID:</strong> {productId}</p>
            </div>
            <div>
                <h2 style={styles.subHeader}>Categories:</h2>
                <ul style={styles.list}>
                    {Object.keys(allCategories).map((categoryId) => (
                        <li key={categoryId} style={styles.listItem}>
                            <label>
                                <input
                                    type="checkbox"
                                    checked={Object.keys(categories).includes(categoryId) && !removedCategories.includes(categoryId) || addedCategories.includes(categoryId)}
                                    onChange={() => handleCheckboxChange(categoryId)}
                                />
                                {allCategories[categoryId].category_name}
                            </label>
                        </li>
                    ))}
                </ul>
            </div>
            <div className="mt-8 flex justify-center">
                <div onClick={onSubmit} className="bg-green-600 text-white font-bold py-2 px-4 rounded cursor-pointer">Save</div>
           </div>
           {successMessage && <p style={styles.success}>{successMessage}</p>}
        </div>
    );
}

const styles = {
    container: {
        padding: '20px',
        maxWidth: '600px',
        margin: '0 auto',
        fontFamily: 'Arial, sans-serif',
    },
    header: {
        fontSize: '24px',
        marginBottom: '20px',
        textAlign: 'center',
    },
    subHeader: {
        fontSize: '20px',
        marginBottom: '10px',
    },
    error: {
        color: 'red',
        marginBottom: '10px',
    },
    infoContainer: {
        marginBottom: '20px',
        padding: '10px',
        border: '1px solid #ddd',
        borderRadius: '5px',
    },
    list: {
        listStyleType: 'none',
        padding: '0',
    },
    listItem: {
        background: '#f9f9f9',
        padding: '10px',
        borderBottom: '1px solid #ddd',
    },
};
