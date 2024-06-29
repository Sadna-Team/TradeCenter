"use client";

import "./globals.css";
import Header from '../components/Header';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { useState, useEffect } from 'react';
import api from '@/lib/api';

export default function RootLayout({ children }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [stores, setStores] = useState([]);
  
  // fetch stores from server
  useEffect(() => {
    async function fetchStores() {
      try {
        const response = await api.get('/store/my_stores');
        setStores(response.data.message);
      } catch (error) {
        console.error('Failed to fetch stores:', error);
      }
    }
    if(sessionStorage['isConnected']) fetchStores();
  }, []);
  
  const handleToggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };
  
  const handleCloseSidebar = () => {
    setIsSidebarOpen(false);
  };

  return (
    <html lang="en">
      <head>
        <title>Trade Center</title>
      </head>
      <body className="flex">
        <Sidebar isOpen={isSidebarOpen} onClose={handleCloseSidebar} hasStores={stores.length>0} />
        <div className="flex flex-col flex-grow">
          <header>
            <Navbar onToggleSidebar={handleToggleSidebar} />
          </header>
          <main className="p-4">{children}</main>
          <footer>© 2024 Ben Gurion University</footer>
        </div>
      </body>
    </html>
  );
}
