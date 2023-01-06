import React, { useContext } from "react";
import './List.css';
// import { useSelectedMovieIds } from "../searchbar/SearchBar";
import SelectedMovieIdsContext from "../selectmoviesIdsContext/SelectedMovieIdsContext";

const List = () => {
    const selectedMovieIds = useContext(SelectedMovieIdsContext);
    // if (selectedMovieIds !== undefined) {
    //     console.log(selectedMovieIds.join(', '));
    // }
    return (
        <div className="my-list">
            <div>Selected movie IDs: {selectedMovieIds}</div>;
        </div>
    )
}

export default List;