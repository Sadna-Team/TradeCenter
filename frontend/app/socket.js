import { io } from 'socket.io-client';

let socketInstance = null; // Global variable to store the socket instance

export function buildSocket(token, close) {
  if (socketInstance) { // Disconnect the socket instance if it exists
    socketInstance.disconnect();
    console.log('Socket disconnected:', socketInstance.connected);
  }
  
  if (close) return; // Return if the close flag is set

  // Create a new socket instance
  socketInstance = io('http://localhost:5000', {
    autoConnect: false,  // Prevent auto connection to ensure headers can be set first
    extraHeaders: {
      Authorization: 'Bearer ' + token,  // Set the Authorization header with the token
    },
  });

  // Connect the socket instance when created
  socketInstance.connect();
  socketInstance.emit('join');
  console.log('Socket connected:', socketInstance.connected);

  return socketInstance; // Return the socket instance
}

export function closeSocket() {
  buildSocket(0, true); // Rebuild the socket instance to disconnect
}

export const getSocket = () => {
  return socketInstance;
};