"""
This script creates a MongoDB database called movies and a collection called movies.
"""

import pandas as pd
import pymongo

# Connect to the movies database
client = pymongo.MongoClient("mongodb+srv://aryankhatana01:Karyan123@cluster0.xogmpy8.mongodb.net/?retryWrites=true&w=majority")
db = client["movies"]


# Read the movies.csv file
movies_df = pd.read_csv('../input/movie.csv')

# Convert the DataFrame to a list of dictionaries
movies_list = movies_df.to_dict('records')

# print(movies_list)

# Insert the movie documents into the movies collection
db.movies.insert_many(movies_list)
