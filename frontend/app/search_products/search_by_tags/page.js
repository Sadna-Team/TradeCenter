"use client";

export default function SearchByTags() {
    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
          <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
            <h1 className="text-2xl font-bold mb-4 text-center">Search By Tags</h1>
            <form>
              <div className="mb-4">
                <label className="block text-gray-700">Tags</label>
                <input
                  type="text"
                  className="w-full p-2 border border-gray-300 rounded mt-1"
                  placeholder="Enter tags"
                />
              </div>
              <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded">
                Search
              </button>
            </form>
          </div>
        </div>
      );
}