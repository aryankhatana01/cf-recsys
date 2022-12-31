"""
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

To Run the Server:
uvicorn api:app --reload
"""

from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/predict")
def create_pred(a, b):
    return {"sum": int(a) + int(b)}