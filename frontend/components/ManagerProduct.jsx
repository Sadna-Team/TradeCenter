import React from 'react';
import Link from 'next/link';

const ManagerProduct = ({ product, store_id }) => {

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
        <button className="delete-all-btn" style={{ backgroundColor: '#e74c3c', color: 'white', border: 'none', padding: '10px 20px', fontSize: '1rem', cursor: 'pointer' }}>Delete</button>
      </div>
    </div>
  );
};

export default ManagerProduct;
