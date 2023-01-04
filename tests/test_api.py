import pandas as pd
import pymongo

# Connect to the movies database
client = pymongo.MongoClient("mongodb+srv://aryankhatana01:Karyan123@cluster0.xogmpy8.mongodb.net/?retryWrites=true&w=majority")
db = client["movies"]

# Search for movies that match the search term
movies_cursor = db.movies.find({"title": {"$regex": "harry potter", "$options": "i"}})
# print(movies_cursor)
movies = []
for movie in movies_cursor:
    movies.append(movie)
for movie in movies:
    del movie['_id']
print(movies)