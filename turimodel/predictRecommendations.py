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
    movieIds=[1, 74, 52, 44, 200], 
    ratings=[5, 4, 3, 2, 1], 
    userIds=[5000000, 5000000, 5000000, 5000000, 5000000]
)

# Making recommendations
recommendations = model.recommend([5000000], new_observation_data=new_user_ratings)

print(recommendations)