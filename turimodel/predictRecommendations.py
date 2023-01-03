"""
This script predicts recommendations using a turicreate model.
"""

import pandas as pd
import turicreate as tc

# utility function to load the model
def load_model(model_dir):
    model = tc.load_model(model_dir)
    return model

# Loading the model
model = load_model('movie_recs.model')

# Defining a new user with their ratings
def create_new_user_ratings(movieIds: list, ratings: list, userIds: list):
    new_user_ratings = tc.SFrame({
        'movieId': movieIds,
        'rating': ratings,
        'userId': userIds
    })
    return new_user_ratings

# Creating a new user with their ratings
new_user_ratings = create_new_user_ratings(
    movieIds=[1073, 919, 1097], 
    ratings=[5, 5, 5], 
    userIds=[5000000, 5000000, 5000000]
)

# Making recommendations
recommendations = model.recommend([5000000], new_observation_data=new_user_ratings)

# Converting the recommendations to a list
list_of_recommandations = list(recommendations['movieId'])

# A function to convert the list of recommendations to their corresponding titles
def convertRecommendationsToTitle(list_of_recommandations):
    df = pd.read_csv('../input/movie.csv')
    df = df[['movieId', 'title', 'genres']]
    df = df.set_index('movieId')
    df = df.loc[list_of_recommandations]
    return df

# Converting the recommendations to their corresponding titles
df = convertRecommendationsToTitle(list_of_recommandations)

# Printing the top 10 recommendation's titles
print(df.head(10))