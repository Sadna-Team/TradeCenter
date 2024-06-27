// frontend/components/NavbarWrapper.jsx
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import GuestNavBar from './GuestNavBar';
import ClientNavBar from './ClientNavBar';

const NavbarWrapper = ({ onToggleSidebar }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [isHydrated, setIsHydrated] = useState(false);
  const router = useRouter();

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedIsConnected = sessionStorage.getItem('isConnected') === 'true';
      setIsConnected(storedIsConnected);
      setIsHydrated(true); // Mark hydration complete

      const handleRouteChange = () => {
        const storedIsConnected = sessionStorage.getItem('isConnected') === 'true';
        setIsConnected(storedIsConnected);
      };

      if (router.events?.on) {
        router.events.on('routeChangeComplete', handleRouteChange);
      }

      return () => {
        if (router.events?.off) {
          router.events.off('routeChangeComplete', handleRouteChange);
        }
      };
    }
  }, [router.events]);

  return isHydrated ? (
    isConnected ? (
        <ClientNavBar onToggleSidebar={onToggleSidebar} isConnected={isConnected} />
    ) : (
      <GuestNavBar />
    )
  ) : null;
};

export default NavbarWrapper;
