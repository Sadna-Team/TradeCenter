"use client";

import api from '@/lib/api';
import React, { useState, useEffect } from 'react';
import Popup from '@/components/Popup';
import DatePopup from '@/components/DatePopup';
import Link from 'next/link';
import Button from '@/components/Button';

export default function MembersManagementPage() {
    const [users, setUsers] = useState([]);
    const [errorMessage, setErrorMessage] = useState(null);
    const [rerender, setRerender] = useState(false);
    const [datePopup, setDatePopup] = useState(null);
    const [selectedUserId, setSelectedUserId] = useState(null);

    const fetchUsers = async () => {
        try {
            const usersResponse = await api.get('/user/get_all_members');
            setUsers(usersResponse.data.users);
        } catch (error) {
            console.error('Failed to fetch users', error);
            setErrorMessage('Failed to fetch users');
        }
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    const getAge = (user) => {
        const today = new Date();
        const year = user.year;
        const month = user.month - 1;
        const day = user.day;
        const birthDate = new Date(year, month, day);

        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDifference = today.getMonth() - birthDate.getMonth();
        const dayDifference = today.getDate() - birthDate.getDate();

        if (monthDifference < 0 || (monthDifference === 0 && dayDifference < 0)) {
            age--;
        }

        return age;
    };

    useEffect(() => {
        fetchUsers();
    }, [rerender]);

    const is_system_manager = async (user) => {
        try {
            const response = await api.post('/user/check_system_manager', { admin_id: user.user_id });
            console.log(user.user_id + ": " + response.data.is_system_manager);
            return response.data.is_system_manager;
        } catch (error) {
            console.error('Failed to check if user is system manager', error);
            setErrorMessage('Failed to check if user is system manager');
            return false;
        }
    };

    const handleSuspend = async (id, date) => {
        try {
            const response = date
                ? await api.post('/user/suspend_user', { suspended_user_id: id, date: date })
                : await api.post('/user/suspend_user', { suspended_user_id: id });

            if (response.status === 200) {
                setRerender(!rerender);
            } else {
                console.error('Failed to suspend user', response.data.message);
                setErrorMessage('Failed to suspend user');
            }
        } catch (error) {
            console.error('Failed to suspend user', error);
            setErrorMessage('Failed to suspend user');
        }
    };

    const handleUnsuspend = async (id) => {
        try {
            const response = await api.post('/user/unsuspend_user', { suspended_user_id: id });
            if (response.status === 200) {
                setRerender(!rerender);
            } else {
                console.error('Failed to unsuspend user', response.data.message);
                setErrorMessage('Failed to unsuspend user');
            }
        } catch (error) {
            console.error('Failed to unsuspend user', error);
            setErrorMessage('Failed to unsuspend user');
        }
    };

    const handleDatePopupClose = (date) => {
        setDatePopup(null);
        if (selectedUserId) {
            handleSuspend(selectedUserId, date);
            setSelectedUserId(null);
        }
    };

    const handleDatePopupCancel = () => {
        setDatePopup(null);
        setSelectedUserId(null);
    };

    return (
        <div>
            <div>
                <h1>Manage Members</h1>
            </div>
            {errorMessage && <Popup initialMessage={errorMessage} is_closable={true} onClose={() => setErrorMessage(null)} onCancel={() => setDatePopup(null)} />}
            <div className="scrollable-div">
                <table className="users-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Age</th>
                            <th>Phone</th>
                            <th>Suspended</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(user => (
                            <tr key={user.user_id} className="users">
                                <td>{user.user_id}</td>
                                <td>{user.username}</td>
                                <td>{user.email}</td>
                                <td>{getAge(user)}</td>
                                <td>{user.phone}</td>
                                <td>{user.is_suspended ? "yes" : "no"}</td>
                                <td>
                                    <div className="actions-container">
                                        {!user.is_system_manager ?  
                                            (!user.is_suspended ? 
                                                (<div
                                                    onClick={() => {
                                                        setSelectedUserId(user.user_id);
                                                        setDatePopup("Do you want to enter a date?");
                                                    }}
                                                    className="action-button suspend-button"
                                                >
                                                    Suspend
                                                </div>) : (
                                                <div
                                                    onClick={() => handleUnsuspend(user.user_id)}
                                                    className="action-button unsuspend-button"
                                                >
                                                    Unsuspend
                                                </div>)
                                            )
                                            : (
                                                <p className="system-manager-text">System manager cannot be suspended</p>
                                            )
                                        }
                                        <Link href={{
                                                pathname: `/system-manager/manage-users/purchase-history/${user.user_id}`,
                                                query: { userId: user.user_id },
                                            }}>
                                            <Button className="purchase-history-button">View Purchase History</Button>
                                        </Link>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            {datePopup && <DatePopup initialMessage={datePopup} onClose={handleDatePopupClose} onCancel={handleDatePopupCancel}/>}
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
                .users-table {
                    width: 100%;
                    border-collapse: collapse;
                }
                .users-table th, .users-table td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }
                .users-table th {
                    background-color: #f2f2f2;
                    font-weight: bold;
                }
                .users:nth-child(even) {
                    background-color: #f9f9f9;
                }
                .users a {
                    color: blue;
                    text-decoration: none;
                }
                .users a:hover {
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
                .suspend-button {
                    background-color: red;
                }
                .unsuspend-button {
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
                .actions-container {
                    display: flex;
                    align-items: center;
                }
                .purchase-history-button {
                    margin-left: 10px;
                }
                .system-manager-text {
                    color: grey;
                    margin-right: 10px;
                    max-width: 80px;
                    white-space: normal;
                    word-break: default;    
                    font-size: 14px;
                    font-weight: bold;
                }
            `}</style>
        </div>
    );
}
