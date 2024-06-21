import Link from 'next/link';
import Logo from './Logo';
import Button from './Button';

export default function Navbar() {
  return (
    <nav className="flex justify-between items-center p-4 bg-gray-800 text-white">
      <Link href="/">
        <Logo />
      </Link>
      <div className="flex space-x-4">
        <Link href="/cart">
          <Button className="bg-green-500 text-white py-2 px-4 rounded">
            Cart
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
}
