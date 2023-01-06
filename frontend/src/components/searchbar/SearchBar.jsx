import React from "react";
import './SearchBar.css';
import { useState, createContext, useContext } from 'react';

// Create a context to share the selected movieIds
export const SelectedMovieIdsContext = createContext();

export function useSelectedMovieIds() {
  return useContext(SelectedMovieIdsContext);
}

const SearchBar = () => {
    const [search, setSearch] = useState('');
    const [results, setResults] = useState([]);
    const [selectedMovieIds, setSelectedMovieIds] = useState([]);
    const handleSearch = () => {
        // Make a request to the API with the search query
        fetch(`http://127.0.0.1:8000/search_movies?term=${search}`)
          .then(response => response.json())
          .then(data => {
            // Update the search results with the data returned from the API
            setResults(data["search_results"]);
          });
      }
    const handleMovieClick = movieId => {
    // Update the selected movieIds with the movieId
        if (!selectedMovieIds.includes(movieId)) {
            setSelectedMovieIds([...selectedMovieIds, movieId]);
        }
    };
    return (
        <div className="search-bar">
            <input type="text" 
            placeholder="Search" 
            value={search} 
            onChange={event => setSearch(event.target.value)}
            />
            <button onClick={handleSearch}>Search</button>
            <SelectedMovieIdsContext.Provider value={selectedMovieIds}>
                {Object.values(results).map(movie => (
                <div key={movie.movieId} 
                onClick={() => handleMovieClick(movie.movieId)} 
                style={{ cursor: 'pointer' }}>
                    {movie.title}
                </div>
                ))}
                {/* <h1>{results}</h1> */}
                <div>Selected movie IDs: {selectedMovieIds.join(', ')}</div>
            </SelectedMovieIdsContext.Provider>
        </div>
    )
}

export default SearchBar;