import { io } from 'socket.io-client';

let socketInstance = null; // Global variable to store the socket instance

export function buildSocket(token) {
  if (!socketInstance) { // Create socket instance only if it doesn't exist
    socketInstance = io('http://localhost:5000', {
      autoConnect: false,  // Prevent auto connection to ensure headers can be set first
      extraHeaders: {
        Authorization: 'Bearer ' + token,  // Set the Authorization header with the token
      },
    });

    // Connect the socket instance when created
    socketInstance.connect();
    socketInstance.emit('join');

    // Listen for incoming messages and show notifications
    socketInstance.on('message', (data) => {
      console.log('Message received:', data);

      // Check if the browser supports notifications
      if ('Notification' in window) {
        console.log('Notification API supported.');

        // Request permission to show notifications if not already granted
        if (Notification.permission !== 'granted') {
          console.log('Requesting notification permission.');
          Notification.requestPermission();
        }

        // Create and show the notification
        console.log('Creating notification:', data);
        const notification = new Notification('New Message', {
          body: data,
        });
        // show the notification
        notification.onclick = () => {
          window.focus();
          notification.close();
        };
      } else {
        console.log('Notification API not supported.');
      }
    });
  }

  return socketInstance; // Return the socket instance
}

export default socketInstance; // Export the global socket instance
