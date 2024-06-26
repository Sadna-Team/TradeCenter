import React from 'react';
import Link from 'next/link';
import Logo from './Logo';
import Button from './Button';

const GuestNavBar = ({ onToggleSidebar }) => {
  return (
    <nav className="flex justify-between items-center p-4 bg-gray-800 text-white">
      <div className="flex items-center">
        <Link href="/">
          <Logo />
        </Link>
      </div>
      <div className="flex space-x-4 items-center">
        <Link href="/auth/login">
          <Button className="bg-blue-500 text-white py-2 px-4 rounded">
            Login
          </Button>
        </Link>
        <Link href="/auth/register">
          <Button className="bg-green-500 text-white py-2 px-4 rounded">
            Register
          </Button>
        </Link>
      </div>
    </nav>
  );
};

export default GuestNavBar;
