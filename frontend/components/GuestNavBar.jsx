import Link from 'next/link';
import Logo from './Logo';
import Button from './Button';

const GuestNavBar = () => {
  const handleLogout = () => {
    localStorage.setItem('isConnected', 'false');
    window.location.reload(); // Reload to update the navbar state
  };

  return (
    <nav className="flex justify-between items-center p-4 bg-gray-800 text-white">
      <div className="flex items-center">
        <Link href="/">
          <Logo />
        </Link>
      </div>
      <div className="flex space-x-4 items-center">
        <Link href="/cart">
          <button className="relative">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 8a1 1 0 011-1h12a1 1 0 011 1v11a2 2 0 01-2 2H7a2 2 0 01-2-2V8z"
              />
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 8V6a5 5 0 0110 0v2"
              />
            </svg>
          </button>
        </Link>
        <Link href="/search_products">
          <Button>
            Search Products
          </Button>
        </Link>
        <Link href="/auth/login">
          <Button className="bg-blue-500 text-white py-2 px-4 rounded">
            Login
          </Button>
        </Link>
        <Link href="/auth/register">
          <Button>
            Register
          </Button>
        </Link>
      </div>
    </nav>
  );
};

export default GuestNavBar;
