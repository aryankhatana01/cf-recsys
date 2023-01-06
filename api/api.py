"""
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

To Run the Server:
uvicorn api:app --reload
"""

from typing import Union, List
from fastapi import FastAPI, Query
from pydantic import BaseModel
import utils
from fastapi.middleware.cors import CORSMiddleware
import pymongo

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### GLOBAL VARIABLES ###
model_path = '../turimodel/movie_recs.model'
userId = 5000000
#######################

# Connect to the movies database
client = pymongo.MongoClient("mongodb+srv://aryankhatana01:Karyan123@cluster0.xogmpy8.mongodb.net/?retryWrites=true&w=majority")
db = client["movies"]

@app.get("/search_movies")
def search_movies(term: str):
    # Search for movies that match the search term
    movies_cursor = db.movies.find({"title": {"$regex": term, "$options": "i"}})
    movies = []
    for movie in movies_cursor:
        movies.append(movie)
    for movie in movies:
        del movie['_id']
    return {"search_results": movies}

# Defining the input parameters for Recommendation
class Recommendation(BaseModel):
    movieIds: List[int]
    ratings: List[float]

class MovieId(BaseModel):
    movieIds: List[int]

# Loading the model
model = utils.load_model(model_path)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/recommend")
# def create_pred(movieIds: List[int] = Query(None), ratings: List[int] = Query(None)):
#     new_user_ratings = utils.create_new_user_ratings(movieIds, ratings, userId)
#     list_of_recommandations = utils.make_recommendations(model, new_user_ratings, userId)
#     list_of_movie_titles = utils.getTitlesFromMovieIds(list_of_recommandations)
#     # print(list_of_recommandations)
#     return {"recommendations": list_of_movie_titles}

@app.post("/recommend")
def create_pred(recommendation: Recommendation):
    new_user_ratings = utils.create_new_user_ratings(recommendation.movieIds, recommendation.ratings, userId)
    list_of_recommandations = utils.make_recommendations(model, new_user_ratings, userId)
    list_of_movie_titles = utils.getTitlesFromMovieIds(list_of_recommandations)
    return {"recommendations": list_of_movie_titles}

@app.post("/getMovieTitle")
def getMovieTitle(movieIdsC: MovieId):
    movie_titles = utils.getTitlesFromMovieIds(movieIdsC.movieIds)
    return {"movie_title": movie_titles}

@app.get("/sum")
def add(q: List[int] = Query(None)):
    # c = a + b
    return {"x": q}