"""
This file contains utility functions for the API
"""

import turicreate as tc
import pandas as pd

# Defining a userId
# userId = 5000000

# utility function to load the model
def load_model(model_dir: str):
    """
    args:
        model_dir: path to the model
    returns:
        model: the model
    """
    model = tc.load_model(model_dir)
    return model

# A function to convert the list of recommendations to their corresponding titles
def convertRecommendationsToTitle(list_of_recommandations: list):
    """
    args:
        list_of_recommandations: a list of movieIds
    returns:
        df: a dataframe of movieIds, titles and genres
    """
    df = pd.read_csv('../input/movie.csv')
    df = df[['movieId', 'title', 'genres']]
    df = df.set_index('movieId')
    df = df.loc[list_of_recommandations]
    return df

# A function to return a list of titles from a list of movieIds
def getTitlesFromMovieIds(movieIds: list):
    """
    args:
        movieIds: a list of movieIds
    returns:
        titles: a list of titles corresponding to the movieIds
    """
    df = pd.read_csv('../input/movie.csv')
    df = df[['movieId', 'title', 'genres']]
    df = df.set_index('movieId')
    df = df.loc[movieIds]
    return list(df['title'])

# Create a list of userIds for the new user
def create_userIds_list(userId: int, length: int):
    """
    args:
        userId: the userId of the new user
        length: the length of the list
    returns:
        userIds: a list of userIds
    """
    return [userId] * length

# Defining a new user with their ratings
def create_new_user_ratings(movieIds: list, ratings: list, userId: int):
    """
    args:
        movieIds: a list of movieIds
        ratings: a list of ratings
        userId: the userId of the new user
    returns:
        new_user_ratings: a dataframe of movieIds, ratings and userIds
    """
    userIds = create_userIds_list(userId, len(movieIds))
    new_user_ratings = tc.SFrame({
        'movieId': movieIds,
        'rating': ratings,
        'userId': userIds
    })
    return new_user_ratings

# A function to make recommendations
def make_recommendations(model, new_user_ratings, userId):
    """
    args:
        model: the model
        new_user_ratings: a dataframe of movieIds, ratings and userIds
        userId: the userId of the new user
    returns:
        list_of_recommandations: a list of movieIds
    """
    recommendations = model.recommend([userId], new_observation_data=new_user_ratings)
    list_of_recommandations = list(recommendations['movieId'])
    return list_of_recommandations