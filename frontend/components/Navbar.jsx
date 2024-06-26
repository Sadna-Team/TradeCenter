import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import GuestNavBar from './GuestNavBar';
import ClientNavBar from './ClientNavBar';

const NavbarWrapper = ({ onToggleSidebar }) => {
  const [isConnected, setIsConnected] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // Ensure this runs only on the client side
    if (typeof window !== 'undefined') {
      const storedIsConnected = localStorage.getItem('isConnected') === 'true';
      setIsConnected(storedIsConnected);

      const handleRouteChange = () => {
        const storedIsConnected = localStorage.getItem('isConnected') === 'true';
        setIsConnected(storedIsConnected);
      };

      if (router?.events?.on) {
        router.events.on('routeChangeComplete', handleRouteChange);
      }

      // Cleanup listener on unmount
      return () => {
        if (router?.events?.off) {
          router.events.off('routeChangeComplete', handleRouteChange);
        }
      };
    }
  }, [router?.events]);

  if (typeof window === 'undefined') {
    return null; // Prevent server-side rendering issues
  }

  return isConnected ? (
    <ClientNavBar onToggleSidebar={onToggleSidebar} />
  ) : (
    <GuestNavBar />
  );
};

export default NavbarWrapper;
