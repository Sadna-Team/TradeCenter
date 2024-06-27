// app/socket.js

import React, { createContext, useState } from 'react';
import { io } from 'socket.io-client';

const socketContext = createContext(null);

export const SocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);

  const buildSocket = (token) => {
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
      window.location.href = '/';
    });

    setSocket(socketInstance);

    return socketInstance;
  };

  const closeSocket = () => {
    if (socket) {
      socket.disconnect();
      console.log('Socket disconnected');
    }
  };

  return (
    <socketContext.Provider value={{ socket, buildSocket, closeSocket }}>
      {children}
    </socketContext.Provider>
  );
};

export const useSocket = () => {
  const context = React.useContext(socketContext);
  if (!context) {
    throw new Error('useSocket must be used within a SocketProvider');
  }
  return context;
};
