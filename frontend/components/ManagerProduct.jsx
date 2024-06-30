import React, { useState } from 'react';
import Link from 'next/link';

const ManagerProduct = ({ product, store_id, deleteProduct }) => {

  const [showConfirm, setShowConfirm] = useState(false);

  const cancelDelete = () => {
    setShowConfirm(false);
  };

  const confirmDelete = () => {
    setShowConfirm(true);
  };

  const handleDelete = () => {
    console.log('Deleting product:', product.product_id);
    deleteProduct(store_id, product.product_id);
  };

  return (
    <div className="product-container" style={{ backgroundColor: '#f0f0f0', border: '1px solid #ccc', padding: '16px', marginBottom: '16px', borderRadius: '8px' }}>
      <h2 style={{ fontSize: '1.5rem', marginBottom: '12px' }}>{product.name}</h2>
      <div className="product-details" style={{ marginBottom: '12px' }}>
        <p><strong>Weight:</strong> {product.weight}</p>
        <p><strong>Description:</strong> {product.description}</p>
        <p><strong>Price:</strong> ${product.price}</p>
        <p><strong>Amount:</strong> {product.amount}</p>
      </div>
    
      <div className="button-container" style={{ display: 'flex', justifyContent: 'space-between' }}>
        <Link
            href={{
              pathname: `/stores/${store_id}/edit-product/${product.product_id}`,
              query: { storeId: store_id, productId: product.product_id },
            }}
          >
          <button className="edit-fields-btn" style={{ backgroundColor: '#3498db', color: 'white', border: 'none', padding: '10px 20px', fontSize: '1rem', cursor: 'pointer' }}>Edit Fields</button>
        </Link>
        <button onClick={confirmDelete} className="delete-all-btn" style={{ backgroundColor: '#e74c3c', color: 'white', border: 'none', padding: '10px 20px', fontSize: '1rem', cursor: 'pointer' }}>Delete</button>
        {showConfirm && (
          <div className="confirm-container" style={{ marginTop: '16px', padding: '16px', backgroundColor: '#fff', border: '1px solid #ccc', borderRadius: '8px' }}>
          <p>Are you sure you want to delete this item?</p>
          <div className="button-container" style={{ display: 'flex', justifyContent: 'space-between' }}>
            <button onClick={handleDelete} className="confirm-delete-btn" style={{ backgroundColor: '#e74c3c', color: 'white', border: 'none', padding: '10px 20px', fontSize: '1rem', cursor: 'pointer' }}>Yes</button>
            <button onClick={cancelDelete} className="cancel-delete-btn" style={{ backgroundColor: '#3498db', color: 'white', border: 'none', padding: '10px 20px', fontSize: '1rem', cursor: 'pointer' }}>No</button>
          </div>
        </div>
      )}

      </div>
    </div>
  );
};

export default ManagerProduct;
