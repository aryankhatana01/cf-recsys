"""
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

To Run the Server:
uvicorn api:app --reload
"""

from typing import Union, List
from fastapi import FastAPI, Query
import utils

app = FastAPI()

### GLOBAL VARIABLES ###
model_path = '../turimodel/movie_recs.model'
userId = 5000000
#######################

# Loading the model
model = utils.load_model(model_path)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/recommend")
def create_pred(movieIds: List[int] = Query(None), ratings: List[int] = Query(None)):
    new_user_ratings = utils.create_new_user_ratings(movieIds, ratings, userId)
    list_of_recommandations = utils.make_recommendations(model, new_user_ratings, userId)
    list_of_movie_titles = utils.getTitlesFromMovieIds(list_of_recommandations)
    # print(list_of_recommandations)
    return {"recommendations": list_of_movie_titles}

@app.get("/sum")
def add(q: List[int] = Query(None)):
    # c = a + b
    return {"x": q}