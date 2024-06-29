import { useState, useEffect } from 'react';
import api from '@/lib/api';

const ProductPage = ( { onSave, existingData } ) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState('');
  const [weight, setWeight] = useState('');
  const [amount, setAmount] = useState('');
  const [allTags, setAllTags] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [searchText, setSearchText] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const tagsResponse = await api.get('/store/tags');
        setAllTags(tagsResponse.data.message);
      } catch (error) {
        console.error('Failed to fetch tags', error);
        return;
      }
    };
    fetchData();
  }, []);

  useEffect(() => {
    if (existingData) {
      setName(existingData.name);
      setDescription(existingData.description);
      setPrice(existingData.price);
      setWeight(existingData.weight);
      setAmount(existingData.amount);
      setSelectedTags(existingData.tags);
    }
  }, [existingData]);

  const handleSelect = (e) => {
    const { value, checked } = e.target;
    setSelectedTags((prev) =>
      checked ? [...prev, value] : prev.filter((tag) => tag !== value)
    );
  };

  const handleSearchChange = (e) => {
    setSearchText(e.target.value);
  };

  const dropDownShow = () => {
    setIsOpen(!isOpen);
  };

  const filteredTags = allTags.filter((tag) =>
    tag.toLowerCase().includes(searchText.toLowerCase())
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission
    onSave(name, description, price, weight, amount, selectedTags);
  };

  return (
    <div className="container mx-auto p-4 max-w-lg">
      <h1 className="text-2xl font-bold mb-4">Add Product</h1>
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-lg">
        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">Name</label>
          <input
            type="text"
            value={name}
            placeholder='Product Name'
            onChange={(e) => setName(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded mt-1"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">Description</label>
          <textarea
            value={description}
            placeholder='Product Description'
            onChange={(e) => setDescription(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded mt-1"
            required
          ></textarea>
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">Price</label>
          <input
            type="number"
            placeholder='Product Price'
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded mt-1"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">Weight</label>
          <input
            type="number"
            placeholder='Product Weight'
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded mt-1"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">Amount</label>
          <input
            type="number"
            placeholder='Product Amount'
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded mt-1"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">Tags</label>
          <div className="relative">
            <button
              type="button"
              onClick={dropDownShow}
              className="w-full p-2 border border-gray-300 rounded mt-1"
            >
              Select tags
            </button>
            {isOpen && (
              <div className="w-full max-w-xs mx-auto bg-white rounded-lg overflow-hidden shadow-lg max-h-60 overflow-y-auto mt-1">
                <input
                  type="text"
                  className="w-full p-2 border border-gray-300 rounded mt-1"
                  placeholder="Select tags..."
                  value={searchText}
                  onChange={handleSearchChange}
                />
                {filteredTags.map((tag) => (
                  <div key={tag} className="px-4 py-2 border-b border-gray-200 last:border-0">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        value={tag}
                        onChange={handleSelect}
                        checked={selectedTags.includes(tag)}
                        className="mr-2"
                      />
                      {tag}
                    </label>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        <button
          type="submit"
          className="w-full p-2 bg-blue-500 text-white font-bold rounded mt-4 hover:bg-blue-600"
        >
          {existingData ? 'Update Product' : 'Add Product'}
        </button>
      </form>
    </div>
  );
};

export default ProductPage;
