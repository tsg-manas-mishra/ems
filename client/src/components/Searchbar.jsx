import React, { useState } from "react";

const Searchbar = ({ onSearch }) => {
  const [searchField, setSearchField] = useState("name");
  const [searchValue, setSearchValue] = useState("");

  const handleSearchClick = () => {
    onSearch(searchField, searchValue.trim());
};


  return (
    <div className="flex gap-2 p-4">
      <select
        value={searchField}
        onChange={(e) => setSearchField(e.target.value)}
        className="p-2 border rounded"
      >
        <option value="name">name</option>
        <option value="department">department</option>
        <option value="designation">designation</option>
      </select>

      <input
        type="text"
        value={searchValue}
        onChange={(e) => setSearchValue(e.target.value)}
        placeholder="Enter search term..."
        className="p-2 border rounded"
      />

<button 
    onClick={handleSearchClick} 
    className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
>
    Search
</button>

    </div>
  );
};

export default Searchbar;