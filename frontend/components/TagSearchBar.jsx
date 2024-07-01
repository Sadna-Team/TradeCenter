import React, { useState } from 'react';
import { Form } from 'react-bootstrap';

const SearchForm = ({ onSearch, tags, stores }) => {
    const [selectedTags, setSelectedTags] = useState([]);
    const [storeName, setStoreName] = useState('');
    const [isOpen, setIsOpen] = useState(false);
    const [searchText, setSearchText] = useState('');
    const [filteredTags, setFilteredTags] = useState([]);

    const handleSelect = (e) => {
        const value = e.target.value;
        if (selectedTags.includes(value)) {
            setSelectedTags(selectedTags.filter((tag) => tag !== value));
        } else {
            setSelectedTags([...selectedTags, value]);
        }
    };

    // Handle form submission by calling the onSearch function passed as a prop
    const handleSubmit = (e) => {
        e.preventDefault();
        onSearch(selectedTags, storeName);
    };

    const handleSearchChange = (e) => {
    const value = e.target.value;
    setSearchText(value);
    // Filter tags based on search text
    setFilteredTags(tags.filter((tag) => tag.toLowerCase().startsWith(value.toLowerCase())));
    };

    const dropDownShow = () => {
    setIsOpen(!isOpen);
    };

    return (
    <div className="flex items-start justify-center min-h-screen bg-gray-100">
    <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
    <h1 className="text-2xl font-bold mb-4 text-center">Search By Tags</h1>
    <form onSubmit={handleSubmit}>
        <div className="mb-4">
            <label className="block text-gray-700">Tags</label>
            <div className="relative">
                <button
                type="button"
                onClick={dropDownShow}
                className="w-full p-2 border border-gray-300 rounded mt-1"
                >
                Select tags
                </button>
                {isOpen && (
                <div className="w-full max-w-xs mx-auto bg-white rounded-lg overflow-hidden shadow-lg max-h-60 overflow-y-auto">
                    <input
                    type="text"
                    className="w-full p-2 border border-gray-300 rounded mt-1"
                    placeholder="Search tags..."
                    value={searchText}
                    onChange={handleSearchChange}
                    />
                    {filteredTags.map((tag) => (
                    <Form.Check
                        key={tag}
                        type="checkbox"
                        label={tag}
                        value={tag}
                        onChange={handleSelect}
                        checked={selectedTags.includes(tag)}
                        className="px-4 py-2 border-b border-gray-200 last:border-0"
                    />
                    ))}
                </div>
                )}
            </div>
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
