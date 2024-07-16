import React from 'react';

const ManagerDiscount = ({ discount }) => {
    // Static amount from props
    const amount = discount.amount; //what is this for?
    const [showPredicate, setShowPredicate] = useState(false);

  // Function to handle editing fields (you can implement your specific edit logic here)
  const handleEditFields = () => {
    // Implement edit functionality
    console.log(`Editing fields for ${discount.discount_id}`);
  };

  // Function to handle deleting all (you can implement your specific delete logic here)
  const handleDeleteAll = () => {
    // Implement delete functionality
    console.log(`Deleting ${discount.discount_id}`);
  };

  const togglePredicate = () => {
    setShowPredicate(prevShowPredicate => !prevShowPredicate);
  };


  let predicate_content; 

  let content;
  if (discount.discount_type === 'Product Discount'){
    //add a toggle where if clicked will display the predicate information
    content = <div className="product-discount-details" style={{ marginBottom: '12px' }}>
                <p><strong>Description:</strong> {discount.discount_description}</p>
                <p><strong>StartingDate:</strong> {discount.starting_date} GMT +3</p>
                <p><strong>EndingDate:</strong> {discount.ending_date} GMT +3</p>
                <p><strong>Percentage:</strong> {discount.percentage}%</p> 
                <p><strong>ProductID:</strong> {discount.product_id}</p>
                <p><strong>StoreID:</strong> {discount.store_id}</p>
                <p><strong>Predicate:</strong> 
                  <button onClick={togglePredicate} style={{ marginLeft: '8px' }}>
                    {showPredicate ? 'Hide Details' : 'Show Details'}
                  </button>
                </p>
                {showPredicate && (predicate_content)}
              </div>
              
  }else if(discount.discount_type === 'Category Discount'){
    content = <div className="category-discount-details" style={{ marginBottom: '12px' }}>
                <p><strong>Description:</strong> {discount.discount_description}</p>
                <p><strong>StartingDate:</strong> {discount.starting_date} GMT +3</p>
                <p><strong>EndingDate:</strong> {discount.ending_date} GMT +3</p>
                <p><strong>Percentage:</strong> {discount.percentage}%</p> 
                <p><strong>Category:</strong> {discount.category}</p>
                <p><strong>StoreID:</strong> {discount.store_id}</p>
                <p><strong>Predicate:</strong> 
                  <button onClick={togglePredicate} style={{ marginLeft: '8px' }}>
                    {showPredicate ? 'Hide Details' : 'Show Details'}
                  </button>
                </p>
                {showPredicate && (predicate_content)}
              </div>

  }else if(discount.discount_type === 'Store Discount'){
    content = <div className="store-discount-details" style={{ marginBottom: '12px' }}>
                <p><strong>Description:</strong> {discount.discount_description}</p>
                <p><strong>StartingDate:</strong> {discount.starting_date} GMT +3</p>
                <p><strong>EndingDate:</strong> {discount.ending_date} GMT +3</p>
                <p><strong>Percentage:</strong> {discount.percentage}%</p> 
                <p><strong>StoreID:</strong> {discount.store_id}</p>
                <p><strong>Predicate:</strong> 
                  <button onClick={togglePredicate} style={{ marginLeft: '8px' }}>
                    {showPredicate ? 'Hide Details' : 'Show Details'}
                  </button>
                </p>
                {showPredicate && (predicate_content)}
              </div>
  }else if(discount.discount_type ==='And Discount' ){

    content = <div className="and-discount-details" style={{ marginBottom: '12px' }}>
                <p><strong>Description:</strong> {discount.discount_description}</p>
                <p><strong>StartingDate:</strong> {discount.starting_date} GMT +3</p>
                <p><strong>EndingDate:</strong> {discount.ending_date} GMT +3</p>
                <p><strong>Discount1:</strong> {discount.discount_1_info}</p>
                <p><strong>Discount2:</strong> {discount.discount_2_info}</p>
                <p><strong>StoreID:</strong> {discount.store_id}</p>




              </div>

  }else if(discount.discount_type ==='Or Discount' ){
    content = <div className="or-discount-details" style={{ marginBottom: '12px' }}>
                <p><strong>Description:</strong> {discount.discount_description}</p>
                <p><strong>StartingDate:</strong> {discount.starting_date} GMT +3</p>
                <p><strong>EndingDate:</strong> {discount.ending_date} GMT +3</p>
                <p><strong>Discount1:</strong> {discount.discount_1_info}</p>
                <p><strong>Discount2:</strong> {discount.discount_2_info}</p>
                <p><strong>StoreID:</strong> {discount.store_id}</p>
              </div>
  }else if(discount.discount_type ==='Xor Discount' ){
    content = <div className="or-discount-details" style={{ marginBottom: '12px' }}>
                <p><strong>Description:</strong> {discount.discount_description}</p>
                <p><strong>StartingDate:</strong> {discount.starting_date} GMT +3</p>
                <p><strong>EndingDate:</strong> {discount.ending_date} GMT +3</p>
                <p><strong>Discount1:</strong> {discount.discount_1_info}</p>
                <p><strong>Discount2:</strong> {discount.discount_2_info}</p>
                <p><strong>StoreID:</strong> {discount.store_id}</p>
              </div>
  }else if(discount.discount_type ==='Max Discount' ){
    content = <div className="max-discount-details" style={{ marginBottom: '12px' }}>
                <p><strong>Description:</strong> {discount.discount_description}</p>
                <p><strong>StartingDate:</strong> {discount.starting_date} GMT +3</p>
                <p><strong>EndingDate:</strong> {discount.ending_date} GMT +3</p>
                <p><strong>Discounts:</strong> {discount.discounts_info}</p>
                <p><strong>StoreID:</strong> {discount.store_id}</p>
              </div>

  }else{
    content = <div className="additive-discount-details" style={{ marginBottom: '12px' }}>
                <p><strong>Description:</strong> {discount.discount_description}</p>
                <p><strong>StartingDate:</strong> {discount.starting_date} GMT +3</p>
                <p><strong>EndingDate:</strong> {discount.ending_date} GMT +3</p>
                <p><strong>Discounts:</strong> {discount.discounts_info}</p>
                <p><strong>StoreID:</strong> {discount.store_id}</p>

              </div>
  }

  
  return (
    <div className="discount-container" style={{ backgroundColor: '#f0f0f0', border: '1px solid #ccc', padding: '16px', marginBottom: '16px', borderRadius: '8px' }}>
      <h2 style={{ fontSize: '1.5rem', marginBottom: '12px' }}>{discount.discount_id}</h2>
      <div className="discount-details" style={{ marginBottom: '12px' }}>
        {content}
      </div>
    
      <div className="button-container" style={{ display: 'flex', justifyContent: 'space-between' }}>
        <button className="edit-fields-btn" style={{ backgroundColor: '#3498db', color: 'white', border: 'none', padding: '10px 20px', fontSize: '1rem', cursor: 'pointer' }} onClick={handleEditFields}>Edit Fields</button>
        <button className="delete-all-btn" style={{ backgroundColor: '#e74c3c', color: 'white', border: 'none', padding: '10px 20px', fontSize: '1rem', cursor: 'pointer' }} onClick={handleDeleteAll}>Delete All</button>
      </div>
      <h3> The buttons don't work</h3>
    </div>
  );
};

export default ManagerDiscount;