// socketContext.js

import React, { createContext, useContext, useState } from 'react';
import { io } from 'socket.io-client';

const SocketContext = createContext(null);

export const SocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);

  const buildSocket = (token) => {
    if (socket) {
      console.log('Socket already exists:', socket.connected);
      return socket;
    }
    const socketInstance = io('http://localhost:5000', {
      autoConnect: false,
      extraHeaders: {
        Authorization: 'Bearer ' + token,
      },
    });

    socketInstance.connect();
    socketInstance.emit('join');

    socketInstance.on('connected', () => {
      console.log('Socket connected:', socketInstance.connected);
      sessionStorage.setItem('isConnected', true);
      sessionStorage.setItem('listener', false);
        window.location.href = '/';
    });

    setSocket(socketInstance);
    return socketInstance;
  };

  const closeSocket = () => {
    if (socket) {
      socket.disconnect();
      console.log('Socket disconnected');
      setSocket(null); // Clear socket state on disconnection
    }
  };

  return (
    <SocketContext.Provider value={{ socket, buildSocket, closeSocket }}>
      {children}
    </SocketContext.Provider>
  );
};

export const useSocket = () => useContext(SocketContext);
