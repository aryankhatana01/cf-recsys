import React, { useContext } from "react";
import './List.css';
// import { useSelectedMovieIds } from "../searchbar/SearchBar";
import SelectedMovieIdsContext from "../selectmoviesIdsContext/SelectedMovieIdsContext";
import GetRecommendationsButton from '../getRecommendations/GetRecommendationsButton';

const List = () => {
    const selectedMovieIds = useContext(SelectedMovieIdsContext);
    // if (selectedMovieIds !== undefined) {
    //     console.log(selectedMovieIds.join(', '));
    // }
    return (
        <div className="my-list">
            <div>Selected movie IDs: {selectedMovieIds.join(', ')}</div>;
            <GetRecommendationsButton selectedMovieIds={selectedMovieIds}/>
        </div>
    )
}

export default List;