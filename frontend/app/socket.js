import { io } from 'socket.io-client';

let socketInstance = null; // Global variable to store the socket instance

// close socket
export function closeSocket() {
  if (socketInstance) {
    socketInstance.disconnect();
    console.log('Socket disconnected:', socketInstance.connected);
  }
}

export function buildSocket(token) {
  if (socketInstance) {
    closeSocket();
  }
  socketInstance = io('http://localhost:5000', {
    autoConnect: false,  // Prevent auto connection to ensure headers can be set first
    extraHeaders: {
      Authorization: 'Bearer ' + token,  // Set the Authorization header with the token
    },
  });

  socketInstance.connect();
  socketInstance.emit('join');

  socketInstance.on('connected', () => {
    console.log('Socket connected:', socketInstance.connected);
    sessionStorage.setItem('socket', socketInstance);
    window.location.href = '/';
  });

  return socketInstance; // Return the socket instance
}

export function getSocket() {
  return socketInstance;
}
