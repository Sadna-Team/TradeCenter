"use client";
import { useState, useEffect } from 'react';
import api from '@/lib/api';
import Link from 'next/link'; // Import the Link component

export default function SystemManagerPage() {
    const [categories, setCategories] = useState({});
    const [errorMessage, setErrorMessage] = useState('');
    const [rerender, setRerender] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const categoriesResponse = await api.get('/store/category_ids_to_names');
                setCategories(categoriesResponse.data.message);
            } catch (error) {
                console.error('Failed to fetch categories', error);
                setErrorMessage('Failed to fetch categories');
                return;
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const categoriesResponse = await api.get('/store/category_ids_to_names');
                setCategories(categoriesResponse.data.message);
            } catch (error) {
                console.error('Failed to fetch categories', error);
                setErrorMessage('Failed to fetch categories');
                return;
            }
        };

        fetchData();
    }, [rerender]);

    const handleRemoveCategory = (id) => {
        console.log(`Remove category with ID: ${id}`);
        const removeCategory = async () => {
            try {
                const request = await api.post('/store/remove_category', { category_id: id });
                if(request.status === 200) {
                    setRerender(!rerender);
                    return;
                }
                console.error('Failed to remove category', request.data.message);
            }
            catch (error) {
                console.error('Failed to remove category', error);
                setErrorMessage('Failed to remove category');
            }
        };
        removeCategory();
    };

    const handleAssignSubCategory = (id) => {
        const subCategoryId = window.prompt('Enter the sub-category ID:');
        if (!subCategoryId) {
            setErrorMessage('Please enter a sub-category ID');
            return;
        }
        console.log(`Assign sub-category with ID: ${subCategoryId} to category with ID: ${id}`);

        const assignSubCategory = async () => {
            try {
                const request = await api.post('/store/add_subcategory_to_category', { parent_category_id: id, subcategory_id: subCategoryId });
                if(request.status === 200) {
                    setRerender(!rerender);
                    return;
                }
                console.error('Failed to assign sub-category', request.data.message);
            }
            catch (error) {
                console.error('Failed to assign sub-category', error);
                setErrorMessage('Failed to assign sub-category');
            }
        };
        assignSubCategory();
    };

    const handleAddCategory = () => {
        const categoryName = window.prompt('Enter the category name:');
        if (!categoryName) {
            setErrorMessage('Please enter a category name');
            return;
        }
        console.log(`Add category with name: ${categoryName}`);

        const addCategory = async () => {
            try {
                const request = await api.post('/store/add_category', { category_name: categoryName });
                if(request.status === 200) {
                    setRerender(!rerender);
                    return;
                }
                console.error('Failed to add category', request.data.message);
                setErrorMessage('Failed to add category');
            }
            catch (error) {
                console.error('Failed to add category', error);
                setErrorMessage('Failed to add category');
            }
        };
        addCategory();
    }

    return (
        <div className="container">
            <h1 className="title">System Manager Page</h1>
            {errorMessage && <p className="error">{errorMessage}</p>}
            <div className="scrollable-div">
                <table className="category-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Parent ID</th>
                            <th>Sub Categories</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Object.entries(categories).map(([id, category]) => (
                            <tr key={id} className="category-item">
                                <td>{id}</td>
                                <td>
                                    <Link href={`/category/${id}`}>
                                        {category.category_name}
                                    </Link>
                                </td>
                                <td>{category.parent_category_id}</td>
                                <td>{category.sub_categories.join(', ')}</td>
                                <td>
                                    <div
                                        onClick={() => handleRemoveCategory(id)}
                                        className="action-button remove-button"
                                    >
                                        Remove
                                    </div>
                                    <div
                                        onClick={() => handleAssignSubCategory(id)}
                                        className="action-button assign-button"
                                    >
                                        Assign Sub-category
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <p>*Parent Id is -1 if category has no parent category</p>
            <div className='add-category'>
                <button onClick={handleAddCategory}>Add Category</button>
            </div>
            <style jsx>{`
                .container {
                    padding: 20px;
                }
                .title {
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }
                .error {
                    color: red;
                }
                .scrollable-div {
                    height: 200px;
                    overflow-y: scroll;
                    border: 1px solid #ccc;
                    padding: 10px;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }
                .category-table {
                    width: 100%;
                    border-collapse: collapse;
                }
                .category-table th, .category-table td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }
                .category-table th {
                    background-color: #f2f2f2;
                    font-weight: bold;
                }
                .category-item:nth-child(even) {
                    background-color: #f9f9f9;
                }
                .category-item a {
                    color: blue;
                    text-decoration: none;
                }
                .category-item a:hover {
                    text-decoration: underline;
                }
                .action-button {
                    display: inline-block;
                    padding: 5px 10px;
                    margin-right: 10px;
                    border-radius: 5px;
                    cursor: pointer;
                    color: white;
                    text-align: center;
                }
                .remove-button {
                    background-color: red;
                }
                .assign-button {
                    background-color: green;
                }
                .add-category {
                    display: flex;
                    justify-content: center;
                    margin-top: 20px;
                }
                .add-category button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }
                .add-category button:hover {
                    background-color: #45a049;
                }
            `}</style>
        </div>
    );
}
