import React from "react";
import { FaSearch } from "react-icons/fa";
import "./searchbar.css";

const SearchBar = () => {
  return (
    <div className="input-wrapper">
      <FaSearch id="search-icon"/>
      <input type="text" placeholder="Search..." />
    </div>
  );
};

export default SearchBar;