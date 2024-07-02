"use client";

import { useState, useEffect } from 'react';
import api from '/lib/api';
import config from '@/postcss.config.mjs';

export default function EditProductCategoriesPage() {
    const [payments, setPayments] = useState([]);
    const [allPayments, setAllPayments] = useState([]);
    const [addedPayments, setAddedPayments] = useState([]);
    const [removedPayments, setRemovedPayments] = useState([]);
    const [successPaymentsMessage, setSuccessPaymentsMessage] = useState('');
    const [errorPaymentMessage, setErrorPaymentMessage] = useState('');
    const [rerenderPayment, setRerenderPayment] = useState(false);
    const [supplies, setSupplies] = useState([]);
    const [allSupplies, setAllSupplies] = useState([]);
    const [addedSupplies, setAddedSupplies] = useState([]);
    const [removedSupplies, setRemovedSupplies] = useState([]);
    const [successSuppliesMessage, setSuccessSuppliesMessage] = useState('');
    const [errorSuppliesMessage, setErrorSuppliesMessage] = useState('');
    const [rerenderSupplies, setRerenderSupplies] = useState(false);

    useEffect(() => {
        const fetchPayment = async () => {
            try {
                const allPaymentsResponse = await api.get("/third_party/payment/get_all");
                if (allPaymentsResponse.status !== 200) {
                    console.error('Failed to fetch all payments:', allPaymentsResponse);
                    setErrorPaymentMessage('Failed to fetch all payments');
                    setSuccessPaymentsMessage('');
                    return;
                }
                setAllPayments(allPaymentsResponse.data.message);
            } catch (error) {
                console.error('Failed to fetch all payments:', error);
                setErrorPaymentMessage('Failed to fetch all payments');
                setSuccessPaymentsMessage('');
            }
            try {
                const activePaymentsResponse = await api.get("/third_party/payment/get_all_active");
                if (activePaymentsResponse.status !== 200) {
                    console.error('Failed to fetch active payments:', activePaymentsResponse);
                    setErrorPaymentMessage('Failed to fetch active payments');
                    setSuccessPaymentsMessage('');
                    return;
                }
                setPayments(activePaymentsResponse.data.message);
            } catch (error) {
                console.error('Failed to fetch active payments:', error);
                setErrorPaymentMessage('Failed to fetch active payments');
                setSuccessPaymentsMessage('');
            }
        };

        const fetchSupply = async () => {
            try {
                const allSuppliesResponse = await api.get("/third_party/delivery/get_all");
                if (allSuppliesResponse.status !== 200) {
                    console.error('Failed to fetch all supplies:', allSuppliesResponse);
                    setErrorSuppliesMessage('Failed to fetch all supplies');
                    setSuccessSuppliesMessage('');
                    return;
                }
                setAllSupplies(allSuppliesResponse.data.message);
            } catch (error) {
                console.error('Failed to fetch all supplies:', error);
                setErrorSuppliesMessage('Failed to fetch all supplies');
                setSuccessSuppliesMessage('');
            }
            try {
                const activeSuppliesResponse = await api.get("/third_party/delivery/get_all_active");
                if (activeSuppliesResponse.status !== 200) {
                    console.error('Failed to fetch active supplies:', activeSuppliesResponse);
                    setErrorSuppliesMessage('Failed to fetch active supplies');
                    setSuccessSuppliesMessage('');
                    return;
                }
                setSupplies(activeSuppliesResponse.data.message);
            } catch (error) {
                console.error('Failed to fetch active supplies:', error);
                setErrorSuppliesMessage('Failed to fetch active supplies');
                setSuccessSuppliesMessage('');
            }
        };

        fetchPayment();
        fetchSupply();
    }, []);

    useEffect (() => {
        const fetchActivePayments = async () => {
            try {
                const activePaymentsResponse = await api.get("/third_party/payment/get_all_active");
                if (activePaymentsResponse.status !== 200) {
                    console.error('Failed to fetch active payments:', activePaymentsResponse);
                    setErrorPaymentMessage('Failed to fetch active payments');
                    setSuccessPaymentsMessage('');
                    return;
                }
                setPayments(activePaymentsResponse.data.message);
                setAddedPayments([]);
                setRemovedPayments([]);
            } catch (error) {
                console.error('Failed to fetch active payments:', error);
                setErrorPaymentMessage('Failed to fetch active payments');
                setSuccessPaymentsMessage('');
            }
        }
        fetchActivePayments();
    }, [rerenderPayment]);

    useEffect (() => {
        const fetchActiveSupplies = async () => {
            try {
                const activeSuppliesResponse = await api.get("/third_party/delivery/get_all_active");
                if (activeSuppliesResponse.status !== 200) {
                    console.error('Failed to fetch active supplies:', activeSuppliesResponse);
                    setErrorSuppliesMessage('Failed to fetch active supplies');
                    setSuccessSuppliesMessage('');
                    return;
                }
                setSupplies(activeSuppliesResponse.data.message);
                setAddedSupplies([]);
                setRemovedSupplies([]);
            } catch (error) {
                console.error('Failed to fetch active supplies:', error);
                setErrorSuppliesMessage('Failed to fetch active supplies');
                setSuccessSuppliesMessage('');
            }
        }
        fetchActiveSupplies();
    }, [rerenderSupplies]);

    const handleAddPayment = (method) => {
        if (payments.includes(method)) {
            setRemovedPayments((prev) => prev.filter((name) => name !== method));
            return;
        }
        setAddedPayments((prev) => [...prev, method]);
    }

    const handleRemovePayment = (method) => {
        if (payments.includes(method)) {
            setRemovedPayments((prev) => [...prev, method]);
            return;
        }
        setAddedPayments((prev) => prev.filter((name) => name !== method));
    }

    const handlePaymentCheckboxChange = (method) => {
        if (payments.includes(method) && !removedPayments.includes(method)) {
            handleRemovePayment(method);
            console.log('removing payment method:', method);
            return;
        }
        else if (payments.includes(method) && removedPayments.includes(method)) {
            handleAddPayment(method);
            console.log('adding payment method:', method);
            return;
        }
        else if (!payments.includes(method) && addedPayments.includes(method)) {
            handleRemovePayment(method);
            console.log('removing payment method:', method);
            return;
        }
        console.log('adding payment method:', method);
        handleAddPayment(method);
    };

    const handleAddSupply = (method) => {
        if (supplies.includes(method)) {
            setRemovedSupplies((prev) => prev.filter((name) => name !== method));
            return;
        }
        setAddedSupplies((prev) => [...prev, method]);
    }

    const handleRemoveSupply = (method) => {
        if (supplies.includes(method)) {
            setRemovedSupplies((prev) => [...prev, method]);
            return;
        }
        setAddedSupplies((prev) => prev.filter((name) => name !== method));
    }

    const handleSupplyCheckboxChange = (method) => {
        if (supplies.includes(method) && !removedSupplies.includes(method)) {
            handleRemoveSupply(method);
            console.log('removing supply method:', method);
            return;
        }
        else if (supplies.includes(method) && removedSupplies.includes(method)) {
            handleAddSupply(method);
            console.log('adding supply method:', method);
            return;
        }
        else if (!supplies.includes(method) && addedSupplies.includes(method)) {
            handleRemoveSupply(method);
            console.log('removing supply method:', method);
            return;
        }
        console.log('adding supply method:', method);
        handleAddSupply(method);
    };

    const onPaymentSubmit = async () => {
        try {
            for (const method of addedPayments) {
                const response = await api.post("/third_party/payment/add", { method_name: method, config: {} });
                if (response.status !== 200) {
                    console.error('Failed to add payment method:', response);
                    setErrorPaymentMessage('Failed to add payment method');
                    setSuccessPaymentsMessage('');
                    return;
                }
            }
        }
        catch (error) {
            console.error('Failed to add payment method:', error);
            setErrorPaymentMessage('Failed to add payment method');
            setSuccessPaymentsMessage('');
        }
        try {
            for (const method of removedPayments) {
                const response = await api.post("/third_party/payment/delete", { method_name: method });
                if (response.status !== 200) {
                    console.error('Failed to remove payment method:', response);
                    setErrorPaymentMessage('Failed to remove payment method');
                    setSuccessPaymentsMessage('');
                    return;
                }
            }
            setSuccessPaymentsMessage('Payment methods updated successfully');
            setErrorPaymentMessage('');
            setRerenderPayment(!rerenderPayment);
            
        }
        catch (error) {
            console.error('Failed to remove payment method:', error);
            setErrorPaymentMessage('Failed to remove payment method');
            setSuccessPaymentsMessage('');
        }
    };
    
    const onSupplySubmit = async () => {
        try {
            for (const method of addedSupplies) {
                const response = await api.post("/third_party/delivery/add", { method_name: method, config: {} });
                if (response.status !== 200) {
                    console.error('Failed to add supply method:', response);
                    setErrorSuppliesMessage('Failed to add supply method');
                    setSuccessSuppliesMessage('');
                    return;
                }
            }
        }
        catch (error) {
            console.error('Failed to add supply method:', error);
            setErrorSuppliesMessage('Failed to add supply method');
            setSuccessSuppliesMessage('');
        }
        try {
            for (const method of removedSupplies) {
                const response = await api.post("/third_party/delivery/delete", { method_name: method });
                if (response.status !== 200) {
                    console.error('Failed to remove supply method:', response);
                    setErrorSuppliesMessage('Failed to remove supply method');
                    setSuccessSuppliesMessage('');
                    return;
                }
            }
            setSuccessSuppliesMessage('Supply methods updated successfully');
            setErrorSuppliesMessage('');
            setRerenderSupplies(!rerenderSupplies);
        }
        catch (error) {
            console.error('Failed to remove supply method:', error);
            setErrorSuppliesMessage('Failed to remove supply method');
            setSuccessSuppliesMessage('');
        }
    }

    return (
        <div>
            <div style={styles.container}>
                <h1 style={styles.header}>Edit Payment Methods</h1>
                {errorPaymentMessage && <p style={styles.error}>{errorPaymentMessage}</p>}
                <div>
                    <h2 style={styles.subHeader}>Payment Methods:</h2>
                    <ul style={styles.list}>
                        {allPayments.map((method) => (
                            <li key={method} style={styles.listItem}>
                                <label>
                                    <input
                                        type="checkbox"
                                        checked={payments.includes(method) && !removedPayments.includes(method) || addedPayments.includes(method)}
                                        onChange={() => handlePaymentCheckboxChange(method)}
                                    />
                                    {method}
                                </label>
                            </li>
                        ))}
                    </ul>
                </div>
                <div className="mt-8 flex justify-center">
                    <div onClick={onPaymentSubmit} className="bg-green-600 text-white font-bold py-2 px-4 rounded cursor-pointer">Save</div>
            </div>
            {successPaymentsMessage && <p style={styles.success}>{successPaymentsMessage}</p>}
            </div>
            <div style={styles.container}>
                <h1 style={styles.header}>Edit Supply Methods</h1>
                {errorSuppliesMessage && <p style={styles.error}>{errorSuppliesMessage}</p>}
                <div>
                    <h2 style={styles.subHeader}>Supply Methods:</h2>
                    <ul style={styles.list}>
                        {allSupplies.map((method) => (
                            <li key={method} style={styles.listItem}>
                                <label>
                                    <input
                                        type="checkbox"
                                        checked={supplies.includes(method) && !removedSupplies.includes(method) || addedSupplies.includes(method)}
                                        onChange={() => handleSupplyCheckboxChange(method)}
                                    />
                                    {method}
                                </label>
                            </li>
                        ))}
                    </ul>
                </div>
                <div className="mt-8 flex justify-center">
                    <div onClick={onSupplySubmit} className="bg-green-600 text-white font-bold py-2 px-4 rounded cursor-pointer">Save</div>
                </div>
                {successSuppliesMessage && <p style={styles.success}>{successSuppliesMessage}</p>}
            </div>
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
