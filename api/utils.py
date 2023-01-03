"""
This file contains utility functions for the API
"""

import turicreate as tc
import pandas as pd

# Defining a userId
userId = 5000000

# utility function to load the model
def load_model(model_dir: str):
    model = tc.load_model(model_dir)
    return model

# A function to convert the list of recommendations to their corresponding titles
def convertRecommendationsToTitle(list_of_recommandations: list):
    df = pd.read_csv('../input/movie.csv')
    df = df[['movieId', 'title', 'genres']]
    df = df.set_index('movieId')
    df = df.loc[list_of_recommandations]
    return df

# A function to return a list of titles from a list of movieIds
def getTitlesFromMovieIds(movieIds: list):
    df = pd.read_csv('../input/movie.csv')
    df = df[['movieId', 'title', 'genres']]
    df = df.set_index('movieId')
    df = df.loc[movieIds]
    return list(df['title'])

# Create a list of userIds for the new user
def create_userIds_list(userId: int, length: int):
    return [userId] * length

# Defining a new user with their ratings
def create_new_user_ratings(movieIds: list, ratings: list):
    userIds = create_userIds_list(userId, len(movieIds))
    new_user_ratings = tc.SFrame({
        'movieId': movieIds,
        'rating': ratings,
        'userId': userIds
    })
    return new_user_ratings

# A function to make recommendations
def make_recommendations(model, new_user_ratings):
    recommendations = model.recommend([userId], new_observation_data=new_user_ratings)
    list_of_recommandations = list(recommendations['movieId'])
    return list_of_recommandations