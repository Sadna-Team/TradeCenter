import React, { useState } from 'react';

const CartProduct = ({ product, storeName, onRemove }) => {
  const [amount, setAmount] = useState(1);

  const decreaseAmount = () => {
    if (amount > 1) {
      setAmount(amount - 1);
    }
  };

  const increaseAmount = () => {
    setAmount(amount + 1);
  };

  const handleRemove = () => {
    // Call the parent handler to remove the product from the cart
    onRemove(product.id);
  };

  return (
    <div className="product-container" style={{ backgroundColor: '#f0f0f0', border: '1px solid #ccc', padding: '16px', marginBottom: '16px', borderRadius: '8px' }}>
      <h2 style={{ fontSize: '1.5rem', marginBottom: '12px' }}>{product.product_name}</h2>
      <p><strong>Store:</strong> {storeName}</p>
      <div className="product-details" style={{ marginBottom: '12px' }}>
        <p><strong>Weight:</strong> {product.weight}</p>
        <p><strong>Description:</strong> {product.description}</p>
        <p><strong>Price:</strong> ${product.price}</p>
        <p><strong>Rating:</strong> {product.rating}/5</p> {/* Display rating from database */}
      </div>
      <div className="amount-control" style={{ marginBottom: '12px', display: 'flex', alignItems: 'center' }}>
        <button className="amount-btn" style={{ backgroundColor: '#D5DBDB', color: '#333', border: 'none', padding: '8px 12px', fontSize: '1rem', cursor: 'pointer', marginRight: '4px' }} onClick={decreaseAmount}>-</button>
        <input type="text" className="amount-input" style={{ width: '50px', textAlign: 'center', fontSize: '1rem', padding: '8px', margin: '0 4px' }} value={amount} readOnly />
        <button className="amount-btn" style={{ backgroundColor: '#D5DBDB', color: '#333', border: 'none', padding: '8px 12px', fontSize: '1rem', cursor: 'pointer', marginLeft: '4px' }} onClick={increaseAmount}>+</button>
      </div>
      <button className="remove-btn" style={{ backgroundColor: '#FF5733', color: 'white', border: 'none', padding: '8px 12px', fontSize: '0.875rem', cursor: 'pointer' }} onClick={handleRemove}>Remove the item(s)</button>
    </div>
  );
};

export default CartProduct;
