"use client";

import "./globals.css";
import Header from '../components/Header';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { useState, useEffect } from 'react';
import api from '@/lib/api';
import { SocketProvider } from './socketContext';

export default function RootLayout({ children }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [stores, setStores] = useState({});
  const [isSystemManager, setIsSystemManager] = useState(false);
  
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

    async function isSystemManager() {
      try {
        const response = await api.get('/user/is_system_manager');
        console.log('isSystemManager response:', response);
        if(response.status !== 200) {
          console.error('Failed to check if user is system manager:', response.data.message);
          return;
        }
        const data = response.data.is_system_manager;
        if(data) {
          setIsSystemManager(true);
        }
      } catch (error) {
        console.error('Failed to check if user is system manager:', error);
      }
    }
    if(sessionStorage['isConnected']) {
      fetchStores();
      isSystemManager();
    }
  }, []);
  
  const handleToggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };
  
  const handleCloseSidebar = () => {
    setIsSidebarOpen(false);
  };

  return (

    <SocketProvider>
      <html lang="en">
        <head>
          <title>Trade Center</title>
        </head>
        <body className="flex">
          <Sidebar isOpen={isSidebarOpen} onClose={handleCloseSidebar} hasStores={Object.keys(stores).length > 0} isSystemManager={isSystemManager}/>
          <div className="flex flex-col flex-grow">
            <header>
              <Navbar onToggleSidebar={handleToggleSidebar} />
            </header>
            <main className="p-4">{children}</main>
            <footer>© 2024 Ben Gurion University</footer>
          </div>
        </body>
      </html>
    </SocketProvider>
  );
}
