"use client";

import "./globals.css";
import Header from '../components/Header';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { useState } from 'react';

export default function RootLayout({ children }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

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
        <Sidebar isOpen={isSidebarOpen} onClose={handleCloseSidebar} />
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
