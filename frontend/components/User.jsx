import React, { useState } from 'react';

const User = ({ user }) => {
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const permissions = [
    'View Products',
    'Manage Products',
    'View Orders',
    'Manage Orders',
    'View Customers',
    'Manage Customers',
    // Add more permissions as needed
  ];

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  return (
    <div className="user-card" style={{ backgroundColor: '#f0f0f0', border: '1px solid #ccc', padding: '16px', marginBottom: '16px', borderRadius: '8px' }}>
      <h2 style={{ fontSize: '1.5rem', marginBottom: '12px', fontWeight: 'bold' }}>{user.name}</h2>
      <div className="user-details" style={{ marginBottom: '12px' }}>
        <p><strong>Username:</strong> {user.username}</p>
        <p><strong>Birthday:</strong> {user.birthday}</p>
        <p><strong>Phone Number:</strong> {user.phone}</p>
        <p><strong>Suspended:</strong> {user.isSuspended ? 'Yes' : 'No'}</p>
      </div>
      <div className="permissions" style={{ marginBottom: '12px' }}>
        <p style={{ fontWeight: 'bold' }}>Employee's permissions:</p>
        <div style={{ position: 'relative' }}>
          <button onClick={toggleDropdown} style={{ padding: '8px 16px', border: '1px solid #ccc', borderRadius: '4px', backgroundColor: '#fff', cursor: 'pointer' }}>
            Select Permissions
          </button>
          {dropdownOpen && (
            <div style={{ position: 'absolute', top: '40px', left: '0', backgroundColor: '#fff', border: '1px solid #ccc', borderRadius: '4px', boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)', zIndex: 1000, width: '200px' }}>
              {permissions.map((permission, index) => (
                <div key={index} style={{ padding: '8px 16px', display: 'flex', alignItems: 'center' }}>
                  <input type="checkbox" id={`permission-${index}`} name={`permission-${index}`} />
                  <label htmlFor={`permission-${index}`} style={{ marginLeft: '8px' }}>{permission}</label>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      <button className="fire-employee-btn" style={{ backgroundColor: '#C70039', color: 'white', border: 'none', padding: '12px 20px', fontSize: '1rem', cursor: 'pointer', borderRadius: '8px' }}>
        Fire Employee
      </button>
    </div>
  );
};

export default User;
