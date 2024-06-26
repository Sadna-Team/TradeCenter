import React from 'react';

const ManagerProduct = ({ product }) => {
  // Static amount from props
  const amount = product.amount;

  // Function to handle editing fields (you can implement your specific edit logic here)
  const handleEditFields = () => {
    // Implement edit functionality
    console.log(`Editing fields for ${product.product_name}`);
  };

  // Function to handle deleting all (you can implement your specific delete logic here)
  const handleDeleteAll = () => {
    // Implement delete all functionality
    console.log(`Deleting all ${product.product_name}(s)`);
  };

  return (
    <div className="product-container" style={{ backgroundColor: '#f0f0f0', border: '1px solid #ccc', padding: '16px', marginBottom: '16px', borderRadius: '8px' }}>
      <h2 style={{ fontSize: '1.5rem', marginBottom: '12px' }}>{product.product_name}</h2>
      <div className="product-details" style={{ marginBottom: '12px' }}>
        <p><strong>Weight:</strong> {product.weight}</p>
        <p><strong>Description:</strong> {product.description}</p>
        <p><strong>Price:</strong> ${product.price}</p>
        <p><strong>Rating:</strong> {product.rating}/5</p> 
        <p><strong>Amount:</strong> {product.amount}</p>
      </div>
    
      <div className="button-container" style={{ display: 'flex', justifyContent: 'space-between' }}>
        <button className="edit-fields-btn" style={{ backgroundColor: '#3498db', color: 'white', border: 'none', padding: '10px 20px', fontSize: '1rem', cursor: 'pointer' }} onClick={handleEditFields}>Edit Fields</button>
        <button className="delete-all-btn" style={{ backgroundColor: '#e74c3c', color: 'white', border: 'none', padding: '10px 20px', fontSize: '1rem', cursor: 'pointer' }} onClick={handleDeleteAll}>Delete All</button>
      </div>
      <h3> The buttons don't work</h3>
    </div>
  );
};

export default ManagerProduct;
