import React, { useContext, useState, useEffect } from "react";
import './List.css';
// import { useSelectedMovieIds } from "../searchbar/SearchBar";
import SelectedMovieIdsContext from "../selectmoviesIdsContext/SelectedMovieIdsContext";
import GetRecommendationsButton from '../getRecommendations/GetRecommendationsButton';

const List = () => {
    const selectedMovieIds = useContext(SelectedMovieIdsContext);
    const [selectedTitles, setselectedTitles] = useState([]);
    // if (selectedMovieIds !== undefined) {
    //     console.log(selectedMovieIds.join(', '));
    // }
    const fetchTitles = async () => {
        const response = await fetch('http://localhost:8000/getMovieTitle', {
            method: 'POST',
            body: JSON.stringify({
                "movieIds": selectedMovieIds,
            }),
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        });
        const data = await response.json();
        setselectedTitles(data["movie_title"]);
    }
    useEffect(() => {
        fetchTitles();
    }, []);
    return (
        <div className="my-list">
            <div>Selected movie IDs: {selectedMovieIds.join(', ')}</div>;
            {selectedTitles.map(item => (
                <div key={item}>{item}</div>
            ))}
            <GetRecommendationsButton selectedMovieIds={selectedMovieIds}/>
        </div>
    )
}

export default List;