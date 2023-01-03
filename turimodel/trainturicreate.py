"""
This script trains a turicreate model and saves it to a file.
"""

import pandas as pd
import turicreate as tc

data = tc.SFrame.read_csv('../input/ratingsCleaned.csv')
train, test = data.random_split(0.9)

model = tc.item_similarity_recommender.create(
    train, 
    'userId', 
    'movieId', 
    target='rating'
)

def save_model(model):
    model.save('movie_recs.model')

save_model(model)