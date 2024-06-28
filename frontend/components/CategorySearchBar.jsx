import React, { useState } from 'react';

const SearchForm = ({ onSearch, categories, stores }) => {
    const [selectedCategory, setSelectedCategory] = useState('');
    const [storeName, setStoreName] = useState('');

    // Handle form submission by calling the onSearch function passed as a prop
    const handleSubmit = (e) => {
        e.preventDefault();
        onSearch(selectedCategory, storeName);
    };

    return (
        <div className="flex items-start justify-center min-h-screen bg-gray-100">
            <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
                <h1 className="text-2xl font-bold mb-4 text-center">Search By Category</h1>
                <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                        <label className="block text-gray-700">Category</label>
                        <select
                            value={selectedCategory}
                            className="w-full p-2 border border-gray-300 rounded mt-1"
                            onChange={(e) => setSelectedCategory(e.target.value)}
                        >
                            <option value="">Select category</option>
                            {categories.map((category) => (
                                <option key={category} value={category}>
                                    {category}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="mb-4">
                    <label className="block text-gray-700">Store Name(Optional)</label>
                    <select
                        value={storeName}
                        onChange={(e) => setStoreName(e.target.value)}
                        className="w-full p-2 border border-gray-300 rounded mt-1"
                    >
                        <option value="">Select store</option>
                        {stores.map((store) => (
                        <option key={store} value={store}>
                            {store}
                        </option>
                        ))}
                    </select>
                    </div>
                    <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded">
                        Search
                    </button>
                </form>
            </div>
        </div>
    );
};

export default SearchForm;
