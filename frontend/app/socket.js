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

  // Provide socket and functions through context
  return (
    <socketContext.Provider value={{ socket, buildSocket, closeSocket }}>
      {children}
    </socketContext.Provider>
  );
};

export const useSocket = () => {
  return React.useContext(socketContext);
};
