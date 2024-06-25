// src/socket.js
import { io } from 'socket.io-client';

const socket = io('http://localhost:5000', {
  autoConnect: false,  // Prevent auto connection to ensure headers can be set first
});

export default socket;
