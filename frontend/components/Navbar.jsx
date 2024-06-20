import Link from 'next/link';
import Logo from './Logo';
import Button from './Button';

export default function Navbar() {
  return (
    <nav className="flex justify-between items-center p-4 bg-gray-800 text-white">
      <Link href="/">
        <Logo />
      </Link>
      <Link href="/auth/login">
        <Button className="bg-blue-500 text-white py-2 px-4 rounded">
            Login
        </Button>
      </Link>
    </nav>
  );
}
