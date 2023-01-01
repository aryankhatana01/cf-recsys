"""
This file contains the inference APi for the project
"""

import torch
import numpy as np
import pandas as pd
from model import RecSysModel
from config import cfg

def load_model(model, model_dir):
    state_dict = torch.load(model_dir,
                            map_location=torch.device('cpu'))  # ensure all storage are on gpu
    model.load_state_dict(state_dict)
    print("Weights loaded from: ", model_dir)
    return model

def preprocess(df):
    user_ids = df["userId"].unique().tolist()
    user2user_encoded = {x: i for i, x in enumerate(user_ids)}
    userencoded2user = {i: x for i, x in enumerate(user_ids)}

    movie_ids = df["movieId"].unique().tolist()
    movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}
    movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}

    return user2user_encoded, userencoded2user, movie2movie_encoded, movie_encoded2movie


if __name__ == "__main__":
    # Reading the dataframe
    df = pd.read_csv('../input/ratingsCleaned.csv') # UserId, MovieId, Rating
    df2 = {'userId': 5000000, 'movieId': 123, 'rating': 1}
    df = df.append(df2, ignore_index = True)

    # Preprocessing the dataframe for inference
    user2user_encoded, userencoded2user, movie2movie_encoded, movie_encoded2movie = preprocess(df)
    df["userId"] = df["userId"].map(user2user_encoded)
    df["movieId"] = df["movieId"].map(movie2movie_encoded)

    # Intitailizing the model
    model = RecSysModel(
        n_users=len(user2user_encoded),
        n_movies=len(movie_encoded2movie)
    )

    # Loading the weights in the model
    model = load_model(model, '../model.pth')
    # print(model)

    device = cfg.device
    # print(device)
    model.to(device)

    # Predictions
    movies_watched_by_user = [1, 3, 52, 326, 5732]
    movies_not_watched = df[
        ~df["movieId"].isin(movies_watched_by_user)
    ]["movieId"]
    
    movies_not_watched = list(
        set(movies_not_watched).intersection(set(movie2movie_encoded.keys()))
    )

    movies_not_watched = [movie2movie_encoded.get(x) for x in movies_not_watched]

    user_id = 5000000
    user_encoder = user2user_encoded.get(user_id)
    user_ids = [user_encoder] * len(movies_not_watched)

    user_ids = torch.tensor(user_ids)
    movies_not_watched = torch.tensor(movies_not_watched)
    user_ids = user_ids.to(device)
    movies_not_watched = movies_not_watched.to(device)

    ratings = model(user_ids, movies_not_watched)
    print(ratings)

    top_ratings_indices = torch.argsort(ratings, dim=0)
    top_ratings_indices = top_ratings_indices.cpu().numpy()
    top_ratings_indices = top_ratings_indices[::-1]
    top_ratings_indices = top_ratings_indices[:10]
    top_ratings_indices = top_ratings_indices.tolist()

    top_ten_preds = []
    for pred in top_ratings_indices:
        p = pred[0]
        top_ten_preds.append(p)
    
    # print(top_ten_preds)

    movies_not_watched = movies_not_watched.cpu().detach().tolist()

    recommended_movie_ids = [
    movie_encoded2movie.get(movies_not_watched[x]) for x in top_ten_preds
    ]
    
    moviesdf = pd.read_csv("../input/movie.csv")
    recommovies = moviesdf[moviesdf['movieId'].isin(recommended_movie_ids)]
    print(recommovies.title)