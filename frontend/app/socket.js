// SocketSingleton.js
import { useRouter } from 'next/navigation';
import { io } from 'socket.io-client';

class SocketSingleton {
    static instance = null;
  constructor(token) {
    if (!SocketSingleton.instance) {
      this.socket = io('http://localhost:5000', {
        autoConnect: false,
        extraHeaders: {
          Authorization: 'Bearer ' + token,
        },
      });

      this.socket.connect();
      this.socket.emit('join');

      this.socket.on('connected', () => {
        if (sessionStorage.getItem('isConnected') !== 'true') {
          console.log('Socket connected:', this.socket.connected);
          sessionStorage.setItem('isConnected', true);
          // sessionStorage.setItem('listener', false);
        }
      });


      this.socket.on('disconnect', (reason) => {
        console.log('Socket disconnected:', reason);
        sessionStorage.setItem('isConnected', false);
        sessionStorage.setItem('listener', false);
        if ((reason === 'io server disconnect' || reason === 'io client disconnect') && sessionStorage.getItem('isConnected') === 'true') {
          // Reconnect logic
          setTimeout(() => {
            this.socket.connect();
          }, 1000); // Retry connection after 1 second
      }
});

      SocketSingleton.instance = this;
    }

    return SocketSingleton.instance;
  }

  getInstance() {
    return this.socket;
  }

  static closeSocket() {
    if (SocketSingleton.instance) {
      SocketSingleton.instance.socket.disconnect();
      console.log('Socket disconnected');
      SocketSingleton.instance = null;
    }
  }
}

export default SocketSingleton;
