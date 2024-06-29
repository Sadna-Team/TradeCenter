// NotificationPopup.js
import React, { useEffect, useRef } from 'react';

const NotificationPopup = ({ notifications, onClose }) => {
  const popupRef = useRef(null);

  useEffect(() => {
    // Add event listener to handle clicks outside the popup
    const handleClickOutside = (event) => {
      if (popupRef.current && !popupRef.current.contains(event.target)) {
        onClose();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      // Clean up the event listener
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [onClose]);

  return (
    <div ref={popupRef} className="fixed top-4 left-4 w-64 bg-white text-black rounded-md shadow-lg z-10">
      <div className="p-4">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-lg font-semibold">Notifications</h2>
          <button onClick={onClose} className="text-red-500 font-semibold">X</button>
        </div>
        {notifications.length === 0 ? (
          <p>No new notifications</p>
        ) : (
          notifications.map((notification, index) => (
            <div key={index} className="mb-2 p-2 border-b">
              {notification.message}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default NotificationPopup;
