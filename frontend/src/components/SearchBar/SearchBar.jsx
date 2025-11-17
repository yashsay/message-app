import PropTypes from "prop-types";
import "./SearchBar.scss";

const SearchBar = ({ query, onQueryChange, onSearch, useAI, onToggleAI }) => {
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      onSearch();
    }
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search messages..."
        value={query}
        onChange={(e) => onQueryChange(e.target.value)}
        onKeyPress={handleKeyPress}
        className="search-bar__input"
      />
      <button onClick={onSearch} className="search-bar__button">
        Search
      </button>
      <label className="search-bar__toggle">
        <input
          type="checkbox"
          checked={useAI}
          onChange={(e) => onToggleAI(e.target.checked)}
        />
        <span>Advanced Search</span>
      </label>
    </div>
  );
};

SearchBar.propTypes = {
  query: PropTypes.string.isRequired,
  onQueryChange: PropTypes.func.isRequired,
  onSearch: PropTypes.func.isRequired,
  useAI: PropTypes.bool.isRequired,
  onToggleAI: PropTypes.func.isRequired,
};

export default SearchBar;
