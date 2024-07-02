"use client";
import { useState, useEffect } from 'react';
import Link from 'next/link';
import api from '@/lib/api';

export default function StoreManagementTable() {

    const [stores, setStores] = useState({});
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        const fetchStores = async () => {
            const response = await api.get('/store/get_all_stores');
            if (response.status !== 200) {
                console.log('Error fetching stores');
                setErrorMessage('Error fetching stores');
                return;
            }
            setStores(response.data.message);
            setErrorMessage('');
            console.log(response.data.message);
        };
        fetchStores();
    }, []);

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
                            <th>Address</th>
                            <th>Founder ID</th>
                            <th>Closed</th>
                            <th>Opening Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Object.entries(stores).map(([id, store]) => (
                            <tr key={id} className="category-item">
                                <td>{id}</td>
                                <td>{store.store_name}</td>
                                <td>
                                    <div>
                                        {store.address.address}, {store.address.city}, {store.address.country}, {store.address.zip}
                                    </div>
                                </td>
                                <td>{store.store_founder_id}</td>
                                <td>
                                    {store.is_active ? 'No' : 'Yes'}
                                </td>
                                <td>{store.found_date}</td>
                                <td>
                                    <Link href={{
                                        pathname: `/system-manager/store-management/store-purchase-history/${id}`,
                                        query: { storeId: id },
                                        }}>
                                        <div
                                            className="action-button product-history-button"
                                        >
                                            Purchase History
                                        </div>
                                    </Link>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
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
                    height: 400px;
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
                .product-history-button {
                    background-color: blue;
                }
            `}</style>
        </div>
    );
}