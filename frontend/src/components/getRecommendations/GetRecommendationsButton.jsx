import React from "react";
import './GetRecommendationsButton.css';
import { useState } from 'react';

const GetRecommendationsButton = (props) => {
    const [recommendations, setRecommendations] = useState([]);
    const selectedMovieIds = props.selectedMovieIds;
    const ratings = Array(props.selectedMovieIds.length).fill(5);

    const fetchRecommendations = async () => {
        const response = await fetch('http://localhost:8000/recommend', {
            method: 'POST',
            body: JSON.stringify({
                "movieIds": selectedMovieIds,
                "ratings": ratings
            }),
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        });
        const data = await response.json();
        setRecommendations(data["recommendations"]);
    }
    return (
        <div className="Get-Recommendations">
            <button onClick={fetchRecommendations}>Get Recommendations</button>
            {Object.entries(recommendations).map(([key, value]) => (
                <div key={key}>{key}: {value}</div>
            ))}
        </div>
    );
}

export default GetRecommendationsButton;